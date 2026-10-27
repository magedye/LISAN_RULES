# بوابات G0–G12 والسياسات وعقود التنفيذ — مواصفة تنفيذية

## ثلاث طبقات لا يجوز خلطها

1. **توجيه النموذج**: Instructions/Skills/Prompts، تحسن الالتزام لكن لا تمنع تنفيذ مخالفة تقنيًا.
2. **منع عمليات غير مصرح بها**: صلاحيات LibreChat، `toolApproval` وMCP وخادم المجال، تشكل Enforcement عند الحدود المدعومة والمختبرة.
3. **المراجعة الدلالية**: تقييم قوة الاستدلال وصدق ادعاء معنى، لا يُستنتج من مطابقة النص أو schema أو توافق النماذج.

المصفوفة الكاملة في [`GATES_13.csv`](../catalogs/GATES_13.csv). حالات البوابة: `PASS, FAIL, BLOCKED, NOT_RUN`. كل مدخل في البوابة يحمل `study_id`, `revision`, `corpus_sha256`, `policy_version`, `method_version`, `actor_subject_from_host`, `input_digest`, `validator_version`, `verdict`, `reason`. لا يملك النموذج تعديل Verdict صادر عن الخادم.

## العقود العملية

| البوابة | مالك الإنفاذ | المدخل المطلوب | نتيجة آلية ممكنة | حدّها |
| --- | --- | --- | --- | --- |
| G0 Router | Policy/Host | نية المستخدم، mode، نطاق، صلاحيات حقيقية | منع وضع/أداة/تفويض غير مأذون | لا يقرأ عقل النموذج |
| G1 Corpus | Corpus Authority | id/version/sha/source authenticity | تعليق إن تغير pinned source | Owner attestation ليست شهادة مستقلة |
| G2 Coverage | فهرس/Corpus Adapter | selector، fingerprints، retrieved/analyzed/remaining | إثبات حدود Query المصرّح به | TOKEN لا يشمل الجذر كله |
| G3 Observation | Evidence Validator | ref، quote، نوع ملاحظة، مصدر وسم | رفض تحريف أو نقل استنباط إلى نص مباشر | صحة علاقة نحوية تحتاج مراجعة |
| G4 Hypothesis | Research Engine | فرضية منافسة وشرط رفض وwarrant | رفض غياب الحقول/القابلية للإبطال الواضحة | جودة المنافس مسؤولية الباحث والمراجع |
| G5 Countersearch | الأدوات + السجل + ناقد | بحث فعلي ونطاق ونتيجة حتى إن لم يظهر ناقض | رفض غياب سجل بحث، لا إلزام اختلاق مضاد | الحكم بأن الشاهد ينقض غير حتمي |
| G6 Semantic Warrant | مراجع دلالي مستقل | الشواهد، الحجة، البدائل، الحدود | طلب مراجعة/UNRESOLVED | لا توجد «دالة دحض» تثبت صحة معنى |
| G7 Lock | Registry مع معاملة CAS | Snapshot وmethod/policy/source | SHA-256 وإصدار ثابت | hash = ثبات bytes فقط |
| G8 Review | Review Service | reviewer مختلف عن الباحث وقرار معلل | حفظ قرار مراجعة وحالته | ليس اعتمادًا |
| G9 Approval | AuthZ + Approver | قرار معتمد لـsnapshot ونطاق وإصدار | تخويل قبول/رفض وفق دور حقيقي | لا يأخذه من نص LLM |
| G10 Contextualize | SEM + Validator | نتائج المفردات المحورية وسياق الآية | كشف نقص مؤثر، توثيق التركيب | لا يُنتج معنى جديدًا بلا سند |
| G11 External | Policy + separate context | طلب صريح، internal lock | منع الوصول قبل القفل | لا يزيل تدريب النموذج |
| G12 Publication | Trusted Publisher | snapshot حيّ ومعتمد ومراجع ومقفل | WITHHOLD عند غياب شرط أو إبطال | لا يمنع جوابًا حرًا غير موسوم بحد ذاته |

## Policy-as-code في النموذج المرجعي

- `Policy.tool_allowed(mode,tool)`: قائمة ضيقة لسبع أدوات القراءة الأصلية في المراحل الداخلية؛ خارجها **DENY**.
- `Policy.choose_route(...)`: سياسة حتمية للاختيار بين reuse/extension/new/blind/post-lock؛ مدخل `finding_accepted` يجب أن يأتي من Registry موثوق لا من النموذج.
- `Registry.create` يحصر selector بواسطة Corpus Adapter لا يقبل مقامات كتبها النموذج.
- `Registry.observe` يتحقق من النص الحرفي/ref، ويفرض `STRUCTURAL_CANDIDATE` على الأوصاف غير النصية.
- `Registry.hypothesize` يطلب فرضية ومنافسًا وشرط رفض ووجه استدلال؛ لا يصدر دعمًا معتمدًا.
- `Registry.countersearch` يوثق مراجع فحص محددة ويقبل `NOT_FOUND_IN_EXAMINED_SCOPE`. **إقرار الباحث بأنه فحصها يحتاج إيصال استدعاء host موثوق في النظام الإنتاجي**؛ المرجع يسجل هذا الحد بدل إخفائه.
- `Registry.seal` يقفل snapshot بصمة ومراجعة عددية لـ`FULL_DECLARED`، ولا يقول semantic FULL.
- `Registry.review`, `approve`, `release` تفصل الهويات: الباحث ≠ المراجع، المعتمد ≠ المراجع/الباحث، الناشر ≠ الباحث. **هذه الدوال لا تُعرض بوصفها أدوات نموذج**.
- `Registry.public_card` يعيد نشر CURRENT فقط إذا تطابقت نسخة السجل وقرار المراجعة والاعتماد والإصدار ولم يوجد أثر إبطال تابع. لا يفتح Web أو تفسيرًا.
- `Registry.reopen` ينشئ إصدارًا جديدًا ويضع الأبناء المتأثرين في NEEDS_REVALIDATION.

