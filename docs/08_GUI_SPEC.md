# 08_GUI_SPEC.md

## Purpose

This document specifies the visual system and component-level requirements for QuantumUI: layout, components, states, and accessibility rules that implement `07_UX_SPEC.md` and the visual language defined in `04_DESIGN.md`.

## Layout System

- **Grid:** 12-column responsive grid, with a single-column collapse below 768px width.
- **Primary layout regions:** Top navigation bar (product identity, account, help), left context panel (templates/history, collapsible), main experiment canvas (three-part: Ask / Run / Result), and a persistent status strip showing current experiment state.
- **Spacing scale:** 4px base unit; use multiples of 4 for all padding/margin to keep rhythm consistent across components.

## Core Components

### Template Card

Displays template name, one-line description, difficulty tag (Beginner/Intermediate/Advanced), and a "Start" action. Cards must have a visible focus state and a minimum touch target of the full card area.

### Prompt Box

Multi-line text input with inline suggestion chips below it. Suggestion chips are buttons, not plain text, and must be independently focusable and activatable by keyboard.

### Circuit Visualizer

Renders the generated circuit using labeled gates and a distinct visual treatment for measurement operations. Must provide a text-based alternative description (a plain-language list of operations) for screen reader users, since a visual-only circuit diagram is not sufficient on its own.

### Code Panel

Monospaced, syntax-highlighted Qiskit code view with a persistent badge: "AI-generated" or "Edited by you." Includes copy, edit, and regenerate actions, each a clearly labeled button rather than an icon-only control.

### Execution Control Bar

Shows backend selector (Simulator vs. Hardware, visually and structurally separated), shot count input, and the primary run action. Hardware selection triggers the confirmation flow specified in `07_UX_SPEC.md`; this must be a distinct visual step, not a modal that only changes the button label.

### Status Badge

A compact, reusable component showing one of: Draft, Validating, Ready, Running (Simulator), Running (Hardware), Complete, Failed, Cancelled. Each state pairs a color with a distinct icon and text label so state is never conveyed by color alone. [web:120]

### Result Panel

Displays raw output (for example, measurement histogram), the plain-language explanation, and a visible label distinguishing Simulator from Hardware results.

### Sharing Panel

Four independent toggle controls (Repository, Dataset, Social, Research package), each opening its own preview before confirmation, matching Flow 4 in `07_UX_SPEC.md`.

## Design Tokens

- **Color:** Define semantic tokens (e.g., `color-status-success`, `color-status-warning`, `color-status-hardware`) rather than raw hex values in components, so palette or contrast adjustments propagate consistently.
- **Typography:** A single readable sans-serif family for UI text, a monospaced family for code, with a minimum body text size of 16px and scalable line height to support zoom and reflow.
- **Contrast:** All text and meaningful icons must meet at least WCAG AA contrast ratios against their background; focus indicators must meet the WCAG 2.2 Focus Appearance contrast requirement of at least 3:1 between focused and unfocused states. [web:120][web:122]

## Interactive Element Rules

- Minimum interactive target size follows WCAG 2.2 Target Size (Minimum) guidance: at least 24x24 CSS pixels, or sufficient spacing from adjacent targets when a control cannot be made that large. [web:120][web:95]
- Focus indicators must be at least 2px thick and clearly connected to the focused element, per WCAG 2.2 Focus Appearance. [web:120][web:128]
- Any component supporting drag interaction (reordering, resizing) must ship a non-drag equivalent (buttons or a menu action). [web:120]
- No component may trigger its primary action on pointer-down; activation occurs on pointer-up/release only, to prevent accidental hardware submissions or destructive actions. [web:120]

## Responsive Behavior

- Below 768px, the left context panel collapses into a slide-over drawer; the experiment canvas remains single-column and preserves the Ask/Run/Result vertical order.
- Circuit visualizations must remain legible at narrow widths through horizontal scroll with visible scroll affordance, not by shrinking text below 12px.

## States and Motion

- Loading states use a determinate progress indicator when duration is estimable (for example, known queue position) and an indeterminate one otherwise; never use motion alone to convey meaning without an accompanying text label.
- Transitions are limited to 200 to 300ms for UI state changes and must respect reduced-motion user preferences by disabling non-essential animation.

## Related Documents

See `07_UX_SPEC.md` for flows and interaction rules this specification implements, and `04_DESIGN.md` for the underlying visual and content philosophy.
