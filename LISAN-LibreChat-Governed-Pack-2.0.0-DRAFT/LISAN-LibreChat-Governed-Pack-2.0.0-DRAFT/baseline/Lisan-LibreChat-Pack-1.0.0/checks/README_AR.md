# إعادة الفحص محليًا

هذه سكربتات تحقق للحزمة، وليست تعديلات على شفرة LibreChat أو خدمة لسان. لا تستدعي نموذجًا سحابيًا أو تعدل قاعدة بيانات. التشغيل من هذا المجلد:

```powershell
node .\probe-mcp.cjs
node .\probe-sdk.cjs 'D:\APP\LibreChat\node_modules'
node .\validate-config.cjs 'C:\Users\Majed\AppData\Local\Temp\lisan-librechat-source-20261022' 'D:\APP\LibreChat\node_modules' '..\config\librechat.native.yaml'
node .\validate-skills.cjs 'C:\Users\Majed\AppData\Local\Temp\lisan-librechat-source-20261022' 'D:\APP\LibreChat\node_modules'
& 'D:\APP\tafseer\lisanapp3\.venv\Scripts\python.exe' .\check-package.py
```

العميل SDK ومكتبات typescript/zod/js-yaml تُقرأ من تثبيت LibreChat الموجود؛ لا يجري تثبيتها أو تحديثها. validator يقرأ شفرة المصدر المثبتة مع تلك المكتبات، ولا يشغل تطبيق LibreChat. إذا نُقلت الحزمة إلى جهاز آخر يلزم توفير هذه المتطلبات أو الاكتفاء بـprobe-mcp ذي Node فقط. لا تحفظ مسار temp بصفته ضمانًا طويل الأمد؛ يمكن إعادة جلب commit الموثق من المستودع الرسمي.

check-package يتحقق من عدد الأدوار والمهارات والوظائف والطبقات، والروابط المحلية المؤلفة، وJSON، وتطابق runtime مع المصدر وبصماته. يستثني روابط الوثائق الأصلية لأنها قد تشير إلى بنية الأرشيف الذي جاءت منه. فحص أنماط مفاتيح محدودة ليس تدقيق أسرار شاملًا. تقرأ السكربتات المدخلات ولا تمس الخدمات العاملة.

لإعادة الفحص على إعداد آخر، مرر ملف YAML إضافيًا إلى validate-config. لا تعِد الفحوص الناجحة إلا بعد تغيير مؤثر أو حاجة تأهيل لبيئة أخرى. فحوص واجهة LibreChat والنموذج والتصفح الخارجي والحاوية موثقة كـNOT_RUN، وتنفذ وفق docs/09_ACCEPTANCE_AR.md عند التهيئة لاحقًا.
