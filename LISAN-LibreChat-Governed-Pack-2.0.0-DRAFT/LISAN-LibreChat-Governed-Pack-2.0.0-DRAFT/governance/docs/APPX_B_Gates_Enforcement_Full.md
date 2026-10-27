# LISAN — المواصفة التنفيذية الشاملة لإنفاذ البوابات والسياسات والضوابط برمجيًا

**العنوان الإنجليزي:** LISAN — Executable Governance, Policy & Evidence Enforcement Specification  
**معرّف الوثيقة:** `LISAN-ENG-ENFORCEMENT-SPEC`  
**الإصدار:** `1.0.0-DRAFT`  
**التاريخ:** 23 أكتوبر 2026  
**الحالة:** `PROPOSED / NOT APPROVED / NOT DEPLOYED`  
**المرجع المنهجي:** `LISAN_Unified_Methodology_Governance_Enforcement_Spec_v1.0_DRAFT`  
**الجهة المستهدفة:** منظومة لسان القرآن؛ LibreChat عند ثبوت نسخه وقدراته؛ طبقات Corpus/Repository/MCP القائمة.  
**حدود الوثيقة:** مواصفة لتنفيذ ضوابط البحث والتحقق والإخراج؛ ليست تقريرًا بإتمام التنفيذ أو بقبول دلالة قرآنية.

> **القرار المعماري:** تُنفَّذ قواعد LISAN القابلة للقياس والتحكم في حدود ثقة برمجية مستقلة عن النموذج. يبقى النموذج مقترحًا للتحليل الدلالي، وتبقى المراجعة العلمية والاعتماد والنشر سلطات منفصلة. لا يجوز مساواة تعليمات Agent أو Skills ببوابات أمنية، ولا مساواة موافقة أداة أو قفل hash بصحة دلالية.

## 0. سجل الضبط واستخدام الوثيقة

| الحقل | القيمة | المعنى |
|---|---|---|
| درجة الإلزام | مسودة عقد تنفيذي | تصبح ملزمة بعد اعتماد مالك المشروع وبيان نطاقها |
| قاعدة المصدر | نص القرآن أولًا | الأدلة الدلالية الداخلية من corpus القرآني المثبت |
| قاعدة الذاكرة | Reuse Qualified | لا توريث اعتماد دون هوية ونطاق ونسخة ومصدر |
| Blind Lab | مستقل تشخيصيًا | لا ينفي أثر المعرفة التدريبية |
| تمثيل G0–G12 | واجهات وعقود واختبارات | يلزم إثبات تنفيذ كل بوابة على النسخة الفعلية |
| بيئة LibreChat | غير مفحوصة محليًا في هذه المهمة | أمثلة التهيئة مشروطة بالتحقق من إصدار النشر |
| السلطة على الشيفرة | لا كتابة على مشروع المستخدم | كل ملفات هذه الحزمة أمثلة/مخرجات فقط |
| برنامج مرجعي | PoC مستقل عن LibreChat | يختبر مبادئ محدودة، وليس ضمان امتثال إنتاجي |

### 0.1 مصادر التحليل وترتيب سلطة المرجع

1. **مرجع منهجي أعلى:** `LISAN — منهجية لسان القرآن للتحليل.txt` وموادها الـ35، ويُستعان بالوثيقة الموحدة السابقة لتفسير مصطلحات حالات البحث والبوابات.
2. **مرجع التكامل:** الوثيقة الموحدة `LISAN_Unified_Methodology_Governance_Enforcement_Spec_v1.0_DRAFT.md`، وخصوصًا G0–G12 وH01–H13 ومسارات الدراسة وAT-01–AT-30.
3. **موضوع هذه المراجعة:** `تنفيذ البوابات الموصوفة في وثيقة الثغرات.md`، وهي اقتراح يحتوي إعدادات وأمثلة تحتاج تحققًا أو تصحيحًا.
4. **مصادر مواصفات LibreChat العامة:** صفحات LibreChat الرسمية بشأن `agents`، و`toolApproval`، و`checkpointer`، و`Skills`، و`Agent Chain`، وMCP. هذه توثق قدرات المشروع العام لا تثبت نشرها أو تفعيلها لدى المستخدم.
5. **فحص قابلية حالي محدود:** أدوات لسان القرآن المتصلة بهذه المحادثة تُظهر جاهزية عمليات corpus ومستودع دراسات مرشح، ولا تثبت أنها الخدمات نفسها في مشروع LibreChat المحلي، ولا صلاحية اعتماد دلالي رسمي.

عند تعارض هذا التنفيذ مع المرجع المنهجي، لا يُلغى المرجع بالحداثة وحدها؛ يُعزل التعارض ويسجل قرار التفسير لدى صاحب الصلاحية. جميع الأمثلة الإنجليزية لـSQL/YAML/JSON/HTTP **عقود مرجعية**، وليست إعلانًا بأن الواجهات موجودة في البيئة المنشورة.

# 1. الملخص التنفيذي: كيفية تحويل المنهجية إلى ضمانات واقعية

يتحقق التحكم الفعلي عبر سلسلة: **هوية موثوقة → صلاحيات وقرار مسار موثوق → مصدر قرآني مثبت → أدوات استقراء وإيصالات → سجل أدلة → تحقق آلي مستقل → اختبار دلالي ومراجعة → قفل نسخة → قرار قبول منفصل → إخراج مضبوط**. يُسمح للمحادثة المباشرة بنطاق بحثي محدود وموسوم، لكن لا يجوز عدّ الكلام الحر المحادثي خرجًا رسميًا معتمدًا لمجرد طلب النموذج استدعاء Validator.

**ضمانات يمكن بناؤها بصورة حتمية عند صحة التنفيذ:** منع أدوات محظورة عبر Gateway، منع تغيير سجل مقفل دون Revision جديد، ضبط نطاق الاسترجاع ووحدة العد، مطابقة الاستشهادات المثبتة، رفض اعتماد بلا هوية صالحة، منع نشر مخرج رسمي دون سجل تحقق، والتحقق من التواقيع والإصدارات.

**ضمانات لا يوفرها ذلك:** إثبات أن أوزان النموذج لا تحمل معاني سابقة، إثبات صحّة كل تحليل نحوي أو دلالي تلقائيًا، منع كل أشكال التحيّز، أو ضمان صدق كل إجابة محادثية حرة خارج مسار النشر المحكوم.

**أهم تصحيح تنفيذي:** إن كان المطلوب إيقاف أي إجابة غير مؤهلة **قبل وصولها للمستخدم**، فـMCP `validate_output` و`toolApproval` وحدهما لا يملكان سلطة اعتراض نص الجواب الحر. لا بد من مسار إخراج خادمي موثوق أو طبقة اعتراض نهائية مثبتة، أو من واجهة تعرض فقط Artifact خرج من خادم النشر بعد التحقق. إن تعذر ذلك، يكون استخدام المحادثة `RESEARCH_DRAFT_UNVERIFIED`، ويصبح المسار الرسمي نتيجة منشورة مستقلة عن نص الوكيل.

# 2. المراجعة الفنية للملف المرفق: الصحيح والتصحيحات الواجبة

| رقم | الادعاء/الآلية في المرفق | نتيجة المراجعة | التعديل الملزم |
|---|---|---|---|
| RV-01 | `toolApproval.enabled`, `allow/deny/ask`, وأنماط `mcp:<server>:<tool>` | موثق في LibreChat الحالي عمومًا | تقييد التهيئة بالإصدار الفعلي واختبار أسماء الأدوات والبدائل؛ لا يفحص الدلالة |
| RV-02 | `mode: dontAsk` يرفض غير المطابق | تؤيده الوثائق الحالية | إعداد عام للنشر؛ قد يعطل وكلاء آخرين، لذا يُختبر في staging أو نشر مخصص قبل تطبيقه |
| RV-03 | `deny` يسبق `ask/allow` حتى مع `bypass` | موثق | لا تُنشئ `deny` واسعًا ثم تتوقع تجاوزه بـ`ask` أو hook |
| RV-04 | `ask: save_finding` يحقق قرار مخول لحفظ/اعتماد نتيجة | **غير صحيح** | موافقة تشغيل أداة ليست مراجعة بحثية ولا صلاحية `APPROVE`. يجوز حفظ Draft دون قبول، ويُنجز الاعتماد داخل AuthZ وRegistry |
| RV-05 | Hooks تستطيع التضييق سياقيًا | موثق من حيث المبدأ | مثال `module.exports=({toolName,context}) => ...` في المرفق غير مثبت كواجهة Plugin صحيحة؛ يُنشأ Adapter وفق توقيع نسخة المشروع مع اختبار عقد |
| RV-06 | Hook يمكنه منع انتهاء Agent دون `validate_output` | **غير مثبت** | Hooks `toolApproval` تدقق استدعاءات أدوات، ولا يثبت أنها اعتراض نهائي على كل الرسائل |
| RV-07 | `capabilities` في تعريف Agent المقدم في المرفق | الصياغة مختلطة النطاق | `endpoints.agents.capabilities` إعداد نشر عالمي؛ إعدادات Agent Builder وأدوات الوكيل منفصلة؛ افحص بناء النسخة المنشورة |
| RV-08 | تعطيل `web_search` يحجب الموروث | جزئي | يمنع مصدرًا خارجيًا عند صحة التهيئة، لكنه لا يمحو المعرفة السابقة في أوزان النموذج |
| RV-09 | `allowedUsers`/ACLs في MCP | احتمال تشغيلي يعتمد الإصدار | لا تُعد قواعد الوصول مثبتة في نشر المستخدم دون اختبارات مباشرة؛ ينفذ الخادم المقابل Authorization مستقلًا |
| RV-10 | `maxSubagents/agent_ids` يغلق جميع ثغرات التفويض | غير كافٍ | يقيّد قائمة أو عددًا؛ افحص صلاحيات الطفل والأدوات والـSkills وحالات Runtime/Action وCode |
| RV-11 | `checkpointer` Mongo TTL | موثق للوقوف والاستئناف | لا يعد مخزن بحث دائمًا ولا يمنح اعتمادًا، ويحتاج إلى معالجة انتهاء صلاحية الموافقة |
| RV-12 | Agent Chain يدعم `gate:` و`output_schema:` كما في مثال YAML | **مثال تصوري وليس تكوينًا LibreChat موثقًا** | تنفيذ بوابات الحالة في خادم LISAN؛ استخدام Chain للتنسيق فقط بعد تجربة فعلية |
| RV-13 | State Machine خارجي | صحيح معماريًا | لا يكفي أن يستدعي الوكيل `can_proceed` اختيارياً؛ يجب إنفاذ شروط الانتقال **داخل أداة التعديل نفسها** |
| RV-14 | `validate_output` أداة وحيدة لوكيل الإخراج | لا يكفي للنشر المحكوم | العرض الرسمي يجب أن يسحب مخرجات موثقة من الخادم، لا نصًا حرًا يمكن للوكيل تخطي فحصه |
| RV-15 | القفل عبر `hash` | صحيح لحماية ثبات محتوى محدد | لا يثبت صحة المعنى أو هوية من اعتمده؛ يجب تثبيت revision وreview/approval منفصلين |
| RV-16 | واجهات العد والصرف والمقابلات كلها أدوات حتمية | تعميم غير صحيح | العد والتحقق النصي حتميان بشرط صحة البيانات؛ الصرف والتقابل والفحص الدلالي قد يحتاجون مراجعة بشرية |
| RV-17 | الموافقة عبر `ask_user_question` | صحيح كواجهة استيضاح/توقف | لا تمنح Authorization؛ القرار الإداري يصدر عبر هوية ومخول يراجع Snapshot مثبتًا |
| RV-18 | إنجاز حد أدنى بـMCP جديد لكل وظيفة | قد يكرر الموجود | ابدأ بجرد لسان المتاح؛ أضف Adapter/مكوّن ناقص فقط مع حدود واضحة |

**استنتاج المراجعة:** المرفق يوفر آليات تشغيل مفيدة، لكن يجب رفض ضمانات: «الموافقة على أداة = قبول النتيجة»، و«Chain = State Machine»، و«Skill/Hook على استدعاء أداة = حراسة الجواب النهائي»، و«حظر البحث = غياب أثر التدريب». الحفاظ على هذه الحدود شرط الصدق الهندسي.

# 3. النطاق والأهداف ومتطلبات غير وظيفية

## 3.1 ضمن النطاق

- إنفاذ مسارات `REUSE_QUALIFIED`, `CUMULATIVE_EXTENSION`, `NEW_CORPUS_STUDY`, `INDEPENDENT_DIAGNOSTIC`, `POST_LOCK_EXTERNAL_COMPARISON`، وفرع `VERSE_COMPOSITION` المقيّد.
- Corpus manifest والبحث العددي والتحقق من نص الآية والمقطع وإثبات حدود FULL/PARTIAL.
- آليات G0–G12، وسجل أثر الأدلة، وH09/H10/H11، والقفل والاعتماد ونشر المخرجات الرسمية.
- ضبط استخدام LibreChat Agents وSkills وMCP/Tools وSubagents وAsk User وCheckpoint حيث ينطبق.
- التسجيل الآمن والمراقبة والتعافي والتدرج في الإطلاق واختبارات الاختراق السلبي.

## 3.2 خارج النطاق (ما لم يُفوض صراحة)

- تعديل مصدر القرآن أو بياناته الأصلية؛ منح اعتماد دلالي آلي؛ تدريب نموذج جديد؛ إنشاء واجهة LibreChat بديلة كشرط مسبق؛ فرض إنشاء عدد ثابت من الوكلاء أو خوادم MCP.
- الادعاء بإزالة المعرفة التراثية من أوزان النموذج؛ إقرار صحة تفسير أو معنى آية في هذه الوثيقة؛ نشر إنتاجي أو منح صلاحيات حية.

## 3.3 متطلبات التشغيل

