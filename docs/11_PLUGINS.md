# 11_PLUGINS.md

## Purpose

QuantumUI supports a plugin system so the community can add templates, provider adapters, model adapters, and explanation styles without modifying core services. This keeps the core small, auditable, and provider-neutral.

## Plugin Types

- **Template Plugins** — add new guided experiments (prompt text, suggestions, difficulty level, default backend).
- **Model Adapter Plugins** — add support for a new open-source or hosted LLM behind the `12_AI.md` adapter interface.
- **Execution Adapter Plugins** — add support for a new quantum provider behind the `09_BACKEND.md` execution interface.
- **Explanation Style Plugins** — add alternate explanation tones/levels (for example, a classroom mode or a research-notation mode).
- **Export Plugins** — add new export targets beyond Jupyter/Colab/GitHub (for example, a different notebook host).

## Plugin Interface Contract

Every plugin must declare, in a manifest file:

```
name, version, type, entry_point, permissions_requested, min_core_version
```

Plugins may only access the specific service interface for their declared type (a Template Plugin cannot call execution APIs directly, for example). This isolation prevents a template or explanation plugin from silently gaining hardware-execution or credential access.

## Safety and Review Requirements

- No plugin may request access to secrets, credentials, or the Community Service consent state directly; all such access goes through core service calls with the same confirmation flows defined elsewhere.
- Execution Adapter Plugins must implement and pass a policy-compliance test suite (no cryptographic-attack, key-breaking, or offensive-security capability) before listing.
- Model Adapter Plugins must implement the safety-boundary system instructions described in `12_AI.md`.
- All first-party and community plugin submissions go through a manual security and policy review before being listed in the official plugin registry; users may still install unlisted plugins at their own risk, with a clear warning.

## Versioning and Compatibility

Plugins declare a minimum core version and are checked against the running QuantumUI core version at load time. Breaking changes to any plugin interface require a major version bump of that interface, documented in `16_DECISIONS.md` and `18_CHANGELOG.md`.

## Related Documents

See `09_BACKEND.md` for the execution adapter contract, `12_AI.md` for the model adapter contract, and `20_SECURITY.md` for the broader threat model plugins must respect.
