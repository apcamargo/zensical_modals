import xml.etree.ElementTree as etree
from functools import cache
from pathlib import Path

import zensical
from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import Block, type_boolean, type_string

ICON_DIR = Path(zensical.__file__).resolve().parent / "templates" / ".icons"


@cache
def _load_icon(name: str) -> str:
    """Return the theme's inline SVG markup for an icon such as ``lucide/x``."""
    icon_path = ICON_DIR / f"{name}.svg"
    if not icon_path.is_file():
        raise FileNotFoundError(f"missing icon: {icon_path}")
    return icon_path.read_text(encoding="utf-8")


def _append_icon(parent: etree.Element, name: str) -> None:
    """Append a theme SVG while preserving ordinary HTML tag names."""
    icon = etree.fromstring(_load_icon(name))
    for element in icon.iter():
        if element.tag.startswith("{"):
            element.tag = element.tag.rsplit("}", 1)[1]
    parent.append(icon)


class ModalBlock(Block):
    """Render a dialog whose body is parsed as normal Markdown."""

    NAME = "modal"
    ARGUMENT = None
    OPTIONS = {
        "key": (None, type_string),
        "omit-header": (False, type_boolean),
        "opaque": (False, type_boolean),
        "min-height": (None, type_string),
        "max-height": (None, type_string),
    }

    def on_validate(self, parent: etree.Element) -> bool:
        """Validate the dialog's public authoring contract."""
        title = self.argument
        key = self.options["key"]
        attrs = self.options["attrs"]

        if not isinstance(title, str) or not title.strip():
            raise ValueError("modal blocks require a title after '|'")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("modal blocks require a non-empty key")
        if "id" in attrs:
            raise ValueError("modal blocks must not use attrs.id")
        if attrs:
            raise ValueError("modal blocks do not support attrs")

        modal_keys = self.tracker.setdefault("keys", set())
        if key in modal_keys:
            raise ValueError(f"duplicate modal key: {key}")
        modal_keys.add(key)
        return True

    def on_create(self, parent: etree.Element) -> etree.Element:
        """Create the dialog chrome and retain its Markdown body container."""
        title = self.argument
        key = self.options["key"]
        classes = ["modal"]
        if self.options["opaque"]:
            classes.append("modal--opaque")
        if self.options["omit-header"]:
            classes.append("modal--no-header")

        style_parts = []
        if min_height := self.options["min-height"]:
            style_parts.append(f"--modal-min-height: {min_height}")
        if max_height := self.options["max-height"]:
            style_parts.append(f"--modal-max-height: {max_height}")

        attributes = {
            "class": " ".join(classes),
            "modal": key,
            "aria-label": title,
        }
        if style_parts:
            attributes["style"] = "; ".join(style_parts)

        dialog = etree.SubElement(parent, "dialog", attributes)
        etree.SubElement(dialog, "div", {"class": "modal__backdrop"})
        surface = etree.SubElement(dialog, "div", {"class": "modal__surface"})

        if self.options["omit-header"]:
            self._close_button(surface, title)
        else:
            header = etree.SubElement(surface, "header", {"class": "modal__header"})
            heading = etree.SubElement(
                header,
                "div",
                {"class": "modal__title", "role": "heading", "aria-level": "3"},
            )
            heading.text = title
            self._close_button(header, title)

        self.body = etree.SubElement(surface, "div", {"class": "modal__body"})
        return dialog

    def on_add(self, block: etree.Element) -> etree.Element:
        """Send nested Markdown into the dialog body rather than its chrome."""
        return self.body

    def on_markdown(self) -> str:
        """Parse the dialog contents as block-level Markdown."""
        return "block"

    @staticmethod
    def _close_button(parent: etree.Element, title: str) -> None:
        button = etree.SubElement(
            parent,
            "button",
            {
                "class": "modal__close",
                "type": "button",
                "data-modal-close": "",
                "aria-label": f"Close {title}",
            },
        )
        _append_icon(button, "lucide/x")


class ModalBlockExtension(BlocksExtension):
    """Register the modal Block with PyMdown's shared Block manager."""

    def extendMarkdownBlocks(self, md, block_mgr) -> None:
        """Register the modal authoring construct."""
        block_mgr.register(ModalBlock, self.getConfigs())


def makeExtension(*args, **kwargs) -> ModalBlockExtension:
    """Return the Markdown extension entry point."""
    return ModalBlockExtension(*args, **kwargs)
