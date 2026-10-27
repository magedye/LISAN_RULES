# إعداد COMPARE

الاسم المقترح: `Lisan COMPARE — باحث المقارنة واسترجاع الدراسات المراجعة`. الوصف: يعرض دراسة مراجعة في نطاقها أو يجري مقارنة تراكمية وتشخيصية وخارجية معلنة.

1. أنشئ Agent في Agent Builder؛ الصق محتوى [COMPARE.instructions.md](COMPARE.instructions.md) كاملًا في Instructions.
2. اختر مزودًا ونموذجًا متاحين فعلًا يدعمان tool calling. اترك المعاملات الافتراضية أولًا؛ لا تفرض temperature على نموذج لا يدعمه. تأهيل النموذج موضح في [دليل التشغيل](../docs/03_SETUP_AND_OPERATION_AR.md).
3. Tools: اختر الأدوات السبع لخادم `lisan_readonly` فقط: lisan_status, lisan_search, lisan_get_verses, lisan_verify_quote, lisan_validate_analysis, lisan_prepare_research, lisan_check_study. لا تختَر خادمًا كاملًا آخر. نطاق الأدوات هنا قراءة وفحص؛ ليس حفظًا أو اعتمادًا.
4. Enable skills = On؛ Scope = المهارات المختارة فقط؛ Allow skill authoring = Off. اختر: lisan-cumulative, lisan-external-compare, lisan-logic, lisan-output, lisan-evidence. تحقق من Available to agent لكل مهارة. لا تختَر الكتالوج كله.
5. Subagents = Off؛ Allow self-spawn = Off؛ Share files = Off. لا تحدد أطفالًا أو Teams أو Chain.
6. Recursion Limit = 24 كبداية تشغيلية، لا وعد بإكمال الدراسة. تعطيل Memory وWeb Search وFile Search وCode وActions وOCR في هذا الملف. المشاركة عامة = Off. لا تضف ملفات معرفة للوكيل الداخلي.
7. خارجي/مقارنة؛ لا يختاره ORCH كطفل. الويب الخارجي يحتاج ملف نشر منفصلًا وأدوات مهيأة؛ النسخة الأساسية تستقبل مصادر يقدمها الإنسان فقط ولا تدعي تصفحها.

هذه ورقة إدخال للواجهة، وليست صيغة Agent JSON قابلة للاستيراد. لا توجد في الحزمة معرفات وكلاء أو مهارات أو مفاتيح مزود وهمية.


للإجابة من سجل مراجعة قدم البطاقة وإصدارها وسجل مراجعتها صراحة؛ لا يلزم إنتاج دراسة جديدة قبل عرضها. للمقارنة التشخيصية قدم نسختي الأصل وBLIND بعد انتهاء البحث المعزول. هذه إجراءات في الدور نفسه، ولا تضيف صلاحية حفظ أو اعتماد.
