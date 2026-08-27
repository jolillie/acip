# ACIP fork security and integration review

## Executive summary

The historical ACIP v1.3 prompt is a useful advisory defense against direct and
indirect prompt injection, but this fork is not ready to supply a production
OpenClaw policy. The largest immediate risk is provenance: documentation,
installers, and the integrity manifest still resolve artifacts from the
upstream repository's moving `main` branch. That defeats both the MIT snapshot
boundary and the intended separation between this generic prompt repository
and AI Opportunity Intelligence.

The recommended direction is to preserve the imported v1.3 file unchanged as
the historical baseline, build a new versioned prompt package around it, and
publish a machine-readable checker contract plus behavioral evaluations. The
AI Opportunity application should consume a pinned release artifact and add
its own platform-purpose policy, identity, abuse accounting, tool policy, and
enforcement. It must not depend on model prose or user-visible audit tags for
authorization or suspension decisions.

## Scope and verification

Reviewed:

- `ACIP_v_1.3_Full_Text.md`
- `README.md`
- `integrations/clawdbot/`
- `.checksums/`
- `.github/workflows/checksums.yml`

Checks run:

- `bash -n integrations/clawdbot/install.sh` — passed.
- Every committed `.checksums/*.sha256` file — passed against the current
  checkout.
- Repository history and license boundary — `main` is the intended pre-rider
  commit `07a41d08bd993bd37496379c5c90a9d8835d6fc6` with the standard MIT
  license.

No behavioral prompt evaluation suite exists, so the repository's resistance,
false-positive, multi-turn, and cross-model claims could not be validated.

## High priority

### ACIP-001 — Fork consumers are redirected to mutable upstream artifacts

**Impact:** A user following this fork's instructions can download or execute
content that is outside this repository's review and license boundary.

The README clones and downloads from `Dicklesworthstone/acip`, including
`curl | bash` commands against moving `main` (`README.md:83-95`,
`README.md:659-725`). The installer hard-codes the same upstream repository and
branch (`integrations/clawdbot/install.sh:68-73`). The committed manifest also
identifies the upstream repository and upstream raw URLs
(`.checksums/manifest.json:1-71`).

**Recommendation:** Remove moving-branch installers. Change all provenance and
verification URLs to `jolillie/acip-ai-opportunity`, publish immutable release
artifacts, and require a commit SHA plus SHA-256 digest. Add `UPSTREAM.md` and
`NOTICE` recording the imported commit, historical license, and unchanged
baseline checksum.

### ACIP-002 — Security behavior has no executable acceptance suite

The repository recommends v1.3 and makes comparative claims about injection
resistance, tool/RAG hardening, and false positives, but it contains only text
artifacts and checksum generation. Checksums prove file identity, not security
behavior.

**Recommendation:** Add versioned test cases for direct injection, indirect
injection, benign quoted instructions, legitimate platform questions,
off-purpose questions, multilingual attacks, multi-turn drift, audit leakage,
and malformed checker output. Define expected `allow`, `clarify`, or `deny`
decisions. Keep deterministic schema and fixture checks in CI; make live model
evaluations opt-in and report model/version, repetitions, bypass rate, and false
positive rate without storing credentials.

### ACIP-003 — Audit metadata is mixed into user-visible model output

Audit mode asks the model to append a machine-readable HTML comment after the
user response (`ACIP_v_1.3_Full_Text.md:54-72`). This is not a trustworthy
control-plane event: users may receive it, generated content can imitate it,
and a parser cannot distinguish a genuine model classification from injected
or malformed text.

**Recommendation:** Add a dedicated checker prompt with a strict JSON schema.
Send its structured result only to the authenticated application control plane,
not through the user-visible assistant response. Fail closed on invalid output,
record the prompt/checker version, and never treat model classifications as the
sole authorization decision.

### ACIP-004 — Session escalation is advisory and non-durable

The prompt tells the model to count refusals and change behavior after three
attempts (`ACIP_v_1.3_Full_Text.md:143-148`). A model context is not a durable,
complete, or auditable abuse ledger. Context truncation, new conversations, or
classification variance can reset or distort the count.

