# crispy-tabler

A [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) template pack for the [Tabler](https://tabler.io) UI kit.

Tabler is built on Bootstrap 5, and `crispy-bootstrap5` renders most forms acceptably under it. The gaps are the places where Tabler has its own class: range sliders, colour pickers, fieldsets, form footers, read-only values. `crispy-tabler` is a self-contained copy of the `crispy-bootstrap5` templates with those gaps fixed, plus a few widgets and layout objects. Its templates never reference `bootstrap5/`.

Requires Python 3.12+, Django 5.2+ and django-crispy-forms 2.4+. It ships no CSS; load Tabler yourself.

## Install

```bash
pip install crispy-tabler
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    "crispy_forms",
    "crispy_tabler",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ("crispy_tabler",)
CRISPY_TEMPLATE_PACK = "crispy_tabler"
```

`crispy-bootstrap5` is installed automatically as a dependency, but it does not need to be in `INSTALLED_APPS`.

## What is fixed

| # | Problem under Tabler | Fix |
|---|----------------------|-----|
| 1 | `UneditableField` emits the Bootstrap 2 class `uneditable-input` and no `form-control` | `form-control-plaintext`, label gets `form-label` |
| 2 | `type="range"` inputs get `form-control` and lose their track | `form-range` |
| 3 | `type="color"` inputs get `form-control` and stretch to a full-width bar | `form-control-color` |
| 4 | `Fieldset` renders a bare `<fieldset><legend>` | `form-fieldset` by default; an explicit `css_class` is appended |
| 5 | `FormActions` buttons sit directly under the last field, separated only by its `mb-3` margin | `form-footer` |
| 6 | Radio and checkbox group labels are shrunk with `fs-6` | plain `form-label`, same size as other labels |

Range and colour inputs are detected by their `type` attribute (`NumberInput(attrs={"type": "range"})` works) or, failing that, by the widget's `input_type`.

## Import swap for layout objects

`UneditableField`, `FloatingField` and `Switch` must be imported from `crispy_tabler.layout`:

```python
# before
from crispy_forms.bootstrap import UneditableField
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch

# after
from crispy_tabler.layout import UneditableField, FloatingField, Switch
```

The originals cannot be fixed from a template. `UneditableField` sets a Bootstrap 2 class on the widget in Python. `FloatingField` and `Switch` hardcode `bootstrap5/layout/...` template paths, so with `crispy_bootstrap5` not in `INSTALLED_APPS` they raise `TemplateDoesNotExist`. The `crispy_tabler.layout` versions subclass the originals and follow `CRISPY_TEMPLATE_PACK`. The `FloatingField` / `Switch` part is reported upstream as [crispy-bootstrap5#226](https://github.com/django-crispy-forms/crispy-bootstrap5/issues/226); if that is fixed, those two subclasses become unnecessary.

`BS5Accordion` needs no swap: its template path is `%s`-relative, so keep importing it from `crispy_bootstrap5.bootstrap5` and it renders through this pack. It is why `crispy-bootstrap5` remains a dependency.

## Widgets and fields

```python
from crispy_tabler.fields import ColorField, PlaintextField, RangeField
from crispy_tabler.widgets import ColorInput, PlaintextInput, RangeInput

class ProductForm(forms.Form):
    sku = PlaintextField(initial="SKU-1")      # value in a form-control-plaintext element, no input
    rating = RangeField(min_value=1, max_value=5)
    accent = ColorField()
```

`RangeInput` and `ColorInput` only set the right `input_type`; the CSS classes come from the templates. `PlaintextInput` renders the value, not an input. Bounds given only to the widget (`RangeInput(min=1, max=5)`) are presentation, not validation: a posted `99` still validates. Use `min_value` / `max_value` on the field, which also render the `min` / `max` attributes.

`PlaintextField` is disabled by default, so a posted value is ignored. The value must therefore come from `initial` (on the field or the form). It appears in `cleaned_data` as that initial, `has_changed()` is always `False`, and passing `disabled=False` makes the field accept posted data that the widget never renders. `PlaintextInput` keeps extra CSS classes you pass (`attrs={"class": "fw-bold"}`) next to `form-control-plaintext`.

## Known gap: django-crud-views detail pages

If you use [django-crud-views](https://github.com/jacob-consulting/django-crud-views), its create, update, detail and delete pages and the list filter all render through this pack, and `crispy_bootstrap5` can stay out of `INSTALLED_APPS`. (`crud_views/detail/field.html` hardcodes `bootstrap5/...` includes, but nothing renders that template; reported upstream as django-crud-views#217.)

## Provenance

Every vendored template starts with a comment naming the `crispy-bootstrap5` version and file it came from. Templates under `templates/crispy_tabler/widget/` are original to this package.

## License

MIT.
