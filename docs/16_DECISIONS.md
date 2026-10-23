# 16_DECISIONS.md

## Purpose

This is QuantumUI's architecture decision record (ADR) log. Each significant technical or product trade-off is recorded here so future contributors and AI agents understand *why* the system is built the way it is, not just *how*.

## Format

Each decision uses this structure:

```
## [DEC-XXX] Short title
Date:
Status: Proposed | Accepted | Superseded by DEC-YYY
Context:
Decision:
Consequences:
```

## Example Entries

### [DEC-001] Simulator-first default execution

Date: Phase 0 planning
Status: Accepted
Context: Beginners need a safe, free, always-available first experience; hardware queues are shared, finite, and can produce noisy or confusing results for newcomers.
Decision: All new experiments default to a local/cloud simulator backend. Hardware execution requires a separate, explicit confirmation step described in `07_UX_SPEC.md`.
Consequences: Slightly more friction for advanced users who want hardware immediately, offset by a safer, more predictable onboarding experience and reduced accidental hardware usage.

### [DEC-002] Provider-neutral adapter interfaces for models and execution backends

Date: Phase 0 planning
Status: Accepted
Context: Locking into a single LLM vendor or a single quantum hardware provider would contradict the openness goal in `01_VISION.md` and create business and technical risk.
Decision: Generation Service and Execution Service are defined by internal adapter interfaces (see `12_AI.md` and `09_BACKEND.md`), with IBM Qiskit Runtime as the first reference execution implementation, not an assumed dependency.
Consequences: Additional interface-design and testing overhead up front, in exchange for long-term flexibility and community-contributed adapters via `11_PLUGINS.md`.

### [DEC-003] Dataset participation is opt-in per experiment, not account-wide

Date: Phase 5 planning
Status: Accepted
Context: A single account-level consent setting risks accidental publication of sensitive or exploratory private experiments.
Decision: Every experiment carries independent sharing flags (Repository, Dataset, Social, Research) as specified in `07_UX_SPEC.md`; none defaults to on, and none implies another.
Consequences: More UI surface and explanation required, in exchange for meaningfully stronger privacy guarantees and user trust.

### [DEC-004] Progressive template rollout strategy

Date: Phase 1 planning
Status: Accepted
Context: Managing development velocity while meeting user onboarding goals across documentation targets (3 core foundational templates vs 5 MVP templates vs 10 v1 library templates).
Decision: Adopt a multi-phase progressive rollout:
- Phase 1 (MVP): Launch with 3 core foundational templates (The Coin Flipper, The Quantum Link, and The Phase Shift) plus 2 intermediate templates (Interference and Phase Flip) to satisfy the MVP standard of 5 templates.
- Phase 2 (Learning Depth): Expand the library to 10 reviewed templates including Deutsch-Jozsa, Superdense Coding, Quantum Teleportation, Grover's Search, and VQE.
Consequences: Allows developers and AI coding agents to focus on solidifying the foundational 3-to-5 templates in Phase 1 before scaling to complex algorithmic layouts.

### [DEC-005] Secret management for multi-tenant vs. local deployments

Date: Phase 1 planning
Status: Accepted
Context: QuantumUI supports both self-hosted local execution and multi-tenant hosted service patterns. Secret handling must remain secure and coherent across both modes.
Decision: Secret management is split by deployment pattern:
- Local/Self-Hosted Mode: Credentials (IBM API tokens, LLM API keys) can be loaded from a local `.env` file into server environment variables or memory.
- Hosted Multi-Tenant Mode: Frontend never handles or stores raw keys in persistent storage. Users enter keys on-demand in the UI; they are transmitted via HTTPS to a server-side session-secrets store. The server returns a short-lived internal credential ID to the frontend to reference for that session.
Consequences: Maintains zero-credential persistence on clients in multi-user settings while keeping local setup friction-free for individual developers and students.

## Maintaining This Log

Add a new entry for any decision that changes a documented default, a public interface, a safety boundary, or a sharing/consent behavior. Superseding an old decision requires updating its status and linking the new entry, never silently deleting history.