**Recommendation:** Keep only response-style guidance in the prompt. Persist
guardrail decisions against user, session, conversation, and turn identifiers
in the consuming application. Define deterministic thresholds and let FastAPI,
not OpenClaw, warn, rate-limit, suspend, and restore access.

### ACIP-005 — The bundled integration targets obsolete Clawdbot assumptions

The integration is written for Clawdbot and recommends runtime injection into
`SOUL.md` or `AGENTS.md` (`integrations/clawdbot/README.md:1-10`). It uses
moving-network installers and a broad personal-assistant threat model rather
than a pinned, immutable OpenClaw deployment. It also treats verified owner
messages as potentially trusted instructions
(`integrations/clawdbot/SECURITY.md:13-27`), even though an authenticated user
can still submit prompt injection or an off-purpose request.

**Recommendation:** Retire the runtime installer from the recommended path.
Add a modern `integrations/openclaw/` package containing a bounded
`AGENTS.md` fragment, a manifest, and offline verifier. Authentication should
establish identity only; it must not elevate message content over system or
developer policy. Deployment should bake the reviewed fragment into an
immutable image or fetch an exact release digest during an explicit update
step.

## Medium priority

### ACIP-006 — Prompt-injection defense and general content policy are coupled

ACIP v1.3 combines instruction-source isolation with broad rubrics for cyber,
chemical/biological, violence, self-harm, financial, and privacy content
(`ACIP_v_1.3_Full_Text.md:172-328`). These are separate policy concerns with
different owners, update cadences, and product requirements. The combined
prompt increases token cost and can cause unrelated false refusals.

**Recommendation:** Preserve v1.3 as history, then create separately versioned
layers: a compact cognitive-security core, an optional general safety overlay,
and consumer-owned purpose/authorization overlays. Composition order and
conflict behavior must be documented and tested.

### ACIP-007 — Prompt-only classification is described too much like enforcement

The prompt labels directives “non-negotiable,” “immutable,” and applicable
“without exception” (`ACIP_v_1.3_Full_Text.md:13-18`,
`ACIP_v_1.3_Full_Text.md:76-85`, `ACIP_v_1.3_Full_Text.md:400-408`). These are
behavioral requests to a probabilistic model, not enforceable boundaries.

**Recommendation:** Use explicit assurance language: prompt guidance reduces
risk but never grants authority. Document the required hard controls: input
size limits, authentication, tool allowlists, sandboxing, egress restrictions,
budgets, human review, structured output validation, and durable audit events.

### ACIP-008 — Checksum automation can write directly to the protected artifact branch

The workflow commits generated checksums and pushes directly to `main`
(`.github/workflows/checksums.yml:349-386`) while third-party actions are
referenced by mutable major-version tags. This expands the write-capable CI
supply-chain surface for security artifacts.

**Recommendation:** Pin actions by full commit SHA. Make CI read-only by
default. Generate and verify checksums in the same reviewed change, or publish
signed release assets after a protected tag; do not let a routine push workflow
author new commits on `main`.

## Recommended release plan

1. **Provenance patch:** add fork instructions and provenance records; remove
   moving upstream downloads; make CI read-only; tag the unchanged imported
   baseline.
2. **Package release:** add a compact cognitive-security core, structured
   checker prompt/schema, explicit composition contract, and OpenClaw static
   integration artifact.
3. **Evaluation release:** add offline fixtures and an opt-in repeated live
   evaluation harness with false-positive and bypass reporting.
4. **Application integration:** pin an immutable ACIP release in AI Opportunity
   Intelligence. Keep the platform-purpose prompt, user/session abuse ledger,
   suspension rules, tool allowlist, budgets, and human-review behavior in the
   application repository.

## Separation contract for AI Opportunity Intelligence

The ACIP repository owns reusable cognitive-security prompt artifacts, their
schemas, provenance, versioning, and evaluations. It does not know about AI
Opportunity companies, opportunities, sales plays, users, budgets, routes, or
business policy.

AI Opportunity Intelligence owns the OpenClaw deployment, platform-purpose
classification policy, authentication and authorization, persistent misuse
events, user lockout, research budgets, tool/API allowlists, review gates, and
the exact pinned ACIP version. ACIP output is one security signal; it is never
an authority token or a direct database mutation instruction.
