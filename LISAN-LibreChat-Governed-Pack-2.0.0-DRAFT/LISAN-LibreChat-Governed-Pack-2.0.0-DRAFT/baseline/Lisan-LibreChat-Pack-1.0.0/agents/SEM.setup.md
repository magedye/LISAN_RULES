# إعداد SEM

الاسم المقترح: `Lisan SEM — باحث الدلالة والسياق`. الوصف: يختبر المفهوم والمعنى الموضعي والفروق والعلاقات الداخلية.

1. أنشئ Agent في Agent Builder؛ الصق محتوى [SEM.instructions.md](SEM.instructions.md) كاملًا في Instructions.
2. اختر مزودًا ونموذجًا متاحين فعلًا يدعمان tool calling. اترك المعاملات الافتراضية أولًا؛ لا تفرض temperature على نموذج لا يدعمه. تأهيل النموذج موضح في [دليل التشغيل](../docs/03_SETUP_AND_OPERATION_AR.md).
3. Tools: اختر الأدوات السبع لخادم `lisan_readonly` فقط: lisan_status, lisan_search, lisan_get_verses, lisan_verify_quote, lisan_validate_analysis, lisan_prepare_research, lisan_check_study. لا تختَر خادمًا كاملًا آخر. نطاق الأدوات هنا قراءة وفحص؛ ليس حفظًا أو اعتمادًا.
4. Enable skills = On؛ Scope = المهارات المختارة فقط؛ Allow skill authoring = Off. اختر: lisan-study, lisan-context, lisan-compare, lisan-particles, lisan-letters, lisan-layers, lisan-narrative, lisan-evidence. تحقق من Available to agent لكل مهارة. لا تختَر الكتالوج كله.
5. Subagents = Off؛ Allow self-spawn = Off؛ Share files = Off. لا تحدد أطفالًا أو Teams أو Chain.
6. Recursion Limit = 24 كبداية تشغيلية، لا وعد بإكمال الدراسة. تعطيل Memory وWeb Search وFile Search وCode وActions وOCR في هذا الملف. المشاركة عامة = Off. لا تضف ملفات معرفة للوكيل الداخلي.
7. المسار الداخلي. اختر المسار والمهارات بحسب السؤال، وليس تشغيل جميع المهارات في كل مرة.

هذه ورقة إدخال للواجهة، وليست صيغة Agent JSON قابلة للاستيراد. لا توجد في الحزمة معرفات وكلاء أو مهارات أو مفاتيح مزود وهمية.
