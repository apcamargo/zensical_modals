"""Build-time macros for the modal boilerplate."""

from functools import cache
from html import escape
from pathlib import Path

import zensical

ICON_DIR = Path(zensical.__file__).resolve().parent / "templates" / ".icons"


@cache
def _load_icon(name: str) -> str:
    """Return the theme's inline SVG markup for an icon such as ``lucide/x``."""
    icon_path = ICON_DIR / f"{name}.svg"
    if not icon_path.is_file():
        raise FileNotFoundError(f"missing icon: {icon_path}")
    return icon_path.read_text(encoding="utf-8").strip()


def _close_button(escaped_name: str) -> str:
    return (
        '<button class="modal__close" type="button" '
        f'data-modal-close aria-label="Close {escaped_name}">'
        f"{_load_icon('lucide/x')}</button>"
    )


def _height_style(min_height: str | None, max_height: str | None) -> str:
    """Build a ``style`` attribute setting the modal's height CSS variables.

    Returns an empty string when neither bound is given, so the modal falls
    back to the CSS defaults.
    """
    vars_ = []
    if min_height is not None:
        vars_.append(f"--modal-min-height: {min_height}")
    if max_height is not None:
        vars_.append(f"--modal-max-height: {max_height}")
    if not vars_:
        return ""
    return f' style="{escape("; ".join(vars_))}"'


def _render_modal(
    modal_id: str,
    title: str,
    body: str,
    show_header: bool = True,
    min_height: str | None = None,
    max_height: str | None = None,
    transparent: bool = True,
) -> str:
    """Render a dialog element with a close button and a body.

    ``title`` labels the dialog (visibly in the header when ``show_header``
    is true, via ``aria-label`` otherwise) and is independent of the trigger
    button's label. ``show_header`` toggles the title bar. Without it, the
    dialog is labelled via ``aria-label`` (there is no visible title to
    point ``aria-labelledby`` at) and the close button floats over the body
    instead. ``min_height`` and ``max_height`` are CSS length values (e.g.
    ``"20rem"``) that override the dialog's default height bounds; omit
    either to keep its default. ``transparent`` toggles the dialog's
    translucent, blurred background; set it to false for an opaque panel
    (which also drops the now-useless backdrop blur).
    """
    title_id = f"{modal_id}-title"
    escaped_title = escape(title)
    height_style = _height_style(min_height, max_height)
    classes = ["modal"]
    if not transparent:
        classes.append("modal--opaque")

    if show_header:
        return "\n".join(
            [
                f'<dialog class="{" ".join(classes)}" id="{modal_id}" '
                f'aria-labelledby="{title_id}"{height_style}>',
                '<div class="modal__backdrop"></div>',
                '<div class="modal__surface">',
                '<header class="modal__header">',
                f'<h3 id="{title_id}">{escaped_title}</h3>',
                _close_button(escaped_title),
                "</header>",
                '<div class="modal__body">',
                body,
                "</div>",
                "</div>",
                "</dialog>",
            ]
        )

    classes.append("modal--no-header")
    return "\n".join(
        [
            f'<dialog class="{" ".join(classes)}" id="{modal_id}" '
            f'aria-label="{escaped_title}"{height_style}>',
            '<div class="modal__backdrop"></div>',
            '<div class="modal__surface">',
            _close_button(escaped_title),
            '<div class="modal__body">',
            body,
            "</div>",
            "</div>",
            "</dialog>",
        ]
    )


def modal(
    label: str = "Example modal",
    modal_id: str = "example-modal",
    title: str | None = None,
    body: str | None = None,
    min_height: str | None = None,
    max_height: str | None = None,
    transparent: bool = True,
) -> str:
    """Render a modal trigger button and its dialog.

    ``label`` is the trigger button's label, ``modal_id`` the dialog element
    id (which the trigger's ``data-modal`` references). ``title`` is the
    dialog's own label, independent of ``label``; when given, it's shown in
    a header with a close button, otherwise the dialog has no header (it's
    labelled via ``aria-label``, falling back to ``label``) and the close
    button floats over the body. ``body`` is the pre-rendered HTML body of
    the dialog (defaults to the demo body). ``min_height`` and
    ``max_height`` are CSS length values (e.g. ``"20rem"``) overriding the
    dialog's default height bounds (``max-height: min(90vh, 40rem)``, no
    minimum); leave either as ``None`` to keep its default. Set
    ``transparent`` to false for an opaque dialog panel — this also drops
    the backdrop blur, which would otherwise have nothing to blur through.
    """
    show_header = title is not None
    dialog_label = title if title is not None else label
    body = body if body is not None else (
        "<p>This is a modal dialog styled to mirror the Zensical search "
        "dialog. It can be dismissed with the close button, by clicking "
        "the backdrop, or by pressing Escape.</p>"
        "<pre><code>{{ modal() }}</code></pre>"
    )
    escaped_label = escape(label)
    return "\n".join(
        [
            # Wrapped in a block-level element so python-markdown treats the
            # whole thing as a single raw HTML block. Without it, the leading
            # <button> (an inline tag) makes markdown parse this as paragraph
            # content and inject stray <p> tags around the <dialog>.
            "<div>",
            '<button class="modal-trigger" type="button" '
            f'data-modal="{modal_id}" aria-haspopup="dialog" '
            f'aria-controls="{modal_id}" aria-label="View {escaped_label}">'
            f"{escaped_label}</button>",
            _render_modal(
                modal_id,
                dialog_label,
                body,
                show_header=show_header,
                min_height=min_height,
                max_height=max_height,
                transparent=transparent,
            ),
            "</div>",
        ]
    )


def define_env(env) -> None:
    """Register documentation macros with Zensical."""

    env.macro(modal, "modal")
