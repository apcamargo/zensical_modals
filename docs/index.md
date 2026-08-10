# Modals in Zensical

## Writing a modal

A modal is created with the `modal()` macro (defined in `docs/scripts/docs_macros.py`). It renders a trigger `<button>` plus the `<dialog>` element it opens:

{% raw %}```
{{ modal(
    label="Example modal",
    modal_id="example-modal",
    title=None,
    body="<p>Any HTML string.</p>",
    min_height=None,
    max_height=None,
) }}
```{% endraw %}

- `label`: the trigger button's label.
- `modal_id`: the `<dialog>` element's `id`. Must be unique per page.
- `title`: the modal's header. Leave it as `None` (the default) for a headerless modal.
- `body`: the modal's content in raw HTML.
- `min_height` / `max_height`: CSS length values (e.g. `"20rem"`) that override the modal's default height bounds.
- `transparent`: defaults to `True`, giving the panel a translucent, blurred background. Set it to `False` for an opaque panel.

## Examples

### Default

{{ modal(body="<p>Modal with default parameters.</p><pre><code>{{ modal() }}</code></pre>") }}

### With a header

{{ modal(label="Modal with a header", modal_id="header-modal", title="Modal with a header", body="<p>Passing <code>title</code> gives the modal a header bar with that title and a close button, instead of the default headerless layout.</p><pre><code>{{ modal(label=&quot;Modal with a header&quot;, modal_id=&quot;header-modal&quot;, title=&quot;Modal with a header&quot;) }}</code></pre>") }}

### Custom height bounds

{{ modal(label="Minimum height", modal_id="min-height-modal", title="Minimum height", min_height="30rem", body="<p><code>min_height</code> sets a floor on the modal&#x27;s height, so it stays tall even when its content is short.</p><pre><code>{{ modal(label=&quot;Minimum height&quot;, modal_id=&quot;min-height-modal&quot;, title=&quot;Minimum height&quot;, min_height=&quot;30rem&quot;) }}</code></pre>") }}

### Opaque background

{{ modal(label="Opaque modal", modal_id="opaque-modal", title="Opaque modal", transparent=False, body="<p>Setting <code>transparent</code> to <code>False</code> gives the panel a solid background instead of the default translucent, blurred one.</p><pre><code>{{ modal(label=&quot;Opaque modal&quot;, modal_id=&quot;opaque-modal&quot;, title=&quot;Opaque modal&quot;, transparent=False) }}</code></pre>") }}
