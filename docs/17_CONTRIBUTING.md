# 17_CONTRIBUTING.md

## Welcome

Thank you for considering a contribution to QuantumUI. This project welcomes contributions from people at every experience level, from first-time open-source contributors to quantum-computing researchers. Please read `CODE_OF_CONDUCT.md` before participating.

## Ways to Contribute

- Report bugs or usability issues with clear reproduction steps.
- Suggest or build new experiment templates.
- Improve accessibility, explanations, or beginner-facing content.
- Contribute a model adapter or execution adapter plugin (see `11_PLUGINS.md`).
- Improve documentation in `/docs`.
- Review pull requests and help triage issues.

## Before You Start

- Check open issues to avoid duplicate work.
- For significant changes (new services, new safety-relevant behavior, new public API), open an issue or discussion first so the design can be reviewed against `06_ARCHITECTURE.md` and `02_PRODUCT_REQUIREMENTS.md` before implementation begins.
- Read `AGENTS.md` if you are an AI coding agent contributing to this repository.

## Development Setup

Follow `INSTALL.md` for environment setup. Run the test suite described in `14_TESTING.md` locally before opening a pull request.

## Pull Request Process

1. Fork or branch according to the workflow in `19_DEVELOPMENT_WORKFLOW.md`.
2. Make focused, well-described commits following `15_CODING_STANDARDS.md`.
3. Update relevant `/docs` files and add a `16_DECISIONS.md` entry for significant trade-offs.
4. Add or update tests per `14_TESTING.md`; all CI checks must pass.
5. Open a pull request describing the change, its motivation, and any user-facing or safety impact.
6. Address review feedback; safety-relevant services require sign-off from a maintainer with review authority over that area.

## Contribution Boundaries

Contributions must not introduce cryptographic-attack, key-breaking, or offensive-security capability, must not bypass consent or sharing safeguards, and must not weaken accessibility requirements defined in `07_UX_SPEC.md` and `08_GUI_SPEC.md`.

## Recognition

Contributors are credited in release notes and, where applicable, in `18_CHANGELOG.md`. Substantial or ongoing contributors may be invited into a maintainer role following project governance norms established as the community grows.

## Getting Help

Open a discussion thread or issue for questions. For security concerns specifically, follow the private disclosure process in `20_SECURITY.md` rather than opening a public issue.
