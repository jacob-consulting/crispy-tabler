# Changelog

## 0.1.0 (unreleased)

First release.

- Template pack `crispy_tabler`: all templates of `crispy-bootstrap5` 2026.9, vendored and self-contained (no `bootstrap5/` references).
- Tabler fixes: `form-range`, `form-control-color`, `form-control-plaintext` for `UneditableField`, `form-fieldset`, `form-footer`, and full-size labels on radio and checkbox groups.
- `crispy_tabler.layout`: `UneditableField`, `FloatingField` and `Switch`, which follow `CRISPY_TEMPLATE_PACK`.
- `crispy_tabler.widgets`: `RangeInput`, `ColorInput`, `PlaintextInput`.
- `crispy_tabler.fields`: `RangeField`, `ColorField`, `PlaintextField`.
- Runtime dependency on `crispy-bootstrap5>=2026.9`, because `crispy_tabler.layout` subclasses its `FloatingField` and `Switch`.
- Known gap: django-crud-views detail pages still include Bootstrap partials.
