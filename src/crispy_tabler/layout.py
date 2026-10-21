"""Layout objects whose Bootstrap originals cannot be fixed from a template."""

from crispy_forms.bootstrap import UneditableField as BootstrapUneditableField


class UneditableField(BootstrapUneditableField):
    """Read-only value rendered with Tabler's form-control-plaintext.

    The crispy_forms original sets the Bootstrap 2 class "uneditable-input"
    on the widget in Python, which a template cannot remove.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Swap the class in place so a css_class argument is kept.
        self.attrs["class"] = self.attrs["class"].replace(
            "uneditable-input", "form-control-plaintext"
        )
