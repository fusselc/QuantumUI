# 10_PIPELINE.md

## Scope

This document covers two related pipelines: the **software delivery pipeline** (CI/CD for QuantumUI itself) and the **experiment execution pipeline** (how a single user request flows from prompt to saved record). Both must be reliable, auditable, and safe by default.

## Software Delivery Pipeline

### Stages

1. **Commit and lint** — style, type checks, and static analysis run on every push (see `14_CODING_STANDARDS.md`).
2. **Unit and integration tests** — cover Generation, Validation, Execution, Explanation, and Experiment Store logic in isolation and together (see `13_TESTING.md`).
3. **Security and secret scanning** — every pull request scans for committed credentials, vulnerable dependencies, and policy violations before merge.
4. **Preview deployment** — a scoped, non-production environment for manual and automated review.
5. **Staged rollout** — production deploys progress through canary and full-traffic stages with automatic rollback on error-rate or latency regressions.
6. **Post-deploy verification** — smoke tests confirm the private simulator workflow (the core acceptance path from `02_PRODUCT_REQUIREMENTS.md`) still functions end-to-end.

### Rules

- No deployment proceeds if secret scanning or the core smoke test fails.
- Any change touching the Generation Service, Validation Service, or Community Service policy logic requires an additional manual safety review before merge.
- Dataset release pipelines (see below) are entirely separate from the application deployment pipeline and never share the same approval gate.

## Experiment Execution Pipeline

This is the runtime pipeline a single experiment moves through, corresponding to the data flow in `06_ARCHITECTURE.md`:

```
Prompt/Template
   -> Intent Parsing (12_AI.md)
   -> Code + Circuit Generation
   -> Static Validation + Policy Screening
   -> User Review / Edit
   -> Execution Approval (simulator default; hardware requires explicit confirmation)
   -> Transpilation (target-backend adaptation)
   -> Job Submission (job / session / batch, per 09_BACKEND.md)
   -> Result Retrieval
   -> Explanation Generation
   -> Experiment Record Saved (Private by default)
   -> Optional Export / Sharing Pipelines
```

Qiskit Runtime's own execution model supports running primitives as individual jobs, within a session, or as a batch, which the Execution Service should expose as selectable modes rather than a single hardcoded submission style. [web:105]

## Optional Downstream Pipelines

### Export Pipeline

Converts a saved experiment into a runnable Jupyter notebook or a Colab-compatible notebook, and optionally commits it to a user-authorized GitHub repository. This pipeline never has access to provider secrets beyond a short-lived, scoped export token, and never embeds credentials in generated artifacts.

### Community Dataset Pipeline

A separate, opt-in pipeline defined jointly with `COMMUNITY.md` and `DATA_LICENSE.md`:

1. User sets per-experiment dataset consent.
2. Automated secret and PII filtering.
3. Moderation queue review at appropriate scale.
4. Schema validation against the current dataset version.
5. Versioned release with dataset card, license, and provenance metadata.

This pipeline runs on its own schedule, independent of software deployment, and requires a distinct sign-off before any public release.

### Social Sharing Pipeline

Generates a proposed shareable asset (circuit image, plain-language summary, caveats) for a specific experiment, but always stops at a user-approval step before anything is posted publicly. No automated posting occurs without that explicit action.

## Monitoring and Alerting

Track, per pipeline stage: latency, failure rate, validation pass rate, hardware-confirmation abandonment rate, and dataset-consent opt-in rate. Alert on any spike in policy-violation flags from the Validation Service or Community Service, since this may indicate a prompt-injection attempt or a gap in safety screening.

## Related Documents

See `06_ARCHITECTURE.md` for system structure, `09_BACKEND.md` for service contracts, `13_TESTING.md` for test strategy across these pipelines, and `20_SECURITY.md` for the threat model informing pipeline gates.