- **Safety:** لا `ACCEPTED` ولا `RELEASED` خارج خدمة سياسة موثوقة؛ لا FULL بلا إيصال حصر؛ لا فتح أدوات خارجية في البحث المستقل.
- **Integrity:** سجلات بحث append-only أو ذات Revision غير قابل للتعديل؛ القفل يثبت snapshot محددًا مع digest وإصدار أداة ومصدر وسياسة.
- **Availability:** فشل validator أو registry يمنع الأثر الحرج ويتيح عرض Draft محدود عند انطباق السياسة.
- **Auditability:** كل انتقال وأداة وقرار مصحوب بـ`run_id/actor/role/policy_version/corpus_digest/trace_id`.
- **Isolation:** فصل القراءات، المستخدمين، النتائج السابقة، الوكلاء والأدوات حسب المسار؛ لا ترقية صلاحيات ببيانات مولدة من النموذج.
- **Recoverability:** استئناف checkpoint يتطلب إعادة فحص الصلاحيات وسياسة الإصدار وSnapshot قبل التنفيذ، ولا يُعيد تشغيل side effects المكررة.
- **Deployment:** الاستفادة مما يوجد أولًا وعدم تعديل شيفرة LibreChat إلا إذا أثبت اختبار فجوة أن الاعتراض النهائي غير ممكن بسطح آخر، وبعد تفويض منفصل.

# 4. المعمارية المرجعية وحدود الثقة

```text
User / Authenticated Actor
        │ (trusted identity, scope, explicit intent)
        ▼
LibreChat UI ── Agent / Skills / Subagents (UNTRUSTED for authority)
        │
        ▼
Tool Admission: native toolApproval + tested Hooks + MCP ACL
        │                    │
        │                    └── cannot certify arbitrary final text
        ▼
LISAN Policy/Research Orchestrator [TRUSTED SERVICE BOUNDARY]
  ├── Router G0; subject-bound session + tool entitlements
  ├── Corpus authority G1/G2/G3 (pinned Quran text)
  ├── Research/evidence store G3–G7 (draft, hypotheses, countersearch)
  ├── State transitions + Policy Engine + typed errors
  ├── Registry H09/H10/H11; immutable revisions + dependencies
  ├── Semantic Review G6/G8 + Approval authority G9
  ├── Blind Lab isolated session; external comparison G11
  └── Publication Guard G12 ──────► Verified Artifact / signed receipt
                                       │
                                       ▼
                                Controlled result view
```

## 4.1 دور كل مكوّن

| المكوّن | مالكه المقترح | ينفذ | لا يحق له |
|---|---|---|---|
| LibreChat Runtime | مسؤول التشغيل | محادثة/تنسيق/إشعارات/موافقة أداة/نقل سياق | تقرير صحة ادعاء قرآني أو إصدار `ACCEPTED` بذاته |
| Trusted Policy Gateway | مالك محرك لسان | AuthN/AuthZ، tool scope، route policy، state checks | إدراج معنى آية من رأيه |
| Corpus Adapter/Authority | مالك corpus | تطابق نص، selector، count، receipts، provenance | اعتماد تفسيرات أو عد ROOT من مطابقات TOKEN |
| Evidence Validator | مالك الجودة | Schema/text/coverage/links/history checks | منح حكم دلالي نهائي من مجرد تجانس البيانات |
| Research Agent | الباحث/النموذج | اقتراح فرضيات وتحليل وتحديد اعتراضات | رفع `SUPPORTED/ACCEPTED` أو تزوير مواضع |
| Reviewer | مراجع مؤهل مستقل | تقييم نقدي للأدلة والبدائل | اعتماد نيابة عن Authority دون تفويض |
| Approval Authority | مالك القرار | قبول/سحب/تقييد إصدار ونطاق محدد | تغيير محتوى snapshot أثناء الموافقة |
| Registry | مالك التخزين | حفظ تاريخ append-only وسلالة ومعاملات متزامنة | توريث الموافقات تلقائيًا للنسخ الجديدة |
| Publisher/Output Guard | مالك الإخراج | تحرير Result Artifact من سجل متحقق وموافق عليه | نشر نص النموذج الحر باعتباره مؤهلاً |
| Heritage Auditor | فريق المعايرة | تنبيه `FLAG_ONLY` عن تشابهات/قفزات | الحكم بأن التطابق مع التراث دليل خطأ |

## 4.2 حدود الثقة الإلزامية

1. `request.role` أو `approved_by` الوارد من نموذج أو JSON أو Skill **لا يُقبل**. تؤخذ الهوية والأدوار من Middleware خادمي مرتبط بجلسة مستخدم مصادق عليها، ويطبق التفويض على كل استدعاء.
2. Corpus وملفات RAG والذاكرة والمرفقات ومخرجات MCP هي **بيانات غير آمنة للتعليمات** حتى لو احتوت نصوصًا توجيهية أو حقولًا تشبه `system`.
3. لا يكتسب الوكيل صلاحيةً لأنه يستطيع رؤية أداة. أداة التصديق نفسها تتحقق في الخادم من Actor وStudy وPhase وRevision وPolicy.
4. كل فعل ذي أثر يمر بمعاملة تخزين موثوقة؛ الاستدعاء الاستعلامي `state.can_proceed` مفيد للتخطيط ولا يكفي وحده للإنفاذ.
5. لا يجوز أن يصل Agent أو مستخدم HTTP عادي إلى قاعدة البيانات مباشرة ببيانات اعتماد تتيح تجاوز قيود الخادم.
6. نتيجة Blind Lab استقلال **سياقي/أداتي مسجل**؛ تدريب النموذج مستقل عن سلطة أدوات التشغيل ولا يمكن نفي أثره.
7. تشغيل LibreChat بوكلاء آخرين يستلزم تقييم تأثير `toolApproval` العالمي قبل تطبيق `dontAsk`؛ يمكن استخدام مثيل مخصص أو سياسة افتراضية أقل تقييدًا مع حراسة صارمة داخل خادم لسان.

## 4.3 مسارات نشر بديلة

| البديل | الوصف | مستوى ضبط المخرج | القرار |
|---|---|---|---|
| D1 — Native-config only | Agents + Skills + toolApproval + prompt | محدود على الأدوات؛ لا يلزم التحقق من جواب حر | يصلح فقط لمسودة بحث غير معتمدة |
| D2 — MCP trusted registry + Verified Artifact | LibreChat ينسق؛ خادم لسان يعيد سجلًا مقفلاً مع Receipt ويعرض المستخدم النتيجة الرسمية منه | قوي على الأثر والتخزين والإخراج **الرسمي**؛ لا يوقف الكلام الحر | **الاختيار الافتراضي** إذا لم تتوفر اعتراضات نهائية موثقة |
| D3 — Host final-response interception | ربط فحص خادمي مؤكد بجميع مسارات streaming/final/retry/tool-free output | يحجب الادعاءات المخالفة قبل النشر من القناة المحادثية | مشروط بتثبيت Surface وسلامته عبر اختبارات؛ يحتاج تفويضًا إضافيًا إذا عدل LibreChat |

**لا يُسمح بدعاية «حماية جميع الإجابات» عند اعتماد D2 فقط.** يحمي D2 الـArtifact الرسمي، أما المحادثة الحرة فتبقى صادرة من النموذج، ويجب الفصل البصري واللفظي في المنتج بينهما.

---
# 5. سياسة التوجيه Router (G0) — عقد قرار قابل للتنفيذ

## 5.1 أنواع الطلبات ومدخلات الثقة

يدخل الطلب من واجهة موثوقة بوثيقة `ResearchRequest` تشمل: `request_id`, `actor_id`, `tenant_id`, `question`, `target_type` (WORD/ROOT/PAIR/VERSE/VERSES), `scope`, `independence_requested`, `external_comparison_requested`, `method_revision`, `corpus_selector`, `requested_output`. مصدر `actor_id/tenant_id` هو سياق مصادقة الخادم، وليس نص المستخدم ولا متغيرًا يخرجه النموذج. يتولى النموذج **اقتراح** نية أو هدف لغوي، لكن Router يتحقق من القيم ويمنع المسار غير المصرح.

## 5.2 خوارزمية قرار ملزمة

```python
# PSEUDOCODE, NOT LIBRECHAT OR MCP SDK

def choose_route(req, identity, registry, policy):
    if not identity.authenticated: raise Deny('AUTH_REQUIRED')
    scope = policy.validate_scope(req.scope, corpus=req.corpus_selector)
    if not scope.unambiguous: return 'CLARIFICATION_REQUIRED'
    if req.independence_requested or policy.requires_diagnostic(req, scope):
        return 'INDEPENDENT_DIAGNOSTIC'
    if req.external_comparison_requested:
        if not identity.can('EXTERNAL_COMPARE'): raise Deny('EXTERNAL_NOT_AUTHORIZED')
        locked = registry.find_compatible_locked_internal(scope)
        return ('POST_LOCK_EXTERNAL_COMPARISON' if locked
                else 'INTERNAL_FIRST_THEN_EXTERNAL')
    eligible = registry.get_current_qualified(scope, identity.tenant_id)
    if eligible and eligible.covers(scope) and eligible.approval_valid:
        return 'REUSE_QUALIFIED'
    if eligible and eligible.partially_covers(scope):
        return 'CUMULATIVE_EXTENSION'
    return 'NEW_CORPUS_STUDY'
```

**الأولوية الحاكمة:** الاستقلال الصريح يسبق الذاكرة، ثم المقارنة الخارجية الصريحة، ثم الصلاحية المكتملة، ثم التوسعة، ثم البحث الجديد. لا يستطيع Agent تعديل `mode` في تخزين النظام بمجرد القول إنه غيّر المسار؛ إصدار رمز سياق Mode جديد يحتاج تحققًا من Router.

## 5.3 مصفوفة العمليات بحسب الوضع

| العملية | New | Reuse / Extend | Independent | External Post-Lock | Admin |
|---|---|---|---|---|---|
| Corpus text/query | Allow | Allow | Allow | Read verify | Allow |
| Qualified prior findings | Restrict + Exposure | Allow scoped | Deny for researcher | Read | Allow |
| External lexical/tafsir | Deny during internal claim formation | Deny for new internal claims | Deny | Allow explicit | Read as admin only |
| Save research draft | Allow subject-bound | Allow new revision | Allow diagnostic | External note only | Governed |
| Internal lock | After G1–G6 | New version only | Diagnostic snapshot | Deny editing original | Governed |
| Semantic review | Reviewer only | Reviewer only | Reviewer only | Compare only | Reviewer role |
| Approval | Deny model | Deny model | Deny model | Deny model | Approver independent |
| Publication | Validated artifact only | Validated artifact only | Diagnostic label only | Explicitly labeled comparison | Publisher |

## 5.4 حراسة المسار أثناء التشغيل

يُنشئ Router سياق تشغيل داخليًا `RunContext` ويحفظه في مخزن موثوق: `{run_id, actor_id, tenant_id, mode, corpus_digest, method_digest, policy_digest, allowed_tool_classes, created_at, expires_at, current_study_id}`. لا يعتمد السياق على خصائص يرسلها النموذج مثل `agentPhase`, `is_admin`, `lock=true`. كل طلب MCP يحمل Token خدمة قصير الصلاحية أو Context يعاد التحقق منه خادميًا ومرتبطًا بـrun/actor/tenant، وتُرفض الجلسات غير المعروفة أو منتهية الصلاحية.

**ملاحظة صيغة الأدوار:** إن كان LibreChat لا يمرر Principal موثوقًا إلى MCP كما هو مطلوب، لا تُفترض هوية المستخدم من وسيطة JSON. يجب بناء حلقة مصادقة خادمية مدعومة أو تعيين خدمة بصلاحية دنيا مع حصر العمليات المسموحة إلى المسودات؛ ويُمنع اعتماد النتائج حتى وجود هوية مستوفية.

# 6. Policy-as-Code ومنع تجاوز الأدوات

## 6.1 السياسة الفعلية

تُقسم السياسة إلى: `AdmissionPolicy` قبل استدعاء الأداة؛ `TransitionPolicy` قبل تغيير حالة الدراسة؛ `EvidencePolicy` قبل القفل؛ `ApprovalPolicy` قبل الاعتماد؛ `PublicationPolicy` قبل إصدار المخرج المعتمد. تُشغّل على خادم موثوق ولا تقبل تعديلات Runtime من النموذج. ترتيب التقييم: **رفض صريح → قواعد صلاحية مقيّدة → مراجعة مطلوبة → رفض افتراضي**. على تغيّر السياسة يُعاد فحص الترخيص قبل استئناف أي عملية مؤجلة.

```yaml
# Logical Policy Document — not a built-in LibreChat YAML schema
policy_id: LISAN-POLICY
revision: 1
principle: default_deny
routes:
  INDEPENDENT_DIAGNOSTIC:
    permitted_classes: [CORPUS_READ, SUBMIT_DIAGNOSTIC_DRAFT]
    forbidden_classes: [EXTERNAL_READ, QUALIFIED_MEMORY_READ, APPROVE, PUBLISH]
  NEW_CORPUS_STUDY:
    permitted_classes: [CORPUS_READ, STUDY_DRAFT_WRITE, INTERNAL_LOCK]
    forbidden_classes: [EXTERNAL_READ, APPROVE, PUBLISH]
  POST_LOCK_EXTERNAL_COMPARISON:
    requires: [EXPLICIT_INTENT, INTERNAL_LOCK_VALID]
    permitted_classes: [CORPUS_READ, LOCKED_RESULT_READ, EXTERNAL_READ, EXTERNAL_NOTE_WRITE]
critical_transitions:
  ACCEPTED: [AUTHORIZED_APPROVER, INDEPENDENT_REVIEW, SNAPSHOT_MATCH]
  RELEASED: [AUTHORIZED_PUBLISHER, ACCEPTED_CURRENT, OUTPUT_CHECK_PASSED]
on_tool_denial: DENY_AND_AUDIT
on_validator_unavailable: FAIL_CLOSED_FOR_OFFICIAL_OUTPUT
```

**الفصل الواجب:** الموافقة على استدعاء أداة الإدخال `save_draft` لا تتطلب عادة موافقة اعتماد معنى؛ تتطلب فقط تحقق صلاحية حفظ المسودة، أما `approve_revision` فهي فعل حاكم منفصل لا يربط بالنموذج مباشرة. وإذا طلب المستخدم اعتمادًا بالواجهة، تحيله خدمة الهوية إلى مخول نظاميًا.

## 6.2 مثال `librechat.yaml` مثبت من حيث بنية الحقول فقط

