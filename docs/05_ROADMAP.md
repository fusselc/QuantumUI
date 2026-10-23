# 05_ROADMAP.md

## Roadmap Principles

This is an outcome-based roadmap, not a promise of dates. Advance only when the prior phase meets its acceptance criteria, safety reviews, and usability evidence. Keep the private simulator workflow valuable even if hardware, provider, or dataset features are delayed.

## Phase 0 — Foundation

**Outcome:** A maintainable, safe project base exists before feature acceleration.

- Establish repository structure, licenses, governance, `AGENTS.md`, development workflow, security practices, and CI.
- Define experiment record schema, consent model, AI adapter interface, provider adapter interface, and threat model.
- Build a static design system and accessibility baseline.

**Exit criteria:** Documentation is internally consistent; secrets are protected; private experiment schema is versioned; core architecture receives review.

## Phase 1 — Private Simulator Lab (MVP)

**Outcome:** A beginner can complete a trustworthy private simulator experiment.

- Curated templates and guided prompt experience.
- Natural-language-to-Qiskit draft generation through a swappable model adapter.
- Code/circuit display, validation, simulation, results, plain-language explanation, and saved experiment record.
- Editable code, technical diagnostics, and private Jupyter/Colab-compatible export.

**Exit criteria:** A usability test with beginners shows the main v1 flow can be completed in ten minutes or less; every saved run contains required provenance; no hardware, social, or public-dataset feature is required.

## Phase 2 — Trust and Learning Depth

**Outcome:** Users understand and can verify what they ran.

- Multi-level explanations, result comparisons, noise-oriented learning templates, accessible circuit visualizations, and “what changed?” views after edits.
- Evaluation suite for generated Qiskit: syntax, imports, circuit validity, simulator execution, policy compliance, and human quality review samples.
- Improved error recovery and safety redirection.

**Exit criteria:** Explanation and generation-quality metrics meet the initial targets in `03_GOALS.md`; accessibility audit identifies no critical blockers.

## Phase 3 — Connected Workspaces

**Outcome:** Advanced users can take ownership of their work outside QuantumUI.

- Reviewed GitHub repository connection and explicit experiment commits.
- Notebook improvements for Google Colab and standard Jupyter environments.
- User-managed hosted-model API keys and documented self-hosted/open-model connector.

**Exit criteria:** Exports run from a clean environment using documented setup; no credentials are present in generated notebooks or commits.

## Phase 4 — Responsible Hardware Access

**Outcome:** Users can deliberately run suitable experiments on approved provider hardware.

- IBM Quantum/Qiskit Runtime provider adapter, account connection, backend selection, queue/status visibility where available, and explicit execution approval.
- Hardware-aware validation, job lifecycle tracking, cancellation/status handling, usage safeguards, and hardware-vs-simulator comparison.

**Exit criteria:** Hardware jobs are never submitted without confirmation; provider integration passes security review; users can distinguish noisy hardware results from ideal simulation output.

## Phase 5 — Opt-In Community Dataset

**Outcome:** A privacy-conscious, documented public dataset can be released responsibly.

- Consent UI, privacy/secret filtering, review queue, public-record schema, dataset card, `DATA_LICENSE.md` adoption, provenance, versioning, and deletion process.
- Community moderation tooling and research-quality reporting.

**Exit criteria:** Independent review confirms consent, licensing, privacy, and removal processes; first release has documented limitations and reproducible provenance.

## Phase 6 — Sharing and Research Support

**Outcome:** Community work is discoverable without overstating what it means.

- User-approved social sharing assets that show circuit, context, result, and caveats.
- Reproducibility bundles and research-submission drafting support; never automatic arXiv submission.
- Public examples, education partnerships, and model/dataset evaluation reports.

**Exit criteria:** Shared content follows scientific-communication guidelines; users explicitly approve posts; publication language clearly distinguishes a draft package from review or acceptance.

## Deferred Until Evidence Supports It

Multi-provider hardware expansion, collaborative real-time editing, marketplace/plugin ecosystems, fine-tuning initiatives, mobile-native apps, and automated publication integrations are intentionally deferred. Each requires a separate decision record, user demand, safety assessment, and maintainable ownership.
