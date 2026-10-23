# 06_ARCHITECTURE.md

## Architectural Goals

QuantumUI's architecture must keep three properties true simultaneously: beginners get a fast, safe path to a real result; advanced users get full inspection and portability; and no single AI vendor, quantum provider, or notebook platform is structurally required. The system is organized as a set of adapters around a stable core, so providers can be added or removed without redesigning the product.

## System Overview

```
[Web Client] -> [API Gateway] -> [Orchestration Layer]
                                     |-- Generation Service (LLM adapters)
                                     |-- Validation Service (static + lint checks)
                                     |-- Execution Service (simulator/hardware adapters)
                                     |-- Explanation Service
                                     |-- Experiment Store (private by default)
                                     |-- Export Service (Notebook/Colab, GitHub)
                                     |-- Community Service (consent, filtering, dataset)
```

Each service is independently deployable and communicates through well-defined internal contracts, so it can be scaled, replaced, or disabled without breaking the others.

## Core Components

### API Gateway

Handles authentication, rate limiting, request validation, and routing. It is the only public entry point and enforces consent checks before any request reaches community-sharing services.

### Orchestration Layer

Coordinates the experiment lifecycle as a controlled workflow rather than a single large prompt: interpret request, generate candidate code, validate, request execution approval, execute, interpret results, and persist a record. This mirrors the graph-based, tool-calling orchestration pattern used in modern agent frameworks, where a controller node decides the next step and routes to specialized tool nodes rather than letting a model act unconstrained. [web:113][web:115]

### Generation Service

Wraps natural-language-to-Qiskit generation behind a provider-neutral interface (`AI.md` defines this in depth). It supports open-source/self-hosted models and hosted API keys interchangeably and never hardcodes a single vendor.

### Validation Service

Performs static analysis, import/dependency checks, circuit-construction checks, and safety-policy screening (rejecting cryptographic-attack or offensive-security requests) before anything is offered for execution.

### Execution Service

Wraps quantum backends behind a provider-neutral interface. The default path uses local or cloud simulators; hardware execution is a separate, explicitly confirmed path. IBM's Qiskit Runtime primitives model — Sampler and Estimator, executed as jobs, sessions, or batches, on simulators or real backends — is the reference execution pattern this service is designed around. [web:103][web:105]

### Explanation Service

Generates plain-language, intermediate, and technical explanations for a completed run, explicitly labeling simulated versus hardware-derived results and flagging noise or low-shot uncertainty.

### Experiment Store

The system of record for every experiment: prompt, generated/edited code, circuit representation, validation outcome, execution configuration, results, and sharing-status flags (Private/Repository/Dataset/Social). Private is the default state for every new record.

### Export Service

Produces runnable Jupyter notebooks and Colab-compatible notebooks, and manages explicit, reviewed GitHub commits. It never embeds credentials in exported artifacts.

### Community Service

Implements consent capture, secret/PII filtering, moderation queueing, dataset schema versioning, and licensing metadata as defined in `COMMUNITY.md` and `DATA_LICENSE.md`. It is the only service permitted to move a record from private to public state, and only after explicit user consent.

## Data Flow: A Single Experiment

1. User submits a natural-language request or selects a template.
2. Generation Service produces draft Qiskit code and a circuit description.
3. Validation Service checks correctness signals and policy compliance.
4. User reviews/edits code; Orchestration Layer requests execution approval, defaulting to simulator.
5. Execution Service runs the job (simulator by default; hardware only after explicit confirmation) and returns raw results.
6. Explanation Service produces a plain-language interpretation with uncertainty framing.
7. Experiment Store persists the full record as Private.
8. Optionally, the user triggers Export Service (notebook/Colab/GitHub) or Community Service (dataset/social), each requiring its own explicit action.

## Key Architectural Boundaries

- **No implicit escalation:** moving from simulator to hardware, or from private to any public state, always requires a distinct, explicit user action — enforced in the Orchestration Layer, not just the UI.
- **Provider neutrality:** Generation Service and Execution Service are defined by interfaces, not by any single vendor SDK; IBM Qiskit Runtime is the first reference implementation, not an assumed dependency. [web:107]
- **Immutable provenance:** once persisted, an experiment record's generated content and execution metadata are not silently altered; edits create a new versioned entry.
- **Secrets isolation:** API keys and provider credentials are stored in a dedicated secrets layer, accessed only by the service that needs them, and never included in Experiment Store exports.

## Deployment Model

QuantumUI supports two deployment shapes: a hosted multi-user service, and a self-hosted/local instance for individuals, classrooms, or institutions that want full data control. Both shapes share the same core service contracts so features stay consistent regardless of deployment.

## Related Documents

Read `12_AI.md` for the Generation Service's internal design, `09_BACKEND.md` for service-level implementation details, and `10_PIPELINE.md` for how an experiment moves through CI/CD and runtime pipelines.
