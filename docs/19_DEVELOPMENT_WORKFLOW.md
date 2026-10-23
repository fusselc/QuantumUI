# 19_DEVELOPMENT_WORKFLOW.md

## Branching Model

- `main` is always deployable and reflects the latest released or release-candidate state.
- Feature work happens on short-lived branches named `feature/<short-description>`, `fix/<short-description>`, or `docs/<short-description>`.
- No direct commits to `main`; all changes land through reviewed pull requests.

## Pull Request Requirements

- At least one maintainer approval for standard changes.
- An additional sign-off from a designated safety reviewer for changes touching Generation Service, Validation Service, Execution Service, or Community Service logic, per `15_CODING_STANDARDS.md`.
- All CI checks green: lint, type check, unit tests, integration tests, safety/policy tests, and accessibility checks per `14_TESTING.md`.
- Relevant `/docs` files updated in the same PR as the behavior they describe.

## Issue Triage

Incoming issues are labeled by area (frontend, backend, generation, execution, docs, accessibility, security) and severity. Security-relevant reports are redirected to the private process in `20_SECURITY.md` rather than triaged publicly.

## Release Cadence

QuantumUI ships on a regular minor-release cadence once past Phase 1 in `05_ROADMAP.md`, with patch releases issued as needed for urgent fixes. See `RELEASE_PROCESS.md` for the release checklist.

## Code Review Focus Areas

Reviewers check for: correctness against `02_PRODUCT_REQUIREMENTS.md`, adherence to `15_CODING_STANDARDS.md`, test coverage per `14_TESTING.md`, accessibility per `07_UX_SPEC.md`/`08_GUI_SPEC.md`, and whether any consent, sharing, or execution-default behavior changed without a corresponding `16_DECISIONS.md` entry.

## Working with AI Coding Agents

AI agents contributing to this repository should read `00_PROJECT.md` and `AGENTS.md` first, then follow the same PR process as human contributors, including safety sign-off requirements for sensitive services. Agents must never bypass the consent, sharing, or hardware-confirmation flows to "simplify" implementation.

## Related Documents

See `17_CONTRIBUTING.md` for the external contributor process this workflow supports, and `10_PIPELINE.md` for how CI/CD enforces these gates automatically.
