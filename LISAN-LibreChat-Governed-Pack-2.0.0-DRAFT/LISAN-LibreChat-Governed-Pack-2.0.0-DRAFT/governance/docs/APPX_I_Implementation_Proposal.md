تنفيذ البوابات الموصوفة في وثيقة الثغرات **ممكن فعلياً في LibreChat**، لكن بشرط التمييز بين ثلاثة مستويات: ما يمكن إنفاذه بالإعداد الأصلي، وما يحتاج **MCP مخصصاً**، وما يبقى **خارج LibreChat** في محرك لسان. سأركّز على الآليات الحقيقية لا على التمني.

---

## أولاً: الآليات الأصلية التي يمكن الاعتماد عليها فعلياً

### 1. `toolApproval` — البوابة الأساسية لسياسة الأدوات

هذا هو **أقوى ما يقدمه LibreChat أصلياً** لمنع تنفيذ أدوات غير مرخصة. يُضبط في `librechat.yaml` تحت `endpoints.agents.toolApproval`:

```yaml
endpoints:
  agents:
    toolApproval:
      enabled: true
      mode: default          # default / dontAsk / bypass
      allow:
        - 'mcp:lisan-corpus:read_*'
      deny:
        - 'mcp:*:delete_*'
        - 'mcp:*:write_*'
      ask:
        - 'mcp:lisan-registry:save_finding'
      reason: 'Review {tool} before it runs.'
```

**ما يمنحه هذا فعلياً:**

- **`deny` يتقدم دائماً**، حتى في وضع `bypass`. هذا يعني أن أدوات `write` و`delete` يمكن منعها منعاً قاطعاً، وهو ما تحتاجه لسياسة "لا كتابة في وضع الاكتشاف".
- **`ask`** يفرض موافقة بشرية (HITL) قبل تنفيذ الأداة. يُستخدم لـ`save_finding` و`request_approval`، فيتحقق شرط "قرار مخوّل" قبل حفظ أي نتيجة.
- **أنماط glob** تسمح بتحديد دقيق: `mcp:<server>:<tool>`. يمكن منع أدوات corpus كاملة عن وكيل معين، أو السماح بأدوات قراءة فقط.
- **يطبق على Subagents المتداخلة** أيضاً، لأن القواعد تُطابق أسماء MCP runtime والأسماء الظاهرة للنموذج، بما فيها الأدوات التي تُستدعى عبر Subagents المتداخلة. هذا يغلق ثغرة "الوكيل الفرعي يتجاوز السياسة".

**حدّه:** `toolApproval` يقرر **هل تُنفَّذ الأداة**، لا **هل المخرج صحيح**. فهو يمنع `save_finding` قبل الاعتماد، لكنه لا يمنع حفظ نتيجة خاطئة إذا مُنح الاعتماد. لذلك هو بوابة **صلاحيات**، لا بوابة **صحة**.

### 2. Hooks — السياسات البرمجية السياقية

إذا لم تكفِ القواعد الثابتة، يمكن تحميل **hooks برمجية** تعمل داخل عملية LibreChat، وتستقبل سياق كل استدعاء أداة وتصدر قراراً (`allow`/`ask`/`deny`):

```yaml
toolApproval:
  enabled: true
  hooks:
    - module: './hooks/lisan-policy-gate.js'
      matcher: '^mcp:lisan-'
```

الـHook يمكنه فحص:
- هل الوكيل الحالي في وضع `NEW_CORPUS_STUDY`؟
- هل الأداة المطلوبة من نوع `external` (معجم/تفسير)؟
- هل المخرج السابق يحمل `INTERNAL_LOCK`؟
- هل المستخدم يملك صلاحية `APPROVE`؟

**هذه هي الطريقة الوحيدة** لتنفيذ سياسات مركبة مثل: "إذا كان الوضع `NEW_CORPUS_STUDY`، فمنع كل أداة خارجية، وإذا حاول النموذج استدعاء `external_comparison`، أعِد `deny` مع سبب". القواعد الثابتة لا تستطيع التعبير عن هذا الشرط السياقي.

**تحذير مهم:** الـHook يمكنه فقط **تضييق** السياسة، لا توسيعها. لا يمكنه السماح بأداة منعتها القاعدة الثابتة. هذا تصميم آمن: الطبقة البرمجية لا تستطيع تجاوز الطبقة التصريحية.