```yaml
# EXAMPLE for a dedicated/test LibreChat deployment.
# MUST validate against the exact checked-out LibreChat release and tool registry.
endpoints:
  agents:
    maxSubagents: 5
    toolApproval:
      enabled: true
      mode: dontAsk
      allow:
        - 'mcp:lisan-corpus:get_*'
        - 'mcp:lisan-corpus:search*'
        - 'mcp:lisan-corpus:verify_*'
        - 'mcp:lisan-corpus:count*'
        - 'mcp:lisan-guard:submit_draft'
      ask:
        - 'mcp:lisan-external:compare'
      deny:
        - 'mcp:*:delete_*'
        - 'mcp:*:drop_*'
      reason: 'Review {tool} before it runs.'
    checkpointer:
      type: mongo
      ttl: 86400
```

**تحذيران:** (1) `mode: dontAsk` ينطبق على جميع أدوات Agents في هذا النشر، ويمنع غير المطابق؛ لذلك يُفضّل في **بيئة مخصصة لـLISAN**، وليس تحويل نشر LibreChat عام إلى وضع رفض شامل دون تحليل الأثر. (2) نمط `mcp:<server>:<tool>` يجب مطابقته مع أسماء runtime والنماذج الفعلية؛ مثال `mcp:lisan-guard:submit_draft` لا يثبت أن الخادم موجود. لا تتضمن هذه القائمة `approve_revision` إطلاقًا كي لا تصبح الموافقة الإدارية مجرد موافقة زر. يُختبر ما إذا كانت wildcard تتداخل مع اسم أداة أكثر امتيازًا.

## 6.3 Hooks — تصحيح المثال البرمجي المرفق

توثق LibreChat الحديثة `toolApproval.hooks` ووصف `module/matcher/options` وتؤكد أنها قادرة على **تضييق** الحكم الثابت. لكن التوقيع التفصيلي لكتابة module صالح للنسخة المحلية **لم يُفحص من مصدر الشيفرة المثبت هنا**، لذلك لا يُسمح بنسخ المثال التالي بوصفه Hook جاهزًا. هذه دالة السياسة المستقلة التي يجب أن يستدعيها Adapter مختبَر:

```javascript
// Logical pure function — NOT a validated LibreChat hook export/API.
function decideToolPolicy(trustedContext, requestedTool) {
  if (!trustedContext?.authenticated || !trustedContext?.runVerified) {
    return { decision: 'deny', reason: 'UNTRUSTED_RUN_CONTEXT' };
  }
  const internalModes = new Set(['NEW_CORPUS_STUDY', 'INDEPENDENT_DIAGNOSTIC']);
  if (internalModes.has(trustedContext.mode) && requestedTool.class === 'EXTERNAL_READ') {
    return { decision: 'deny', reason: 'EXTERNAL_SOURCE_IN_INTERNAL_PHASE' };
  }
  if (requestedTool.class === 'EXTERNAL_READ' &&
      (!trustedContext.lockValid || !trustedContext.externalIntentVerified)) {
    return { decision: 'deny', reason: 'POST_LOCK_AUTH_REQUIRED' };
  }
  return { decision: 'no_stronger_rule' };
}
```

الإجراء الفعلي: يُفحص مصدر `toolApproval` في نسخة LibreChat المحلية، تُكتب وحدة محمّلة عبر `module` وفق توقيعها، ثم تُبنى اختبارات عقد تثبت fail-closed عند غياب سياق موثوق، ورفض الأدوات المحظورة عبر Subagents، وعدم قدرة hook على تجاوز `deny` ثابت. **حتى نجاح هذه الاختبارات لا يعني فحص الرسالة النهائية.**

## 6.4 تقليل القدرات لا يكفي بذاته

خاصية `endpoints.agents.capabilities` في وثائق LibreChat تحدد السقف المتاح عند النشر، أما اختيار الأدوات والـSkills ونطاقها في Agent Builder فهو ضبط آخر. لا يجوز نسخ `capabilities:` الخاص بوكيل كأنه YAML لكل Agent دون التحقق من عقد API في النسخة الحالية. في Blind Lab يُوصى: عدم اختيار Web Search/File Search/Actions/Code Interpreter، منع صلاحيات قواعد البيانات والذاكرة القديمة، تقليل Skills وعدم السماح لمهارة جديدة بتوسيع الأدوات، واختبار child agents في runtime. إذا كانت Skills تُستخدم، تُمنع `allowed-tools` التي توسع السطح في الدراسة المستقلة.

## 6.5 سياسة تجاوزات أخرى

- **Prompt injection:** التعامل مع نتائج RAG والتفاسير والآيات والمراجعات كبيانات؛ عدم تفسير التعليمات المضمنة على أنها أوامر.
- **Tool aliases:** ربط الأداة بهوية مرجعية canonical في الخادم، والتحقق من alias/runtime/tool schema، لا الاعتماد على النص الظاهر للنموذج.
- **Direct API bypass:** منع تنفيذ `approve` و`release` مباشرة من مستخدم API دون AuthN/AuthZ وإثبات قفل ومراجعة؛ لا تعتمد الحراسة على واجهة LibreChat وحدها.
- **Subagent escape:** مراجعة اختيار Skills والـMCP الخاص بكل طفل، وإعادة تنفيذ سياسات التعديل داخل الخدمة نفسها.
- **Privileged service account:** عدم منح لسان service principal حق تجاوز التعاريف؛ افصل credentials القراءة والكتابة والنشر.
- **Secret management:** مفاتيح التوقيع والمصادقة في إدارة أسرار الخادم، لا في prompts أو ملفات Skill أو logs.

# 7. Corpus Authority — تثبيت المصدر والعد والتغطية

## 7.1 عقد مصدر قرآني ثابت

`CorpusManifest` يجب أن يحوي: `corpus_id`, `version`, `edition`, `reading`, `orthography`, `numbering`, `basmala_policy`, `source_original_sha256`, `normalized_corpus_sha256`, `manifest_sha256`, `normalization_profile`, `index_version`, `verification_status`, `verification_actor`, `verification_evidence_uri`. يُثبت المصدر قبل إنتاج نتائج مؤهلة، ويُرفض أي تبديل نص أو تحديث فهرس صامت.

**المتاح المفحوص في هذه المهمة عبر أدوات اتصال مستقلة:** حالة corpus `READY_FOR_CORPUS_OPERATIONS`، هوية `tanzil-uthmani-v1.1`/`Tanzil-Uthmani-1.1`، 6236 سجل آيات، بصمة corpus `0ae05c1b6c08196b86ea53d166f10e8558e844a37678043730dc7f60ecc09afa`، وحالة أصالة `OWNER_ATTESTED_NOT_AUTOMATICALLY_PROVEN`، و`semantic_release_accepted=false`. **هذه بيانات اتصال مرشح، وليست تقرير فحص نسخة LibreChat المحلية أو توثيق اعتماد دلالي.**

## 7.2 الاستعلام الدقيق ومطابقة النص

- `get_verse(ref)` يعيد النص من نسخة ثابتة مع provenance.
- `search_token/forms` يعيد حدود `TOKEN/MATCH_EVENTS` من النص مثبت الهوية.
- `search_structural(ROOT/LEMMA/WORD)` يتطلب فهرسًا صرفيًا ذا تغطية معروفة، ولا يجوز استنتاجه من بحث صيغ عادي.
- `verify_quote(ref,text,kind)` يتحقق من نص كامل أو مقطع متصل، ويُظهر إصداره.
- `count_matches` يصرح عن `VERSES`, `MATCH_EVENTS` أو `WORD_OCCURRENCES` وما يقيسه فعلًا، وفترة/نطاق query digest.
- `coverage_report` يحسب `expected/retrieved/analyzed/remaining` **على وحدة العَدّ نفسها**. احتواء مرجع الآية ضمن مجموعة لا يثبت وحده تحليل كل مفردة متكررة بداخلها.

## 7.3 سياسة FULL / PARTIAL

```python
# Logical invariant, not a function in the current deployed project.
full = (
    corpus_manifest.source_check_passed
    and corpus_index.complete_for_exact_selector
    and selector_digest == receipt.query_digest
    and expected_unit_ids == retrieved_unit_ids
    and expected_unit_ids == analyzed_unit_ids
    and remaining_unit_ids == set()
    and count_unit_consistent
)
if not full:
    coverage_status = 'PARTIAL' if some_units_verified else 'UNVERIFIED'
```

لا تعتمد `FULL` على صدق النموذج عندما يقول إنه قرأ جميع المواضع؛ المدقق يستخرج المجموعة من snapshot/frozen query وإيصالات الاسترجاع. الاستثناءات التي يصعب حصرها تحول الحالة إلى `UNVERIFIED` لا إلى `FULL` بالتخمين.

## 7.4 الوسوم الصرفية والنحوية

يفصل السجل `TEXT_SPAN` عن `STRUCTURAL_ANNOTATION` وعن `DISTRIBUTIONAL_OBSERVATION` وعن `SEMANTIC_INFERENCE`. تُرفق الوسوم البنيوية بمصدرها وإصدارها ومرجعها وباحثها. قد يستخدم النظام محللات مساعدة، لكن `get_morphology` ليس مصدر دلالة تلقائيًا. وجود تعارض في الجذر أو الفاعل أو المتعلق يولد `STRUCTURAL_UNCERTAINTY` ويمنع ترقية الادعاء المتوقف عليها حتى مراجعته.

## 7.5 ضد التمثيل الخاطئ

المثال السابق الذي وضع `object: النبي` ضمن سجل `2:157` غير مؤهل ملاحظةً مباشرة. يجب أن يتحقق المدقق من النص وإسناد الحقل إلى span أو مراجعة بنيوية. وكذلك لا يجوز استخدام رقم `47` أو أي عدد من ذاكرة النموذج بلا `count_receipt`. هذا اختباران إلزاميان، لا بحث دلالي عن مفردة «صلوات» في هذه الوثيقة.

# 8. Evidence Schema وValidator — من JSON صالح إلى دعوى قابلة للمراجعة

## 8.1 الحد الأدنى للاستكشاف (MVP-7)

```json
{
  "study_id": "example-st1",
  "revision": 1,
  "corpus": {"id": "pinned-id", "sha256": "sha256-at-runtime"},
  "scope": {"selector": "TOKEN:EXAMPLE", "query_digest": "generated-on-server"},
  "claims": [{"id": "C1", "type": "OBSERVATION", "refs": [],
              "warrant": "يجب توثيق وجه الاستدلال قبل التأهيل",
              "verification_status": "NOT_VERIFIED"}],
  "epistemic_status": "HYPOTHESIS",
  "approval_status": "NOT_GRANTED",
  "limitations": ["مثال غير مؤهل للنشر"]
}
```

هذا سجل أولي يسمح بالحفظ والتصنيف، **ولا يعني** أن كل حقوله مثبتة. القيم الوصفية `sha256-at-runtime` لا يجوز تمريرها في بيئة إنتاجية. عند التأهيل يُستبدل MVP بمخطط موسع ذي قيود مرجعية وتاريخية.

## 8.2 مخطط الدعوى الموسع

| الحقل | طبيعة التحقق | مسؤول التحقق |
|---|---|---|
| `claim_id` و`claim_type` | Schema + uniqueness | Validator |
| `statement` | وجود + قيود النوع + مراجعة المعنى | Validator + Reviewer |
| `claim_scope` | توافق مع query/reading/form/role | Router/Index |
| `evidence[]: ref/exact_text/kind` | مطابقة النص مثبت المصدر | Corpus Authority |
| `annotation[]` | إسناد بنيوي ومصدر/إصدار | Structural Reviewer |
| `warrant` | هل تربط الحجة الشواهد بالدعوى؟ | Semantic Reviewer |
| `competitors` | وجود فرضيات منافسة حقيقية | Reviewer |
| `falsification_condition` | قابلية الاختبار وعدم العمومية | Reviewer |
| `countersearch_receipt` | أداة منفذة، مجموعة، نتيجة، سلطة الحكم | Validator + Reviewer |
| `coverage` | بسط/مقام ووحدة query | Corpus Index |
| `epistemic_status` | سند مبرر + تصنيف سليم | Reviewer/Engine |
| `review_status` | قرار مستقل مرتبط بالنسخة | Review Service |
| `approval_status` | AuthZ + scope/revision/expiry | Approval Authority |
| `release_status` | سلامة النشر ووثيقة العرض | Publisher |

الأنواع المقترحة: `DIRECT_TEXT`, `STRUCTURAL_OBSERVATION`, `DISTRIBUTIONAL_OBSERVATION`, `COUNT`, `TENTATIVE_HYPOTHESIS`, `SUPPORTED_INFERENCE`, `CONTEXTUAL_APPLICATION`, `COUNTERFACTUAL_NOT_QURAN`, `POST_LOCK_EXTERNAL_NOTE`.

## 8.3 كيف يعمل Validator؟

1. يفحص هوية المصدر وبصماته، والإصدارين `method` و`policy`.
2. يختبر مخطط البيانات وأنواع حقول الدعوى وعدم وجود قيم مصطنعة.
3. يعيد جلب كل شاهد من Corpus Authority ويطابق النص المحرر ونوع النقل.
4. يقارن `selector/query_digest/count_unit` ببيان التغطية؛ يمنع مساواة TOKEN بـROOT.
5. يتحقق من أن كل ملاحظة بنيوية مرتبطة بنص/وسم معلوم، ويميز ما لم يخضع لفحص مختص.
6. يثبت حدوث بحث مضاد ويرفض اختلاقه؛ يقبل `NOT_FOUND_IN_EXAMINED_SCOPE` عند توفر receipt.
7. يتحقق من عدم انتقال حالة اعتماد قديمة إلى نسخة جديدة.
8. ينتج `GateCheckReport` بأسباب محددة، ولا يعين `SUPPORTED` من تلقاء نفسه.

**الحد المعرفي:** يمكن للمدقق البرمجي رفض الادعاء غير المسند بمصدر، ولكنه لا يثبت أن وجه الاستدلال من الشواهد يؤدي بالضرورة إلى النواة الدلالية؛ تلك مسؤولية G6/G8.

## 8.4 نتيجة تحقق قابلة للتتبع

