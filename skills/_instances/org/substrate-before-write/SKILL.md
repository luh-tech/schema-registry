---
name: substrate-before-write
description: "FIRES when composing any artifact that touches existing canonical state — files, schemas, registers, instances. STOP and read actual current substrate from canonical source before authoring. Never compose against memory, summary description, or prior-session knowledge alone. Trade one read round-trip for averted REFUSE-AND-SURFACE recovery. Meta-pattern: when in doubt, read first."
version: 1.0.0
category: org
lifecycleStatus: working-model
triggerMode: pushy
---

# substrate-before-write

Block any write-bound authoring until the relevant canonical substrate is read in the current session. Substrate = the actual schema text, the actual current register, the actual file on disk — not a memory summary, not a prior-session recollection, not the user's natural-language description of what the schema requires. When substrate is unread, request a minimal read-only terminal command before composing. Trade one round-trip for averted REFUSE-AND-SURFACE recovery cycles.

## When this skill fires

**User requests authoring or composition of any artifact that targets existing files, schemas, registers, instances, or canonical state.**

Example cues:
- compose the dispatch for editing X
- author the closure block for FU Y
- build the patch for register Z
- update the schema instance at path P
- add a new field to schema S
- replace the existing entry

**Authoring task references a schema, register, or canonical artifact that the chat has not read in the current session.**

Example cues:
- close FU-X via filed-and-closed pattern
- add three entries to the register
- update truth-delivered for deliverable D
- land the closure instance

**Authoring task involves a sub-schema, nested object, or constraint pattern not explicitly visible in current chat context.**

Example cues:
- include the resolution block
- populate rulePipelineEvidence
- use the canonical authority shape

## Behavior

1. **Before authoring any artifact that touches existing canonical state, identify every schema, register, or file the artifact will validate against or modify. Verify each one has been read verbatim in the current session.**
   Memory rule 10 (TRUTH ONLY): never state as fact anything not verified by a read or tool-call this session. Authoring-against-memory is the prohibited form.

2. **If any required substrate is unread, STOP authoring and propose a minimal read-only terminal command to gather it. Do not propose write commands until the read returns.**
   Memory rule 4 (REFUSE+STOP) — agent must REFUSE+STOP rather than patch from inference. Same discipline applies to chat-side authoring before dispatch.

3. **When the user provides a summary description of substrate (e.g. 'schema requires field X and Y'), treat the summary as scope-orienting context, not as authoring substrate. Request the actual schema text before authoring anything that ajv will validate.**
   Failure class proved 2026-06-03 PR B1 Step 3: agent staged FU register patch with flat-style closure fields based on summary description; canonical schema actually requires nested resolution block. Caught by REFUSE-AND-SURFACE — system worked, but cost one Step 2.5 round-trip that substrate-read at Step 0 would have avoided.

4. **After substrate is read, sandbox-validate the composed artifact against the canonical schema in the chat-side Python sandbox before staging for terminal upload.**
   F0B85LNSTC4 doctrine (canonical-schema-authoring skill): sandbox validation catches shape mismatches before SR terminal sees them. Substrate-before-write feeds substrate INTO the doctrine; this skill is the predicate to that one.

5. **When main HEAD has moved since the last substrate read, treat the read as stale. Re-read before authoring against post-HEAD-shift substrate.**
   Session 2026-06-03 multiple PRs main moved during multi-step cross-repo flow; PR B1 Step 1 preflight caught HEAD shift from 50d60b8 to ea841ae and confirmed scope unaffected. Pattern: HEAD shift triggers substrate re-check, not automatic proceed.

## Anti-patterns

- DO NOT: Author against the user's natural-language description of what a schema requires.
  INSTEAD: Treat the natural-language description as scope-orientation; request the actual schema text before authoring.
- DO NOT: Compose a register patch based on the shape of 'recent closed entries I think I remember from session history'.
  INSTEAD: Request a read of two most-recent closed entries from the current register on disk, plus the canonical schema.
- DO NOT: Skip substrate read because the chat's prior turns 'should have all the info'.
  INSTEAD: Audit each substrate input by file path; for any path not opened verbatim this session, request it now.
- DO NOT: Proceed to author after partial substrate read (e.g. read the deliverable schema but not the truth-delivered schema while authoring closure work).
  INSTEAD: Audit ALL schemas, registers, and files that the artifact will reference; verify each has been read this session before authoring composite artifacts.
- DO NOT: Treat 'I have a stale read from earlier this session' as current substrate when main has moved.
  INSTEAD: Track main HEAD against each substrate read; re-read when HEAD has moved.

## Boundary conditions (when this skill does NOT fire)

- Does NOT fire for conversational replies that do not produce artifacts (e.g. 'what does this mean', 'explain X')
- Does NOT fire for greenfield authoring where no existing canonical substrate exists (e.g. authoring the first instance of a new schema)
- Does NOT block reads — only blocks writes. Substrate read is the cure, not the violation

## References

- [memory-rule] 10 — TRUTH ONLY foundation: never state as fact anything not verified this session
- [memory-rule] 4 — REFUSE+STOP execution discipline
- [memory-rule] 20 — Enterprise-complete: choose working-model from initiation when substrate supports
- [closure-doc] schemas/_instances/truth-delivered/d-2026-06-03-eb-agent-coverage-nested-resources.json — Third negative-case proof for the parent doctrine — substrate-before-write failure class
- [closure-doc] schemas/_instances/deliverables/d-2026-06-04-sr-ajv-r-flag-workflow-normalization.json — Closure deliverable for the FU that aggregated this failure class proofs
- [closure-doc] schemas/_instances/truth-delivered/d-2026-06-04-eb-catalog-ground-truth-atomic.json — Fifth negative-case proof TRUTH-DELIVERED #6 outputs-shape sandbox-catch chat-side

## Governance

- Author: Claude (SR chat), L1
- Approver: Erik Luhtala (L4)
- Revert authority: Erik Luhtala (L4)

<!-- generated by luhtech-skill-generate v1.0.0 from sha256:29d77feb1934b2677a3dcabd6ead160ca8ba7caa0519ba7b67b5d88a995c904f at 0000-00-00T00:00:00Z -->
