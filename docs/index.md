# Modals in Zensical

## Writing a modal

A modal has two parts: a PyMdown [BracketSpan](https://facelessuser.github.io/pymdown-extensions/extensions/bracketspan/) trigger in the prose and a `modal` [Block](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/) that defines the dialog.

````md
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

<div class="result" markdown>

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

</div>

The `key` option is required and must be unique among modal Blocks on its page.
Any number of BracketSpan triggers can use the same key. The title after `|` is
also required: it is shown in the dialog header and supplies its accessible name.

- `omit-header: true` hides the visible header while preserving the title as the
  dialog's accessible name.
- `min-height` / `max-height` accept CSS length values such as `20rem`.
- `opaque: true` gives the panel a solid background instead of the default
  translucent, blurred surface.

The Block body is Markdown, so it can contain paragraphs, lists, code blocks,
and raw HTML. A normal triple-backtick code block can appear directly inside a
modal. Use a longer slash fence only when nesting another Block.

## Examples

### Headerless

````md
Open the [headerless modal]{modal="headerless-modal"}.

/// modal | Headerless modal
    key: headerless-modal
    omit-header: true

The title remains available to assistive technology, but no header bar is
shown.
///
````

<div class="result" markdown>

Open the [headerless modal]{modal="headerless-modal"}.

/// modal | Headerless modal
    key: headerless-modal
    omit-header: true

The title remains available to assistive technology, but no header bar is
shown.
///

</div>

### Custom height bounds

````md
Open the [minimum-height modal]{modal="min-height-modal"}.

/// modal | Minimum height
    key: min-height-modal
    min-height: 30rem

`min-height` keeps this dialog tall even when its content is short.
///
````

<div class="result" markdown>

Open the [minimum-height modal]{modal="min-height-modal"}.

/// modal | Minimum height
    key: min-height-modal
    min-height: 30rem

`min-height` keeps this dialog tall even when its content is short.
///

</div>

### Opaque background

````md
Open the [opaque modal]{modal="opaque-modal"}.

/// modal | Opaque modal
    key: opaque-modal
    opaque: true

`opaque` disables the translucent, blurred panel background.
///
````

<div class="result" markdown>

Open the [opaque modal]{modal="opaque-modal"}.

/// modal | Opaque modal
    key: opaque-modal
    opaque: true

`opaque` disables the translucent, blurred panel background.
///

</div>
