# Design notes (v2)

Skills used: `frontend-design`, `ui-ux-pro-max` (product search: banking/finance, ux search: accessibility), `cybersecurity-analyst`.

## Direction

"Ledger and signal": a dense, calm operations board for project managers who scan many cards quickly.
Swiss-style structure (hairlines, strong alignment, tabular numbers) on navy, trust blue and a single gold accent
(the primary action and focus ring on dark surfaces). Blue palette is required by the original brief.

## What changed from v1

- Stat tiles replaced by one progress band: percent complete, a stacked status bar and a text legend. Overdue count is a text flag.
- Lanes carry a status glyph (dashed circle, half circle, slashed circle, check), so status is never colour-only.
- Priority is a 4-bar level icon plus the word. Due state is a text chip: "Overdue 2d", "Due today", "Due in 3d".
- Emoji icons replaced by inline SVG. Avatars show initials.
- Dark theme (follows the OS, toggle in header, not persisted). Reduced-motion and 44px touch targets on coarse pointers.
- Added: text search, filter-aware result count and empty state, screen-reader announcements for moves/adds/deletes.
- Layout: 1 column below 720px, 2 columns to 1099px, 4 columns above. No page-level horizontal scroll.

## Tokens

Light: canvas `#edf1f7`, surface `#fff`, ink `#0d1b2e`, blue `#1553b0`, gold `#f0b429`, navy `#0a1628`.
Dark: canvas `#070f1d`, surface `#101c30`, ink `#e8eef8`, blue `#6ea3ff`, focus `#ffcf4d`.
Type: system stacks only. Display = Avenir Next / Segoe UI Variable, body = system-ui, IDs = ui-monospace.
Radius: 6px cards, 10px lanes, pill chips. Motion: 150-220ms ease-out, only in response to an action.

## Constraints kept from v1

Vanilla single file, no CDN/fonts/images, works from `file://`, no persistence, no `!important`, FormSubmit failure never breaks the board.
