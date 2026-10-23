# 03_GOALS.md

## Product Goal

Make a first real quantum-computing experiment understandable, safe, and achievable in under ten minutes for a person with no programming background — while preserving a clear path to inspectable Qiskit code and reproducible advanced work.

## North-Star Outcome

A user describes an experiment in plain English, reviews a transparent generated circuit, runs it on a simulator, understands the result in plain language, and saves or exports a reproducible record without needing to write Python.

## v1 Goals

### Accessible Creation

- Provide at least 10 reviewed templates covering superposition, measurement, entanglement, interference, noise, and introductory algorithms.
- Let users generate, inspect, edit, copy, and regenerate Qiskit code from a natural-language request.
- Offer beginner, intermediate, and technical explanation modes for every completed experiment.
- Meet WCAG 2.2 AA where feasible, including keyboard-operable controls and non-color-only status cues.

### Safe, Useful Execution

- Make simulation the default; a user must explicitly approve every hardware submission.
- Record reproducibility metadata for 100% of completed runs: prompt version, code, circuit, backend, run configuration, result, timestamps, and software versions where available.
- Clearly distinguish simulator from hardware output and explain that hardware noise and changing calibration affect outcomes.
- Support IBM Quantum-compatible execution as the first external provider integration, without designing the core system around one vendor.

### Portable Learning

- Export every saved experiment as a runnable Jupyter notebook and offer a Google Colab-compatible route.
- Let a user save experiments privately without creating a public repository, dataset record, or social-media post.
- Allow reviewed, explicit GitHub commits for users who connect a repository.

### Responsible Community Value

- Make dataset participation opt-in per experiment; target zero accidental public releases.
- Publish a versioned, documented public dataset only after consent, secret/PII filtering, quality controls, and legal review are in place.
- Produce shareable visual explainers that accurately communicate what a circuit did and did not demonstrate.

## Success Metrics

Measure these after privacy review and with no secrets or unnecessary personal data in analytics:

- **First-run success:** at least 70% of new users complete a simulator experiment in their first session.
- **Time to first run:** median of 10 minutes or less from onboarding to a completed simulator result.
- **Understanding:** at least 70% of surveyed first-time users correctly answer a simple question about their own result after reading its explanation.
- **Generation quality:** track compilation/validation pass rate, successful execution rate, user edits before running, and user ratings by template category.
- **Reproducibility:** at least 95% of saved experiments contain all required provenance fields; aim for 100%.
- **Safety:** zero confirmed credential disclosures, zero unconsented dataset releases, and zero unapproved hardware submissions.
- **Community health:** track resolved moderation reports, contributor retention, accessible-content coverage, and voluntary public experiment contributions.

Targets are hypotheses, not claims of current performance; update them through `16_DECISIONS.md` as evidence accumulates.

## Non-Goals

QuantumUI will not promise quantum advantage, scientific novelty, flawless AI output, peer review, or automatic research publication. It will not build cryptographic attacks, key-breaking utilities, offensive cybersecurity features, custom quantum hardware, or a proprietary foundation model from scratch.
