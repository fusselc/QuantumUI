# 00_PROJECT.md

## What is QuantumUI?

QuantumUI is an open-source, no-code interface that lets anyone — regardless of programming or physics background — design, run, and understand real quantum computing experiments. Users interact through a simple web GUI: pick a template, describe an experiment in plain English, and QuantumUI converts that natural-language prompt into working Qiskit code using either an uploaded open-source LLM or the user's own API key (OpenAI, Anthropic, etc.). The generated circuit can then run on a local simulator, IBM Quantum hardware, or any other supported quantum backend.

QuantumUI is explicitly not a cybersecurity or cryptography tool. It is an education and experimentation platform aimed at curious non-experts: students, hobbyists, artists, and researchers outside the quantum field who want to learn by doing rather than by reading a textbook first.

## Why It Exists

Quantum computing today is gated behind Python fluency and Qiskit's API surface. That gate excludes far more people than it lets in. QuantumUI removes the gate. Every experiment a user runs is automatically documented by the AI (what was tried, what circuit was generated, what the results were) and saved back into the project's GitHub repository. Users can optionally publish notable experiments to arXiv directly from their saved run.

## The Three Pillars

1. **Accessibility** — Templates, a suggestion-driven prompt box, natural-language-to-Qiskit conversion, and dual support for Google Colab / Jupyter notebooks so users can go as deep as they want, whenever they want.
2. **Openness** — Open-source core, bring-your-own-LLM or bring-your-own-API-key, connects to IBM Quantum or any other backend. No vendor lock-in.
3. **Community Dataset** — Every public experiment (prompt → generated code → hardware result) becomes part of a growing, shareable dataset. Social media is used deliberately to demystify quantum computing and grow this dataset, turning curiosity into a research asset for the entire community — including IBM and other hardware providers.

## Who This Is For

- A student who has never written Python but wants to see superposition happen for real.
- A researcher who wants to prototype an idea in plain English before writing formal Qiskit.
- A hobbyist who wants to post "I ran a real quantum experiment" on social media.
- A future ML researcher who wants a large, labeled, natural-language-to-quantum-circuit dataset that doesn't yet exist at scale.

## What Success Looks Like

A non-programmer runs their first real quantum circuit on IBM hardware within 10 minutes of opening QuantumUI, understands what happened because the AI explained it in plain language, and optionally shares it — contributing to a public dataset that helps improve quantum tooling for everyone.

## Where to Read Next

Read `01_VISION.md` for the long-term direction, then `AGENTS.md` if you are an AI agent building this project.
