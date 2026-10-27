# اختبارات القبول وصدق الأدلة: المرجع مقابل المنتج

## ماذا اختُبر فعلًا؟

- حفظ baseline كما هو وفحص SHA للـZIP الأصلي وفحص Catalog counts.
- 57 اختبارًا وحدويًا محليًا لكود `reference` باستخدام **نصوص صناعية غير قرآنية**، تشمل سياسات القراءة، الحصر المقيد، الفرضية، النقض، القفل، الأدوار، الإصدارات، التبعيات، منع النشر وread-only publisher.
- اتصال محلي live-read-only مع `runtime/tools/stdio.mjs` الأصلي: status، استعلام صريح عن شكل كلمة، استرجاع نص مرجع، مطابقة نص، رفض تحريف؛ لا إنتاج معنى أو إطلاق رسمي.

**النتيجة لا تثبت:** استقلال المراجعة البشرية في المنتج، صلاحيات LibreChat الحية، قبول source أصالة مستقلة، مطابقة نماذج AI للمنهجية، تأهيل 37 وظيفة أو 30 طبقة أو 38 قدرة، ولا جودة النتائج الدلالية.

## طبقات الاختبار

| الطبقة | موضوعها | الحالة عند التسليم |
| --- | --- | --- |
| L0 — package/static | صحة checksum والمسارات وCSV/JSON والهيكل | يُنفّذ بفاحص الحزمة محليًا |
| L1 — reference engine unit | invariants وحدود أدوات/أدوار/قفل/نشر | 57 PASS على fixtures |
| L2 — actual Quran corpus MCP | نقل status/search/verse/quote وعدم اختلاق النص | smoke محدود PASS؛ مصدره owner-attested |
| L3 — LibreChat integration | YAML/Agent Builder/Skills/ACLs/child contexts/hooks | NOT_RUN في هذه البيئة |
| L4 — semantic quality | test suite مع أسئلة قرآنية فعلية ومراجعين مستقلين | NOT_RUN |
| L5 — release/security | هوية الموافقة، tenant isolation، server output interception، audit anchoring | NOT_RUN |

## مصفوفات قابلة للاستخدام

- [`ACCEPTANCE_AT_38.csv`](../catalogs/ACCEPTANCE_AT_38.csv): 38 اختبارًا مشتقًا من وثيقة إنفاذ البوابات؛ الحالة `NOT_RUN_ON_LIVE`.
- [`AI_EVALS_EC_42.csv`](../catalogs/AI_EVALS_EC_42.csv): 42 اختبارًا إيجابيًا وسلبيًا لقدرات AI؛ الحالة `NOT_RUN_ON_LIVE`.
- `baseline/.../docs/09_ACCEPTANCE_AR.md`: 33 حالة T01–T12 وLC01–LC21؛ كلها `NOT_RUN` في المصدر السابق.
- `reference/tests`: فحوص كود مرجعي مستقلة، ولا تعادل أيًا من المصفوفات الثلاثة بحكم مطابقتها الظاهرية.

## معايير القبول الحاسمة

| Gate | اختبار يثبت المنع | اختبار يثبت القيمة البحثية | قرار الفشل |
| --- | --- | --- | --- |
| G0 | محاولة تشغيل external في BLIND، وحقن finding من الذاكرة | توجيه سؤال دلالي صحيح دون تعطيل SEM | عزل خاطئ → BLOCKED نشر رسمي |
| G1/G3 | آية برقم خاطئ أو نص محرف أو وسم فاعل مختلق | استرجاع نص قرآني صحيح مع مصدره | FAIL كامل لتلك الدعوى |
| G2 | إدعاء FULL لجذر باستعلام شكل واحد | عد صحيح لمطابقات QUERY محددة | رفض تعميم شمول الجذر |
| G4/G5 | فرضية بلا شرط رفض؛ counterevidence ملفق | منافس قوي وموضع صعب موثق، أو عدم العثور على مضاد | HYPOTHESIS/UNRESOLVED لا SUPPORTED |
| G6/G8 | reviewer == author أو تصويت نماذج بلا warrant | مراجعة بشرية تعارض تفسيرًا مألوفًا وتقدم سببًا | لا مراجعة مستقلة |
| G7/G9 | تعديل locked snapshot أو ادعاء approve قديم | فتح إصدار جديد مع cascade للاعتماديات | WITHHOLD |
| G11 | قراءة تفسير أثناء بحث corpus داخلي | مقارنة واضحة بعد القفل مع فصل المصدر | منع المقارنة عن المسار الداخلي |
| G12 | جواب حر يدعي الاعتماد بلا artifact | بطاقة رسمية لا تخرج إلا من snapshot مؤهل | لا ادعاء حماية شاملة حتى اعتراض الخروج |

## عقد Evidence Log لكل اختبار حي

سجل `test_id`, `run_id`, `baseline_commit`, `agent_ids`, `model_provider_and_version`, `corpus_sha`, `policy_sha`, `skill_versions`, `setup`, `actual_tool_calls`, `observed_output`, `expected`, `verdict`, `failure_code`, `evidence_file_digests`, `independent_reviewer`. لا تكتب PASS دون أثر تنفيذ. `BLOCKED` و`NOT_RUN` لا يعاد تسميتهما نجاحًا.

## تقييم فاعلية تقسيم الوكلاء

شغّل دراسة واحدة بنطاق متطابق في أربعة تكوينات، بعد مراجعة أسئلة واقعية ومراجعين معميين قدر الإمكان: **A)** وكيل واحد مع corpus، **B)** ORCH+SEM+CRITIC، **C)** +MORPH+AUDIT، **D)** +Blind عند trigger. احسب قيمة اكتشاف منافسين أصعب، معدل أخطاء الإسناد، زمن المراجعة، كلفة التوكنات وعدد انتقالات الأدوات. لا يعتبر عدد الوكلاء مؤشر جودة. عدم ظهور عائد مستمر يجيز دمج الدور تشغيليًا مع الحفاظ على وظيفة المنهج.

## منع خداع الاختبارات

- احتفظ ببيانات اختبار مستقلة عن أمثلة Instructions وعينات تحسين Prompt.
- لا تشغل اختبار دلاليًا على بيانات fixture اصطناعية وتصفه تحققًا من القرآن.
- لا تستخدم النموذج المنشئ نفسه حكمًا وحيدًا على صحة عبارات warrant؛ يتدخل مراجع متمكن.
- لا تعد اختبار صحة quotation تحققًا من معنى الآية.
- لا تسمح بفحص coverage يتجاهل pagination أو يخلط MATCH_EVENTS مع VERSES.
