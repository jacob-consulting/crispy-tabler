"""Widgets for markup that Django's default widgets cannot produce.

The CSS classes (form-range, form-control-color) are applied by field.html,
which detects RangeInput and ColorInput through their input_type.
"""

from django import forms


class RangeInput(forms.NumberInput):
    """A slider: RangeInput(min=1, max=5) instead of a NumberInput with type=range."""

    input_type = "range"

    def __init__(self, attrs=None, *, min=None, max=None, step=None):
        bounds = {"min": min, "max": max, "step": step}
        super().__init__(
            attrs={**{k: v for k, v in bounds.items() if v is not None}, **(attrs or {})}
        )


class ColorInput(forms.TextInput):
    """A colour picker."""

    input_type = "color"


class PlaintextInput(forms.Widget):
    """Renders the value as text in a form-control-plaintext element, not an input."""

    template_name = "crispy_tabler/widget/plaintext.html"
