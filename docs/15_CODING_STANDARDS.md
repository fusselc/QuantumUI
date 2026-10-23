# 15_CODING_STANDARDS.md

## Purpose

Consistent, reviewable code keeps QuantumUI maintainable for both human contributors and AI coding agents working from `AGENTS.md`. These standards are enforced automatically wherever possible.

## General Principles

- Prefer clarity over cleverness; a reviewer or AI agent should understand intent without external context.
- Keep functions small and single-purpose; extract logic rather than nesting deeply.
- Document the *why* behind non-obvious decisions in code comments; the *how* should be evident from the code itself.
- Treat compiler/linter warnings as errors in CI.

## Language-Specific Conventions

### Python (backend, generation, validation, execution services)

- Follow PEP 8 formatting, enforced via an automated formatter and linter in CI.
- Use type hints on all public function signatures; enforce with static type checking in CI.
- Structure Qiskit-related code so circuit construction, transpilation, and execution are clearly separated functions, matching the pipeline stages in `10_PIPELINE.md`.

### TypeScript/JavaScript (frontend)

- Strict TypeScript mode enabled project-wide; reject `any` types in new code.
- Components follow a consistent state-management pattern documented in the frontend README; no ad hoc global state.
- All new UI components must have accompanying accessibility tests per `14_TESTING.md`.

## API and Data Conventions

- Follow the resource naming, versioning, and error-format conventions defined in `13_API.md` for any new endpoint.
- Never introduce a breaking API change without a version bump and an entry in `18_CHANGELOG.md`.

## Security-Sensitive Code

- Any code touching credentials, secrets, or provider authentication must go through the review process defined in `20_SECURITY.md`, regardless of file size.
- Never log full prompts, generated code, or credentials at a verbosity level enabled in production by default.

## Commit and PR Standards

- Commit messages describe what changed and why, not just what file changed.
- Pull requests referencing safety-relevant services (Generation, Validation, Community) require an explicit reviewer sign-off beyond standard code review, per `19_DEVELOPMENT_WORKFLOW.md`.

## Documentation-as-Code

- Any change to a documented behavior (API contract, sharing flow, execution default) must update the relevant `/docs` file in the same pull request.
- Significant architectural or product trade-offs must be recorded as a new entry in `16_DECISIONS.md`, not only described in a PR description.

## Related Documents

See `19_DEVELOPMENT_WORKFLOW.md` for how these standards are enforced during review, and `14_TESTING.md` for the automated checks that accompany them.
