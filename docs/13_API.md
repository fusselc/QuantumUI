# 13_API.md

## Purpose

This document specifies QuantumUI's public API surface: resources, endpoints, versioning, error format, and authentication rules. It complements the representative endpoints listed in `09_BACKEND.md`.

## Versioning

The API is versioned in the URL path (for example, `/v1/experiments`), since path-based versioning remains the dominant approach for public-facing APIs and is simplest for external integrators to reason about. [web:147] Breaking changes require a new major version; additive, backward-compatible changes may ship within the same version.

## Authentication

- User-facing requests use short-lived bearer tokens issued after standard account authentication.
- Provider credentials (for example, an IBM Quantum API key) are stored server-side in the secrets layer defined in `09_BACKEND.md` and referenced by an internal credential ID; they are never returned in any API response.
- Self-hosted/open-model adapters authenticate through a local service token, not a public-facing credential.

## Core Resources

### Experiments

```
POST   /v1/experiments                     Create from prompt or template
GET    /v1/experiments                     List (paginated, cursor-based)
GET    /v1/experiments/{id}                Retrieve one
POST   /v1/experiments/{id}/generate       Request or regenerate code
POST   /v1/experiments/{id}/validate       Run static validation
POST   /v1/experiments/{id}/execute        Submit for execution (simulator default)
GET    /v1/experiments/{id}/status         Poll execution status
POST   /v1/experiments/{id}/sharing        Set one sharing flag (repository/dataset/social/research)
POST   /v1/experiments/{id}/export/notebook
POST   /v1/experiments/{id}/export/github
```

### Templates

```
GET    /v1/templates
GET    /v1/templates/{id}
```

### Providers and Backends

```
GET    /v1/providers                       List configured execution providers
GET    /v1/providers/{id}/backends         List available backends (simulator/hardware)
```

## Pagination

List endpoints use cursor-based pagination (`?cursor=...&limit=...`) rather than offset pagination, which scales better and avoids skipped/duplicated records under concurrent writes. [web:138]

## Error Format

Errors follow a structured problem format (aligned with RFC 9457 "Problem Details"): a `type`, `title`, `status`, `detail`, and an optional `instance` identifying the specific request. [web:138]

```json
{
  "type": "https://quantumui.dev/errors/validation-failed",
  "title": "Circuit validation failed",
  "status": 422,
  "detail": "The generated circuit references an undefined qubit register.",
  "instance": "/v1/experiments/abc123/validate"
}
```

## Idempotency

State-changing requests that could trigger real hardware execution (`POST /experiments/{id}/execute` with a hardware backend) must include an `Idempotency-Key` header. Repeated requests with the same key return the original result rather than submitting a duplicate job, which is essential given shared, finite hardware queue time. [web:138]

## Rate Limiting

Standard responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers. Hardware-execution endpoints carry stricter, separate limits from simulator and generation endpoints to protect shared provider capacity.

## Documentation Format

The API is specified with OpenAPI 3.1, generated from source annotations so documentation cannot drift from the implemented contract. [web:140]

## Related Documents

See `09_BACKEND.md` for service-level responsibilities behind these endpoints and `20_SECURITY.md` for authentication and credential-handling requirements.