### 3. `capabilities` — تقييد القدرات على مستوى الوكيل

`endpoints.agents.capabilities` تحدد ما يستطيع الوكيل فعله أصلاً. يمكن تعطيل `web_search` و`file_search` و`actions` لوكيل Blind Lab، فيصبح **غير قادر** على الوصول إلى مصادر خارجية، لا مجرد "ممنوع" من استخدامها:

```yaml
# في تعريف الوكيل
capabilities:
  - tools
  - skills
  - context          # يمكن إبقاؤه لتمرير نص corpus
  # web_search معطّل
  # file_search معطّل
  # actions معطّل
  # execute_code معطّل
```

الفرق بين `capabilities` و`toolApproval`:
- `capabilities` تحدد ما هو **موجود** في سياق الوكيل.
- `toolApproval` تحدد ما هو **مسموح تنفيذه** من الموجود.

للـBlind Lab، **يلزم الاثنان معاً**: تعطيل `web_search` و`file_search` في `capabilities` (فلا تظهر الأدوات للنموذج)، ومنع أدوات MCP خارجية في `toolApproval` (فلا تُنفَّذ حتى لو استدعاها النموذج بأسماء أخرى).

### 4. MCP Gating وصلاحيات الخادم

LibreChat يتحقق من صلاحيات MCP عبر `createMCPPermissionContext`، فلا يستطيع المستخدم الوصول إلا إلى الخوادم المسموح بها. ويمكن تقييد خادم MCP بأكمله لمستخدمين محددين عبر `allowedUsers`، أو عبر ACLs على مستوى `MCPSERVER` بأدوار `VIEWER`/`EDITOR`/`OWNER`.

هذا يسمح ببناء طبقة صلاحيات على مستوى الخادم نفسه:
- `lisan-corpus-mcp`: متاح لكل الوكلاء.
- `lisan-registry-mcp`: متاح فقط لوكلاء الحفظ والاعتماد.
- `lisan-external-mcp`: متاح فقط لوكلاء المقارنة الخارجية، ومعطّل تماماً في Blind Lab.

### 5. `maxSubagents` و`agent_ids` — تقييد التفويض

`maxSubagents` (1–50، افتراضي 10) يحدد عدد الوكلاء الفرعيين الذين يمكن لوكيل واحد الإشارة إليهم. و`agent_ids` قائمة بيضاء تُتحقق منها الخادم. هذا يمنع وكيلاً من تفويض مهمة إلى وكيل غير مصرح به، حتى لو حاول النموذج ذلك.

### 6. `checkpointer` و`ask_user_question` — HITL المتين

`checkpointer` (MongoDB افتراضياً، TTL افتراضي 86400 ثانية) يحفظ حالة التشغيل الموقوف عند نقطة موافقة، ويستأنفها بعد restart أو على replica آخر. و`ask_user_question` يسمح للوكيل بالتوقف لطلب إدخال أو موافقة ثم الاستئناف.

هذا ضروري لبوابة G9 (الاعتماد): عند وصول نتيجة إلى `request_approval`، يتوقف التشغيل، ويُحفظ في checkpoint، ولا يُستأنف إلا بقرار مخوّل. إذا أُعيد تشغيل الخادم، يبقى القرار معلقاً ولا يُفقد.

---

## ثانياً: ما لا تستطيع الآليات الأصلية فعله — والحل عبر MCP مخصص

### الفجوة 1: التحقق من صحة المخرج (Output Guard)

LibreChat **لا يملك** آلية أصلية للتحقق من أن مخرج النموذج مطابق لمخطط دلالي، أو أن كل ادعاء يحمل سنداً. `toolApproval` يتحكم في **استدعاء الأداة**، لا في **نص الإجابة**.

**الحل:** بناء `lisan-guard-mcp` يعرض أداة `validate_output`، وتُستدعى **إجبارياً** كآخر خطوة قبل عرض أي نتيجة:

```yaml
# في تعريف وكيل الإخراج
tools:
  - mcp:lisan-guard:validate_output
```

