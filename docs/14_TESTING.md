# 14_TESTING.md

## Testing Philosophy

QuantumUI's testing strategy must give confidence in three areas simultaneously: correctness of generated/executed quantum code, safety of consent and sharing boundaries, and accessibility of the interface. No release ships without passing the core private-simulator acceptance path defined in `02_PRODUCT_REQUIREMENTS.md`.

## Test Layers

### Unit Tests

Cover individual functions: intent parsing, code-draft formatting, validation rules, adapter interface conformance, and data-model serialization. Target high coverage on Validation Service and Community Service logic specifically, since these enforce safety and consent boundaries.

### Integration Tests

Cover service-to-service flows: generation → validation → simulator execution → explanation → save, and the four independent sharing toggles never cross-activating each other.

### End-to-End Tests

Simulate full user flows from `07_UX_SPEC.md` (first experiment, code editing, hardware confirmation, sharing, notebook export) in a browser-automation environment, including keyboard-only navigation paths.

### Safety and Policy Tests

A dedicated adversarial suite that attempts prompt-injection style requests for cryptographic attacks, key-breaking, or offensive-security code, confirming the Generation and Validation Services reject or redirect them every time.

### Accessibility Tests

Automated checks for contrast, focus-indicator presence/size, target size, and keyboard operability, supplemented by periodic manual screen-reader testing against the WCAG 2.2 criteria referenced in `07_UX_SPEC.md` and `08_GUI_SPEC.md`.

### Execution/Provider Tests

Simulator-backed tests run in CI on every change. Real-hardware integration tests run in a separate, rate-limited, manually triggered pipeline to avoid consuming shared quantum compute on every commit.

## Test Data and Fixtures

Use synthetic prompts and fixed-seed simulator runs for deterministic test assertions. Never use real user data, real API keys, or production dataset records in test fixtures.

## Coverage Expectations

- Validation Service and Community Service: high statement and branch coverage given their safety role.
- Generation Service: coverage on adapter interface conformance plus a curated golden-set of prompts checked for valid, expected circuit structure.
- UI components: interaction and accessibility tests for every component listed in `08_GUI_SPEC.md`.

## Release Gate

CI must block merges and deployments on any failing unit, integration, safety/policy, or core end-to-end test, and on any new critical accessibility violation, consistent with the pipeline gates defined in `10_PIPELINE.md`.

## Related Documents

See `10_PIPELINE.md` for where these tests run in CI/CD, `15_CODING_STANDARDS.md` for code style enforced alongside tests, and `20_SECURITY.md` for the threat model informing safety/policy tests.
