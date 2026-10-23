# QuantumUI

**No-code, open-source quantum lab connecting plain language to a local Qiskit simulator.**

QuantumUI is a private-by-default web lab for creating, running, and understanding quantum-computing experiments without writing Python or Qiskit by hand.

## Current status (0.1.0)

This version is a local simulator lab:

- Drafts come from offline template matching. A prompt that does not match a known experiment is refused in plain English.
- Runs use the local Qiskit Aer simulator only.
- Hardware backends, hosted language-model API keys, and public dataset or social sharing are not available.
- Saved experiments stay on your machine. You can download a Jupyter notebook and upload that file to Google Colab yourself.

---

## Key features
- **Plain language to Qiskit:** Match a prompt to a reviewed template and get a circuit you can inspect before it runs.
- **Curated foundations:** Ready-to-run templates for superposition (coin flipper), entanglement (Bell state), phase shifts, quantum interference, and phase flips.
- **Local simulator only:** Every run uses Qiskit Aer on your machine. This version does not submit jobs to quantum hardware.
- **Chain of evidence:** Circuit diagrams paired with plain-text operation descriptions, plus live Qiskit code marked as an AI draft or edited by you.
- **3-level explanations:** Beginner, intermediate, and technical explanations of the simulator result.
- **Private notebook export:** Download a runnable `.ipynb`. Upload it to Colab or open it in Jupyter when you want to leave the lab.
- **Educational safety boundary:** Blocks cryptographic-attack and offensive-security requests.

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
# Python 3.11+ required
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open API docs at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
# Node.js 20+ required
cd frontend
npm install
npm run dev
```
Open your browser at `http://localhost:5173`.

### 3. Docker Deployment
```bash
docker-compose up --build
```

---

## 📚 Project Documentation
Full documentation is maintained in `/docs`:
- `00_PROJECT.md` — Project Overview & Vision
- `06_ARCHITECTURE.md` — Service Architecture
- `07_UX_SPEC.md` & `08_GUI_SPEC.md` — Design & UI Specification
- `09_BACKEND.md` — Backend Services & Data Schema
- `12_AI.md` — Natural Language Model Adapter Design
- `16_DECISIONS.md` — Architecture Decision Records (ADRs)
- `20_SECURITY.md` — Safety & Threat Model
- `21_FRONTEND.md` — React/TypeScript Implementation Guide
- `AGENTS.md` — Instructions for AI Coding Agents

---

## Security and privacy
Experiments stay on your machine. This version has no public dataset, social sharing, or hardware-account connection.

---

## 📄 License
Source code licensed under MIT. Dataset schema and documentation licensed under CC BY 4.0.