لكن هذا يظل **اختيارياً من جهة النموذج** إذا لم يُلزم به. لإلزامه:
1. اجعل `validate_output` هي الأداة الوحيدة المتاحة لوكيل الإخراج، مع `deny` لكل ما عداها.
2. استخدم hook يمنع الوكيل من إنهاء التشغيل دون استدعاء `validate_output` (يمكن فحص سجل الأدوات في الـhook).
3. أو استخدم Agent Chain: وكيل الإخراج لا يُنتج النص النهائي، بل يُنتج `draft`، ووكيل التحقق يستلمه ويمرره عبر `validate_output` قبل عرضه.

### الفجوة 2: State Machine خارج النموذج

الوثيقة تشترط "State machine خارج النموذج، وسياسات أداة وبوابات قبل النشر؛ منع أي اختصار تجاوزي" (P0-11). LibreChat لا يوفر State machine جاهزاً للمراحل الدلالية. `Agent Chain` يمرر مخرجات، لكنه لا يمنع وكيلاً من "القفز" إلى مرحلة لاحقة.

**الحل:** بناء `lisan-state-mcp` يحتفظ بحالة كل دراسة (`study_id`, `phase`, `locked`, `approval_status`) ويعرض أدوات:

```python
# lisan-state-mcp tools
state.get(study_id) -> StudyState
state.transition(study_id, from_phase, to_phase, evidence_refs) -> TransitionResult  # fail-closed
state.can_proceed(study_id, requested_phase) -> bool
state.lock(study_id, result_hash) -> LockResult
```

كل وكيل في السلسلة يجب أن يستدعي `state.can_proceed` قبل عمله. إذا لم تكن المرحلة السابقة مكتملة، تعيد `false`، ويمنع الوكيل من المتابعة. هذا يضع الحالة **خارج سياق النموذج**، فلا يستطيع النموذج "تزوير" الانتقال.

### الفجوة 3: التحقق من التغطية والعد

الوثيقة تشترط أن "المقام والبسط من فهرس حتمي ونطاق استعلام مجمد، ووحدة عد ظاهرة" (P0-05). هذا لا يمكن أن يأتي من النموذج.

**الحل:** `lisan-corpus-mcp` يعرض:

```python
corpus.count(selector) -> CountResult  # بسط حتمي
corpus.coverage(study_id, selector) -> CoverageResult  # بسط/مقام/حالة
corpus.verify_citation(ref, text) -> VerificationResult  # التحقق من النص
```

وكيل التغطية لا "يحسب" النسبة، بل يستدعي `coverage` ويعرض النتيجة. إذا لم تُسترجع أداة `coverage`، لا يُسمح بادعاء `FULL`.

### الفجوة 4: القفل (Lock)

الوثيقة تشترط "نتيجة داخلية بإصدار وقفل لا يغير الحكم المعرفي" (G7). LibreChat لا يملك آلية قفل.

**الحل:** `lisan-registry-mcp` يعرض:

```python
registry.lock(study_id, result_json) -> LockReceipt  # hash + timestamp
registry.get_locked(study_id) -> LockedResult
registry.reopen(study_id, reason, authorized_by) -> ReopenReceipt
```

بعد `lock`، أي محاولة تعديل تُرفض، وتُنتج `reopen` بإصدار جديد. هذا يمنع تعديل النتيجة بعد المقارنة الخارجية (P0-12).

---

## ثالثاً: ترجمة طبقات الإنفاذ (A–F) إلى آليات محددة

| الطبقة في الوثيقة | الآلية الفعلية | ما يضمنه | ما لا يضمنه |
| :--- | :--- | :--- | :--- |
| **A. Corpus authority** | `lisan-corpus-mcp` + `toolApproval.deny` لكل مصدر خارجي | النص من مصدر مثبت فقط | جودة الفهرس نفسه |
| **B. Authorized repository** | `lisan-registry-mcp` + `toolApproval.ask` على `save`/`lock` | إصدارات immutable وسجل | صحة الحكم المحفوظ |
| **C. Policy gateway** | `toolApproval` (deny/ask/allow) + hooks برمجية + `capabilities` | منع الأدوات غير المرخصة سياقياً | صحة الحجة داخل الأداة المسموحة |
| **D. Structured evidence pipeline** | `lisan-guard-mcp` + مخططات JSON + `validate_output` | شكل الادعاء وسنده | صحة السند نفسه |
| **E. Independent semantic review** | `ask_user_question` + `checkpointer` + دور مخوّل | مراجعة بشرية موثقة | موضوعية المراجع |
| **F. Output guard** | `lisan-guard-mcp.validate_output` + Agent Chain | رفض الاقتباسات الخاطئة والتغطية غير المثبتة | كل تحريف دلالي |

