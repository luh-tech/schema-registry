---
name: cross-repo-execution-shape
description: "FIRES when a deliverable involves work across two or more repos in the LuhTech portfolio — typically schema-registry (SR) holds the canonical deliverable instance anchor while another repo (EB, ectropy-ai, etc) executes. Five-stage flow: substrate-read -> sandbox-validate -> SR anchor land -> target-repo execute -> SR close with TRUTH-DELIVERED. Composite of substrate-before-write (skill 1) + canonical-schema-authoring (skill 2). Seven iterations proven across session arc."
version: 1.0.0
category: dev-pipeline
lifecycleStatus: working-model
triggerMode: pushy
---

# cross-repo-execution-shape

Apply the canonical 5-stage cross-repo flow: (1) substrate-read all canonical schemas + current state across both repos; (2) sandbox-validate authored artifact chat-side against canonical schema; (3) SR-anchor first — land deliverable spec in SR schemas/_instances/deliverables/ via squash-merge PR; (4) target repo executes against anchored spec via its own PR; (5) SR closes — transitions S4 -> S6 -> S7 -> S8, authors TRUTH-DELIVERED in SR, captures any process deviation in closureNotes.overrideRecord. Each stage uses its own PR per memory #18 branch scope-lock. Surface coordination events via canvas + channel relay per memory #5 cross-chat-surface-notification.

## When this skill fires

**Deliverable scope crosses repos — work executes in one repo (e.g. EB) but canonical state needs to land in another (e.g. SR schemas/_instances/deliverables/).**

Example cues:
- EB deliverable that needs SR anchor
- close EB PR with SR TRUTH-DELIVERED
- ectropy-ai schema work with SR registry update
- land cross-repo instance
- compose closure for EB execution

**Closure work for a previously-anchored deliverable — appending S6/S7/S8 transitions, authoring TRUTH-DELIVERED, capturing process deviations.**

Example cues:
- close deliverable D after EB merge
- TRUTH-DELIVERED for PR #N
- append closure transitions
- lifecycleState advance to S8-closed

**Process deviation surfaced — EB shipped before SR anchor, or amendment required after initial landing, or unanchored close requested.**

Example cues:
- retroactive anchor
- EB merged without SR landing
- amendment to landed instance
- process exception

## Behavior

1. **Stage 1 — Before authoring: read canonical schemas via substrate-before-write skill. Read current state of all canonical files the deliverable will touch.**
   Stage 1 failure = downstream cascade. PR #122 caught this — composed catalog spec from channel-message summary; corrected via fixup tarball substrate read.

2. **Stage 2 — Validate authored spec against canonical deliverable.schema.json in chat sandbox before staging for SR terminal. Same for any TRUTH-DELIVERED or closure-block authoring.**
   Canonical-schema-authoring skill (PR 2) doctrine — chat-side sandbox catches shape mismatches before terminal sees them.

3. **Stage 3 — Land SR anchor FIRST when shipping new cross-repo deliverable. Spec lands at S4-authored in schemas/_instances/deliverables/<deliverable-id>.json via squash-merge PR. Target repo does not execute until anchor is on SR main.**
   Cross-repo doctrine: anchor before execute. Pattern observed twice this week where EB shipped before SR anchor (PR #290, PR #294) — captured as FU-SR-PROCESS-EB-PRE-SR-SHIP-PATTERN-1 for L4 doctrine refinement.

4. **Stage 4 — Target repo executes against anchored spec via its own PR. Target repo PR commit message references the SR deliverable id. Target repo squash-merges; SHA captured for stage 5.**
   Anchor-bound execution is auditable. Channel relay surfaces SR PR merge SHA + target repo PR merge SHA so SR-chat and target-chat both have substrate for next stage.

5. **Stage 5 — SR closure PR appends S6 -> S7 -> S8 transitions, lands TRUTH-DELIVERED with closureStatus=closed-clean (or closed-with-debt + closureNotes.debt + closureNotes.overrideRecord), files any new FUs surfaced during execution per memory #20.**
   Closure captures the full lifecycle. TRUTH-DELIVERED is the canonical record of cross-repo coordination. closureNotes.overrideRecord names process deviations explicitly.

## Anti-patterns

- DO NOT: Target repo ships before SR anchor lands (EB-pre-SR-ship deviation).
  INSTEAD: SR anchor first, then target repo executes. If deviation already happened, land retroactive anchor before closure (PR #122 pattern).
- DO NOT: Combine landing + closure in same PR to 'save a round-trip'.
  INSTEAD: Each stage gets its own PR per memory #18 scope-lock. Combined-purpose PRs lose lifecycle clarity.
- DO NOT: Skip canvas/channel relay because 'the work is on the same machine'.
  INSTEAD: Always relay merge SHAs via channel + canvas per memory #5 cross-chat-surface-notification. Future agents read canvas, not session memory.
- DO NOT: Close S4 -> S8 directly, collapsing S6/S7 transitions because 'they all happened today'.
  INSTEAD: Author each transition with its own trigger field. Lifecycle integrity is the audit trail.

## Boundary conditions (when this skill does NOT fire)

- Does NOT fire for single-repo deliverables — only cross-repo. EB-internal housekeeping deliverable that has no SR side falls outside this skill.
- Does NOT fire for SR-internal work (workflow normalization PR B1, skill instances themselves) — those are single-repo SR work, not cross-repo
- Does NOT prescribe specific PR shape — encodes the 5-stage flow; individual PRs vary in scope/file-count/commit-count per their specific deliverable

## References

- [memory-rule] 5 — Cross-chat surface notification — canvas + channel relay at every stage
- [memory-rule] 18 — Branch scope-lock — each stage gets its own PR
- [memory-rule] 20 — Enterprise-complete — full lifecycle integrity, no collapsed transitions
- [memory-rule] 15 — Documented-override-not-compliance — process deviations named in closureNotes.overrideRecord, not silently bypassed
- [closure-doc] schemas/_instances/truth-delivered/d-2026-06-04-eb-catalog-ground-truth-atomic.json — Latest cross-repo closure with EB-pre-SR-ship deviation captured in overrideRecord

## Governance

- Author: Claude (SR chat), L1
- Approver: Erik Luhtala (L4)
- Revert authority: Erik Luhtala (L4)

<!-- generated by luhtech-skill-generate v1.0.0 from sha256:dca30ac99c9bb7596bfec0e136fb8b9f2648ab101426593a434f6740a3536b19 at 0000-00-00T00:00:00Z -->
