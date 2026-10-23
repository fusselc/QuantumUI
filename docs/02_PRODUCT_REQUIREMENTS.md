# 02_PRODUCT_REQUIREMENTS.md

## Product Summary

QuantumUI is an open-source web application that enables users to create, understand, run, save, export, and optionally share quantum-computing experiments. The primary workflow translates a natural-language request into inspectable Qiskit code and a visual circuit, then runs the experiment on a simulator or a user-authorized provider backend.

## Target Users

- **Beginners:** People with no Python, Qiskit, or quantum-computing experience who need templates, guided prompts, safe defaults, and plain-language explanations.
- **Learners and educators:** Users who need reproducible classroom or self-study experiments, notebooks, and shareable demonstrations.
- **Researchers and developers:** Users who need editable Qiskit output, run metadata, provider choice, repository integration, and exportable artifacts.
- **Contributors and evaluators:** People who want to improve or assess the opt-in natural-language-to-Qiskit dataset and models.

## Functional Requirements

### Experiment Creation

- The product must provide curated templates for foundational, non-security quantum experiments.
- The product must accept natural-language experiment requests and offer prompt suggestions suitable for beginners.
- The product must generate Qiskit code, a circuit representation, a plain-language explanation, and a validation status for each request.
- Users must be able to inspect, copy, edit, regenerate, and export generated code before execution.
- The generation layer must support a provider-neutral adapter interface for self-hosted/open models and user-provided hosted-model API keys.

### Execution

- The product must support local or cloud simulation as the default execution route.
- The product must support approved external quantum providers through user-authorized connections, beginning with IBM Quantum/Qiskit Runtime compatibility.
- Hardware execution must require an explicit user confirmation that identifies the selected backend, expected queue/cost information when available, and shots/configuration.
- The product must capture backend name, simulator/hardware status, compiler/runtime version when available, shots, execution time, configuration, output, and errors for every run.
- The product must explain failures in user-friendly language while retaining technical diagnostics for authorized users.

### Learning and Explainability

- The UI must explain each experiment at a beginner, intermediate, or technical level selected by the user.
- It must distinguish generated code from user-edited code and simulation results from hardware results.
- It must communicate uncertainty, noise, and limitations without presenting results as scientific proof.

### Save, Export, and Reproduce

- Users must be able to save an experiment as a structured record containing prompt, code, circuit, explanation, configuration, results, and metadata.
- Users must be able to export a runnable Jupyter notebook and create/open a Google Colab-compatible notebook.
- Users must be able to connect a GitHub repository and commit an experiment only after review and explicit confirmation.
- An exported or committed experiment must include enough metadata for a reasonable attempt at reproduction.

### Community and Publishing

- Dataset inclusion must be disabled by default and require explicit, per-experiment consent.
- Dataset sharing, repository visibility, and social-media sharing must be separate controls.
- Before public release, the product must scan for secrets and unnecessary personally identifying information and hold flagged content for review.
- The product may generate a social-share asset and a research-submission package, but users retain approval and responsibility for every publication.
- The product must never represent an experiment as peer-reviewed, novel, or accepted by arXiv.

## Non-Functional Requirements

- **Privacy and security:** Never log or commit API keys, tokens, model weights, or secrets. Encrypt sensitive credentials at rest where stored and use least-privilege provider authorization.
- **Accessibility:** Meet WCAG 2.2 AA where feasible; support keyboard operation, readable visualizations, clear errors, and non-color-only indicators.
- **Transparency:** Clearly identify the model/provider used, generated content, validation outcome, execution backend, and data-sharing status.
- **Reliability:** Preserve private experiment records and prevent duplicate hardware submissions; use idempotent run requests and clear job states.
- **Portability:** Do not make core workflows dependent on a single LLM vendor, quantum provider, or notebook platform.
- **Observability:** Record privacy-safe operational telemetry and auditable experiment provenance without retaining secrets.

## Safety Constraints

QuantumUI must reject or redirect requests for cryptographic attacks, key breaking, offensive cybersecurity, malware, credential theft, or misuse of shared quantum resources. It must provide an educational, non-actionable explanation where appropriate.

## Release Acceptance Criteria

The first public release is acceptable only when a beginner can create a template experiment, generate inspectable Qiskit, run it on a simulator, receive an understandable explanation, export a runnable notebook, save a reproducible record, and keep it private by default. Provider integrations, hardware runs, GitHub commits, public datasets, social sharing, and publication packages must remain opt-in and must not block the core private simulator workflow.

## Out of Scope for v1

- Building or training a foundation model from scratch
- Guaranteed correctness or scientific novelty of generated experiments
- Automatic submission to arXiv or any journal
- A custom quantum-hardware provider or quantum processor
- Cybersecurity, cryptographic attack, or key-breaking features
