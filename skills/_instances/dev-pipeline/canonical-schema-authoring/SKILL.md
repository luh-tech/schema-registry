---
name: canonical-schema-authoring
description: "FIRES when authoring any artifact that must validate against a canonical schema before cross-repo handoff — deliverable specs, skill instances, rule instances, FU register patches, TRUTH-DELIVERED records. Sandbox-validate against the canonical schema in chat-side Python BEFORE staging artifact for terminal upload. Pairs with substrate-before-write (the substrate input) and cross-repo-execution-shape (the broader 5-stage flow). F0B85LNSTC4 doctrine seven-times-proven across session arc."
version: 1.0.0
category: dev-pipeline
lifecycleStatus: working-model
triggerMode: pushy
---

# canonical-schema-authoring

Sandbox-validate every authored artifact against its canonical schema in chat-side Python (jsonschema.Draft7Validator with $ref neutering for offline operation) BEFORE staging for terminal upload. Catch shape mismatches, missing required fields, additionalProperties violations, pattern failures, and constraint violations at authoring time rather than at terminal ajv invocation time. Trade one chat-side validation round-trip for averted REFUSE-AND-SURFACE recovery cycles at terminal.

## When this skill fires

**Authoring any artifact that will be validated against a canonical schema by ajv-cli or jsonschema at terminal time.**

Example cues:
- compose deliverable spec for X
- author skill instance for Y
- build the FU register patch
- create the TRUTH-DELIVERED instance
- patch the rule instance

**Cross-repo handoff of authored artifact to another agent (terminal, EB-chat, SR-chat) for landing or execution.**

Example cues:
- stage for SR terminal
- send to EB-chat for execution
- tarball for handoff
- upload for terminal

**Modifying an existing instance that will re-validate post-edit (closure transitions, lifecycleState advances, FU status changes).**

Example cues:
- append closure transitions
- advance lifecycleState to S8-closed
- close FU with resolution block
- update register meta block

## Behavior

1. **After authoring any artifact JSON, immediately validate against its canonical schema using jsonschema.Draft7Validator in chat sandbox. If validation fails, fix and re-validate. Do not stage artifact to outputs/ until validation PASSES.**
   F0B85LNSTC4 doctrine — chat-side sandbox catches what terminal ajv would catch, but earlier (cheaper, no round-trip). Seven-times-proven across 2026-06-03 and 2026-06-04 cross-repo arcs.

2. **When canonical schema has external $refs (e.g. $ref to luhtech-enums.schema.json or forbidden-audit-paint-names.schema.json), neuter URL-form $refs in chat sandbox before validation; use the canonical -r flag for terminal ajv invocations.**
   Chat sandbox has no resolver for URL-form $refs. Terminal ajv-cli requires -r flag for external $ref resolution. PR #106 + PR #119 both proved this — -r flag omission causes ajv compile failure. PR #121 closed FU-SR-AJV-COMPILE-INVOCATION-NORMALIZATION-1 after second proof.

3. **When schema has additionalProperties:false (strict mode), audit authored artifact for any fields not in schema properties[]. Strip extra fields rather than adding properties.**
   PR #124 caught case: composed TRUTH-DELIVERED outputs[] with id + description fields, canonical schema requires outputId only with additionalProperties:false. Caught chat-side by sandbox-validate before terminal saw it.

4. **When schema has conditional requirements (allOf/if-then-else), audit authored artifact for the if-clause trigger and verify then-clause requirements are satisfied.**
   Skill schema requires evidenceClass on UP-promotions to formalized (allOf if to==formalized then evidenceClass required). Missing this on a future promotion would fail terminal ajv.

5. **Cache canonical schemas in chat-side filesystem (/tmp/<schema>.schema.json) after first read; re-validate against cached schema on every authored artifact for the same target type.**
   Reduces substrate-read round-trips when authoring multiple instances of the same target type (e.g. three skill instances in this arc all validate against /tmp/skill.schema.json cached once).

## Anti-patterns

- DO NOT: Author artifact, stage to outputs/, and rely on terminal ajv to catch shape problems.
  INSTEAD: Validate chat-side first; only stage after PASS. Terminal ajv is the second gate, not the first.
- DO NOT: Skip chat-side validation because 'the artifact looks right by inspection'.
  INSTEAD: Always validate. Eye-inspection misses additionalProperties violations, exact pattern matches, and nested-shape requirements.
- DO NOT: Validate against summary description of schema instead of canonical schema text.
  INSTEAD: Read canonical schema text via substrate-before-write skill, cache, then validate against the cached canonical.
- DO NOT: Author artifact against memory of a similar instance from a prior session.
  INSTEAD: Read canonical schema fresh; do not assume prior-session instance shape still matches current schema.

## Boundary conditions (when this skill does NOT fire)

- Does NOT fire for conversational replies, explanations, or analysis that does not produce a schema-bound artifact
- Does NOT fire when schema is unknown — substrate-before-write fires first to read the canonical schema
- Does NOT block ajv-cli at terminal — chat-side validation is additive, not substitutive

## Paired rule

This skill pairs with rule instance: `urn:luhtech:rule:dev-pipeline:canonical-schema-authoring-doctrine:1.0.0`

## References

- [memory-rule] 10 — TRUTH ONLY: validate before stating valid
- [memory-rule] 20 — Enterprise-complete: validate at authoring time, not deferred to terminal
- [closure-doc] schemas/_instances/deliverables/d-2026-06-04-sr-ajv-r-flag-workflow-normalization.json — Closed FU-SR-AJV-COMPILE-INVOCATION-NORMALIZATION-1 after the -r flag canonical pattern was proved across session
- [closure-doc] schemas/_instances/truth-delivered/d-2026-06-04-eb-catalog-ground-truth-atomic.json — Captures fifth negative-case proof — TRUTH-DELIVERED outputs-shape sandbox-catch

## Governance

- Author: Claude (SR chat), L1
- Approver: Erik Luhtala (L4)
- Revert authority: Erik Luhtala (L4)

<!-- generated by luhtech-skill-generate v1.0.0 from sha256:f03d23c3b0259a772d1bb967ab6dc1441ec00dbe255d007e7075b511fc6ffb3f at 0000-00-00T00:00:00Z -->
