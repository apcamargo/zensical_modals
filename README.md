# Zensical modals

This repository is a boilerplate for modals to a [Zensical](https://zensical.com) website. Modals are created with a `modal()` macro that renders a trigger button plus the `<dialog>` element it opens.

## Getting started

```
{{ modal(label="Open", modal_id="my-modal", title="My modal", body="<p>Hello!</p>") }}
```

- `label` — the trigger button's text.
- `modal_id` — a unique id for the dialog.
- `title` — an optional header; omit it for a headerless modal.
- `body` — the modal content in raw HTML.
- `min_height` / `max_height` — optional CSS length values (e.g. `"20rem"`).
- `transparent` — `True` (default) for a translucent, blurred panel, `False` for an opaque one.
