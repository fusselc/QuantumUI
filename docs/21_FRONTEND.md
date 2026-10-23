# 21_FRONTEND.md

## Purpose

This document specifies the frontend implementation: stack, structure, state management, API integration, and build/test conventions. It complements `07_UX_SPEC.md` (flows) and `08_GUI_SPEC.md` (visual/component spec) with the concrete engineering approach an AI coding agent or contributor should follow when writing frontend code.

## Stack

- **Framework:** React 18+ with TypeScript in strict mode (no `any`, per `15_CODING_STANDARDS.md`).
- **Build tool:** Vite, for fast local dev and production builds.
- **Styling:** Plain CSS with design tokens (semantic color/spacing variables) as defined in `08_GUI_SPEC.md`. No CSS-in-JS runtime dependency is required for the core app.
- **State management:** Local component state and React context for cross-cutting concerns (current experiment, active sharing state). No global state library is required at MVP scale; if one becomes necessary, document the choice in `16_DECISIONS.md` before adopting it.
- **Testing:** Vitest for unit/component tests, plus accessibility assertions (axe-core or equivalent) for every new interactive component, per `14_TESTING.md`.

## Directory Structure

```
frontend/
  src/
    api/            Typed client functions for each backend endpoint (one module per resource)
    components/      Reusable UI building blocks (TemplateCard, PromptBox, CircuitVisualizer,
                      CodePanel, ExecutionControlBar, StatusBadge, ResultPanel, SharingPanel)
    types/           Shared TypeScript types mirroring backend schemas (`app/models/schemas.py`)
    styles/          Design tokens and global styles
    main.tsx         App entry point and top-level layout
  public/            Static assets
  index.html
  vite.config.ts
  tsconfig.json
  package.json
```

As the app grows beyond the MVP single-file prototype, split `main.tsx` into the `components/` modules listed above — each component maps directly to a section in `08_GUI_SPEC.md` and should be independently testable.

## API Integration Rules

- All requests go through a single typed client layer (`src/api/`), never `fetch` calls scattered through components. Each function corresponds to one endpoint in `13_API.md`.
- Requests that could trigger hardware execution must include an `Idempotency-Key` header, generated client-side per request attempt, matching the backend contract in `09_BACKEND.md`.
- API errors follow the RFC 9457 Problem Details shape; the client must surface `title`/`detail` in plain language and keep `type`/`instance` available for a technical detail toggle, per the error UX rules in `07_UX_SPEC.md`.
- Never store provider credentials or API keys in frontend state, local storage, or query parameters. Credentials are entered once and handled entirely server-side per `20_SECURITY.md`.

## Component Contracts

- Every component listed in `08_GUI_SPEC.md` must accept props sufficient to render all documented states (Draft, Validating, Ready, Running Simulator, Running Hardware, Complete, Failed, Cancelled) without component-internal fetches — data flows down from the experiment-level container.
- Status must never be conveyed by color alone: every `StatusBadge` state pairs a color token with a distinct icon and text label.
- Primary and destructive actions (especially hardware execution, sharing confirmations) trigger on pointer-up/click release, never on pointer-down, per `07_UX_SPEC.md` and `08_GUI_SPEC.md`.

## Accessibility Requirements (enforced in code, not just design)

- All interactive elements must be reachable and operable via keyboard alone with a visible focus indicator (minimum 2px, 3:1 contrast against adjacent states), per WCAG 2.2 Focus Appearance.
- Minimum interactive target size is 24x24 CSS pixels, or equivalent spacing from neighboring targets.
- The Circuit Visualizer must ship a text-based list-of-operations alternative alongside any graphical rendering.
- Respect `prefers-reduced-motion`; no animation may be the sole carrier of state-change information.
- Run automated accessibility checks in CI for every new or modified component, per `14_TESTING.md`.

## Environment Configuration

Frontend configuration lives in `frontend/.env` (copied from `frontend/.env.example`), currently exposing only `VITE_API_URL`. Never add a frontend environment variable that holds a secret — secrets belong exclusively in the backend secrets layer per `09_BACKEND.md` and `20_SECURITY.md`.

## Build, Lint, and Test

```bash
npm install
npm run dev      # local development server
npm run build    # type-checks then produces a production build
npm run test     # Vitest unit/component/accessibility tests
npm run lint      # ESLint, strict TypeScript, zero warnings allowed
```

CI (`.github/workflows/ci.yml`) runs `npm run build` on every push; lint and test scripts should be added to the same job as the frontend matures.

## Related Documents

See `07_UX_SPEC.md` for interaction flows, `08_GUI_SPEC.md` for the visual/component specification, `13_API.md` for the endpoints this layer calls, and `15_CODING_STANDARDS.md` for TypeScript conventions.
