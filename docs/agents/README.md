# agentic skills

A compact, single-agent workflow for coding assistants operating in this
repository or other local codebases you point them at. The design goal is not
maximum autonomy. It is disciplined execution with low token burn, explicit
quality gates, and predictable artifacts.

This package is intended for Codex-style CLI usage, but the operating model is
general:

- one agent, not a swarm;
- short planning horizons;
- bounded search before edits;
- small diffs by default;
- verification before completion;
- explicit uncertainty and rollback paths.

## Why this shape

A lot of current agent systems over-spend on repeated planning, self-critique,
and parallel role-play. That can increase latency and token cost without a
commensurate reliability gain on ordinary software engineering tasks. Recent
agent evaluations and field reports broadly support a simpler pattern: give the
model a strong execution contract, reduce branching factor, force interaction
with tests and tooling, and require concrete evidence before declaring success.

This package therefore prefers a staged pipeline with hard stop conditions over
open-ended loops.

## Files

- `AGENTS.md`: top-level operating contract and repository interaction rules.
- `skills/implementation-pipeline.md`: end-to-end delivery pipeline.
- `skills/change-planning.md`: bounded planning and search discipline.
- `skills/testing-strategy.md`: test-first and regression-oriented testing.
- `skills/debugging.md`: failure triage and root-cause workflow.
- `skills/code-review.md`: pre-submit review checklist.
- `skills/incident-fix.md`: production-oriented hotfix mode.
- `skills/language-profiles.md`: language/tool-specific verification matrix.
- `prompts/task-template.md`: concise task framing template.
- `prompts/pr-template.md`: PR body template.

## Usage

For a coding session, place the contents of `AGENTS.md` into the agent's repo
instructions or point the agent at this document set if your tool supports
workspace instructions.

Then give the agent only the task-specific context. Avoid stuffing repeated
meta-instructions into every prompt. The skills package already encodes the
execution policy.

## Operating principles

The workflow has five phases.

1. Understand the task and constraints.
2. Inspect the minimum relevant code and docs.
3. Make the smallest correct change.
4. Verify with targeted tests, then broader checks when warranted.
5. Summarize evidence, residual risk, and follow-ups.

The agent should not repeatedly re-plan unless new evidence invalidates the
current plan.

## Expected outputs

A successful run should usually produce:

- a concise plan;
- a focused diff;
- tests or updated tests when behavior changes;
- a brief verification report;
- a PR description with risk and rollback notes.

## Limits

This package intentionally does not try to solve:

- long-horizon autonomous product management;
- multi-agent decomposition;
- speculative refactors without evidence;
- exhaustive file crawling before work starts.

Those modes are expensive and often brittle. Use them only when the task truly
requires them.
