# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file Kanban board for a fictitious bank's internal IT PMO (demo/training tool). The whole app is [index.html](index.html): markup, one `<style>` block, one `<script>` block. There is no build, lint, or test tooling; run it by opening the file in a browser (double-click, or `open index.html`).

## Hard constraints (from the original brief)

- Vanilla HTML/CSS/JS only: no frameworks, bundler, npm, CDN scripts, web fonts, or image files. System font stack, inline SVG/Unicode for icons.
- Must work from `file://` with no server.
- No persistence of any kind (no localStorage/sessionStorage/IndexedDB/cookies). A refresh intentionally resets to seed data, and the UI says so.
- Only backend is FormSubmit's AJAX endpoint (`notifyNewTask()`); a failure there must never break the board.
- No real bank logo/trademarks; neutral "IT PMO" wordmark and blue palette. No `!important`.
- Colour must never be the only signal (priority pills carry text; overdue is a text badge).

## Architecture

State-driven, re-render everything:

- `state = { tasks, filters, ui }` is the single source of truth. `state.ui` holds transient UI state (which card is confirming delete, which has its Move menu open, current drag id, and `focusKey` for restoring focus after re-render).
- Actions (`addTask`, `moveTask`, `deleteTask`, filter handlers) mutate `state` then call `renderBoard()`. `renderBoard()` rebuilds all columns via `renderCard()` as an HTML string and also calls `renderSummary()`. Do not mutate card DOM directly elsewhere.
- Every user-supplied string must go through `escapeHtml()` before entering `innerHTML`. Toasts use `textContent`.
- Because the board is rebuilt on each render, interactions are handled by event delegation on `#board` (`data-action` attributes for buttons; dragstart/dragover/drop for native HTML5 DnD). Keyboard focus is restored after render by matching `data-focus` against `state.ui.focusKey` — set `focusKey` before calling `renderBoard()` whenever a focused control will be replaced.
- Delete confirmation and the "Move ▸" keyboard fallback are inline card states (`state.ui`), not `confirm()` or popups.
- Overdue = `dueDate < today` (local-time ISO string comparison via `isoDate()`) and status ≠ Done. Seed due dates are relative to today so overdue examples always exist.
- Task IDs (prefix `ITPM-`): `TASK_ID_PREFIX` + zero-padded `nextTaskNumber` counter; seeding consumes 0001–0008.
- Add-task flow (`handleSubmit`): validate → optimistic `addTask` → reset/close dialog → toast → `notifyNewTask` in try/catch/finally (warning toast on failure, submit button re-enabled in `finally`).

## v2 additions

- A meta Content-Security-Policy allows the inline script/style by SHA-256 hash. After ANY edit to the `<style>` or `<script>` block run `python3 scripts/update-csp.py` (CI runs it with `--check`). Do not add inline `style=` attributes or inline event handlers; set dynamic styles via `el.style.*` in JS.
- Light/dark theme via `data-theme` on `<html>` and CSS tokens; never persisted.
- Design rationale is in DESIGN.md, security findings in SECURITY.md.
- This repo is the v2 redesign; v1 lives in the separate `it-pmo-board` repo and must not be changed from here.

## Configuration

`FORMSUBMIT_ENDPOINT` at the top of the script holds the notification email address (placeholder `YOUR_EMAIL@example.com`). FormSubmit needs a one-time activation: the first submission triggers a confirmation email, and delivery starts only after its link is clicked. Reference lists (`STATUSES`, `PROJECTS`, `CATEGORIES`, `PRIORITIES`) sit just below and drive both the form selects and the filters.