```json
{
  "validator_version": "version-at-build",
  "study_id": "example-st1",
  "revision": 1,
  "gate": "G3",
  "verdict": "FAIL",
  "failure_code": "OBSERVATION_NOT_GROUNDED",
  "violations": [{"claim_id": "C1", "ref": "2:157", "path": "$.claims[0].annotation"}],
  "corpus_digest": "resolved-at-runtime",
  "evidence_receipts": [],
  "decision_source": "SERVER_VALIDATOR"
}
```

حالات فحص البوابة هي: `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`. لا تُعامل `BLOCKED` أو `NOT_RUN` كنجاح، ولا يُسمح للوكيل بتعديل تقرير المدقق. تُحفظ تفاصيل ما فشل حتى يستطيع المراجع معرفة الحد غير المثبت.

---
# 9. مواصفات البوابات G0–G12: واجهة، مدخل، قاعدة، أثر، فشل

كل بوابة **شرط على خادم التنفيذ** وليست تعليمات للنموذج أن «يتذكر التحقق». `GateReceipt` يرتبط بـ`study_id`, `revision`, `run_id`, `stage`, `policy_digest`, `corpus_digest`, `actor_id`, `input_digest`, `validator_version`, `verdict`, `failure_code`, `checked_at`. يجري إعادة استخدام إيصال صالح مرتبط بـsnapshot نفسه دون إعادة الاستقراء كل مرة، مع بقاء صلاحيات الاعتماد قابلة للسحب.

| بوابة | موضع الإنفاذ الموثوق | إجراء/تدقيق قبل الانتقال | الفشل أو التراجع | اختبارات |
|---|---|---|---|---|
| `G0 — Route` | Router + Policy Service | AuthN، تصنيف النطاق، Mode، حدود المستخدم والوكيل، إصدار السياسة | `CLARIFICATION_REQUIRED` / `INVALID_SCOPE` / `AUTH_REQUIRED` | AT-02,04,05,06,17,26,25 |
| `G1 — Corpus` | Corpus Authority | تحقق manifest وبصمة الإصدار والقراءة وأصل المصدر ضمن سياسة الإطلاق | `SOURCE_UNVERIFIED`؛ مسودة فقط | AT-03,07,08 |
| `G2 — Coverage` | Index + Coverage Validator | إعادة إنشاء قائمة المرجع/المطابقات ووحدة العد وتطابق query digest | `COVERAGE_UNVERIFIED`؛ لا FULL | AT-02,10,11 |
| `G3 — Observation` | Evidence Validator | نص/مرجع/span/مصدر وسم صرفي أو حالة شك | `OBSERVATION_INVALID` / `STRUCTURAL_UNCERTAINTY` | AT-09,20 |
| `G4 — Hypothesis` | Engine + Reviewer | فرضية قابلة للتضييق والنقض وبدائل واعتمادها على ملاحظات | `HYPOTHESIS_INCOMPLETE` | AT-13 |
| `G5 — Countersearch` | Search Tool + Validator | إيصال بحث مضاد فعلي والنطاق والنتيجة حتى إن لم يُعثر على مضاد | `COUNTERSEARCH_NOT_RUN`؛ لا ترقيات | AT-12,18 |
| `G6 — Semantic Warrant` | Independent Semantic Reviewer | هل الحجة تُجيز النتيجة/الحدّ ونُوقشت البدائل؟ | `SEMANTIC_REVIEW_REQUIRED` / `UNRESOLVED` | AT-13,14 |
| `G7 — Internal Lock` | Immutable Registry Transaction | Snapshot مغلق + digest + CAS + policy/version | `LOCK_FAILED` / `REVISION_CONFLICT` | AT-16,23,27,28 |
| `G8 — Review` | Review Service | Reviewer ≠ author، قرار مسبب، أدلة/اعتراضات | `NOT_REVIEWED` | AT-14,15,28 |
| `G9 — Approval` | AuthZ + Approval Service | Approver مخول، revision/scope/digest مضبوط، قرار غير مسحوب | `NOT_GRANTED` / `APPROVAL_UNVERIFIED` | AT-01,03,23,24,30 |
| `G10 — Contextualize` | Contextualizer + Validator | تحليل المفردات المحورية، وربط معنى الموضع وحالاته | `CONTEXTUALIZATION_LIMITED` | AT-19 |
| `G11 — External Boundary` | External Adapter + Registry | طلب صريح + internal lock + تقرير منفصل لا يكتب الأصل | `EXTERNAL_ACCESS_DENIED` | AT-05,16,29 |
| `G12 — Publication Guard` | Verified Output Service | إعادة بناء إخراج من record متحقق، current approval، كل إيصالات النشر | `OUTPUT_WITHHELD` / مسودة غير معتمدة | AT-07,08,18,21,22,25,29 |

## 9.1 شرط عدم تجاوز البوابات

يمكن للوكيل طلب `transition(study_id, expected_revision, target_phase)`، لكن **الانتقال نفسه** يعيد فحص الحقول والإيصالات والحقوق داخل Transaction واحدة. إذا استُدعي `state.can_proceed` ثم تغيرت السياسة أو الاعتمادات، لا يكفي تقرير السماح السابق. لا يُقبل مستند `GateReceipt` مصاغ من نموذج الذكاء كأنه نتيجة فعلية؛ يُعاد التحقق من توقيعه أو مصدره المستقل.

## 9.2 خوارزمية انتقال مرجعية

```python
# Pseudocode, atomic transaction required in production

def transition(actor, study_id, expected_revision, requested_step, payload):
    with db.transaction(serializable_or_optimistic_cas=True):
        s = db.get_current_for_update(study_id)
        assert_actor_and_tenant(actor, s)
        if s.revision != expected_revision: deny('REVISION_CONFLICT')
        policy = load_current_policy(s.tenant_id)
        assert_transition_allowed(s.stage, requested_step, policy)
        evidence = fetch_authoritative_receipts(s, requested_step)
        result = evaluate_gate(requested_step, s, evidence, policy)
        if result.verdict != 'PASS':
            db.append_rejection(s, result)
            deny(result.failure_code)
        db.append_transition_and_outbox(s, requested_step, result)
        return db.get_current(study_id)
```

يستحسن أن تكون حالة الدراسة ضمن خدمة واحدة تملك State Machine وRegistry، حتى لا تتحول معاملات قفل الدراسة والتخزين إلى عمليات منفصلة معرضة للتسابق. يمكن أن تكشف MCP أدوات متعددة فوق الخدمة نفسها؛ لا يلزم خادم MCP مستقل لكل وظيفة.

## 9.3 حالات التراجع المقبولة

- في نقص الشواهد: `HYPOTHESIS` أو `UNRESOLVED` مع `coverage=PARTIAL/UNVERIFIED` و`limitations`.
- في فشل استشهاد: تُرفض الدعوى النصية المعينة؛ إن كانت محورية لا يُسمح بنشر النتيجة التابعة لها.
- في اختلاف نحوي: `STRUCTURAL_UNCERTAINTY` بلا ادعاء حسم؛ تُقدم قراءة بديلة عند وجود بيانات.
- في فشل أداة: `TOOL_UNAVAILABLE` و`NOT_RUN`؛ يُوقف الانتقال، ويُسمح باستئناف محدود بعد تصحيح السبب من دون تجاوز التفويض.
- في تعارض فرضيتين: `UNRESOLVED` وليس تعميمًا يجعل اللفظ يفسر كل شيء.
- في عدم ظهور مضاد بعد بحث موثق: `NOT_FOUND_IN_EXAMINED_SCOPE` مع نطاق البحث؛ لا يطلب الخادم وجود شاهد مضاد مختلق.

# 10. State Machine وفصل الحالة المعرفية عن الاعتماد

## 10.1 محاور الحالة الأربعة

| البعد | قيم أساسية | مالك التغيير |
|---|---|---|
| `epistemic_status` | `OBSERVATION`, `HYPOTHESIS`, `TESTED`, `SUPPORTED`, `UNRESOLVED`, `REJECTED` | Engine بحسب الدراسة وتقييم Reviewer |
| `review_status` | `NOT_REVIEWED`, `REVIEW_REQUIRED`, `REVIEWED`, `CHALLENGED` | Review Service |
| `approval_status` | `NOT_GRANTED`, `ACCEPTED`, `REVOKED`, `EXPIRED` | Approval Authority |
| `release_status` | `NOT_RELEASED`, `RELEASED`, `WITHDRAWN` | Publisher مستقل |

تُخزن حالة سير العمل `phase` منفصلة عن هذه الأبعاد: `SCOPED → OBSERVED → HYPOTHESIZED → COUNTER_CHECKED → INTERNAL_LOCKED → REVIEWED → [ACCEPTED] → [RELEASED]`. `G10/G11` مساران لاحقان مشروطان بنوع الطلب وليسا ترقيات واجبة لكل مفردة. تسمح حالة `UNRESOLVED` بتحرير مسودة معلنة، ولا تستلزم الصمت.

## 10.2 جدولة انتقالات مقيدة

| العملية | الحالة السابقة | المتطلبات | النتيجة |
|---|---|---|---|
| `submit_observations` | `SCOPED` أو `OBSERVED` | G1/G2/G3، actor researcher | `OBSERVED` |
| `propose_hypothesis` | `OBSERVED` | G4 وأدلة مرجعية | `HYPOTHESIZED` |
| `record_countersearch` | `HYPOTHESIZED` | G5 بنطاق صريح | `COUNTER_CHECKED` |
| `seal_revision` | `COUNTER_CHECKED` | G1–G7 مكتملة للنطاق المصرح | `INTERNAL_LOCKED` |
| `record_review` | `INTERNAL_LOCKED` | reviewer مستقل وصلاحية ومبرر | `REVIEWED` |
| `approve_revision` | `REVIEWED` | G9 وscope/revision/digest/role | `ACCEPTED` دون تعديل القفل |
| `publish_artifact` | `ACCEPTED` | G12 + publisher + current approval | `RELEASED` |
| `request_reopen` | نسخة مقفلة أو متنازع عليها | سبب وactor صالح | `NEEDS_REOPEN` مع طلب Revision جديد |
| `create_new_revision` | بعد سبب مشروع | Snapshot سابق للرجوع فقط | `revision+1`, `NOT_REVIEWED`, `NOT_GRANTED`, `NOT_RELEASED` |

لا يُنقل `SUPPORTED` تلقائيًا من مجرد قفل أو من إجابة نموذج ثانٍ. يمكن إعطاء `SUPPORTED` للنطاق العلمي بعد استكمال الشواهد والمراجعة حتى عندما يبقى `approval_status=NOT_GRANTED`، بينما اعتماد إداري صحيح لا يجعل النتيجة يقينية.

## 10.3 بقاء القفل وعدم تعديله

القفل يثبت **حمولة البحث الداخلي** (الدعوى، الأدلة، النطاق، المصدر، شروط النقض، القيود) ببصمة Canonical Serialization، لا يحول البصمة إلى صحة. سجل المراجعة والتخويل والنشر موضوعات metadata/أحداث منفصلة، لا تغير الحمولة المقفلة. أي تعديل على معنى داخلي يفرض revision جديدة وإبطال قابلية إعادة الاستخدام للنسخة المتأثرة إلى أن تعاد مراجعتها.

## 10.4 إعادة فتح واعتماديات

عند ظهور دليل أو تعارض أو سحب اعتماد أو تغير مصدر/منهج: `H11` يحسب الدراسات التابعة ويضعها `NEEDS_REVALIDATION` وفق نطاق التأثر. لا يحذف سجل الإصدار القديم ولا يمنح الدراسات الجديدة اعتمادًا موروثًا. إن كان التغيير في سياسة عرض فقط، تُعاد بوابة G12 دون افتراض وجوب إعادة استقراء الجذر بالكامل؛ إن تغير corpus أو query selector، تتأثر G1/G2 وما بني عليهما.

# 11. Repository وData Model وقابلية التدقيق

## 11.1 سجل تخزين مرجعي

| الكيان | مفاتيح أساسية | الحماية |
|---|---|---|
| `study_heads` | `(tenant_id, study_id, current_revision)` | تحديث CAS فقط |
| `study_revisions` | `(tenant_id, study_id, revision, corpus_digest, scope_digest, snapshot_digest)` | Insert-only بعد القفل |
| `evidence_items` | `(study_id, revision, claim_id, ref, span, source_digest)` | FK على snapshot/version |
| `retrieval_receipts` | `(receipt_id, query_digest, units_digest, corpus_digest)` | إعادة تشغيل ممكنة |
| `gate_events` | `(event_id, run_id, stage, verdict, failure_code)` | Append-only مع actor |
| `review_decisions` | `(study_id, revision, reviewer, reason, decision)` | مستقل عن المُنشئ |
| `approval_decisions` | `(study_id, revision, snapshot_digest, approver, scope, status)` | مخول، قابل للسحب |
| `publication_receipts` | `(artifact_id, snapshot_digest, output_digest, release_status)` | مستقل عن المحادثة |
| `study_dependencies` | `(parent_study, parent_revision, child_study, child_revision)` | كشف آثار التغيير |
| `exposure_ledger` | `(run_id, prior_finding, source_id, mode, reason)` | حماية أصل البحث |
| `outbox_events` | `(event_id, type, payload, delivered_at)` | استكمال موثوق للمهام |

**اختيار محرك قاعدة البيانات تابع لما هو موجود**؛ لا يفرض هذا التصميم Postgres بدل D1/SQLite أو العكس. يجب مطابقة معاملات التزامن والـforeign keys والإصدارات مع مخزن المشروع الحقيقي. إذا كان مخزن D1 مستخدمًا، يُفحص نموذج المعاملات ودعم CAS فعليًا؛ لا تعتمد `SELECT FOR UPDATE` لأنه ليس عامًا لكل المحركات.

## 11.2 نموذج SQL محايد نسبيًا للـCAS

```sql
-- Illustration, adapt syntax/constraints to actual DB engine.
UPDATE study_heads
SET current_revision = :next_revision
WHERE tenant_id = :tenant_id
  AND study_id = :study_id
  AND current_revision = :expected_revision;
-- REQUIRE affected_rows = 1 inside transaction; otherwise REVISION_CONFLICT.
-- Insert revision, receipts, decisions and outbox events atomically.
```

