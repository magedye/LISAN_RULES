# مصفوفة مكونات LibreChat

الاختيار هو استعمال المكونات التي تخدم المنهج، مع قرار صريح لبقية المكونات. «إعداد» لا تعني «تأهيل داخل المضيف»؛ [تقرير التحقق](../evidence/VERIFICATION_AR.md) يحدد المنفذ.

| المكون | الملف/الإعداد المقابل | قرار التبني | الحد |
| --- | --- | --- | --- |
| الواجهة وRTL | native.yaml + اختيار العربية من الواجهة | مفعلة للبحث مع عرض التكلفة والسياق؛ تخصيص بصري محدود | إخفاء الزر لا يثبت منع API أو تغيير Admin؛ واجهة مخصصة تحتاج تطويرًا |
| Models / Providers | اختيار داخل كل Agent + بيئة المثيل | يدوي، دون مفاتيح أو أسماء نموذج مفترضة | يجب تأهيل tool calling والعربية على النموذج الفعلي؛ لا نوصي بنموذج لم نختبره |
| Custom Endpoints / modelSpecs | إعداد المزود القائم أولًا؛ ضبط modelSpecs لاحقًا عند معرفة agent IDs | مستفاد من القدرة دون قالب معرفات وهمية | ليست هذه الحزمة إعداد مزود سحابي جديدًا أو ترقية تلقائية |
| Agents / Agent Builder | agents/*.setup.md و*.instructions.md | 10 أدوار جاهزة للنسخ | لا صيغة import-all غير مثبتة؛ الإنشاء اليدوي مقصود |
| Skills | skills/*/SKILL.md + DEPLOYMENT_SKILLS_DIR | 19 مهارة، Scope مختار وauthoring معطل | Available لا تعني always-apply؛ قواعد المنهج في Instructions |
| Subagents | ORCH يسمح بخمسة؛ allowSelf=false؛ shareFiles=false | التفويض الداخلي مع مراجعة | ليس عزلًا ضد تسرب التكليف الذي يرسله الأب؛ لا BLIND طفلًا |
| Agent Chain / Teams | لا تُفعّل capability chain في الملف الأساسي | مؤجل؛ العلاقة الحالية تنفذ بتكليف محدود | لا يلزم رسم DAG لتلبية المسار؛ تأليفه خارج Builder ليس إعدادًا يدويًا بسيطًا |
| MCP | lisan_readonly stdio + runtime الأصلي | 7 أدوات فعلية للقراءة والفحص | لا أدوات حفظ أو اعتماد؛ لا HTTP أو اتصال Site مفترض |
| Actions / Plugins القديمة | غير مفعلة في capabilities | غير لازمة مع خادم MCP المتاح | لا تعريف OpenAPI جديد ولا توسعة مصادر مخفية |
| Agent Plugins الجديدة | بديل تعبئة تجريبي موصوف في دليل الإعداد | لا نعتمدها افتراضيًا؛ Skills + MCP كافيان | manifest الخاص بـChatGPT ليس manifest LibreChat |
| Projects | projects/RESEARCH.instructions.md | تنظيم المحادثات مع تعليمات ثابتة فقط | شخصية؛ لا إعداد نموذج داخل المشروع ولا ذاكرة مشروع مفترضة؛ BLIND خارجه |
| Memory | memory.disabled=true وpersonalize=false؛ memories=false | معطلة في المسار الصارم | ليست سجل اعتماد معرفي؛ تفضيلات العرض نص ثابت |
| Prompts | prompts/P01..P12.md | نصوص مهام قابلة للإدخال في المكتبة | تساعد الطلب ولا تحل محل تعليمات الوكيل |
| Presets | presets=false؛ دليل يدوي عند الحاجة | مستغنى عنها لأن كل Agent يثبت تعليماته ونموذجه | لا JSON استيراد مجهول ولا System Prompt ثانٍ متعارض |
| Files / RAG / Citations | fileSearch=false وfileCitations=false داخليًا | خارج المسار الصارم؛ مراجعة المصادر يدويًا للمقارنة | Top-k لا يثبت حصر القرآن؛ relevance score ليس درجة ثقة معرفية |
| Web Search | webSearch=false داخليًا؛ librechat.external.yaml للبحث الخارجي | مصادر يدوية أو Tavily بمفتاح المشغّل في مثيل منفصل | إعداد خارجي جاهز لملء المفتاح، لكن الاتصال غير مختبر؛ لا يدعي الوكيل تصفحًا قبل وجوده |
| Code Interpreter / OCR | runCode=false وغياب execute_code وocr | غير مطلوبين لبحث المتن المثبت | OCR لا ينشئ Corpus مرجعيًا؛ أدوات قراءة محكومة أولى للحصر |
| Artifacts | Markdown وجداول جاهزة؛ capability غير مفعلة افتراضيًا | العرض النصي يغطي النسخة الأولى | توليد UI اختياري لا يحول الرسم إلى دليل؛ اقتراح شاشة مخصصة في C07 |
| Access Control / مشاركة | agents/skills/prompts/MCP مشاركة عامة معطلة؛ ملف trial-locked | مرحلة إعداد ثم إغلاق إنشاء الباحث العادي حسب Role | Admin ومالك الوكيل يظلان ذوي سلطة؛ افحص التعديل والصلاحيات فعليًا |
| Bookmarks / Export / History | bookmarks=true وtemporaryChat=false + تصدير موثق | للتنقل وأرشفة نسخة البحث | التاريخ ليس قاعدة canonical؛ لا ضمان عدم تعديل السجل |
| Scheduled Chats / Events | لا مهام مجدولة ولا tools لها في الملف | مؤجل إلى حاجة مثبتة | لا نشر أو قبول تلقائي لنتائج دينية؛ جدولة التذكير لا تعني مراجعة |
| Observability / تكلفة | contextUsage/contextCost + سجل الأدوات وتقرير التجربة | مؤشرات تشغيلية وتصدير يدوي | لا إعداد Langfuse أو خدمة إضافية بلا حاجة؛ عداد التكلفة لا يثبت الجودة |
| المعرفة المقبولة والتبعيات | templates + مراجعة وتصدير؛ C03/C04 | ممكن يدويًا وبنطاق معلن | السجل الدائم المؤهل والاسترجاع المحكوم وإعادة الفحص الآلية تحتاج خدمة |

تفاصيل الحقوق والحقول مستندة إلى [مخطط الإعداد المثبت](https://github.com/LibreChat-AI/LibreChat/blob/61892206974618971b9001d109485d994dac2816/packages/data-provider/src/config.ts) و[وثائق Agents](https://www.librechat.ai/docs/features/agents). توثيق [Projects](https://www.librechat.ai/docs/features/projects) يميز تعليمات المشروع عن إعداد النموذج؛ وتوثيق [Memory](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/memory) لا يجعلها سجل اعتماد دلالي.
