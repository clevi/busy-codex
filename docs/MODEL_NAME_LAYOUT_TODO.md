# Full model names in the weekly dashboard — deferred

Requested behavior: show complete identities such as `6.1 Terra` and `6.0 Astra`.
This branch records the investigation and makes no display behavior changes.

## Findings

- `daemon.status_snapshot()` shortens the model and effort together before
  passing the label to the renderer, losing the original model name.
- `daemon.info_elements()` fits that already-shortened label a second time.
- `LABEL_MAX_PX` is 45 pixels: the upper bar starts at x=50. Estimated width
  of `6.1 Terra high` is 54 pixels, so the model loses characters to preserve
  the effort word. Avatar style and host tags reduce available space further.
- `adapters.codex_status.prettify_model()` retains `6` as `6`; it does not
  normalize a major-only model ID to the requested `6.0` display version.

## TODO before implementation

- Preserve raw model ID and complete display name through report/status data;
  shorten only at the final layout boundary.
- Decide how full names coexist with effort, host tags, and the upper bar:
  dedicated name row, rotation/scrolling, or a revised layout. Keep both bars'
  existing meanings unless the user requests otherwise.
- Normalize recognized major-only GPT versions for display (`6` -> `6.0`),
  preserving provider/custom identifiers and distinguishing suffixes.
- Keep the 72x16 boundary, minimum readable font, and existing model colors.
- Test `6.1 Terra`, `6.1 Sol`, `6.0 Astra`, long/custom IDs, every effort,
  minimal/avatar styles and host tags. Inspect native screenshots before shipping.

No implementation is intended in this branch; revisit the layout with the user.
