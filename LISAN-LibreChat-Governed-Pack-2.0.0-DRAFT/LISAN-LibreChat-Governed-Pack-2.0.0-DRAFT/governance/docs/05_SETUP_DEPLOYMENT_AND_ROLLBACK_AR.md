# دليل التركيب والتشغيل والتراجع — Windows 10 / LibreChat

**لا تفوّض هذه الوثيقة النشر أو تعديل شيفرة مشاريع المالك.** يجب أن تبدأ التجربة في نسخة منعزلة من LibreChat، وأن يراجع مسؤول التشغيل نسخة المصدر المحددة وإعداداتها قبل أي استخدام. Paths في التهيئات أمثلة ولا تُنشأ ملفات في D: بواسطة هذه الحزمة.

## 0 — المتطلبات والإعدادات التي لا يجوز افتراضها

- Node.js **22 أو أحدث** للـruntime الأصلي في `baseline/Lisan-LibreChat-Pack-1.0.0/runtime` كما ينص `package.json` الخاص به.
- Python **3.11 أو أحدث** لتشغيل المثال المرجعي. شُغّل هنا Python 3.13؛ لا توجد تبعيات runtime غير المكتبة القياسية للكود المرجعي.
- مثيل LibreChat مستقل/تجريبي مملوك للمالك، وإمكان تعديل `librechat.yaml` وإعادة تشغيل **المثيل التجريبي فقط** بعد موافقة التشغيل.
- Git commit/baseline، نسخ محلية من `librechat.yaml`, `.env`، قائمة Agents وSkills وMCP، ولقطات للبيانات التي قد تتأثر؛ لا تستعرض الأسرار أو تضعها في التقرير.
- الهوية الدقيقة للمصدر وManifest ومطابقة رخصة النص والبيانات البنيوية.
- لا يلزم تنزيل نموذج أو خدمة جديدة لهذا الفحص المرجعي؛ تشغيل LLM حي مرحلة قبول مستقلة.

## 1 — تحقق من الحزمة محليًا قبل التعديل

من PowerShell (استبدل `<PACK>` بمسار ZIP المستخرج):

```powershell
cd '<PACK>\reference'
python -m unittest discover -s tests -v
python -m lisan_gov demo
python -m lisan_gov corpus-smoke --stdio '..\baseline\Lisan-LibreChat-Pack-1.0.0\runtime\tools\stdio.mjs'
```

- `demo` يشغل **نصوصًا مصطنعة غير قرآنية** في SQLite مؤقتة ثم يتخلص منها.
- `corpus-smoke` يتصل بالـMCP السباعي الأصلي read-only، ويجرب بحث TOKEN محددًا، ويتحقق من نص الآية ويرفض نسخة محرفة، ولا يثبت معنى قرآنيًا.
- لا تعتبر `RUNS=PASS` للعينات اعتمادًا للنشر؛ احتفظ بتقرير JSON ونسخة المصدر في مجلد Evidence.

## 2 — جرد نسخة LibreChat المستهدفة (WP-00)

1. سجل `git rev-parse HEAD`، tag والفرع وحالة `git status --porcelain` على **المثيل التجريبي**؛ لا تعمل على مستودع حي بعمليات إصلاح تلقائية.
2. تحقق من دعم `toolApproval`, `subagents`, `skills`, `mcpServers`, `checkpointer` في نسخة Schema المقروءة محليًا، وليس توثيق `Latest (dev)` وحده.
3. نفذ فحص YAML بمحلل المستودع المثبت، وسجل نتيجة Runtime validation؛ فحص PyYAML العام لا يغني عن Schema LibreChat.
4. افحص `Agent Builder` وصلاحيات أدوات كل وكيل، وطرق عرض Skills و`allowed-tools`، ومنع Web/File Search في الممر الداخلي.
5. تحقق من أهلية الـMCP السباعي واكتشافه من نفس عملية LibreChat على نفس حساب المستخدم؛ صحة تشغيل Node في Terminal لا تثبت الاتصال داخل UI.
6. صنف كل حاجة إلى: `REUSE`, `CONFIGURE`, `COMPLETE`, `DEVELOP`, `DEFER`، ولا تنشئ Adapter جديدًا بينما وظيفة مؤهلة موجودة بالفعل.

## 3 — تهيئة بيئة البحث التجريبية فقط

التكوين المقترح [`librechat.research-trial.reference.yaml`](../config/librechat.research-trial.reference.yaml) هو نسخة **مشتقة** من إعداد التجربة الأصلية `trial-locked` مع `toolApproval.mode: dontAsk` (default deny للأدوات غير المطابقة). يحتوي path مثالًا يحتاج ضبطًا. قبل استخدامه:

