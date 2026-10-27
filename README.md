# LISAN_RULES

مشروع قواعد حوكمة LISAN — المصدر المحلي المرتبط بهذا المستودع:
`D:\APP\quran-lisan-plugin\LISAN_RULES_GITHUB`

## بنية المستودع

| المسار | الوصف |
|---|---|
| `LISAN_RULES_OPERATIONAL_REGISTRY_v2_230_FULL/` | السجل التشغيلي الكامل (230 قاعدة): CSV + JSON + XLSX + أدلة المقاييس والتتبع |
| `LISAN-LibreChat-Governed-Pack-2.0.0-DRAFT/` | حزمة LibreChat المحكومة (أهداف baseline + إعدادات `external/native` + الأرشيف الأصلي) |
| `templates/` | قوالب عربية جاهزة |
| `LISAN_Unified_Methodology_Governance_Enforcement_Spec_v1.0_DRAFT.md` | مواصفة الإنفاذ والحوكمة الموحدة (v1.0.0-DRAFT) |
| `LISAN_AI_Capabilities_Governed_Use_Reference_Implementation_v1.0_DRAFT.md` | مرجع تنفيذ الاستخدام المحكوم لقدرات الذكاء الاصطناعي (v1.0) |
| `LISAN_MultiAgent_Research_Architecture_Updated_v2.1_DRAFT.md` | معمارية البحث متعدد الوكلاء (v2.1) |

## الوثائق والتزمات

- جميع الملفات من نوع مسودة DRAFT ما لم تُذكر صراحة.
- ملفات `*.env.example` قوالب فقط ولا تحتوي مفاتيح حقيقية — لا ترفع أبداً `.env` حقيقية (مستثناة في `.gitignore`).

## سير العمل

```bash
git add <الملفات>
git commit -m "docs: وصف التغيير"
git push origin main
```

---

## English

LISAN Rules governance project: a 230-rule operational registry (CSV/JSON/XLSX),
governance specs in Arabic Markdown, a governed LibreChat pack, and templates.
Local source: `D:\APP\quran-lisan-plugin\LISAN_RULES_GITHUB`. Default branch: `main`.
`*.env.example` are placeholders only; real `.env` files are git-ignored.
