# AGENTS.md

## Who You Are Working For
You are building **QuantumUI** — an open-source, no-code interface where users who don't know Qiskit, Python, or quantum mechanics can design, execute, and understand real quantum computing experiments.

**This is strictly an educational science tool. It contains zero offensive or defensive cybersecurity features and must never generate cryptographic attack tools.**

---

## Core Product Capabilities
1. **Interactive Web GUI:** Ready-made templates, natural-language prompt box, suggestion chips, and live circuit viewer.
2. **NL-to-Qiskit Translation:** Converts user prompts to valid Qiskit code using swappable model adapters (offline generator or user-provided API key).
3. **Simulator-First Execution:** Executes on local Qiskit Aer simulators by default. Real hardware execution requires explicit user confirmation.
4. **Automated Documentation:** Auto-documents hypotheses, circuits, execution telemetry, and 3-level explanations.
5. **Notebook Export:** Generates clean Jupyter notebooks (`.ipynb`) and one-click Google Colab launch links.
6. **Opt-In Community Dataset:** Explicit per-experiment consent controls for repository, dataset, and social sharing.

---

## Non-Negotiable Rules

### ALWAYS DO:
- Write natural-language-to-Qiskit generation that fails safely and explains errors in plain English.
- Treat API keys and credentials as sensitive; never log or commit them.
- Enforce AST static validation before code execution.
- Maintain immutable version history for code edits.
- Pair all visual circuit renderings with text-based operational descriptions for screen readers (WCAG 2.2 AA).
- Default all new experiments to local simulators.

### NEVER DO:
- NEVER generate code for Shor's algorithm RSA cracking, key exfiltration, or cryptographic attacks.
- NEVER execute jobs on real hardware without explicit user confirmation.
- NEVER publish or share an experiment without per-experiment opt-in consent.
- NEVER store secrets in frontend state or localStorage.

---

## Where to Read Next
- Architecture: `docs/06_ARCHITECTURE.md`
- Backend & Schemas: `docs/09_BACKEND.md`
- AI Model Adapters: `docs/12_AI.md`
- Frontend Specs: `docs/21_FRONTEND.md` & `docs/08_GUI_SPEC.md`
- ADR Decisions: `docs/16_DECISIONS.md`
