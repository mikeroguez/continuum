# Guide for agents working with Continuum

> [Leer en español](guia-para-agentes.md)

**Source version:** `c85cf9a`. The Spanish guide is canonical if the two versions differ.

`AI_COLLABORATION.md` contains mandatory rules. This guide explains how to apply them. If they differ, follow the canonical file.

## Goal

Leave the repository in a state that another session can understand and verify. Do not preserve important information only in the conversation.

## Minimal start

1. Read `AI_COLLABORATION.md`, `.ai/HANDOFF.md`, and `.ai/state/estado-dev.md`.
2. If a task exists, read its `task.md` and plan.
3. Use `tools/continuum context --task <slug> --why` to guide further reading.
4. Open topics, code, and additional documentation only when a concrete task need requires them.

Do not load every topic or repeat in a handoff what the diff or tests already establish.

## Choose the workflow

A small, clear change can be handled without a task folder. If it spans a module, several files, risk, or ambiguity, create or resume a task. For large work, use the execution plan as a persistent work queue.

## What to record

Record non-inferable decisions: rejected alternatives, product boundaries, risks, validation, and the next step. Do not record secrets, personal data, local paths, chat transcripts, internal reasoning, or third-party information without authorisation.

When interrupted or finished, update the general handoff, complete a formal task handoff before closing it, and name validation that ran or remains pending. A short exact handoff is better than a long chronicle.

## Rules and documentation

- Treat `AI_COLLABORATION.md` as a map of non-negotiable rules.
- Treat `estado-dev.md` as an index, not a history.
- Treat topics and `docs/` as on-demand sources.
- When a rule is critical and recurring, prefer a test, linter, hook, or CI check over more prose.

Do not invent rules to fill gaps. Ask for direction before changing scope, publishing, deleting, disclosing information, or taking irreversible action.

## Coordination and closure

Declare the task and owner when more than one person or agent is involved. Use a branch or worktree for concurrent work. A claim provides visibility; it does not authorise overwriting another person’s work.

A role is a working lens, not a concurrent subprocess. Inspect enabled packs with `tools/continuum roles list`; record a role when starting a task or handoff. `roles sync` generates local Claude Code artifacts that must never be edited manually or committed to Git.

Before proposing completion, run validation proportional to the change, inspect the diff and untracked files, run `tools/continuum doctor` when protocol, memory, or tasks changed, and record residual risk. Leave commits, publication, deployment, and external actions to whoever holds that authority.

## Signals to simplify

Simplify when startup context grows, an instruction repeats repository information, or a small task creates too many files. Split memory by topic and keep only non-inferable facts and necessary actions in the protocol.