**الملاحظة الجوهرية:** الطبقات A–D وF يمكن أن تكون **MCP + إعداد LibreChat**. الطبقة E (المراجعة الدلالية) **لا يمكن أتمتتها**، وتحتاج عنصراً بشرياً أو نموذجاً مستقلاً بدور مخوّل، وهذا يبقى في محرك لسان أو في `ask_user_question` مع checkpoint.

---

## رابعاً: خريطة تنفيذ عملية — من السياسة إلى الإعداد

### الخطوة 1: تثبيت corpus وبناء MCP الأساسي

قبل أي بوابة، يجب أن يوجد ما تُطبَّق عليه البوابات. `lisan-corpus-mcp` يجب أن يعرض على الأقل:

- `search_root` / `search_form` / `search_lemma`
- `count` (بسط حتمي)
- `coverage` (بسط/مقام/حالة)
- `verify_citation` (التحقق من النص والرقم)
- `get_morphology` (مع وسم المصدر والتحقق)

بدون هذه الأدوات، كل بوابة G2 وG5 تبقى نظرية.

### الخطوة 2: ضبط `toolApproval` كسياسة أساسية

```yaml
endpoints:
  agents:
    toolApproval:
      enabled: true
      mode: dontAsk          # الوضع الافتراضي: رفض ما ليس مسموحاً
      deny:
        - 'mcp:*:delete_*'
        - 'mcp:lisan-external:*'   # يُفتح فقط عبر وضع المقارنة
      allow:
        - 'mcp:lisan-corpus:search_*'
        - 'mcp:lisan-corpus:count'
        - 'mcp:lisan-corpus:coverage'
        - 'mcp:lisan-corpus:verify_citation'
      ask:
        - 'mcp:lisan-registry:save_finding'
        - 'mcp:lisan-registry:lock'
        - 'mcp:lisan-guard:request_approval'
```

**لماذا `dontAsk`:** الوضع `dontAsk` يرفض كل ما ليس في `allow`. هذا هو **fail-closed** المطلوب: لا يمر شيء إلا بإذن صريح. وضع `default` يسمح بما ليس مذكوراً، وهذا خطر.

### الخطوة 3: بناء hooks للسياسات السياقية

```javascript
// hooks/lisan-phase-gate.js
module.exports = ({ toolName, context }) => {
  const phase = context.agentPhase; // يُمرر من state MCP
  if (phase === 'NEW_CORPUS_STUDY' && toolName.startsWith('mcp:lisan-external:')) {
    return { decision: 'deny', reason: 'External tools are blocked during discovery phase.' };
  }
  if (phase !== 'LOCKED' && toolName === 'mcp:lisan-external:compare') {
    return { decision: 'deny', reason: 'External comparison requires a locked internal result.' };
  }
  return { decision: 'allow' };
};
```

هذا الـhook يغلق P0-02 (منع الأدوات الخارجية في المسار الداخلي) وP0-12 (منع المقارنة قبل القفل) في مكان واحد.

### الخطوة 4: تعطيل `capabilities` للـBlind Lab

```yaml
# في تعريف وكيل Blind Lab
capabilities:
  - tools
  - skills
  # web_search: معطّل
  # file_search: معطّل
  # actions: معطّل
  # execute_code: معطّل
  # memory: معطّل (إذا كان يدعم التعطيل)
```

مع `toolApproval` أعلاه، يصبح Blind Lab غير قادر على الوصول إلى أي مصدر خارج corpus، سواء بأداة أصلية أو عبر MCP.

### الخطوة 5: Agent Chain مع تحقق بين المراحل

```yaml
# سلسلة مبسطة
chain:
  - agent: blind-analyzer
    output_schema: corpus_observation
  - agent: hypothesis-builder
    input: corpus_observation
    output_schema: semantic_hypothesis
    gate: require_counterevidence_field
  - agent: falsification-tester
    input: semantic_hypothesis
    output_schema: falsification_result
  - agent: result-locker
    input: falsification_result
    tool: mcp:lisan-registry:lock
    gate: require_state_locked
  - agent: heritage-auditor
    input: locked_result
    tool: mcp:lisan-guard:audit
```