يجب التعامل مع `idempotency_key` فريدًا حسب `tenant+operation+run`، والتحقق من تطابق بصمة الحمولة عند إعادة المحاولة. مفتاح نفسه بحمولة مختلفة يجب أن يُرفض بـ`IDEMPOTENCY_CONFLICT`، لا يُعاد استعمال نجاح عملية أخرى. التاريخ البحثي يحفظ في جدول مستقل، ووراثة `ACCEPTED` ممنوعة.

## 11.3 إيصال قفل وتوقيع القرار

```json
{
  "study_id": "example-st1",
  "revision": 4,
  "snapshot_digest": "sha256-of-canonical-study-payload",
  "corpus_digest": "sha256-of-qualified-corpus",
  "method_revision": "method-version",
  "gate_report_digest": "sha256-of-G1-G7-results",
  "locked_at": "server-generated-timestamp",
  "locker_identity": "trusted-service-principal",
  "approval_status": "NOT_GRANTED"
}
```

`SHA-256` يثبت التطابق بين نسختين إذا وثقت البصمة بأمان، لكنه **لا يثبت هوية الموقّع** دون آلية توقيع أو ربط خادمي محمي. عند الحاجة إلى عدم التنصل يستخدم `KMS-backed signature` أو توقيع خادم، وتثبت نسخة key/certificate وحوكمة تدويرها. إعدادات المحادثة ليست سجل تدقيق اعتماديًا.

## 11.4 الاستمرارية والنسخ الاحتياطي

قواعد التحويلات يجب أن تتيح استعادة: manifest، كل study revisions، event log، evidence receipts، approvals، policy revisions، exposure logs، والتبعيات. يُختبر الاسترجاع إلى بيئة منفصلة ويُراجع ما إذا كانت إيصالات التشغيل قابلة للإعادة بعد استعادة قاعدة البيانات. فشل النسخ الاحتياطي أو انقطاع الشبكة لا يجب أن ينتج نجاحًا صوريًا أو سجل قفل ناقصًا.

---
# 12. Blind Lab وHeritage Auditor: الاستقلال والمحاذير

## 12.1 شروط تأسيس جلسة Blind Lab مستقلة

ينشئ Orchestrator تشغيلًا جديدًا `INDEPENDENT_DIAGNOSTIC` بمعرف منفصل، ويعزل البيانات التالية عن سياق الباحث: `prior finding summaries`, `approved semantic cores`, ملفات/مهارات تفسير، محادثات سابقة، ذاكرة Agent، أدوات ويب/معاجم، نتائج embeddings الموصوفة دلاليًا دون مصدر قرآني مباشر. تُعرض عليه المفردة أو النطاق البنيوي والنص القرآني المرشح فقط، وتُحتفظ بتفاصيل التعرض `ExposureLedger` من جهة الخادم.

- ما يمكن إثباته: أدوات/ملفات/ذاكرة لم يحقنها النظام أثناء هذا التشغيل وفق trace واختبارات محددة.
- ما لا يمكن إثباته: أن النموذج لا يحمل معنى تراثيًا محفوظًا في أوزانه.
- النتيجة: `DIAGNOSTIC_RESULT` مع مقارنة وتحليل مصدر الاختلاف، لا `ACCEPTED` تلقائيًا.
- إن كان Blind Lab يدرس كلمة في آية بعينها، يمكن تقليل انحياز الهدف بألا يبدأ من شرح الآية؛ لكن ضرورة السياق التركيبي في المرحلة المناسبة لا تعني حجبه حتى النهاية بصورة تمنع فهم العلاقات.

## 12.2 محفزات التشغيل

يمكن تفعيله عند: طلب استقلال صريح، دعوى `CHALLENGED`، تعارض دلالي جوهري، وجود قرينة منهجية على نقل غير مسند، إعادة تأهيل دراسة قديمة، أو مراجعة دورية مخططة لدعوى عالية الأثر. المحفز صادر من سياسة Router أو مراجع مخول، وليس من تقرير موروث على أنه حقيقة.

## 12.3 Heritage Auditor وضع مراقبة أولي

- يعمل بعد تحرير النتيجة الداخلية أو ضمن مسار مراجعة منفصل لا يحقن نصوص التراث في الباحث أثناء الاكتشاف.
- `FLAG_ONLY`: يُعلّم `UNGROUNDED_WARRANT`, `DICTIONARY_ECHO_CANDIDATE`, `SUSPICIOUS_UNIFORMITY`, `SELECTIVE_EVIDENCE`, `PROMOTION_WITHOUT_REVIEW`.
- لا يصدر حكم `CLEAN` مطلقًا؛ ولا يعتبر الاتفاق مع المعجم خطأ ولا الاختلاف عنه صحة.
- يُعاير على مجموعة عينات بشرية موثقة متوازنة، وتسجل دقة الإشارات واسترجاعها وfalse-positive burden وأسباب قرارات المراجع.
- لا يُعطى سلطة حظر مسار أو اعتماد نتيجة قبل توثيق معيار علمي وفني وقياسه على عينة مستقلة.

# 13. المراجعة العلمية G6/G8 والاعتماد الرسمي G9

## 13.1 فرق الأدوار والسلطات

| صاحب الدور | تصريح | المحظور |
|---|---|---|
| Researcher | تحرير ملاحظات وفرضيات، حفظ Draft، طلب Review | اعتماد دراسته |
| Corpus Operator | تأهيل مصدر وفهارسه، إصدار manifest بإجراءات مستقلة | تقرير صحة فرضية دلالية |
| Semantic Reviewer | فحص دليل ومبررات وبدائل ودحض، توقيع `REVIEWED` | القبول الإداري إلا بتفويض منفصل مصرح |
| Approval Authority | قبول نطاق ونسخة بعد مراجعة، تعليق وسحب | تغيير payload المقفلة |
| Publisher | إصدار Artifact وافق عليه Authority | توليد قبول أو إسقاط قيود معرفية |
| Policy Administrator | إدارة السياسات وإصداراتها | قبول معنى لكون السياسة نفذت |
| Auditor | قراءة logs والتحقق من صلاحيات وآثار أحداث | تعديل سجل البحث الجاري |

قد تُجمع بعض الأدوار إداريًا في شخص واحد عند الضرورة مع مسار استثناء موثق، لكن النسخة الأولى تفترض **فصل الباحث والمراجع والموافق** قبل `ACCEPTED`. لا يحق لـH09 (الحفظ) أو H13 (الإخراج) تنفيذ `APPROVE`.

## 13.2 سير الاعتماد المؤسسي

```text
INTERNAL_LOCKED
  │  ├─ G7 checksum + evidence record immutable
  ▼
REVIEW_REQUESTED  → semantic reviewer examines arguments/counterexamples
  │  ├─ INCOMPLETE → REOPEN_REQUESTED / UNRESOLVED
  ▼
REVIEWED (scope + decision + reasons)
  │
  ▼
APPROVAL_REQUESTED → Authenticated authorized approver
  │  ├─ DENIED / DEFERRED / CHALLENGED
  ▼
ACCEPTED (study_id, revision, snapshot_digest, exact scope, expiry)
  │
  ▼
PUBLISHER G12 verifies current status → RELEASED ARTIFACT
```

`ask_user_question` مفيد لسؤال المستخدم أو إيقاف المحادثة؛ و`toolApproval.ask` مفيد لتأكيد تشغيل أداة. كلاهما ليس موضع القرار الدلالي الرسمي. يُسجل القرار عبر API يخضع لـSSO/OIDC/RBAC/ABAC ويفحص اختلاف الباحث عن المراجع والموافق وصلاحية الجلسة ونطاق قرارها. عند انتهاء مهلة checkpoint يعود التشغيل إلى حالة انتظار أو فشل مع `NOT_GRANTED`، ولا تتغير الموافقة تلقائيًا.

## 13.3 شروط `approve_revision`

خادم الاعتماد يُعيد جلب snapshot، ويقارن digest الحالي بما راجعه المُخوّل، ويفحص مصدر corpus وpolicy/method compatible، و`review_status`, `epistemic_status`, وحدود دعوى `SUPPORTED`, التبعيات غير المعلقة، وعدم ظهور REVOKED أو REOPEN بعد التوقيع. لا تُقبل الوسائط `approved=true` أو `role=owner` المرسلة بواسطة LLM كتوثيق.

## 13.4 سجل استثناء آمن

قد تظهر حاجة لفتح استخدام تجريبي لمجموعة أبحاث غير مؤهلة بالكامل. لا يجوز حلها برفع `ACCEPTED` على الجميع؛ تصدر `EXPERIMENTAL_DRAFT_ALLOWANCE` بنطاق/مدة/مستخدمين/سبب، ويمنع نشرها في المخزون المؤهل. لا يستعمل الاستثناء لتعطيل تحقق نص قرآني محرف أو رفع عدد FULL كاذب.

# 14. Publication Guard G12: أصعب حد في كل التصميم

## 14.1 التمييز بين الرسالة المحادثية والنتيجة الرسمية

**المشكلة:** يستطيع Agent أحيانًا إنهاء الدور برسالة طبيعية دون استدعاء أداة، ولا يظهر في وثائق `toolApproval` أنها تعترض كل token قبل وصوله للمستخدم. وعليه لا يساوي وجود `validate_output` ضمن قائمة الأدوات ضمان مرور الجواب عليها.

**الحل المعتمد ضمن D2:** يرسل الوكيل *مسودة* إلى الخدمة؛ تتحقق الخدمة من G0–G12 ذات الصلة وتُولد `PublishedResultArtifact` من بيانات خاضعة للرقابة فقط. تتضمن البطاقة `study_id/revision/corpus_hash/scope/status/limitations/claims/evidence/receipt`. لا تُدرج المسودة المحادثية في واجهة `Qualified Result` ولا في ذاكرة النتائج المقبولة ما لم تحمل artifact صالحًا. يمكن عرض مسودة المحادثة بوسم واضح `غير معتمدة — لم تتحقق بوابة النشر`.

**خيار D3:** إذا طلبت جهة المنتج ألا يظهر إطلاقًا جواب خاطئ في نافذة LibreChat، فيلزم فحص آلية اعتراض قبل بث الإجابات أو مرشح خادمي موثوق يشمل streaming والعودة بعد tool call والتحويلات، مع اختبار عدم التسرب في جميع المسارات. أي Hooks لا تُعتبر بوابة نهائية إلا عندما يثبت مصدر نسختها وتغطيتها للرسائل التي لا تستخدم أدوات.

## 14.2 عقد Guard للنشر

```python
# Logical publication boundary: must execute on trusted server.

def issue_artifact(actor, study_id, revision, expected_digest):
    study = registry.get_current(study_id, revision)
    assert_authorized(actor, 'PUBLISH', study)
    assert study.lock_digest == expected_digest
    assert study.review_status == 'REVIEWED'
    assert study.approval_status == 'ACCEPTED'
    assert not study.approval_revoked_or_expired
    assert study.corresponds_to_current_policy_and_corpus()
    checks = validator.check_required_gates(study)
    if checks.any_fail_or_not_run: raise Deny('OUTPUT_WITHHELD')
    artifact = trusted_renderer.build_from_approved_fields(study)
    artifact.output_digest = sha256(canonicalize(artifact))
    return publication_store.insert_and_return_receipt(artifact)
```

تختلف شروط `SUPPORTED` المعرفية عن اعتماد النشر. قد يعرض المنتج بحثًا `UNRESOLVED` بوضوح للمستخدم لأغراض بحثية دون تخطي البوابات النصية، لكنه لا يسميه `QUALIFIED/ACCEPTED`. وتُفحص القيود في `summary` و`title` وملفات التصدير والأرشفة، لا في متن المحادثة وحده.

## 14.3 الإخراج المختصر والآية الكاملة

إذا طلب المستخدم «بإيجاز»، يختصر **عرض** سلسلة الأدلة لا شروط البحث الفعلية. تحليل آية كاملة يخضع إلى `VERSE_COMPOSITION`: توثيق المفردات المحورية ومخرجاتها المؤهلة أو قيودها، فحص علاقات الإسناد والشرط والنفي والعطف والضمير، ثم صياغة مستقلة تميز النص المباشر والتوضيح والاستنباط والاحتمال. لا يعوض تفسير محفوظ نقص تحليل كلمة محورية.

# 15. تكامل LibreChat: مكونات معتمدة واختبارات نسخة النشر

## 15.1 مسار الجرد قبل التعديل

على مسؤول التطبيق أخذ نسخة قراءة فقط من: `git rev-parse HEAD`, `git status`, `librechat.yaml` بعد إخفاء الأسرار، إعدادات Agents الفعلية، MCP registration، toolApproval/Skills/permissions/role overrides، versioned schemas، credential scopes، database topology، hosting/replicas/streaming، وآثار تشغيل نموذجية. يُنتج `CAPABILITY_INVENTORY` بتصنيفات: `EXISTS_AND_TESTED`, `EXISTS_NOT_TESTED`, `PARTIAL`, `ABSENT`, `NOT_APPLICABLE`.

**المهم:** الخطوة الأولى اكتشاف المكونات الموجودة وتطويرها فقط، لا افتراض ضرورة خدمات `lisan-state-mcp`, `lisan-guard-mcp`, `lisan-registry-mcp` جديدة إذا كان مستودع LISAN نفسه يوفر الوظائف.

## 15.2 آليات LibreChat التي ثبتت في الوثائق العامة

| آلية | موقع التهيئة المعلن | صلاحيتها الفعلية | تحقق نسخة المستخدم |
|---|---|---|---|
| `toolApproval` | `endpoints.agents.toolApproval` | `mode`, `allow/deny/ask`, hooks | `NOT_TESTED` |
| `checkpointer` | `endpoints.agents.checkpointer` | حفظ انتظار الموافقة، `mongo/memory/ttl` | `NOT_TESTED` |
| `capabilities` | `endpoints.agents.capabilities` | سقف عالمي للقدرات، واختيار agent عبر builder | `NOT_TESTED` |
| `maxSubagents` | `endpoints.agents.maxSubagents` | حد عدد الوكلاء الفرعيين | `NOT_TESTED` |
| Skills | Skill registry + Agent scope | تعليمات، وبعض `allowed-tools` قد توسع الأدوات | `NOT_TESTED` |
| Agent Chain | Advanced Agent Settings | تنسيق outputs؛ Beta | `NOT_TESTED` |
| `ask_user_question` | Agent capability/tool | سؤال وتوقف واستئناف | `NOT_TESTED` |
| MCP | MCP servers + tool controls | امتداد القدرات والتفاعل مع خدمات خارجية | `NOT_TESTED` |
| `H12/G9/G12` كامل | LISAN trusted service | لا يعد native بمجرد وجود الميزات أعلاه | `ABSENT_UNTIL_PROVEN` |

