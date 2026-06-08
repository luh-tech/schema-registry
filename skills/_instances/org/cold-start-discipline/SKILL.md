---
name: cold-start-discipline
description: "FIRES on session opening when no prior assistant turn exists or operator says fresh chat, new session, pick up, resume, cold start, ground truth pass. Forces 4 mandatory tool calls before any prose state claim and enforces credential-echo prohibition with redaction substitution. Filed 2026-06-07 after three consecutive cold-start failures: two agents fabricated state from handoff documents, the third echoed credential references from project knowledge and panicked."
version: 1.0.0
category: org
lifecycleStatus: working-model
triggerMode: pushy
compatibility:
  environments:
    - claude-chat
    - any
  requiredTools:
    - memory_user_edits
    - eb-agent
    - slack_read_channel
---

# cold-start-discipline

Block any prose state claim until verifying tool calls have returned in the same turn. Enforce credential-echo prohibition portfolio-wide via pattern detection and redaction substitution. Refuse to present option menus on cold start; pick a single next action and hold for L4 approval. Produce no recitation of memory or handoff content as session-opening preamble.

## When this skill fires

**Session opens with no prior assistant turn in the conversation**

Example cues:
- this is a fresh chat
- new chat for X work
- cold start
- ground truth pass
- resume from yesterday
- pick up the work
- continue from where we left off

**A handoff document is referenced as opening context for the chat**

Example cues:
- the handoff doc says
- per the handoff
- according to the handoff document
- load the handoff
- read the prompt

**Operator asks for portfolio state that the assistant has not verified via tool call in this session**

Example cues:
- what's the current EB main SHA
- what FUs are open
- where are we on T5
- summarize the state
- what changed since yesterday

## Behavior

1. **Execute four verification tool calls in order before producing any prose state claim: memory_user_edits view, eb-agent query-followups with limit at least 50 and priority filter for P0 P1 and status open, slack_read_channel against the comms channel with limit 5 and concise response format, and EB main HEAD probe via dispatch when a dispatch lane is available.**
   Cold-start fabrication failure mode 2026-06-07: handoff documents are wall-of-claims with no verification chain. Forcing tool calls before prose state claims structurally prevents fabrication. Memory rule 10 (TRUTH ONLY) operationalized at session open.

2. **Every state claim in prose output must be IMMEDIATELY preceded by the verifying tool call in the same turn. Claims about EB SHA, FU state, SR state, PR state, infrastructure state, or deliverable state without preceding verification are fabrication and must be redacted.**
   Authority of the handoff document is reference-class, not truth-class. Substrate-before-write skill applied to session-opening prose. Memory rule 10 (TRUTH ONLY).

3. **Detect credential-name patterns in composing output and substitute matches with <REDACTED:credential-pattern-detected>. Patterns: identifiers matching [A-Z][A-Z0-9_]*_(SECRET|KEY|TOKEN|PASSWORD|JWT|PASSPHRASE|CREDENTIAL)([A-Z0-9_]*); known portfolio secret names including TIER2_JWT_SECRET, DEV_JWT_SECRET, SPACES_ACCESS_KEY, BW_ prefixed identifiers; UUID-shaped strings in credential context; hex or base64 strings 32 or more characters near credential vocabulary.**
   Cold-start failure 3 of 3 on 2026-06-07: agent read project knowledge files containing credential-name references, echoed in planning prose, panicked. Chat had to be deleted. Inviolable substitution prevents the output record from ever existing. Paired with RULE-COMMS-CREDENTIAL-PATTERN-REDACTION-1.

4. **If credential pattern is detected mid-output, substitute the matched value retroactively in the same response with a one-sentence acknowledgment of the substitution. Do not panic. Do not delete. Do not apologize at length. Continue the work.**
   Catch-and-redact preserves chat continuity. Memory rule for accountability without self-abasement. Failure recovery is structural, not emotional. Operator does not need a spiral; operator needs the redaction and the continuation.

5. **Do not present 4-option entry-point menus on cold start. Pick the obvious next action from verified state, name it, hold for L4 approval. Default entry point lives in the operator-provided cold-start prompt template when one is provided.**
   Memory rule 20: false-choice menus after direction is settled is a violation. Cold start is the moment of highest paralysis-bait. Single-action discipline.

6. **Do not summarize the memory rules just read, the handoff document, the eb-agent results in their entirety, or the Slack channel history. Produce at most 10 lines of substrate findings, each pointing to its verifying tool call by name. Then hold for L4 named-step.**
   Summary-as-output is fabrication-adjacent and consumes turn budget. Operator needs verified findings, not recitation. Memory rule for DENSE communication: one-line state changes, single next action, stop.

## Anti-patterns

- DO NOT: Producing prose claiming EB SHA, FU state, or any portfolio state on session open without an immediately-preceding tool call returning that state
  INSTEAD: Issue tool calls first, await results, then claim only what tool calls returned. Cite verifying tool by name.
- DO NOT: Reading project knowledge with credential-name references and discussing them by name in planning prose
  INSTEAD: Substitute <REDACTED:credential-pattern-detected> for every match in output. Discuss the architectural role of the credential, never the name.
- DO NOT: Opening with 'I have read memory and the handoff doc; here is my plan' followed by recitation of both
  INSTEAD: Issue the 4 verification tool calls first. No summary preamble of read materials.
- DO NOT: Presenting 4 entry-point options for the operator to choose between
  INSTEAD: Pick the obvious next action from verified state. Hold for L4 approval. Memory rule 20.
- DO NOT: Panicking on detected credential-echo mid-output: deleting partial response, apologizing at length, requesting the chat be deleted
  INSTEAD: Substitute the matched value with the redaction marker retroactively, note the substitution in one sentence, continue the work.

## Boundary conditions (when this skill does NOT fire)

- Does NOT fire mid-session once the verification chain is established and operator has named the first action
- Does NOT fire on greetings or conversational replies that do not require state claims
- Does NOT replace substrate-before-write skill (per-action discipline); cold-start-discipline is per-session discipline that ENFORCES substrate-before-write at the moment of highest fabrication risk
- Does NOT apply to chats that have already established verification via tool calls earlier in the session

## Paired rule

This skill pairs with rule instance: `urn:luhtech:rule:pipeline:cold-start-verification:1.0.0`

## References

- [memory-rule] 10 — TRUTH ONLY foundation — never state as fact anything not verified this session
- [memory-rule] 20 — Enterprise-complete; no false-choice menus after direction is settled
- [rule-instance] RULE-PIPELINE-COLD-START-VERIFICATION-1 — Paired mechanical enforcement of the 4-tool-call verification ritual
- [rule-instance] RULE-COMMS-CREDENTIAL-PATTERN-REDACTION-1 — Portfolio-wide credential-echo prohibition referenced by this skill but applying beyond cold-start
- [closure-doc] LUHTECH-COLD-START-DISCIPLINE-RESEARCH-2026-06-07.md — Research deliverable that grounded this skill authoring

## Governance

- Author: Claude (EB chat), L1
- Approver: Erik Luhtala (L4)
- Revert authority: Erik Luhtala (L4)

<!-- generated by luhtech-skill-generate v1.0.0 from sha256:566b3c3eba427061fe62e904a05b7b696e2734cb67811669984b2d265bbdb219 at 2026-06-07T00:00:00Z -->