## حدود الإثبات في مرجع Python

**قابل للاختبار:** شكل العملية، ملاءمة mode، اقتباس حقيقي عبر bridge أصلي، رفض ملف خارجي كمصدر قرآني، فتح نسخة وإبطالها، الهوية الممثلة في `Principal`، حساب SHA، عدم تعديل Snapshot مقفل، نشر بطاقة لا ينشئها النموذج.

**غير مؤهل إنتاجيًا:** استخراج Principal من مصادقة LibreChat حقيقية، ربط التحليل النصي بإيصالات استرجاع موقعة ودائمة، multi-tenant ACL، تدقيق قبول أصالة المصدر الرسمي، idempotency keys شاملة، HSM أو توقيع مستقل، audit anchoring، منع streaming replies من LibreChat تلقائيًا، تسلسل الموافقات الحقيقي، وترحيل النسخ السابقة وحماية بياناتها. كل ذلك عمل WP متبقٍ، وليس نجاحًا ضمنيًا للاختبارات المرجعية.

## عقد عينة الادعاء

```json
{
  "claim_id": "C1",
  "claim_kind": "SEMANTIC_HYPOTHESIS",
  "claim_scope": "EXPLICIT_VERSE_SET",
  "selector_id": "sha256-of-declared-query",
  "corpus_sha256": "from-server-only",
  "statement": "اقتراح دلالي لا يحكم بصحته",
  "evidence": [{"ref": "2:157", "quote_kind": "FULL", "verified": "SERVER_VERIFICATION_REQUIRED"}],
  "warrant": "وجه الاستدلال القابل للمراجعة",
  "falsification_condition": "شرط رفض قابل للاختبار",
  "rival": "أقوى تفسير منافس",
  "countersearch_state": "NOT_RUN",
  "epistemic_status": "HYPOTHESIS",
  "release_acceptance": "NOT_GRANTED"
}
```

القيم مثل `from-server-only` علامات شرح لا تصلح كمدخلات فعلية إلى schema المرشح. عقوده الأصلية تبقى في `baseline/.../sources/candidate-references/schemas` ويجب فحص التوافق معها، لا استبدالها بالافتراض.

## عقد منع تسريب الاعتماد في المحادثة

تعليمات `ORCH` يجب أن تمنع وصف نتيجة بالنشر الرسمي ما لم يقدم خادم النشر `released_digest` مطابقًا. ومع ذلك **منع النص المحادثي المخالف منعًا كاملًا** يحتاج خادمًا يعترض نهاية الرسالة أو stream في موضع مضمون؛ `toolApproval` وMCP لا يكفيان. إن لم يوجد ذلك، تعرض إجابات الدردشة بوصفها `RESEARCH_DRAFT` فقط، وتكون البطاقة الرسمية من خادم النشر منفصلة وواضحة.

## السياسات على LibreChat

`toolApproval.mode=dontAsk` يرفض unmatched tool calls؛ `deny` يحظى بأولوية. لكنه إعداد عالمي/خاص بالمثيل وليس محركًا يفهم حالة الدراسة. **الأفضل مثيل بحث داخلي مخصص** ونموذج أدوار مخول. وضع `capabilities` العالمي لا يثبت وحده سياسات كل طفل؛ والتحقق من صلاحيات MCP الأصلية على الخادم ضروري. لا تضف Hook غير موثق حتى تؤهل عقد API للنسخة المنشورة؛ الأمثلة العامة Hooks تعمل لتنقيص السلطة ولا تثبت اعتراض النص النهائي.

## الآثار والتسجيل

كل Gate يحتاج إيصالًا يتضمن verdict، object digest، إصدار validator، corpus/profile، والجهة المعتمدة. سجل الأحداث في النموذج `SHA-256` chain **ليس توقيعًا ضد مالك قاعدة البيانات**؛ لتوفير Tamper-evident خارج صلاحيات DBA يلزم توقيع/anchoring على خدمة منفصلة. لا ينفذ صاحب الصلاحية اعتمادًا داخل `ask_user_question` بمجرد ظهور زر موافقة؛ يجب أن تُربط هوية القرار بAuthN/AuthZ والتوقيع/النسخة داخل خادم المجال.
