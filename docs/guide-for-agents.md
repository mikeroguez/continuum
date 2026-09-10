# Guide for AI Agents (Continuum)

> [Leer en español](guia-para-agentes.md) · [Manual for People](using-continuum.md) · [Canonical Protocol](../AI_COLLABORATION.md)

> [!NOTE]
> `AI_COLLABORATION.md` is the canonical, non-negotiable rulebook. This guide provides practical application context for AI assistants.

---

## Primary Objective

Leave the repository in a fully interpretable and verifiable state for any future session (human or AI). **The repository is the memory; the conversation is merely the execution channel.**

---

## Minimal Session Startup

1. Read [`AI_COLLABORATION.md`](../AI_COLLABORATION.md), [`.ai/HANDOFF.md`](../.ai/HANDOFF.md), and [`.ai/state/estado-dev.md`](../.ai/state/estado-dev.md).
2. If a formal task exists, consult its `task.md` and execution plan.
3. Use `tools/continuum context` to guide initial reading.
4. Consult code, memory topic files, and additional technical docs **only when addressing a specific need**.

---

## Workflow Selection

- **Small/trivial change**: Work directly without creating a formal task directory.
- **Medium/complex change**: Create or resume a formal task (`tools/continuum task start <slug>`).
- **Architectural change**: Use an execution plan (`execution-plan.md`) as a persistent step list.

---

## Memory Logging and Handoffs

Record non-inferrible decisions: discarded alternatives, product boundaries, risks, validations, and next steps.

> [!CAUTION]
> **Privacy and Security:**
> Never record secrets, credentials, personal data, local absolute paths, raw chat transcripts, or confidential information in versioned memory.

Upon interruption or session conclusion:
- Update `.ai/HANDOFF.md`.
- Complete the task handoff in `.ai/tasks/<slug>/handoff.md` before closing.
- List executed and pending unit/integration tests.

---

## Coordination and Handoff Checklist

1. Execute validations proportional to the changes made.
2. Inspect Git diff (`git status`, `git diff`) and clean untracked or temporary files.
3. Run `tools/continuum doctor` if protocol, memory, or `.ai/` infrastructure was modified.
4. Log results and pending risks in the handoff.
5. Defer commits, merges, and pushes to the authorized developer (unless explicitly granted).

---

<div align="center">

Continuum · [MIT License](../LICENSE)

</div>
