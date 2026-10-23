# IMPLEMENTATION_PLAN.md

## QuantumUI Phase 1 Implementation & Coding Agent Handover Plan

### Objective
Provide an end-to-end, fully functional Phase 1 MVP of QuantumUI: an open-source, no-code web gateway that translates natural-language prompts into verified Qiskit circuits, executes them on local Aer simulators, provides multi-level plain-language explanations, and manages private experiment records with Jupyter/Colab exports.

---

### File Structure & Deliverables

#### 1. Backend Engine (`/backend`)
- `app/main.py`: FastAPI server configuration with CORS and RFC 9457 error handlers.
- `app/models/schemas.py`: Pydantic v1 & v2 compatible schemas for templates, experiments, validation reports, and execution results.
- `app/api/router.py`: REST endpoints for `/v1/templates`, `/v1/experiments`, `/v1/providers`.
- `app/services/validation.py`: AST static validation, import restrictions, and blocked crypto-attack screening.
- `app/services/generation.py`: Swappable ModelAdapter interface (Offline template matcher & Hosted LLM adapter).
- `app/services/execution.py`: Quantum execution engine with local Aer simulation, matrix fallback, transpilation, and telemetry.
- `app/services/explanation.py`: Beginner, Intermediate, and Technical explanation generators with uncertainty flags.
- `app/services/store.py`: File-backed atomic experiment store with version history.
- `app/services/export.py`: Jupyter notebook (`.ipynb`) and Google Colab launch URL generator.
- `app/services/templates.py`: 5 curated Phase 1 MVP templates.

#### 2. Frontend Application (`/frontend`)
- `src/main.tsx` & `src/App.tsx`: App root with responsive 12-column cyber-minimalist layout.
- `src/api/client.ts`: Typed API client with Idempotency-Key support.
- `src/types/index.ts`: Shared TypeScript interfaces.
- `src/styles/tokens.css` & `src/styles/index.css`: WCAG 2.2 AA compliant design tokens.
- `src/components/`:
  - `StatusBadge.tsx`: Visual and text indicators for all 8 experiment states.
  - `PromptBox.tsx`: Multi-line prompt input with keyboard-navigable suggestion chips.
  - `TemplateCard.tsx`: Grid of curated beginner-to-advanced templates.
  - `CircuitVisualizer.tsx`: Visual circuit representation with accessible text-alternative table.
  - `CodePanel.tsx`: Live code editor with AI vs User provenance badges.
  - `ExecutionControlBar.tsx`: Simulator vs Hardware selector with explicit hardware confirmation modal.
  - `ResultPanel.tsx`: Histogram chart and 3-level explanation tabs.
  - `SharingPanel.tsx`: 4 independent opt-in sharing toggles with preview modal.

#### 3. Automated Test Suite (`/tests`)
- `test_validation.py`: AST syntax, disallowed imports, and crypto threat screening.
- `test_execution.py`: Quantum simulation, shot counts, and statevector telemetry.
- `test_generation.py`: Swappable adapter translation and template matching.
- `test_api.py`: FastAPI TestClient integration testing for all REST endpoints.
- `test_store_and_export.py`: File storage and notebook generation.

---

### Handover Instructions for Coding Agents (Antigravity / Cursor / Claude Code)
1. **Examine Architecture**: Read `docs/06_ARCHITECTURE.md`, `docs/09_BACKEND.md`, and `docs/12_AI.md`.
2. **Explore ADRs**: Verify accepted trade-offs in `docs/16_DECISIONS.md` (e.g. DEC-001 simulator-first, DEC-004 template roadmap, DEC-005 secrets bifurcated model).
3. **Run Tests**: Execute `pytest` from the repository root.
4. **Stay on the private simulator**: Do not add hardware providers, hosted-model calls, dataset publishing, or social sharing until a later plan explicitly opens that work. Unknown prompts must fail in plain English instead of silently returning another template.

---

## 6. Master Prompt Directive for Google Antigravity, Cursor, and Claude Code

Copy and paste the following prompt into your AI Coding Agent to continue development:

```markdown
Task: Keep QuantumUI a trustworthy private simulator lab

Context: Read `AGENTS.md`, `docs/00_PROJECT.md`, `docs/06_ARCHITECTURE.md`, `docs/09_BACKEND.md`, `docs/12_AI.md`, `docs/16_DECISIONS.md`, and `docs/21_FRONTEND.md`.

Non-Negotiable Directives:
1. Strictly Educational Science Tool: Zero offensive or defensive cybersecurity features. Under no circumstances may the application generate code for Shor's algorithm RSA cracking, key exfiltration, or cryptographic attacks.
2. Simulator only in this version: Every run uses local Qiskit Aer. Do not add IBM Quantum Runtime, hardware confirmation flows, or provider tokens.
3. Secret Isolation: Never log, commit, or expose API keys/secrets to frontend state or localStorage (DEC-005).
4. Accessibility & Provenance: Visual circuits must always be paired with screen-reader text alternatives (WCAG 2.2 AA). Code must track AI vs. User provenance.
5. Fail closed: If a prompt does not match a known template, explain that in plain English and do not save a different circuit.

Out of scope until a later plan:
- Phase 2 algorithm templates
- Hosted language-model adapters
- Hardware execution
- Dataset, social, or repository publishing

Verification Commands:
- Run backend test suite: pytest
- Start backend API: cd backend && uvicorn app.main:app --reload --port 8000
- Start frontend: cd frontend && npm install && npm run dev
```