- لا تكتب فوق `librechat.yaml` الخاص بالمالك. انسخ تهيئة تجربة منفصلة فقط.
- عدل `mcpServers.lisan_readonly.command` و`args` إلى المسارات المثبتة على الجهاز؛ لا تستخدم مسار D: الموروث إذا لم يكن موجودًا.
- افتح فقط سبع أدوات القراءة/التحقق الموجودة في `MCP_TOOL_CATALOG.json`؛ لا تفتح delete/write أو أدوات خارجية في بيئة Blind.
- تعطيل Memory/Web/File Search/Actions/Execute Code في بيئة البحث قرار خاص بهذا المسار؛ لا يعني حذف تلك الميزات من LibreChat العام.
- أضف Skills من baseline كـ`DEPLOYMENT_SKILLS_DIR` أو رفعها يدويًا مع scope مختار، وليس «Use all skills». افحص ألا توسع أي مهارة الأدوات. منشئ الوكلاء لا يمنح اعتمادًا دلاليًا بمجرد تفعيل مهارة.
- أنشئ خمسة أطفال لـORCH وفق `AGENT_CATALOG.csv` وبـ`allowSelf=false`، مع إبقاء BLIND مستقلًا خارج PROJECT/MEMORY؛ `COMPARE/SCIENCE/HISTORY` في مسار مصدر خارجي منفصل بعد القفل.
- امنع مستخدم الاختبار غير الإداري من تعديل الوكلاء والمهارات ومخازن MCP، وقيّد نطاق الشبكة والنظام على المضيف.

## 4 — كيف يتصل النظام بسجل الحوكمة؟

لم يتغير stdio الأصلي ولم تضاف أدوات كتابة إليه. كود `reference/lisan_gov` يقدم نموذجًا مستقلًا لإثبات الآليات. التكامل الإنتاجي يتطلب خدمة domain وسيطًا على جهة الخادم يشتق Principal من هوية المستخدم الموثقة ويطبق صلاحيات mode/revision؛ لا تستدع دوال `approve`, `release` أو `reopen` من Agent Tool قابل لتزوير الهوية.

مرشح مستودع LISAN القائم في هذه المحادثة يوفر أدوات حفظ ودراسات، ولكن **لا يُفترض وجوده داخل LibreChat المثبت**، ولا تتبنى حالاته الحالية قبولًا دلاليًا. في WP-03 ابدأ بمطابقة الـAPI/Storage/ACL قبل بناء SQLite production جديد. لا تعتمد خادم `reference/lisan_gov/public_mcp.py` للتشغيل العام؛ **read-only reference disabled by default** ويحتاج مصدرًا معتمدًا وفحص tenant isolation.

## 5 — اختبار البحث الحي بعد إعداد المثيل

- تحقق من استدعاء أدوات status/verse/quote/search والتحليل المقيد لكل وكيل، واحفظ tool traces كاملة.
- غيّر input إلى اقتباس محرف ورقم آية خاطئ، وتأكّد من المنع الحقيقي لا كلام الوكيل.
- امنع فعليًا Web/File/External في BLIND عند مستوى tool runtime، واختبر ملفًا يحاول حقن تعليمات.
- تحقق من نوع التغطية: matched verses مقابل match events، و`semantic_coverage` غير ثابتة من استعلام form فقط.
- جرّب فرضية جديدة وناقدًا مخالفًا، وتحقق من إمكان النتيجة `UNRESOLVED` من غير اختلاق ناقض.
- اختبر حفظ النسخ وتعارض CAS وإبطال التوابع (بعد تأهيل السجل)، ثم workflow الموافقة وإصدار بطاقة رسمية مع مستخدمين مختلفين.
- اسأل في الدردشة مباشرة عن «نتيجة معتمدة»: تأكد أن الواجهة لا توهم بالموافقة؛ لا تصف السلوك محكومًا كليًا ما لم يوجد اعتراض موثوق لخاتمة الإجابة.

## 6 — سياسة التراجع

في حال فشل أي اختبار عالي الأثر:

1. أوقف **استحقاق نشر النتائج** فقط؛ لا تحذف السجلات التاريخية أو تغير corpus.
2. عد إلى نسخ التهيئة والوكيل قبل التجربة على مثيل مستقل، مع إعادة التشغيل للمثيل التجريبي فقط وبموافقة المسؤول.
3. سجل `failure_code`, affected Gate/Agent, source/policy/version وfixture المشغل وسجل الأدوات.
4. لا تعطل `toolApproval` عالميًا لتجاوز خطأ؛ عالج mismatch أو تجاوز سياسة الصلاحية محليًا.
5. إذا أعيد فتح قرار اعتمدت عليه نتائج أخرى، ضع تلك النتائج تحت إعادة فحص عبر H11 ولا تعيد نشرها على أنها current قبل التأهيل.

## 7 — معايير الترقية للمستويات

- **Exploratory**: corpus pinned مسترجع وفحوص quote/count موثقة؛ نتائج فرضية فقط، لا بطاقات رسمية.
- **Qualified research**: سجل دراسات حي بنطاق وإصدارات، منع تسمية قبول دون تفويض، مراجعة منفصلة وتحقق source.
- **Formal publication**: هوية مخولة مثبتة، approvals معتبرة، Release Guard مضبوط في موضع نشر مؤثر، اختبارات صلاحيات/إبطال/تراجع ناجحة، وعدم إمكان إظهار artifact رسمي من مسار LLM غير محكوم.

مراجع متغيرة تستلزم فحص الإصدار المحلي: https://www.librechat.ai/docs/features/skills ، https://www.librechat.ai/docs/features/subagents ، https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/agents .
