# خادم MCP المعاد استخدامه

الملفات الخمسة عشر في runtime منقولة بايتًا ببايت من الحزمة المحددة في INPUT_CUSTODY، وتشمل إشعارات Tanzil وQAC. لا تثبيت npm داخل هذا runtime؛ يشغّل Node 22 أو أحدث ملف tools/stdio.mjs. التطبيق يتواصل معه عبر stdio، ولا يحتاج نشر HTTP أو مفتاح Site لعمل الأدوات المحلية السبع.

| الأداة | أهم المدخلات الفعلية | الغرض والحد |
|---|---|---|
| lisan_status | كائن فارغ | جاهزية النسخة وهوية المتن والبصمات؛ لا اعتماد دلالي |
| lisan_search | query؛ واختياريًا offset/limit | استعلام حرفي مع عدد الآيات والمطابقات وبيانات الصفحة |
| lisan_get_verses | refs؛ واختياريًا context | النص الأصلي للمراجع والسياق داخل السورة وفق الحد |
| lisan_verify_quote | ref وtext وkind | مطابقة FULL أو EXCERPT بالنص الأصلي؛ الرفض يعيد isError=true |
| lisan_validate_analysis | record | فحص سجل التحليل الأصلي وقيوده الميكانيكية |
| lisan_prepare_research | question؛ واختياريًا mode/selectors والطبقات | تنظيم السؤال والاسترجاع/الفهرسة البنيوية وسجل الدراسة |
| lisan_check_study | record أو study وما يلزمهما بحسب المسار | فحص الدراسة والأدلة والإيصالات؛ لا صحة معنى أو قبول |

المرجع الدقيق للحقول والأنواع والحدود هو [كتالوج الأدوات الذي اكتُشف فعليًا](../evidence/MCP_TOOL_CATALOG.json)، لا اختصار هذا الجدول. في prepare تظهر query وrefs وcomparison_queries وstructural_query وcontext وoffset وlimit وcount_unit وresume_receipt وselected_layers. لا تفترض أن أي تركيب منها صالح؛ اتبع شروط المسار وschema والتحقق الفعلي. يلزم record صحيح؛ كائن فارغ لا ينشئ دراسة.

أمثلة مدخلات صغيرة جرى فحصها محليًا، وليست نتائج دلالية:

```json
{"question":"شرح المنهج","mode":"METHOD"}
```

```json
{"refs":["1:1"],"context":0}
```

في البحث الحرفي query يحتوي forms وmatch بقيمة TOKEN أو SUBSTRING وnormalization بقيمة EXACT أو ARABIC_MARKS_V1. TOKEN وحدات مسافات؛ SUBSTRING مطابقات غير متداخلة لكل صيغة وفق تعريف الخادم. لا يتحول هذا إلى جذر أو إحصاء صرفي صامت. الاستعلام البنيوي في prepare يستخدم structural_query صريحًا؛ QAC مصدر وصف بنيوي بحدود مواءمته، لا مرجع معنى.

احتفظ بما أعادته الأدوات من original_text وrefs وprovenance وpage وreceipts؛ لا تصنع نسخة اقتباس من التطبيع. إيصالات هذه النسخة مؤقتة ومحلية العملية، ويمكن أن تتعذر مشاركتها بين جلسات MCP أو بعد إعادة التشغيل؛ أعد الاسترجاع في السياق المستلم إذا رفضت. لا تسجل HMAC من إنشائك أو تخفف الفحص.

العقد الأصلي موضح في [CANDIDATE_RECORD_AR](../sources/candidate-references/CANDIDATE_RECORD_AR.md) وschemas التابعة له. دفاتر templates مرافقة يدوية؛ لا ترسل RUN_WORKBOOK إلى lisan_check_study كما لو كان quran-lisan-study/1.

لا توجد أدوات حفظ أو بحث مستودع أو صلاحية قبول في هذا الخادم. COPY من كود Site آخر أو عنوان معروف لا يثبت ربطًا مصادقًا في LibreChat. إذا أراد المشغّل خدمة تراكمية بعيدة يلزم اكتشافها وتأهيلها فعليًا وفق C03، مع إبقاء هذا المسار القرآني مستقلًا عند تعطل التخزين.
