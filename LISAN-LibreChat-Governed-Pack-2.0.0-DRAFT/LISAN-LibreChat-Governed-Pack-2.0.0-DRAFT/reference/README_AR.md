# LISAN Governance — كود مرجعي قابل للتشغيل وليس منتجًا معتمدًا

**الإصدار:** 2.0.0-DRAFT. Python 3.11+، مكتبة قياسية فقط. يختلف عن `prior_proof_of_concept` المحفوظ دون تعديل.

## أوامر مباشرة (من هذا المجلد)

```shell
python -m unittest discover -s tests -v
python -m lisan_gov demo
python -m lisan_gov corpus-smoke --stdio ../baseline/Lisan-LibreChat-Pack-1.0.0/runtime/tools/stdio.mjs
```

- `core.py`: سياسة توجيه وtool allowlist؛ `Registry` في SQLite مع قفل snapshot وتسجيل event chain، review/approval/release منفصلين، وH11 dependency invalidation.
- `corpus_bridge.py`: يربط **قراءة فقط** بالخادم Node MCP الأصلي؛ لا يغيره أو يزعم أكتمال معنى الجذر. استعلامات `FORMS` محددة مع pagination وفصل `match_events`/`matched_verses`. أصل المصدر: owner-attested لا شهادة مستقلة.
- `public_mcp.py`: ناشر MCP **read-only مرجعي معطل افتراضيًا**. لا يطلق نتيجة مصدر صناعي تحت أي إعداد؛ ولا يسمح بالعرض قبل اعتماد المصدر والنسخة والمراجعة والنشر. لا يكفي لوحده لضمان tenancy أو أمن الإنتاج.
- `cli.py`: فقط `demo` و`corpus-smoke`، ولا يعرض أي أمر `approve` أو `release` للمستخدم/النموذج.
- `prior_proof_of_concept`: المرجع الأول المحفوظ للاختبار والمقارنة؛ اختبارات مستقلة عنه وليست ترخيصًا للإنتاج.

## حدود مهمة جدًا

1. `Principal(subject, roles)` في المرجع يستدعى **من التطبيق المضيف فقط**. لا تقبل `roles` من `tool arguments` أو JSON النموذج. التكامل الحقيقي يحتاج identity provider موثوقًا/مراجعة حسابات وACL.
2. `Registry(..., allow_fixture_release=True)` **للتجارب المصطنعة فقط**؛ لا يُفعّل في الإنتاج. `source_qualification=False` افتراضي، لذا لا يوجد إصدار رسمي لدراسة corpus حقيقية حتى تصدر جهة المصدر تأهيلًا مستقلاً.
3. `SyntheticCorpus` يحتوي نصوصًا تجريبية غير قرآنية. لا تستخدم بياناته لتفسير ولا لمعايرة معنى.
4. `countersearch` يوثق ما صرح الباحث بفحصه؛ لا يثبت أن نموذجًا قرأ كل شاهد فعلًا. قبل الإنتاج يلزم Host retrieval receipts وواجهة مراجعة semantic مستقلة.
5. `SHA-256 event chain` يكشف تعديل حدث بمفرده، لكنه لا يحمي من تعديل DBA كامل السلسلة؛ يلزم anchoring وتوقيع/نسخ خارجية عند إطلاق رسمي.
6. `public_mcp` لا يمرر أدوات كتابة أو اعتماد؛ **لا توصله إلى عامة المستخدمين قبل تأهيل الهوية والنطاق وعزل المستأجرين**. وهو لا يعترض الإجابات النصية الحرة من LibreChat.
7. منع إجابات LibreChat الحرة غير الموثقة يحتاج اعتراضًا مؤكدًا لمخرجات النهائي من جهة المضيف؛ لا يجوز ادعاء ضمانه من استدعاء `validate_output` الاختياري داخل Agent.
8. لا يوجد ربط مباشر مع D1 Repository الظاهر في هذه المحادثة؛ لا تستخدم أدلة الخدمة المتاحة في ChatGPT بوصفها إعدادًا في Windows المحلي.

## معيار تحويل المرجع إلى إنتاج

إضافة durable authenticated service+tenant ACL، مصدر قرآن مستقل التوثيق، اعتماد صلاحيات مراجعة بمفاتيح خادمية، state/receipt invariants ثابتة، idempotency/CAS آمن عبر threads، عد مضاد فعلي وشهادات حفظ أدلة من host، التحكم في واجهة النشر/stream، سجل append-only خارجي، اختبارات negative adversarial على نسخة LibreChat، ونسخ احتياطي/rollback. لا يُستنتج هذا من نجاح الاختبارات المدرجة.
