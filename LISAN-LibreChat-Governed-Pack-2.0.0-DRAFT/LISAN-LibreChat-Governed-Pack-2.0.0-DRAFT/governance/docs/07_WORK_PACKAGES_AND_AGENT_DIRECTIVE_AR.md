# خطة التنفيذ المحكومة: Work Packages وطلب جاهز للوكيل المطوّر

**الغرض:** استكمال LISAN على LibreChat اعتمادًا على الحزمة المحفوظة، لا بناء منصة موازية. هذه الخارطة تكليف فني مقترح، ولا تفوض تغيير المشروع الحالي أو النشر. افتح مرحلة التعديل بعد جرد البيئة وحدود السلطة والحصول على التصريح الملائم.

| الحزمة | الغرض | المعتمد سابقًا / ما يُعاد استخدامه | الفجوة المستهدفة | شرط الإغلاق |
| --- | --- | --- | --- | --- |
| WP-00 | جرد وصلاحيات ونطاق | ZIP baseline، 10 Agents، 19 Skills، corpus 7 tools | مطابقة نسخة LibreChat وقدرات التشغيل + تداخل عقود lisan الأخرى | مصفوفة 37/30/38/13/Tests مع REUSE/CONFIGURE/COMPLETE/DEVELOP/DEFER |
| WP-01 | Corpus & Structural | stdio الأصلي، pinned Tanzil، QAC candidates | إثبات مصدر، pagination، محاذاة وسوم، count units | quote, bad quote, selector/coverage وsource receipts حية |
| WP-02 | Agents & Skills | تعليمات ووظائف الحزمة الأصلية | Routing واقعي، علاقات أطفال، Blind مستقل، منع Tool bypass | إثبات مسار واحد end-to-end مع أداة لازمة وفشل مصطنع |
| WP-03 | Research Registry | Candidate repo الموجودة إن ثبت توافقها | إصدارات/H09-H11/تعرض/تتبع اعتمادية | حفظ واسترجاع وإعادة فتح وCAS مع منع توريث القبول |
| WP-04 | Policy & Evidence Gates | JSON Schema ومثال Python | trusted caller + G0–G12، receipt، مراجعة semantic | اختبارات تدقيق أذون وإيصالات وتغطية، رفض النزوع إلى الإكمال |
| WP-05 | Blind & External | BLIND/COMPARE/SCIENCE/HISTORY الأصلي | عزل سياق وأدوات ومقارنة post-lock | إثبات سياسة عدم التسرب المرئي وفصل المصادر في المستند |
| WP-06 | Approvals & Publication | قاعدة البيانات المؤهلة بعد WP-03 | AuthN/AuthZ/review/approval/release وG12 | رفض وافق ذاتي، نشر من approved snapshot، إبطال تبعيات |
| WP-07 | Model eval & performance | الـ38 قدرات والـ42 Evals | مقارنة تطبيقية لميزة النموذج، مفاضلة التكلفة | بيانات مرجعية حية موقعة للمراجعة لا نسب مخترعة |
| WP-08 | Hardening & rollout | جميع الحزم أعلاه | أمن المستأجرين، observability، نسخ احتياطي، rollback | قبول مستقل وإذن نشر صريح |

## الترتيب والتبعيات

`WP-00 → WP-01 → WP-02` يمكنه إطلاق بحث **استكشافي فقط**. `WP-03 → WP-04 → WP-06` قبل أي بطاقة رسمية. `WP-05` بعد وضوح Policy والسياق؛ `WP-07` يبدأ من WP-02 ويعاد بعد كل تغيير. `WP-08` لا يسبق إنجاز اختبارات الجودة/الأمان ذات الصلة.

## توجيه تنفيذي مقترح لوكيل Codex/Antigravity

> **Project:** LISAN adoption into LibreChat — Governed Package 2.0.0-DRAFT.
>
> **Inputs:** `baseline/_original_archive`، و`baseline/Lisan-LibreChat-Pack-1.0.0`، و`governance/docs`، و`governance/catalogs`، و`reference/tests`.
>
> **Initial mode: READ-ONLY INVENTORY / NO IMPLEMENTATION.** ابدأ بـWP-00. حدد النسخة والفرع والبصمات وحالة الملفات غير الملتزم بها وحالة التشغيل؛ لا تعدلها أو تمسحها. افحص الأدوات والمهارات والـMCP والـRegistry الموجودة قبل اقتراح بديل. راجع كل قدرة من 37 وظيفة و30 طبقة و38 قدرة AI والبوابات الـ13، وافصل ما ثبت حيًا عما وثق في ZIP أو أداة من جلسة أخرى. لا تعتبر `PASS` في Python تجريبيًا قبولًا للإصدار.
>
> **Decision:** أعِد تقرير فجوات مصنفًا `REUSE/CONFIGURE/COMPLETE/DEVELOP/DEFER` مع أدلة نصية ومراجع الملفات ونسخها، وتبعيات وتقدير أثر تغيير؛ لا تكتب كودًا حتى يُعتمد نطاق الشريحة التالية وتفويضه. بعد التفويض نفذ أصغر شريحة مناسبة مع اختبار سلبي وإيجابي، ولا ترقِّ سلطة النموذج إلى مراجع أو معتمد أو ناشر.
>
> **Non-negotiable:** corpus first؛ لا تفسير خارجي قبل القفل؛ لا root FULL من TOKEN form؛ لا قبول ضمني لـH09/H10/H11؛ لا عزل أوزان مزعوم؛ لا تعديل sealed revision؛ الإيصالات من المضيف؛ فصل الباحث/المراجع/المعتمد/الناشر؛ No merge/push/deploy without separate authorization.
>
> **Deliverables:** Decision log، source/feature matrix، route/gate coverage، test plan مع negative cases، compatibility report v0.8.8/current، implementation proposals tied to actual code، rollback/owner impact؛ ثم تنفيذ الشريحة المفوضة ونتائج اختبار دقيقة.

## المتطلبات الوظيفية الإيجابية (لا تجعل الحوكمة تختزل المنهج)

1. يجوز لـSEM ابتكار فرضية دلالية جديدة متى استندت إلى استعمالات وآثار تركيبية واضحة وشرط نقض.
2. يجوز لـCRITIC نقد نتيجة مقبولة من غير إسقاطها آليًا؛ الخلاف سبب فحص H11/H12.
3. يُسمح بنماذج مختلفة أو embeddings وclustering للكشف الاستكشافي إذا تبقى مرشحات تُرد إلى القرآن.
4. إتاحة صيغة `UNRESOLVED` مقصد أصيل يمنع اختلاق حسم.
5. يختصر ORCH **العرض** لا المسار المنهجي أو الأدلة المؤثرة في الدعم.
6. ترتبط مهارة المستخدم بقدرة وRole محددين؛ لا تفتح مهارة جديدة الأداة الممنوعة من المضيف.

## شروط إيقاف الشريحة فقط

إذا ثبت تعارض لا يحسمه المرجع المحلي (صلاحية corpus، تخويل اعتماد، تعارض نسخ، ملكية بيانات، policy غير مثبتة في مصدر LibreChat)، صنف المتطلب المعني `BLOCKED` واترك بقية الوظائف المستقلة قابلة للاختبار. لا ترجع إلى مسار بناء نظام جديد من الصفر، ولا تتجاوز القيد لأن اختبارًا تعذر تشغيله.
