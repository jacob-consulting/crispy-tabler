from django import forms

from crispy_tabler.fields import ColorField, PlaintextField, RangeField
from crispy_tabler.templatetags.crispy_tabler_field import is_color, is_range
from crispy_tabler.widgets import ColorInput, PlaintextInput, RangeInput
from tests.helpers import render_field


def field_with(widget):
    form = type("F", (forms.Form,), {"f": forms.CharField(widget=widget)})()
    return form["f"]


def test_range_and_color_widgets_are_detected_by_the_filters():
    # These widgets carry no "type" attr, so detection must use input_type.
    assert "type" not in RangeInput(min=1, max=5).attrs
    assert "type" not in ColorInput().attrs
    assert is_range(field_with(RangeInput(min=1, max=5)))
    assert is_color(field_with(ColorInput()))


def test_plaintext_widget_renders_the_value_not_an_input():
    html = render_field(forms.CharField(widget=PlaintextInput(), initial="SKU-1"))
    assert "form-control-plaintext" in html and "<input" not in html
    assert "SKU-1" in html


def test_plaintext_widget_escapes_its_value():
    html = render_field(forms.CharField(widget=PlaintextInput(), initial="<b>x</b>"))
    assert "<b>x</b>" not in html and "&lt;b&gt;" in html


def test_range_widget_carries_its_bounds():
    html = render_field(forms.IntegerField(widget=RangeInput(min=1, max=5)))
    assert 'min="1"' in html and 'max="5"' in html and "form-range" in html


def test_color_widget_renders_a_color_swatch():
    html = render_field(forms.CharField(widget=ColorInput()))
    assert 'type="color"' in html and "form-control-color" in html


def test_fields_bind_their_widgets():
    assert isinstance(PlaintextField().widget, PlaintextInput)
    assert isinstance(RangeField().widget, RangeInput)
    assert isinstance(ColorField().widget, ColorInput)


def test_plaintext_widget_has_one_class_attribute_and_no_form_control():
    html = render_field(forms.CharField(widget=PlaintextInput(), initial="SKU-1"))
    assert html.count('class="form-control-plaintext"') == 1
    assert "plaintextinput" not in html and "required id" not in html
