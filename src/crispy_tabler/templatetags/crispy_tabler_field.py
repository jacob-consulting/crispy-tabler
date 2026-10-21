from django import template

register = template.Library()


def _input_type(field):
    # The type attribute wins: forms.NumberInput(attrs={"type": "range"}) has
    # input_type "number", but renders type="range". Fall back to input_type
    # for widgets that declare it (RangeInput, ColorInput).
    widget = field.field.widget
    return widget.attrs.get("type") or getattr(widget, "input_type", None)


@register.filter
def is_range(field):
    return _input_type(field) == "range"


@register.filter
def is_color(field):
    return _input_type(field) == "color"


@register.simple_tag
def plaintext_control(field):
    # crispy_forms.bootstrap.UneditableField sets the Bootstrap 2 class
    # "uneditable-input" on the widget in Python, so the template cannot
    # simply leave it out. Swap it for Tabler's read-only value class before
    # crispy_field renders the widget. Renders nothing itself.
    classes = [c for c in field.field.widget.attrs.get("class", "").split() if c != "uneditable-input"]
    if "form-control-plaintext" not in classes:
        classes.insert(0, "form-control-plaintext")
    field.field.widget.attrs["class"] = " ".join(classes)
    return ""
