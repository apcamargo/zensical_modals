# Zensical modals

This repository shows how to create Markdown-authored modal dialogs in a
[Zensical](https://zensical.com) site with a custom
[PyMdown Block](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/).

Install the project with uv so Zensical can import the Block extension, then build normally:

```shell
uv sync
uv run zensical build
```

Write the clickable text naturally in the surrounding prose, and associate it
with a modal-only key:

````markdown
This [modal]{modal="my-modal"} uses default parameters and shows a title and
a Markdown body.

/// modal | My modal
    key: my-modal

The dialog body supports the same Markdown syntax used in the surrounding content,
such as **bold** and *italicized* text, inline `code`, lists, and tables.

- Multiple paragraphs
- Tables
- Highlighted code blocks

| Content     | Supported |
|-------------|-----------|
| Lists       | Yes       |
| Tables      | Yes       |
| Code blocks | Yes       |

```python
print("This is highlighted inside the modal.")
```
///
````

The `key` and title are required. The title follows `|` in the opening fence;
options are YAML immediately below it. Keys do not create HTML IDs, so they
cannot collide with heading anchors. Add `omit-header: true` for a headerless
modal, use `min-height: 20rem` or `max-height: 40rem` for size bounds, and add
`opaque: true` for a solid panel. See the documentation page for complete
examples.
