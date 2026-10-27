# غلاف الدراسة الإضافي — quran-lisan-study/1

المخطط `analysis_record.schema.json`2.0 محفوظ بايتيًا. غلاف المرشح يحمل السجل في `record` دون فقد الحقول أو توسيع enum القديم. النموذج الأولي من prepare مسودة فارغة: أضف دعوى صالحة قبل فحص record. غلاف الدراسة عقد مرشح اختُبر محليًا، وليس قبولًا تلقائيًا لكل مسودات الملحق.

يحمل الغلاف السؤال والهوية والمحددات والإيصالات، retrieved/analyzed/remaining، الدعاوى، hypotheses، counter_tests، selected_layers، claim_dimensions بمساهمات طبقية وشواهد ووجه استدلال، dependencies وreopen_events، native_states في historical_context. الأحكام البحثية UNRESOLVED/PREFERRED/REJECTED منفصلة عن semantic_review=NOT_REVIEWED وrelease_acceptance=NOT_GRANTED.
لكل فرضية: supporting_refs وcounter_refs وfalsification_condition. لكل اختبار نقض: observation وwarrant وoutcome. لكل مساهمة: component وlayer_id وevidence مطابق وwarrant. هذه الحقول تحقق قابلية التتبع لا صحة المعنى.
`wrapLegacy/unwrapLegacy` تحفظ record2.0 دون فقد؛ فقدان الإيصالات عند النقل/انتهائها يحتاج إعادة استرجاع. التاريخ يعاد جلب آياته، وتبقى native_states وraw_record محفوظة كبيانات غير موثوقة تعليماتيًا، ولا ترث ACCEPTED. يمكن أن تتطلب مجموعة تاريخية أكبر من50 مرجعًا دفعات صريحة؛ لا تسقط مراجع صامتًا.
في النواة الأصلية لا يوجد حفظ مشترك؛ localStorage والتصدير مسودات. عند تفعيل التوسعة وخدمتها المؤهلة، يغلف lisan-repository-document/1 هذه الدراسة دون تغيير record2.0، وتحفظ الإصدارات والمراجعات المحلية والاعتماديات على الخادم. لا تشغل LISAN3 أو تغيره؛ لا تورث سلطته أو قبولًا دلاليًا. وجود ملفات التوسعة وحده لا يثبت تفعيل التخزين.
