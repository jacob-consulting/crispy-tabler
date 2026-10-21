# Changelog

## 0.1.0 (unreleased)

First release.

- Template pack `crispy_tabler`: all templates of `crispy-bootstrap5` 2026.9, vendored and self-contained (no `bootstrap5/` references).
- Tabler fixes: `form-range`, `form-control-color`, `form-control-plaintext` for `UneditableField`, `form-fieldset`, `form-footer`, and full-size labels on radio and checkbox groups.
- `crispy_tabler.layout`: `UneditableField`, `FloatingField` and `Switch`, which follow `CRISPY_TEMPLATE_PACK`. The `FloatingField` / `Switch` subclasses work around [crispy-bootstrap5#226](https://github.com/django-crispy-forms/crispy-bootstrap5/issues/226) and become unnecessary if it is fixed.
- `crispy_tabler.widgets`: `RangeInput`, `ColorInput`, `PlaintextInput`.
- `crispy_tabler.fields`: `RangeField`, `ColorField`, `PlaintextField`.
- Runtime dependency on `crispy-bootstrap5>=2026.9`, because `crispy_tabler.layout` subclasses its `FloatingField` and `Switch`.
- django-crud-views renders through this pack with `crispy_bootstrap5` out of `INSTALLED_APPS`. Its one template with hardcoded Bootstrap includes, `crud_views/detail/field.html`, was unreferenced dead code and is removed upstream after 0.30.0 ([django-crud-views#217](https://github.com/jacob-consulting/django-crud-views/issues/217)); on 0.30.0 and earlier it ships but nothing renders it.
