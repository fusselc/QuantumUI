# 20_SECURITY.md

## Scope

This document defines QuantumUI's security posture: threat model, secret handling, vulnerability disclosure, and safety boundaries related to misuse.

## Threat Model Summary

Primary risks include: leaked provider credentials or API keys, unauthorized public disclosure of private experiments, prompt-injection attempts seeking cryptographic-attack or offensive-security code, abuse of shared hardware queue time, and injection of unsafe or malicious code through generated Qiskit output.

## Secret Handling

- Provider credentials and API keys are stored in a dedicated secrets store, never in the Experiment Store, logs, or exported notebooks, per `09_BACKEND.md`.
- Secret scanning runs on every commit and blocks merges on detection, per `10_PIPELINE.md`.
- Access to secrets is scoped and short-lived; no service holds broader credential access than it needs for its immediate task.

## Safety Boundaries

- The Generation Service and Validation Service must reject or redirect any request for cryptographic attacks, key breaking, malware, or other offensive-security content, replacing it with an educational, non-actionable explanation, per `12_AI.md`.
- Execution Adapter Plugins must pass a policy-compliance test suite before listing, per `11_PLUGINS.md`.
- Hardware execution always requires explicit, distinct user confirmation to prevent accidental or abusive consumption of shared quantum compute, per `07_UX_SPEC.md`.

## Data Protection

- Public dataset releases require secret and personally identifying information filtering, moderation review, and explicit per-experiment consent, per `COMMUNITY.md` and `DATA_LICENSE.md`.
- Private experiments are never included in any public release, training corpus, or social share without an explicit, separate consent action.

## Vulnerability Disclosure

QuantumUI follows a coordinated disclosure process consistent with widely used industry guidance: researchers report suspected vulnerabilities privately, are given a reasonable remediation window before public disclosure, and receive acknowledgment and, where appropriate, credit. [web:144]

- Report suspected vulnerabilities to the private security contact listed in the repository's security policy file, not through public issues.
- Include reproduction steps, affected component, and potential impact.
- Maintainers aim to acknowledge reports promptly and provide a remediation timeline; public disclosure follows an agreed-upon or reasonable default window after a fix is available. [web:144]

## Secure Coding Practices

Development follows established secure-coding guidance covering input validation, output encoding, authentication, session management, access control, and error handling, adapted for QuantumUI's specific services. [web:146] Security-sensitive pull requests require additional review per `19_DEVELOPMENT_WORKFLOW.md`.

## Incident Response

Confirmed incidents involving credential exposure, unauthorized data disclosure, or safety-boundary bypass trigger: immediate containment, credential rotation where relevant, user notification proportionate to impact, a documented post-incident review, and a corresponding entry in `16_DECISIONS.md` if a systemic fix is required.

## Related Documents

See `09_BACKEND.md` for secrets architecture, `12_AI.md` and `11_PLUGINS.md` for safety-boundary enforcement points, and `COMMUNITY.md`/`DATA_LICENSE.md` for public-data protection rules.