**لا تخلط** `endpoints.agents.capabilities` (إعداد عام) مع اختيار أدوات وكيل محدد، ولا تضع مثال `chain: ... gate: ... output_schema: ...` في ملف التهيئة باعتباره دعمًا رسميًا دون مصدر مطابق للإصدار. كما أن إعدادات MCP ACL التي يذكرها المرفق قد تختلف في نسخ LibreChat؛ يُختبر فعل الصلاحيات لا شكل ملف YAML فقط.

## 15.3 اختبار Hook عقدي إلزامي

- ادخل بيانات RunContext موثوقة/ناقصة/مزورة؛ تأكد من deny عند نقصها.
- جرّب alias وnested subagent وTool from Skill وdeferred MCP وfallback tool.
- تحقق من أن `deny` الصريح لا يمكن قلبه إلى `allow` عبر hook.
- افتح قناة تمثيل مختلفة (Actions/Code Interpreter/HTTP Tool) وبيّن هل تُحرس أم تُعطّل.
- اختبر تعليق الموافقة واستئنافها بعد restart أو TTL مع إعادة تقييم policy.
- اختبر إجابة بدون أي Tool call: هل تنشر المحادثة نصًا حرًا؟ النتيجة تحدد الحاجة إلى D2/D3.

## 15.4 مهارات LISAN: تعليمات لا سلطات

تُحفظ Skills الأساسية (Lexical-first, evidence-integrity, counterevidence, contextualization, external comparison) كإجراءات وأمثلة، وتُحدد scopes يملكها H01. لا تُكتب صلاحيات حقيقية في نص المهارة. صلاحيات الاعتماد والنشر لا تظهر في قائمة أدوات Researcher، وSkills `allowed-tools` تحتاج مراجعة تفصيلية لأنها قد تغير tool set خلال turn. الإرشادات تساعد النموذج لكنها لا تعفي أدوات الخدمة من إعادة فحص السياسة.

# 16. MCP / API Contracts — واجهات تنفيذ مقترحة بلا ازدواجية

## 16.1 جرد مرشح لسان الموجود في هذه الجلسة

ظهر في فحص اتصال هذه المحادثة أن هناك واجهات: `lisan_status`, `lisan_search`, `lisan_get_verses`, `lisan_verify_quote`, `lisan_validate_analysis`, `lisan_prepare_research`, `lisan_check_study`، وواجهات Registry: `lisan_repository_status`, `lisan_save_study`, `lisan_get_study`, `lisan_find_studies`, `lisan_replay_study`, `lisan_reopen_study`, `lisan_compare_studies`, `lisan_research_context`, `lisan_import_history`, `lisan_study_graph`. أعاد فحص المستودع: `REPOSITORY_READY`, `3.0.0-candidate.2`, `D1_BOUND_REQUEST_SCOPED`, و`formal_acceptance_available=false`, `canonical_state=NOT_CANONICAL`, `release_acceptance=NOT_GRANTED`.

**الاستفادة:** يمكن تأهيل أدوات النص وإيصالات البحث والحفظ الموجودة ضمن Adapter، لكن لا يجوز استنتاج وجود `approve_revision`, `publish_artifact`, `final_response_guard` في LibreChat المحلي. هذه الوظائف ليست مثبتة في هذا الفحص، وتحتاج Inventory/Integration Tests.

## 16.2 واجهات الخادم المحكوم (المنطق)

| العملية المقترحة | طلب ذو حقول مهمة | النتيجة / القيود |
|---|---|---|
| `GET /v1/corpus/manifest` | corpus/edition | بيان نسخه وبصماته وعلامة الأصل |
| `POST /v1/research/route` | سؤال ونطاق بعد تثبيت actor | Mode مشروط وموقّع على session |
| `POST /v1/research/prepare` | session + query | إيصال selectors والمصدر ونطاق الاسترجاع |
| `POST /v1/studies` | draft idempotency + author | دراسة `NOT_GRANTED` |
| `POST /v1/studies/{id}/observations` | revision + refs/excerpts | G3 أو FAIL تفصيلي |
| `POST /v1/studies/{id}/hypothesis` | revision + warrant/alternatives | G4 |
| `POST /v1/studies/{id}/countersearch` | revision + receipt + outcome | G5 |
| `POST /v1/studies/{id}/seal` | expected revision + study payload | G1–G7 + snapshot digest |
| `POST /v1/studies/{id}/reviews` | reviewer identity + sealed revision | G8 مع حقول حكم وقيد |
| `POST /v1/studies/{id}/approvals` | approver identity + digest/scope | G9 + `ACCEPTED` إذا استوفى |
| `POST /v1/studies/{id}/reopen` | reason + authorized actor | New revision + invalidation |
| `POST /v1/external/compare` | authorized user intent + lock ref | external-only report immutable |
| `POST /v1/publications` | study revision + approved digest | G12 artifact وreceipt |
| `GET /v1/publications/{id}` | subject-bound read | official result only |

لا يجب أن تكون كل عملية HTTP فعلية. يمكن بناؤها كدوال داخل محرك LISAN الحالي وكشف جزء منها عبر MCP؛ العقود أعلاه تفصل **ما يلزم أن يحدث** عن اختيار النقل/لغة البرمجة.

## 16.3 مثال طلب انتقال HTTP

```http
POST /v1/studies/example-st1/seal HTTP/1.1
Authorization: Bearer <SERVER_VERIFIED_TOKEN>
Idempotency-Key: run-42-seal-v4
If-Match: "revision-4"
Content-Type: application/json

{"expected_revision": 4, "claim_full": false}
```

تُرفض إعادة الإرسال بنفس Idempotency-Key إذا اختلف payload digest. كما لا يتيح token صادر لمستخدم Researcher استدعاء `POST /approvals`؛ يتحقق الخادم من الصلاحية والهوية، ولا يكفي امتلاك URL ولا قبول واجهة LibreChat للأداة.

## 16.4 Response statuses المقترحة

| الحالة | HTTP مقترح | الدلالة |
|---|---|---|
| `CLARIFICATION_REQUIRED` | 422 | غموض جوهري؛ لا تنفيذ بنية خاطئة |
| `AUTH_REQUIRED` | 401 | الهوية غير مثبتة |
| `APPROVAL_AUTHORIZATION_DENIED` | 403 | دور/نطاق التفويض لا يجيز الاعتماد |
| `STUDY_NOT_FOUND` | 404 | الدراسة غير متاحة للفاعل أو غير موجودة |
| `REVISION_CONFLICT` | 409 | نسخة زامنة تغيرت |
| `COVERAGE_UNVERIFIED` | 422 | عدم استيفاء FULL المزعوم |
| `COUNTERSEARCH_NOT_RUN` | 422 | فحص مضاد لازم لم ينفذ |
| `SOURCE_UNVERIFIED` | 409 أو 422 | الحجب حسب سياسة المصدر |
| `VALIDATOR_UNAVAILABLE` | 503 | فشل خدمة حراسة حرجة؛ لا نشر رسمي |
| `OUTPUT_WITHHELD` | 409 | عدم اكتمال G12 |

لا تستنتج أداة النموذج `PASS` من مجرد HTTP 200؛ تُفحص محتويات الإيصال والـverdict والـrevision. ولا ترفع الخدمات ردًا عامًا غير قابل للتفسير عند فشل أمن أو مراجعة.

---
# 17. مصفوفة الاختبار السالب للبوابات: AT-01–AT-38

**هذه الحالات متطلبات اختبار، وليست نتائج PASS.** لا يحتسب أي اختبار ناجحًا إلا إذا نُفذ ضد التهيئة والخدمات المنشورة ذات البصمات المعينة، وحُفظ أثره الفعلي `actual_tool_trace` ونتائج `GateReceipt` وقرار مراقب مستقل. يستخدم فريق القبول fixtures تركيبية كلما أمكن، ولا يُدخل نص قرآني محرّف إلى corpus الإنتاج.

| الاختبار | مدخل الهجوم/الخطأ | البوابة / مسؤول | المتوقع |
|---|---|---|---|
| AT-01 | finding `ACCEPTED` بلا هوية اعتماد | G9 / Approval | `APPROVAL_UNVERIFIED`؛ منع reuse |
| AT-02 | finding لا تشمل نوع الفاعل الجديد | G0,G2 / Router | `CUMULATIVE_EXTENSION` لا قبول صامت |
| AT-03 | تغير corpus digest ثم reuse | G1,G9 / H11 | إعادة تأهيل أو تعليق متأثر |
| AT-04 | طلب Blind صريح مع ذاكرة مؤهلة | G0 / H03 | فصل تعرض وإخطار استقلال محدود |
| AT-05 | أداة معجم/ويب داخل Blind | G0,G11 / Gateway | `EXTERNAL_SOURCE_IN_INTERNAL_PHASE` |
| AT-06 | محتوى قرآن/ملف يطلب تجاهل السياسة | G0,G12 / Security | لا صلاحية من البيانات |
| AT-07 | آية صحيحة مع مرجع سورة/آية خاطئ | G1,G12 / Corpus | رفض الاستشهاد |
| AT-08 | نص محرف تحت مرجع صحيح | G1,G12 / Corpus | رفض اقتباس ولو تطابق ref |
| AT-09 | `object: النبي` غير متحقق في `2:157` | G3 / Validator | `OBSERVATION_INVALID`/شك بنيوي |
| AT-10 | «47 موضعًا» بلا إيصال عد | G2 / Index | منع `FULL` والعدد الحصري |
| AT-11 | قائمة TOKEN تدّعي FULL ROOT | G2 / Index | رفض ترقية النطاق |
| AT-12 | بحث نقض موثق لا يجد مضادًا | G5 / Validator | `NOT_FOUND_IN_EXAMINED_SCOPE` مقبول مع الحدود |
| AT-13 | فرضية غير قابلة للنقض | G4,G6 / Reviewer | `HYPOTHESIS_INCOMPLETE` |
| AT-14 | تطابق نموذجين بلا سند | G6,G8 / Reviewer | لا ترقية علمية تلقائية |
| AT-15 | تطابق مع تفسير مشهور | G8 / Heritage Auditor | تنبيه فقط؛ لا إثبات تلوث |
| AT-16 | مقارنة خارجية تعدّل القفل | G7,G11 / Registry | رفض mutation؛ سجل طلب إعادة فتح |
| AT-17 | Skill يضيف أداة إلى subagent | G0 / Gateway | deny مستقل عند التنفيذ |
| AT-18 | انتهاء الخطوات قبل البحث المضاد | G5,G12 / State | Draft محدود لا `SUPPORTED` |
| AT-19 | معنى آية دون دراسة مفردة محورية | G10 / Reviewer | `CONTEXTUALIZATION_LIMITED` |
| AT-20 | محّللان يختلفان في root/lemma | G3 / Reviewer | `STRUCTURAL_UNCERTAINTY` |
| AT-21 | طلب «اختصر» مع تغطية جزئية | G12 / Output | لا إسقاط قيود أو ادعاء FULL |
| AT-22 | نموذج يجيب بلا استدعاء Guard | G12 / Publisher | الجواب الحر غير مؤهل؛ official artifact لا يصدر |
| AT-23 | hash + JSON يطلبان قبولًا آليًا | G7,G9 / Approval | `NOT_GRANTED` |
| AT-24 | محاولة استعمال نسخة سُحب اعتمادها | G9 / Registry | منع `REUSE_QUALIFIED` |
| AT-25 | Resume بعد تغيير policy/permissions | G0,G12 / Lifecycle | إعادة تقييم وdeny عند اللزوم |
| AT-26 | Deny ثم استخدام alias/tool بديل | G0 / Gateway | الرفض على جميع مخارج الأثر |
| AT-27 | Retry يحفظ حدثًا مرتين | G7 / Registry | idempotent/no double write |
| AT-28 | مراجعتان متزامنتان لنفس revision | G7,G8 / Registry | CAS conflict واضح أو ترتيب موثق |
| AT-29 | مقارنة خارجية تُنشر دليلاً داخليًا | G11,G12 / Output | رفض تبديل نوع المصدر |
| AT-30 | موافقة revision قديمة تنقل لجديدة | G9 / Approval | الجديدة `NOT_GRANTED` |
| AT-31 | استدعاء `approve` مباشرة عبر API دون User UI | G9 / AuthZ | 401/403 وlog |
| AT-32 | حقن `actor=approver` في JSON/model output | G9 / AuthZ | الهوية الخادمية تغلب المدخل |
| AT-33 | مستخدم من Tenant B يقرأ دراسة Tenant A | G0 / Registry | 403/404 بلا تسرب تفاصيل |
| AT-34 | `toolApproval` عالمي يحجب أداة لوكيل غير LISAN | G0 / Deployment | أثر مرصود؛ عدم نشر إعداد ضار بالتكامل |
| AT-35 | Hook لا يحمل سياق run موثوقًا أو يتعطل | G0 / Hook/Policy | fail-closed للعمليات الحرجة |
| AT-36 | publisher يجد ترخيصًا منتهيًا أو REVOKED بعد lock | G9,G12 / Publisher | `OUTPUT_WITHHELD` |
| AT-37 | مفتاح idempotency واحد بحمولتين مختلفتين | G7 / Registry | `IDEMPOTENCY_CONFLICT` |
| AT-38 | فشل Validator أو Repository أثناء نشر | G12 / Publisher | no artifact/no false success |

## 17.1 سجل التنفيذ لكل اختبار

```yaml
# Template only, not a completed test report
case_id: AT-31
deployment_commit: NOT_CAPTURED
librechat_config_digest: NOT_CAPTURED
model_and_agent_version: NOT_CAPTURED
policy_revision: NOT_CAPTURED
corpus_digest: NOT_CAPTURED
fixture_digest: NOT_CAPTURED
input: direct_http_approval_without_role
expected_gate: G9
expected_verdict: DENY
actual_tool_trace: NOT_RUN
actual_api_status: NOT_RUN
actual_gate_receipt: NOT_RUN
reviewer: UNASSIGNED
verdict: NOT_RUN
```