كل انتقال يجب أن يمر عبر `state.can_proceed` (من `lisan-state-mcp`)، وإلا يُرفض. هذا يمنع القفز بين المراحل.

### الخطوة 6: `ask_user_question` للاعتماد

عندما يصل التشغيل إلى `request_approval`، يتوقف عبر `ask_user_question`، ويُحفظ في `checkpointer` لمدة 24 ساعة. لا يُستأنف إلا بقرار مخوّل. هذا يحقق G9 (اعتماد مسجل من مخول).

---

## خامساً: ما لا يمكن إنفاذه — يجب الاعتراف به

1. **التلوث الداخلي لأوزان النموذج:** لا يمكن منعه بأي آلية في LibreChat. يمكن فقط كشف آثاره عبر Heritage Auditor، ووسمها، لا محوها.

2. **صحة الحكم الدلالي:** لا `toolApproval` ولا `validate_output` يثبتان أن "النواة الدلالية" صحيحة. يمكنهما فقط التحقق من أن الادعاء يحمل سنداً وشكلاً صحيحاً. الحكم الدلالي يبقى للمراجعة البشرية (الطبقة E).

3. **الالتفاف عبر الإجابة دون استدعاء أداة:** وكيل يمكنه أن "يجيب" دون استدعاء `validate_output`. الحل الوحيد هو hook يفحص سجل الأدوات ويمنع إنهاء التشغيل دون استدعاء التحقق، أو Agent Chain تفرض أن النص النهائي لا يُعرض إلا بعد وكيل التحقق. هذا ليس ضماناً مطلقاً، لكنه يقلل الالتفاف.

4. **المقارنة الخارجية بعد القفل:** يمكن منعها بـ`deny`، لكن لا يمكن منع النموذج من "تذكر" المعجم في مرحلة لاحقة. القفل يمنع تعديل النتيجة، لا يمنع إعادة تفسيرها في محادثة جديدة.

5. **جودة corpus:** إذا كان الفهرس ناقصاً، فكل البوابات ستكون صارمة على بيانات ناقصة. G1 (تثبيت المصدر) شرط لكل ما بعده.

---

## سادساً: الحد الأدنى القابل للتنفيذ الآن

إذا أردت البدء غداً، هذا هو الحد الأدنى:

1. **`lisan-corpus-mcp`** بأدوات: `search`, `count`, `coverage`, `verify_citation`.
2. **`toolApproval`** بوضع `dontAsk` مع `allow` لأدوات corpus فقط.
3. **وكيل Blind Lab** مع `capabilities` معطّلة لـ`web_search` و`file_search`.
4. **`lisan-registry-mcp`** بأداة `lock` واحدة، مع `ask` على `lock`.
5. **hook** واحد يمنع `external` في وضع الاكتشاف.
6. **`ask_user_question`** عند `lock` لطلب اعتماد.

هذا يغطي P0-01, P0-02, P0-04, P0-05, P0-10, P0-11, P0-12 بدرجة معقولة، ويترك P0-03 (التلوث الداخلي) وP0-06 (الوسم النحوي) وP0-07 (الأدوات الدلالية) لحين بناء `lisan-guard-mcp` و`lisan-state-mcp`.

---

## الخلاصة

تنفيذ البوابات ليس بناء نظام جديد من الصفر. هو **تركيب** من:

- **`toolApproval`** للصلاحيات (deny/ask/allow).
- **Hooks** للسياسات السياقية.
- **`capabilities`** لتقييد ما هو موجود.
- **MCP مخصص** للحالة والقفل والتحقق.
- **Agent Chain + `ask_user_question`** للترتيب والاعتماد.

LibreChat يوفر **الجلد** (الصلاحيات، HITL، checkpoint، تعدد الوكلاء)، ومحرك لسان يوفر **العضلات** (corpus، فهرس، عد، تحقق، حالة، قفل). بدون الجلد، لا إنفاذ. بدون العضلات، لا معنى للإنفاذ. والاثنان معاً يجعلان LISAN **مُنفَّذة** لا **مُوصى بها**.
