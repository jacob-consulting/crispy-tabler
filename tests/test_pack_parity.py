from pathlib import Path

import crispy_bootstrap5
import crispy_tabler
from crispy_forms.utils import render_crispy_form

from crispy_tabler.vendored import CRISPY_BOOTSTRAP5_VERSION
from tests.forms import CoverageForm

BS5_ROOT = Path(crispy_bootstrap5.__file__).parent / "templates" / "bootstrap5"
PACK_ROOT = Path(crispy_tabler.__file__).parent / "templates" / "crispy_tabler"


def _names(root: Path, *, skip: tuple[str, ...] = ()) -> set[str]:
    if not root.is_dir():
        return set()
    return {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.relative_to(root).parts[0] not in skip
    }


def bs5_names() -> set[str]:
    return _names(BS5_ROOT)


def pack_names() -> set[str]:
    # widget/ holds templates with no Bootstrap counterpart (added later).
    return _names(PACK_ROOT, skip=("widget",))


def pack_files() -> list[Path]:
    files = sorted(PACK_ROOT.rglob("*.html"))
    assert files, f"no templates under {PACK_ROOT}"  # never pass vacuously
    return files


def test_every_bootstrap5_template_has_a_counterpart():
    assert bs5_names() - pack_names() == set()


def test_the_pack_adds_nothing_unexpected():
    assert pack_names() - bs5_names() == set()


def test_no_template_references_the_bootstrap5_pack():
    offenders = [p for p in pack_files() if "bootstrap5" in p.read_text()]
    assert offenders == []


def test_every_template_records_its_provenance():
    for p in pack_files():
        assert CRISPY_BOOTSTRAP5_VERSION in p.read_text()


def test_a_form_renders_through_the_pack_without_touching_bootstrap5(settings):
    settings.INSTALLED_APPS = [
        a for a in settings.INSTALLED_APPS if a != "crispy_bootstrap5"
    ]
    html = render_crispy_form(CoverageForm())
    assert "form-control" in html