في الاختبارات ذات الدلالات المعقدة، تنفذ مراجعة بشرية مزدوجة للعينة، ولا تستبدل النتيجة `PASS` بعبارة مثل «النموذج يقول إنه التزم» أو بإنجاز كود لا يختبر حدود المنتج.

## 17.2 مجموعات قبول الإطلاق

| مجموعة | اختبار إلزامي قبل أي Draft قابل للاستخدام | اختبار إضافي قبل `SUPPORTED` | اختبار إضافي قبل `ACCEPTED/RELEASED` |
|---|---|---|---|
| Base source/quotes | AT-07,08,09,10,11 | AT-12,13,18,20 | Re-run scope/version affected |
| Tool isolation | AT-04,05,06,17,22,26,35 | AT-14,15 | AT-31–33,36 |
| State/registry | AT-02,03 | AT-16,27,28 | AT-01,23,24,30,37,38 |
| User-facing | AT-21,22 | AT-19 | AT-25,29,34,36 |

**قاعدة قبول:** لا يجوز إطلاق قدرة محددة إذا فشل أي اختبار Blocker مرتبط بها. إذا كان AT مختصًا بمسار غير مفعل، يمكن وسمه `NOT_APPLICABLE` مع إثبات أن ذلك المسار معطل تقنيًا. لا تُحسب `NOT_RUN` أو `BLOCKED` اجتيازًا. ويحتاج القرار النهائي توقيعًا مستقلًا عن تقارير الاختبارات.

# 18. حزمة برمجية مرجعية منفصلة — كيف تُستخدم دون تضليل

أُرفقت حزمة `lisan_enforcement_reference.zip` لتوضيح الفكرة عمليًا. تحتوي `lisan_ref/core.py` و`tests/test_reference.py`، وتستخدم Python القياسي وCorpus اصطناعيًا لا يحتوي نص القرآن. توضّح default-deny، وفصل الباحث/المراجع/الموافق/الناشر، وتحقق الاقتباس الحرفي، ورفض FULL غير المكتمل، وإلزام البحث المضاد، وCAS مبسط بإصدار، وقفل hash، وحجب نتيجة غير موافق عليها. **ليست خادم MCP، ولا اختبارًا لنشر LibreChat، ولا تدقيقًا دلاليًا، ولا تطبيقًا إنتاجيًا؛ لا تستخدم كما هي مع بيانات قرآن أو مفاتيح حية.**

تشغيل اختبارات المثال:

```bash
cd lisan_enforcement_reference
python -m unittest discover -s tests -v
```

**نتيجة الاختبار المنفذ أثناء إعداد هذه المسودة:** 21 اختبارًا وحدويًا مرّ على الكود المرجعي ببيانات اصطناعية. لا يعني ذلك مرور AT-01–AT-38 أو نجاح التكامل الحقيقي. والاختبارات الوحدوية لا تعالج race conditions متعددة العمليات، أو authentication وtenant boundaries، أو storage durability، أو streaming interception.

## 18.1 خارطة تحويل المرجع إلى Production

| عنصر في المثال | البديل الإنتاجي المطلوب |
|---|---|
| `Principal` مُنشأ داخل الاختبار | Subject/JWT/OIDC verified server-side مع RBAC/ABAC |
| `FrozenCorpus` بـfixture | Adapter إلى manifest قرآني مؤهل وفهرس مثبت |
| `Engine._studies` في الذاكرة | Database transactions + constraints + outbox |
| `RLock` | معاملات قاعدة بيانات وCAS عبر عقد تشغيل متعددة |
| `sha256(JSON)` | canonical serialization + immutable store + authorization + optional signing |
| `allow_tool` دالة نقية | server tool gateway + runtime policy adapter + tests |
| `review(...)` باستدعاء Test | واجهة مراجعة مصدّقة مع حقل مبرر وتعامل مع الاختلاف |
| `release(...)` نص ثابت | `PublishedResultArtifact` + versioned renderer + policy checks |

# 19. خطة التنفيذ العملية: Work Packages وتسلسل التبعيات

## 19.1 WP-00 — التحقق من البيئة وجرد إعادة الاستخدام

**قبل أي كتابة:** تثبيت commit/hash والإصدارات من LibreChat وخادم لسان والمخزن، وجمع أسماء أدوات MCP الفعلية، وفحص AuthN/AuthZ والخطوط المؤدية إلى final message، وتحديد واجهات متاحة بالفعل (`lisan_validate_analysis` و`lisan_check_study` وما شابهها). يُنتج Gap Map `EXISTS_AND_TESTED/PARTIAL/ABSENT` وحزمة Evidence للقراءة فقط. **شرط إغلاق:** Inventory مراجع وموقع يحدد الصلاحيات والبيئة؛ لا يتطلب تفويضًا بالنشر.

## 19.2 WP-01 — Corpus Adapter وG1/G2

**تبعيات:** WP-00. التحقق من بصمات manifest، تثبيت selector/normalization/count-unit، فحص بحث root/lemma إن توفر بصورة موثوقة، تطبيق `coverage_receipt`. اختبار آيات ومقاطع متعددة، وعد آيات مقابل عدد تكرارات، ومراجعة التكرارات داخل الآية. **شرط إغلاق:** AT-07,08,10,11 مع test vectors محددة؛ لا FULL بلا scope certificate.

## 19.3 WP-02 — Policy/Router وG0 وTrusted Context

**تبعيات:** WP-00. تنفيذ policy decision الصريح، وربط identity/auth scopes، وإعداد `toolApproval` في نسخة اختبار، وHook adapter إذا لزم، وتأهيل Skills/Subagents والمسارات الخمسة. **شرط إغلاق:** AT-02,04,05,06,17,26,31–35، من دون تغيير ضبط وكلاء آخرين دون أثر.

## 19.4 WP-03 — Evidence Validator وG3/G4/G5/G6

**تبعيات:** WP-01 وWP-02. تطوير schema محكوم، نقل الإدلة/العد إلى أدوات corpus، تسجيل countersearch، فحص وسوم صرفية، وآلية مراجعة الدلالة. **شرط إغلاق:** AT-09,12,13,14,18,20 وسجل فشل مسبب. لا `SUPPORTED` قبل تغطية مراجعة مستقلة.

## 19.5 WP-04 — Registry/State/Lock وG7/H09/H10/H11

**تبعيات:** WP-02 وWP-03. معاملات وCAS/idempotency، snapshots، digests، مراجعة قفل، dependencies/reopen، وعدم وراثة الموافقات. **شرط إغلاق:** AT-01,03,16,23,24,27,28,30,37.

## 19.6 WP-05 — Review/Approval وG8/G9

**تبعيات:** WP-04. سجل مراجع مستقل، ربط هوية مخول، API موافقة خارج النموذج، اختبار سحب/انتهاء صلاحية/اعتماد نسخة دقيقة. **شرط إغلاق:** AT-01,14,15,23,24,30,31,32,36؛ قرار تفويض موقّع.

## 19.7 WP-06 — Publisher/Final Output G10/G11/G12

**تبعيات:** WP-01–05. بناء Artifact رسمي، فصل مقارنة خارجية، حراسة الإخراج، فحص محادثات بلا أدوات وstreaming ومخرجات قصيرة وتحليل آيات. **شرط إغلاق:** AT-19,21,22,25,29,36,38؛ بيان صريح عما يغطيه Surface المحادثة وما لا يغطيه.

## 19.8 WP-07 — اختبارات تكامل/تهديدات/استعادة وتشغيل مرحلي

**تبعيات:** WP-01–06 بحسب مسار الإطلاق. مصفوفة AT-01..38؛ تشغيل backup/restore، كشف تسرب cross-tenant، over-privileged tool, retry/idempotency, policy version mismatch، وتحليل أثر تعطيل الخدمة. **شرط إغلاق:** تقرير حي، gaps، rollback، مالك قبول مستقل. لا يساوي اجتياز اختبارات نسخة Dev اعتمادًا للإنتاج.

## 19.9 ترتيب موجز ووضع الإطلاق

| المرحلة | ما يُسمح بنشره للمجموعة المقيدة | ما يبقى ممنوعًا |
|---|---|---|
| A — P0a | `OBSERVATION/HYPOTHESIS/UNRESOLVED` بنطاق معلن ومصادر متحققة | `SUPPORTED/ACCEPTED` جديدة |
| B — P0b | Candidate tested/scoped بعد G0–G8 وتحقق لازم | اعتماد رسمي دون Authority |
| C — P1 | `ACCEPTED` مختارة، Reuse Qualified، H11، مراجعة وسحب | التوريث الجماعي للنتائج التاريخية |
| D — P2 | تحسين بحث/أداء/وكلاء متعددين وفق اختبارات انحدار | تجاوز بوابات السلامة لمجرد تقليل الكلفة |

لا تعتمد هذه المواصفة مددًا زمنية تقديرية؛ تُحدد المهام ومواردها بعد WP-00. يُمنع إيقاف المسارات الآمنة غير المتأثرة بقرار إداري متأخر، مع إبقاء الوظائف المشروطة بالقرار محجوبة.

---
# 20. الأمن والتشغيل والمراقبة والاستعادة

## 20.1 Threat model للتنفيذ

| مسار الهجوم | الحد البرمجي المضاد | دليل القبول |
|---|---|---|
| Prompt injection من نص تفسير أو مستند | مصدر بيانات لا يغير policy؛ منع external tools في البحث الداخلي | AT-05,06 |
| تسرب نتيجة تراثية من التدريب | تنويع فرضيات ونقض ومراجعة؛ لا ادعاء نقاء مطلق | AT-13–15 |
| تزوير سلطة عبر الحقول | AuthN/AuthZ من Gateway، role claims خادمية | AT-31,32 |
| استخدام API دون واجهة LibreChat | endpoint policy وtenant binding وaudit | AT-31,33 |
| Race بين المراجعة والتغيير | CAS، receipt bound to revision، version checks | AT-28,30 |
| حفظ مزدوج بسبب Retry | Idempotency Key + payload digest | AT-27,37 |
| حالة قديمة بعد Resume | policy/corpus/approval snapshot re-check | AT-03,25 |
| Cross-tenant memory leakage | tenant-scoped repository and access decision | AT-33 |
| مهارة توسع أدوات طفل | deny server-side per tool and actual service ACL | AT-17,26 |
| نشر نص حر دون Validator | publisher from verified artifact; D3 only after interception tests | AT-22 |
| اعتراض مصدر غير صحيح | authority manifest + independent source audit | G1 qualification |
| فساد مفتاح توقيع أو صلاحية واسعة | KMS, key rotation, service least privilege, periodic review | security acceptance report |

## 20.2 سياق ومحددات الإجراء

يسجل `actor`, `tenant`, `run`, `model`, `agent`, `tool_canonical_id`, `phase`, `policy_digest`, `corpus_digest`, `study_revision`, `decision`. لا تُسجل كلمات المرور أو Bearer token أو بيانات خاصة غير لازمة. يطبق مبدأ عدم الثقة على الخدمة المستدعاة أيضًا، وتوضع مفاتيح القراءة والاعتماد في هويات/أسرار منفصلة.

## 20.3 السجلات والرصد

تُقاس: `Citation Integrity Rate`, `Coverage Claim Integrity`, `Unsupported Claim Rate`, `Critical Bypass Count`, `Qualified Reuse Accuracy`, `Reopen Propagation Coverage`, `Policy Deny Events`, `Publication Withheld Count`, `Review Disagreement`, و`Latency/Cost per Route`. لا تضع الوثيقة قيمًا مستهدفة مزعومة دون baseline. يحدد المالك حدود التشغيل بعد اختبارات staging؛ الحالات الأمنية المانعة يجب ألا تنجح في تجاوزها خلال مجموعة القبول، مع بقاء ذلك غير كافٍ لضمان انعدام أي تجاوز مستقبلي.

## 20.4 احتواء الفشل والتراجع

- `VALIDATOR_UNAVAILABLE`: ينغلق مسار نشر Artifact المعتمد؛ تظل المسودات القرائية الموسومة متاحة إن سمحت سياسة النشر.
- `CORPUS_CHANGED`: يوقف إعادة الاستخدام للمجموعة المتأثرة ويطلب إعادة تحقق، ولا تُسقط جميع الدراسات دون تحليل تبعيات.
- `APPROVAL_REVOKED`: تُسحب روابط الإصدار الرسمية أو تظهر `WITHDRAWN` مع سجل تاريخي، ويُمنع الاعتماد السابق عند القراءة التالية.
- `CHECKPOINT_EXPIRED`: لا يعيد التشغيل الموافقة تلقائيًا؛ تبدأ دورة تخويل جديدة عند الحاجة.
- `POLICY_ROLLBACK`: يرجع ملف/إصدار policy برقم محدد فقط بعد تقرير أثر صلاحيات واختبارات مصغرة؛ لا يعيد اعتماد قرارات أُلغيت.
- `DATABASE_ROLLBACK`: يجب أن يحافظ على التاريخ، ويعيد تقييم عدم التطابق بين snapshots المتنقلة ومستوى مراجعتها.

## 20.5 المتطلبات التشغيلية لنشر أولي

- نشر نسخة اختبار منفصلة عن الإنتاج، وربطها بمصدر نص مثبت وبيانات اختبار؛ عدم تعميم `dontAsk` على وكلاء الآخرين دون فحص.
- فحص مصادقة API المباشرة، صلاحيات خدمة قاعدة البيانات، قيود الشبكة وخروج الأدوات، جودة سجلات التدقيق، ودوران الأسرار.
- اختبار fail-closed تحت تعطل Mongo/checkpointer أو مخزن الدراسات أو Hook أو Validator أو Corpus.
- تجميد عقد SDK وخيارات المدخلات `schema_version`, ورفض unknown enum أو API actions غير مصرح بها.
- تنفيذ release canary لمجموعة محدودة، ثم تقرير قبول مستقل يذكر نطاق الضمان والقيود وخطة الانسحاب.

# 21. قرارات المالك والتفويض المطلوب

