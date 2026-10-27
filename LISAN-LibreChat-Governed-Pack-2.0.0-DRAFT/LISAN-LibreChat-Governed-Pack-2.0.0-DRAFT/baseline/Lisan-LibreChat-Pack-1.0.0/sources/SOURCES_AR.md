# المصادر ومراجع القرار

تاريخ مراجعة المصدر: 22 أكتوبر 2026؛ تجميع الحزمة: 23 أكتوبر 2026. المصادر الخاصة محفوظة كما كانت في وقت القراءة؛ بصماتها في [INPUT_CUSTODY](../evidence/INPUT_CUSTODY.json). لم تُعدّل ملفات المالك الأصلية.

| الرمز | المصدر | طريقة الاستعمال |
|---|---|---|
| I01 | input-01.txt، الجرد الملصق | طلب مكونات؛ تحقق من ادعاءاته على الشفرة |
| I02 | input-02.md، تصور 1 | نقد وترشيد أدوار؛ ليست ادعاءاته التقنية مرجعًا نهائيًا |
| I03 | input-03.md، التصور الشامل | أصل الوظائف الـ37 والعلاقات |
| I04 | input-04.md، تعليمات مهمه | مبادئ الاستدلال وسياسة الأدلة والاختبارات |
| A01 | Quran_Lisan_Complete_Package_2026-10-14.zip | الحزمة الحديثة المستنتجة من الملفات؛ manifest تاريخي لا قبول تشغيل حالي |
| A02 | ACTIVE_METHODOLOGY_PROFILE.md وRESEARCH_EVIDENCE_AND_STATUS_CONTRACT.md | ملف المرشح وعقود مصدره/بحثه |
| A03 | candidate-references/POLICY_AR.md وMETHOD_REFERENCE_AR.md وOUTPUT_CONTRACT_AR.md | قواعد المصدر والإخراج وحدود الفحص |
| A04 | candidate-references/CUMULATIVE_RESEARCH_AR.md وschemas/ | عقود الدراسة والتراكم؛ لا افتراض خدمة متصلة |
| A05 | METHOD_LAYER_MAP.original.csv | أسماء الطبقات الثلاثين ومحدودية الدعم |
| A06 | runtime/ | نسخة بايتية من Site/Source_Snapshot/plugin/runtime داخل A01 |

## LibreChat الرسمي

المستودع: [LibreChat-AI/LibreChat](https://github.com/LibreChat-AI/LibreChat)، المرجع المثبت `61892206974618971b9001d109485d994dac2816`، package version `v0.8.9-rc1`. نسخة محلية منفصلة قُرئت في D:/APP/LibreChat عند `74ccf8e3654a0ec5bbae537d9339e622c0625885` وتعلن `v0.8.8`؛ لم تُحدَّث أو تُشغَّل. وثائق الموقع تعلن Latest(dev)، لذلك لا يكفي اسم صفحة لإثبات توافق إصدار أقدم.

| القرار | مصدره الأولي |
|---|---|
| حقول YAML وMemory وcapabilities وtoolApproval وProjects | [config.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/data-provider/src/config.ts) |
| حدود maxSubagents وحدود نص المشروع | [limits.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/data-provider/src/limits.ts) |
| حقول Agent وsubagents/skills والتحقق | [validation.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/api/src/agents/validation.ts) |
| تحميل المهارات من مجلد filesystem | [deployment.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/api/src/skills/deployment.ts) |
| تحليل SKILL.md | [parse.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/api/src/skills/parse.ts) |
| شكل Agent Plugins | [manifest.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/api/src/plugins/manifest.ts) |
| قواعد موافقات الأدوات | [policy.ts](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/api/src/agents/hitl/policy.ts) |

مصادر الاستخدام: [Agents](https://www.librechat.ai/docs/features/agents)، [Subagents](https://www.librechat.ai/docs/features/subagents)، [Skills](https://www.librechat.ai/docs/features/skills)، [MCP](https://www.librechat.ai/docs/features/mcp)، [Projects](https://www.librechat.ai/docs/features/projects)، [Agent Plugins](https://www.librechat.ai/docs/features/agent_plugins)، [Memory config](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/memory).

الحقائق المتغيرة مرتبطة بهذا المرجع، وليست ضمانًا لإصدار مستقبلي. التصميم الذي يجمع الوظائف في عشرة وكلاء ويستخدم إجراء حفظ يدوي قرار هذه الحزمة، وليس خاصية تدعي LibreChat توفيرها بذاتها.


## مواد ظهرت أثناء التجميع

نسخ First-Docs السبع محفوظة في sources/first-docs وبصماتها في INPUT_CUSTODY. روجعت في 23 أكتوبر 2026 ومقابلها docs/12_FIRST_DOCS_RECONCILIATION_AR وdocs/13_LISAN_35_DIRECTIVES_AR. هذه المواد تضاف إلى حزمة 14 أكتوبر ولا تلغي هويتها؛ الأولى مقترحات وتعليمات تصميم، والثانية مصدر runtime وعقود المرشح. أرقام وأمثلة الدراسات داخل المقترحات أمثلة نصية، وليست نتائج بحث مثبتة هنا.
