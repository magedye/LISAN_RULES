# نموذج التهديد والفجوات والحدود المتبقية

## نموذج التهديد

| الفئة | طريق الهجوم أو الانحراف | الضابط المطلوب | هل أُغلق داخل الحزمة؟ |
| --- | --- | --- | --- |
| Prompt injection | ملف/أداة يزعم حق تعديل السياسة | بيانات غير موثوقة + أدوات مغلقة + عدم تمكين web في Blind | جزئي/إنفاذ مثيل مطلوب |
| Memory contamination | نقل finding سابقة أو معنى تراثي إلى Blind | سياق مستقل دون حقن RAG/Memory؛ Exposure Ledger | مسار موثق؛ لا اختبار UI |
| Training influence | معنى موروث ضمن أوزان LLM | نقد ودحض ومراجعة؛ لا شهادة نقاء | غير قابل للمنع قطعًا |
| Privilege escalation | LLM يرسل `actor_id=admin` | هوية مصادقة من Host، ليست حقل LLM | لم يدمج مع SSO/LibreChat |
| Source substitution | استبدال Tanzil/نسخة القرآن | pin + manifest + source attestation | نص pinned في runtime، الأصالة مشروطة |
| Evidence laundering | JSON صحيح يحوي فاعلاً مختلقًا | رفع النوع `STRUCTURAL_CANDIDATE` ومراجعة `warrant` | جزئي/الاختبارات مصطنعة |
| False coverage | TOKEN يقدَّم استقراءً لكل الجذر | UNIT/selector/count receipt و`semantic_exhaustive:false` | نعم في bridge، لا semantic engine |
| Tool bypass | LLM لا يستدعي validator وينشر جوابًا | server publication boundary | official card مرجعي فقط؛ chat الحر غير محجوب |
| Review spoofing | الباحث يراجع نفسه أو يطلب approve | principals موثوقون + فصل أدوار | وحدة مرجعية؛ ربط المصادقة غير منفذ |
| Tamper/replay | تعديل نسخة قديمة أو إعادة استخدام قبول قديم | CAS + sealed hash + revision match | نمط مرجعي، لا توقيع مستقل |
| Tenant crossover | مستخدم يرى دراسة غير مملوكة | ACL tenant scoping في DB/MCP | غير منفذ |
| Fake QAC semantics | وسم صرفي يُعامل خبرًا قطعيًا | provenance + alignment + conflicts | سياسة مكتوبة؛ المؤهل الكامل غير منفذ |
| Counter-evidence omission | الباحث يختار الشواهد المؤيدة فقط | ضد انتخاب المرجعيات، نقد، سجل مراجع كامل | يلزم إيصال server-side وتحقيق |
| Re-approval after change | تبديل policy/corpus/model مع إبقاء قبول | dependency graph وإبطال الإصدار المتأثر | مرجع H11 جزئي؛ نشر فعلي غير منفذ |
| Malicious Skill | Skill يفتح أدوات إضافية | افحص `allowed-tools` قبل النشر وقيد النطاق | baseline لا يحمل allowed-tools توسعية بحسب تقريره |
| Resource exhaustion | حلقات استدعاء وطلب ROOT شامل | pagination, recursion/tool budgets | يحتاج تكوين وتشغيل حيين |

## مستويات النشر المسموح بوصفها

- **LEVEL-0 / DOCUMENTED:** ZIP، ملفات تعليمات، شيفرة مثال، وسجلات اختبار محلية؛ لا واجهة حية.
- **LEVEL-1 / EXPLORATORY:** مثيل تجريبي مقيد، أدوات قرآن فقط، ووسم دائم `DRAFT/HYPOTHESIS/UNRESOLVED`؛ لا استحقاق رسمي.
- **LEVEL-2 / QUALIFIED_RESEARCH:** وظائف الحفظ/استرجاع ومسار مراجعة مستقل مُجتاز على المصدر الحقيقي؛ لا قبول رسمي بلا جهة مخولة.
- **LEVEL-3 / CONTROLLED_RELEASE:** AuthN/AuthZ، review+approval+release خادمي، Public Guard مثبت، وتهديدات عالية الأثر مختبرة؛ يمكن نشر بطاقات ضمن النطاق المعتمد.

لا يُرفع مستوى من تلقاء نفسه. `PASS` لوحدات Python اختبار للمثال وليس خروجًا إلى LEVEL-2 أو LEVEL-3.

## قرارات لا يمكن حسمها من ZIP

1. هويّة مصدر Quran الرسمية وشهادة أو إقرار المالك اللازم لقبول المصدر وفق نطاقه.
2. جهة الاعتماد الإداري (مالك واحد، لجنة، أو مفوضون) ومدى فصلها عن الباحث والمراجع.
3. السياسة النهائية لسحب نتيجة معتمدة وتأثير ذلك على الاستخدام الخارجي.
4. هل المطلوب نشر بطاقات رسمية عبر LibreChat نفسه أم بوابة منفصلة؟ هذا يؤثر في حراسة stream.
5. هل نسخ الملفات من `D:/APP/tafseer/...` مرخصة للاستخدام في بيئة LibreChat المستهدفة؟ وتأكيد شروط Tanzil/QAC/MASAQ وغيرها.
6. متطلبات أمن قاعدة البيانات الإنتاجية والنسخ الاحتياطي والتدقيق والاحتفاظ.
7. ربط مستخدمي LibreChat الحقيقيين مع principal الذي يستعمله محرك الحوكمة.

هذه القرارات تُجمع في سجل قرار، ويمكن تأجيلها أثناء LEVEL-0 وLEVEL-1 دون ادعاء نشر رسمي.