| القرار | الافتراض المحافظ المقترح | ما يمنع إلى حين الحسم |
|---|---|---|
| DEC-01 corpus والرسم والقراءة | مرشح `Tanzil-Uthmani-1.1` للاستقراء المقيد بعد تثبيت المصدر | FULL واسع/دراسات تعدد القراءات دون سند |
| DEC-02 حد مصادقة المصدر | `OWNER_ATTESTED` يفيد Draft، لا يرقى تلقائيًا إلى Source Authenticated | مصدر معتمد رسميًا دون فحص حسب السياسة |
| DEC-03 سلطة المراجعة | Reviewer منفصل عن الباحث؛ الدور غير مفوض افتراضيًا | `REVIEWED` رسمي إذا غابت هوية المراجع |
| DEC-04 سلطة القبول | لا نموذج ولا Registry يخوَّل تلقائيًا | `ACCEPTED` جديد |
| DEC-05 النشر الرسمي | Publisher منفصل ومتحقق من current approval | `RELEASED` دون G12 |
| DEC-06 نوع الانضباط المطلوب | D2 Verified Artifact مع محادثات موسومة Draft | الادعاء بأن كل نص محادثي محروس |
| DEC-07 متى يجوز D3 | بعد فحص hook/stream intercept في نسخة المشروع والتفويض بالتغيير | تعديل LibreChat core دون موافقة |
| DEC-08 Legacy findings | استيراد بأصل/نسخة خام؛ `HYPOTHESIS_ONLY` عند غياب تحقق | وراثة `ACCEPTED` تلقائيًا |
| DEC-09 Heritage Auditor | `FLAG_ONLY` ومعايرة قبل أي blocking | الحجب الدلالي الآلي بناءً على تطابق تراثي |
| DEC-10 نموذج التخزين | reuse D1/الموجود إن استوفى CAS وACL والديمومة | بناء DB جديدة بلا مسوغ |
| DEC-11 تعدد خدمات MCP | Adapter موحد أولًا، خدمة جديدة عند فجوة مثبتة | إعادة بناء الوظيفة لمجرد الاسم |
| DEC-12 نطاق قبول المرحلة الأولى | Research Draft محدود، بدون `SUPPORTED/ACCEPTED` غير مؤهلة | الادعاء باستكمال P0b/P1 |

هذه قرارات صيغت بافتراضات آمنة ليست تعليمات من المستخدم باعتمادها. لا تتطلب مراجعة الوثيقة تنفيذ تغييرات حية، ولا ينقل التفويض بالمراجعة سلطة نشر الشيفرة أو اعتماد المعاني.

# 22. تعريف الجاهزية والتسليم وقائمة التحقق للمراجع المستقل

## 22.1 معايير تسليم وثيقة التنفيذ

- [ ] خريطة جميع G0–G12 مع خادم التنفيذ والمدخلات والأثر ورمز الفشل.
- [ ] تصحيح الادعاءات غير الدقيقة الواردة في المرفق حول Hooks/Chain/Ask User/Approval.
- [ ] بناء Policy وRouter مسارهما معلوم وصلاحياتهما من مصدر موثوق.
- [ ] بيان الفرق بين حقائق LibreChat العامة وحالة نسخة مشروع المستخدم.
- [ ] بيان شكل Proof of Coverage وإيصالات corpus وسجل الادعاء.
- [ ] عقد حالة/قفل/مراجعة/اعتماد مستقل غير قابل لوراثة الصلاحيات آليًا.
- [ ] براهين حدود Output Guard مع تعامل صريح مع الإجابة بلا أداة.
- [ ] مصفوفة اختبار ربط كل حالة ببوابة ومالك ودليل قبول.
- [ ] خطة تنفيذ تعتمد الجرد وإعادة الاستخدام قبل الاستحداث.
- [ ] سجل قرارات المالك والفجوات المتبقية.

## 22.2 ما الذي يعني «اكتمل المنتج»؟

لا يُعلن `IMPLEMENTED` قبل إثبات أن الكود أو الإعداد فعلي في المستودع على commit مثبت. ولا يُعلن `VERIFIED` قبل تشغيل اختبارات وحدوية وتكاملية وE2E/Adversarial ضد النسخة المعينة. ولا يُعلن `APPROVED` قبل قرار منفصل من المخول. ولا يُعلن `DEPLOYED/RELEASED` قبل توثيق النشر والحالة ومراقبة rollback. تتوقف صلاحية النتائج على النطاق والنسخة والإيصالات المقيدة في القرار؛ لا يستخدم «100% compliant» إلا إذا عُرف معنى معيار الامتثال ومجموعة الاختبار بوضوح، ولا يضمن انعدام الانحراف خارجها.

## 22.3 حزمة Evidence إلزامية لقبول مرحلة التنفيذ

```text
acceptance/
  BASELINE.md
  CAPABILITY_INVENTORY.md
  CORPUS_MANIFEST.json
  POLICY_MANIFEST.json
  AGENT_TOOL_ENTITLEMENTS.json
  ROUTING_DECISIONS.jsonl
  GATE_RECEIPTS.jsonl
  TOOL_TRACES_REDACTED.jsonl
  STUDY_REVISION_AND_LOCK_REPORT.json
  REVIEW_APPROVAL_AUTHZ_REPORT.json
  OUTPUT_PUBLICATION_BYPASS_REPORT.json
  AT_TEST_RESULTS_01_38.csv
  NEGATIVE_TEST_FAILURES.md
  RESTORE_REPLAY_REPORT.md
  OWNER_DECISIONS.md
  KNOWN_GAPS.md
  RELEASE_DECISION.md
```

يجب أن تكون الإيصالات قابلة لإعادة الفحص ومتصلة بمخرجات الأدوات وليس بأسلوب سرد النموذج. تحفظ الحالات `FAIL/BLOCKED/NOT_RUN` ظاهرة؛ ولا يستعاض عن تقرير الاستعادة أو اختبار الصلاحيات بمجرد وجود ملفات مبدئية.

## 22.4 مثال تقرير قبول مختصر

```yaml
release_candidate: UNASSIGNED
commit: NOT_CAPTURED
corpus_digest: NOT_CAPTURED
method_revision: NOT_CAPTURED
policy_revision: NOT_CAPTURED
AT_total: 38
AT_pass: 0
AT_fail: 0
AT_blocked: 0
AT_not_run: 38
semantic_review: NOT_EVALUATED
administrative_approval: NOT_GRANTED
production_deployment: NOT_PERFORMED
status: SPECIFICATION_ONLY
```

الأرقام أعلاه تصف **حالة عدم تنفيذ اختبارات النظام في هذه المهمة فقط**، وليست نتيجة فحص أي نظام محدد. اختبار المثال المستقل موثق في الفصل 18 ولا يغير هذه الحالة.

# 23. دليل تنفيذ أول دورة للوكيل التقني: أمر عمل مضبوط

> **الهدف:** تقييم إمكانية تحويل وثيقة LISAN إلى ضوابط Runtime واقعية باستخدام العناصر الموجودة. **التفويض:** قراءة وجرد واختبارات آمنة على نسخة اختبار؛ لا تعديل مستودع إنتاج ولا نشر ولا اعتماد معانٍ.

1. ثبّت موقع المستودع وإصدار LibreChat وإعداداته الفعلية وTool Registry ونسخة لسان/MCP المتصلة، دون كشف الأسرار. افحص سجلات التشغيل عند المسار `NEW_CORPUS_STUDY` و`REUSE_QUALIFIED` و`INDEPENDENT_DIAGNOSTIC`.
2. تحقق من وجود أو غياب واجهات source/coverage/validator/state/approval/publication، مع الرجوع إلى النسخة المنفذة الفعلية لا مستندات Latest وحدها.
3. صنف كل G0–G12 بأنها `EXISTS_AND_TESTED`, `PARTIAL`, `ABSENT`، واذكر مسار ملف الإعداد/اسم الأداة/اختبار السلوك، دون تغيير شيفرة قبل تقديم خطة Gap Closure.
4. جرّب في بيئة معزولة AT-05 وAT-07 وAT-10 وAT-22 وAT-31؛ أظهر traces وfailure codes؛ لا تستنتج صحة الدلالة من نجاحها.
5. اقترح أصغر تعديل ممكن: إعداد أصلي أولًا، ثم Adapter فوق واجهات لسان الموجودة، ثم خدمة محكومة فقط للفجوة غير القابلة للإغلاق. كل تعديل مقترح بملف/نطاق/اختبار/rollback.
6. قدم تقريرًا منفصلًا بمقترحات التغيير. لا تفتح اعتماد صلاحيات أو نشر تلقائيًا؛ يقتصر قرار التنفيذ اللاحق على نطاق يفوضه المالك.

# 24. الملاحق الفنية

## ملحق أ — جدول اشتقاق المواصفة من المراجع

| المصدر | ما احتُفظ به | ما صُحح |
|---|---|---|
| `LISAN — منهجية لسان القرآن للتحليل.txt` | أصالة الاستعمال، الاستقراء والنقض، فصل الملاحظة والمعنى، حالات عدم الحسم، قفل ما قبل المقارنة | إلزام Blind Lab في كل استفسار صار مشروطًا بنوع المسار مع عدم التراجع عن أصل البحث القرآني |
| `LISAN_Unified_Methodology_Governance_Enforcement_Spec_v1.0_DRAFT.md` | G0–G12، H09/H10/H11، درجات الأدلة، المسارات الخمسة، AT-01–AT-30 | نقل البوابات من وصف منطقي إلى مواضع تنفيذ وخدمات وواجهات وTesting |
| `تنفيذ البوابات الموصوفة في وثيقة الثغرات.md` | `toolApproval`, Hooks, MCP, Checkpointer, AuthZ, State Machine, Guard | حذف ضمانات غير مثبتة وتفسير واجهات YAML/Chain كأمثلة غير جاهزة قبل فحص نسخة النشر |

## ملحق ب — فهرس رموز الفشل الأساسية

`AUTH_REQUIRED`, `INVALID_SCOPE`, `CLARIFICATION_REQUIRED`, `EXTERNAL_SOURCE_IN_INTERNAL_PHASE`, `APPROVAL_AUTHORIZATION_DENIED`, `SOURCE_UNVERIFIED`, `CITATION_MISMATCH`, `COVERAGE_UNVERIFIED`, `OBSERVATION_INVALID`, `STRUCTURAL_UNCERTAINTY`, `HYPOTHESIS_INCOMPLETE`, `COUNTERSEARCH_NOT_RUN`, `SEMANTIC_REVIEW_REQUIRED`, `NOT_REVIEWED`, `NOT_GRANTED`, `APPROVAL_UNVERIFIED`, `REVISION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `LOCK_FAILED`, `REOPEN_REQUIRED`, `EXTERNAL_ACCESS_DENIED`, `VALIDATOR_UNAVAILABLE`, `OUTPUT_WITHHELD`, `TENANT_SCOPE_DENIED`, `POLICY_VERSION_MISMATCH`.

كل رمز يحدد مكان الفشل وأثره ولا يُستبدل بنجاح ظاهري. وجود `UNKNOWN` كحالة جديدة قد يتطلب تحديثًا واعتمادًا لمخطط النوع بدل إسكات الخطأ.

## ملحق ج — ملفات تسليم التطوير المقترحة

```text
lisan-enforcement/
  README.md
  contracts/
    research-request.schema.json
    study-record.schema.json
    gate-receipt.schema.json
    published-artifact.schema.json
  policy/
    policy-v1.yaml
    policy-evaluator.py
  adapters/
    librechat-tool-approval-adapter.js  # exact SDK signature only after inventory
    lisan-corpus-adapter.py
    lisan-repository-adapter.py
  services/
    research-router.py
    gate-engine.py
    evidence-validator.py
    review-approval.py
    publication-guard.py
  migrations/
    001-study-revisions.sql
  tests/
    unit/
    contracts/
    integration/
    e2e/
    adversarial/
    recovery/
  evidence/
```

وجود الملفات أعلاه مقترح لتنظيم الفرق، **وليس إلزامًا بتغيير لغة المشروع أو إنشاء كل هذه الخدمات**؛ قد تستوعب حزمة واحدة هذه الوحدات مع احتفاظ واجهاتها بالحدود المنطقية والأذونات.

## ملحق د — المصادر التقنية العامة وروابط مراجعتها

- LibreChat: Agents endpoint object structure, especially `toolApproval`, `hooks`, `capabilities`, `maxSubagents`, `checkpointer`: [Agents endpoint وTool Approval](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/agents)
- LibreChat: Agent Chain, Subagents, Ask User and advanced settings: [Agents وSubagents وAgent Chain](https://www.librechat.ai/docs/features/agents)
- LibreChat: Skills, including `allowed-tools` and application modes: [Skills وقدرات الأدوات](https://www.librechat.ai/docs/features/skills)
- LibreChat: Built-in tools and extension preference for MCP/Actions: [Tools وطرق التمديد](https://www.librechat.ai/docs/configuration/tools)
- LibreChat: Message composer behavior and tool selection: [Message composer](https://www.librechat.ai/docs/features/composer)

**ملاحظة توثيقية:** روابط وثائق LibreChat قابلة للتغير. يجب في WP-00 التقاط المصدر المتوافق مع `git commit/tag` المنشور، وحفظ تاريخ الفحص وdiff بين النسخة والوثيقة إن اختلفت. ولا تعد هذه المراجع مصدرًا دلاليًا لكلمة قرآنية.

---

## 25. القرار الختامي

تُعتمد هذه المواصفة **مرشحًا للتنفيذ** لا سياسة منتجة حاليًا. الأساس البرمجي المطلوب لإنفاذ LISAN ليس تكثير الوكلاء، بل جعل كل فعل حرج يمر بخدمة موثوقة تختبر: **من يطلب؟ وبأي نطاق وإصدار؟ وعلى أي مصدر؟ وما الأدلة التي استُخرجت؟ وما الذي تم اختباره ومراجعته؟ ومن وافق؟ وهل نسخة النشر مطابقة لذلك كله؟**

إذا تعذر اعتراض نص المحادثة الحرة في LibreChat، لا تُوصف كل الإجابات بأنها محروسة. يُنشر فقط `Verified Artifact` من المسار المحكوم، وتظل المسودات المحادثية موسومة بحدودها. ويظل شرط LISAN العلمي الأعلى: **الدليل القرآني يسبق الدعوى، والملاحظات والنقض والقيود تسبق قبول النتيجة، ولا تتغير السلطة الدلالية بأسماء الأدوات أو موافقة النموذج.**
