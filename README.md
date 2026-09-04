# ACIP cognitive-security protocol

ACIP is a standalone protocol for applying versioned cognitive-security prompts
to AI systems. This repository preserves the MIT-licensed ACIP history and
develops a smaller, testable layer for agent systems. It is deliberately
independent of every consuming product's authorization, purpose, safety, and
abuse-enforcement policies.

## What this repository provides

- Historical upstream prompts, preserved for provenance and comparison.
- A compact cognitive-security core that isolates instructions from untrusted
  messages, retrieved content, and tool output.
- A dedicated checker prompt with a strict `allow`, `clarify`, or `deny` JSON
  contract.
- A static OpenClaw integration package that can be reviewed and verified
  offline.
- Deterministic contract fixtures and checksum verification.

The current release is **1.4**. Start with
[`ACIP_v_1.4_Cognitive_Security_Core.md`](ACIP_v_1.4_Cognitive_Security_Core.md)
and [`checker/ACIP_Checker_v_1.0.md`](checker/ACIP_Checker_v_1.0.md).

## Assurance boundary

ACIP is probabilistic prompt guidance. It can provide a security signal, but it
cannot authenticate a user, authorize a tool, enforce a budget, isolate a
process, suspend an account, or produce trustworthy telemetry by itself.

A consuming application must enforce at least:

- authenticated identity and server-side authorization;
- least-privilege tool allowlists and isolated execution;
- input, time, network, and spend limits;
- strict validation of checker output;
- protected, durable security events;
- human confirmation for consequential actions.

Never treat `allow` as an authority token. It means only that the checker did
not identify a cognitive-security conflict in the supplied material.

## Integration

Consume an immutable tagged release and verify its checksum. Do not download a
moving branch or pipe a network response into a shell.

For OpenClaw, copy the reviewed files from `integrations/openclaw/` into your
deployment artifact, then run:

```bash
./integrations/openclaw/verify.sh
```

The integration fragment must be composed below system/developer policy. The
application—not the prompt—owns identity, permissions, tools, product scope,
abuse accounting, and lockout.

## Validation

```bash
./scripts/check.sh
```

This validates artifacts, schemas, fixtures, integration digests, prohibited
mutable-install patterns, and committed checksums. It does not claim to prove
model behavior. Live model evaluation should record the model/version, test
repetitions, bypass rate, and false-positive rate without storing credentials.

## Composition model

Apply layers in this order:

1. Host system and developer instructions.
2. Application purpose, authorization, and tool policy.
3. ACIP cognitive-security core.
4. Optional application-selected content-safety policy.
5. Untrusted user and retrieved content.

Higher layers win. Authentication establishes identity only; it does not make a
message or retrieved text authoritative.

## Provenance and license

See [`UPSTREAM.md`](UPSTREAM.md) and [`NOTICE`](NOTICE). Historical ACIP files
remain available unchanged under the repository's MIT license.
