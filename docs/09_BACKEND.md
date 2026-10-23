# 09_BACKEND.md

## Scope

This document describes QuantumUI's backend services: their responsibilities, interfaces, data model, and operational rules. It complements `06_ARCHITECTURE.md` (system-level view) and `12_AI.md` (generation logic).

## Service Responsibilities

| Service | Responsibility | Key Interface |
|---|---|---|
| API Gateway | Auth, routing, rate limits, consent gate | REST/GraphQL entry points |
| Generation Service | Natural-language-to-Qiskit drafting | `generate_code`, `explain_result` |
| Validation Service | Static checks, policy screening | `validate_code(draft) -> report` |
| Execution Service | Simulator/hardware job management | `submit_job`, `get_status`, `get_result` |
| Explanation Service | Multi-level result interpretation | `explain(execution_record, level)` |
| Experiment Store | Canonical experiment records | `save`, `get`, `list`, `update_sharing_state` |
| Export Service | Notebook/Colab/GitHub export | `to_notebook`, `commit_to_repo` |
| Community Service | Consent, filtering, dataset release | `set_consent`, `submit_for_review`, `publish_release` |

## Execution Backend Design

The Execution Service wraps quantum backends through a provider-neutral adapter, with the first reference implementation targeting IBM's Qiskit Runtime model. That model exposes two primitives — **Sampler**, for measurement-outcome distributions, and **Estimator**, for expectation values — executable as individual jobs, sessions, or batches, against either simulators or real hardware. [web:103][web:105]

QuantumUI's adapter interface should mirror this shape so other providers can be added without changing calling code:

```
submit_job(circuit, primitive_type, backend_id, shots, mode) -> job_id
get_status(job_id) -> queued | running | complete | failed | cancelled
get_result(job_id) -> raw_result, backend_metadata
```

Default `backend_id` selection must favor local/cloud simulators; hardware `backend_id` values are only reachable after the explicit confirmation flow defined in `06_ARCHITECTURE.md`.

## Circuit Compilation

Before execution, circuits pass through a transpilation step that adapts a logical circuit to a target backend's constraints (qubit connectivity, native gate set, optimization level). Qiskit's pass-manager-based transpiler is the reference approach: a configurable pipeline of passes that can be tuned per backend rather than a single fixed transformation. [web:108][web:109] The Execution Service should expose transpilation settings (optimization level, target backend) as inspectable metadata attached to the run record, not hidden internal state.

## Data Model (Experiment Record)

Core fields persisted for every experiment:

- `experiment_id`, `owner_id`, `created_at`, `updated_at`
- `prompt_text`, `template_id` (nullable)
- `generated_code`, `user_edited_code` (nullable), `code_version_history`
- `circuit_description`, `validation_report`
- `execution_config` (primitive_type, backend_id, shots, mode, transpiler_settings)
- `execution_result` (raw_result, backend_metadata, status, timestamps)
- `explanation_by_level` (beginner, intermediate, technical)
- `sharing_state` (private | repository | dataset | social), each with its own consent timestamp
- `provenance` (software versions, adapter used, schema_version)

## API Surface (Representative)

- `POST /experiments` — create from prompt or template
- `POST /experiments/{id}/generate` — request/regenerate code
- `POST /experiments/{id}/validate`
- `POST /experiments/{id}/execute` — requires explicit backend/mode confirmation for hardware
- `GET /experiments/{id}` / `GET /experiments`
- `POST /experiments/{id}/export/notebook`
- `POST /experiments/{id}/export/github`
- `POST /experiments/{id}/sharing` — sets dataset/social/repository consent flags individually

Full request/response contracts belong in `13_API.md`; this section defines only the backend-relevant surface.

## Operational Rules

- All secrets (provider credentials, API keys) live in a dedicated secrets store, accessed by short-lived, scoped tokens; never persisted in the Experiment Store or logs.
- Hardware submission endpoints require a second confirmation token distinct from the initial request, preventing accidental or replayed submissions.
- Every service emits structured, privacy-safe telemetry (latency, error rates, validation pass rate) without including prompt content or credentials.
- Idempotency keys are required on job-submission endpoints to prevent duplicate hardware runs from retries.

## Related Documents

See `06_ARCHITECTURE.md` for the system-level view, `12_AI.md` for the Generation Service internals, `10_PIPELINE.md` for how code moves through CI/CD, and `13_API.md` for full API contracts.
