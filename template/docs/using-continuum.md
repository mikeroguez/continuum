# Using Continuum

> [Leer en español](como-usar-continuum.md)

**Source version:** `c85cf9a`. The Spanish guide is canonical if the two versions differ.

Continuum keeps useful project context across sessions, people, and AI assistants. It does not replace Git, tests, or human judgment.

For how an assistant should behave, read the [agent guide](guide-for-agents.md).

## Core files

| File | Purpose | Read it when |
| --- | --- | --- |
| `AI_COLLABORATION.md` | Shared operating rules | Working with an agent |
| `.ai/HANDOFF.md` | What the last session left behind | Resuming work |
| `.ai/state/estado-dev.md` | Short project index | Resuming work |
| `.ai/state/topics/` | Topic detail | A task needs it |

The repository is the shared memory; the conversation is only the execution channel.

## First use

After installation, complete the project-specific configuration and run:

```bash
tools/continuum install-hooks
tools/continuum doctor
```

`doctor` checks the protocol, entrypoints, memory, and tasks. Resolve critical findings before relying on Continuum for important work.

## Daily workflow

Resume with:

```bash
tools/continuum session start
tools/continuum status
```

For a registered task:

```bash
tools/continuum context --task my-task --why
```

Do not read all of `.ai/` by default. The index and `context` identify the relevant material.

| Scope | Recommended action |
| --- | --- |
| Small, clear change | Work directly and leave a handoff. |
| One module or several files | Create a `medium` task. |
| Multiple domains, risk, or ambiguity | Create a `large` task and use its plan. |

```bash
tools/continuum task start my-task --size medium
tools/continuum task claim my-task ana
```

A claim provides visibility; it does not lock files or replace human coordination.

Before ending a session, record continuity:

```bash
tools/continuum handoff --message "what changed and what comes next"
tools/continuum task close my-task
```

The second command is for formal tasks. Review generated handoffs and complete decisions, validation, risks, and the next step.

## Useful commands

| Command | Use it for |
| --- | --- |
| `status` | State and a suggested next action. |
| `doctor` | Structure, freshness, and context. |
| `context --why` | What to read and why. |
| `tokens` | Estimated context cost. |
| `task current` | Resuming open work. |
| `metrics report` | Local signals, not scientific evidence. |

Run `tools/continuum --help` for the complete list. Review commands that write, synchronise, publish, or change configuration before applying them.

## Adopt gradually

Start with `HANDOFF.md` and `estado-dev.md`; add tasks when scope or collaboration requires them, and roles only when useful. Measure only to answer a concrete question: metrics neither evaluate people nor prove effectiveness on their own.

## Development teams: use cases and prompts

Continuum lets context survive a change of person, session, or assistant. It
does not replace team conversation or code review: it makes agreements,
changes, and pending validation visible.

| Situation | Recommended use |
| --- | --- |
| A developer starts a feature and an agent implements it | Create a task for `medium` or `large` scope, state the outcome, and ask the agent to read relevant repository context before editing. |
| Another agent or developer resumes partial work | Check `session start`, the handoff, and the task; have the new owner confirm their understanding before continuing. |
| Two changes proceed at once | Use separate branches or worktrees and task slugs; a `claim` shows ownership, while the team still coordinates boundaries. |
| An agent reviews a contribution | Ask it to inspect the diff, tests, and risks within its scope; it must not assume authority to publish or merge. |
| A session or task ends | Record decisions, validation, and the next step in the handoff; close the formal task when ready. |

### Writing useful prompts

A prompt does not need to repeat the protocol. State the expected outcome,
boundaries, and authority, then ask the agent to consult the repository for
details. Replace `<…>` and remove anything that does not apply.

**Start a development task**

```text
Work on <outcome>. Before editing, read the protocol, handoff, and relevant
repository context. Confirm whether the scope requires a formal task. Stay
within <boundaries>. Run relevant validation and leave a clear handoff. Do not
commit, merge, or publish without my approval.
```

**Resume after an interruption or with another assistant**

```text
Resume task <slug>. First read the handoff, task.md, and the context they
identify. Summarise the current state, decisions, and remaining work before
changing files. Preserve scope; if a decision or authority is missing, stop and
ask. When done, update the handoff with tests and the next step.
```

**Parallel work in a team**

```text
You own <slug> within <larger outcome>. Check ownership, boundaries, and
existing changes before editing. Work only in <areas or files>; do not overwrite
other tasks' work. Use an isolated branch or worktree when appropriate. Report
dependencies, validation, and risks in the handoff.
```

**Agent review or testing**

```text
Review <change or task> without changing it unless I authorise that later. Read
the relevant protocol and handoff; inspect the diff and run proportionate tests.
Return concrete findings, risks, and missing tests. Do not approve or publish
changes for me.
```

Prompts work best when they name a task or verifiable outcome. Do not paste
complete chat histories, secrets, personal data, or conflicting instructions:
the repository and its handoffs are the continuity source.

## Safety and teamwork

Use branches and Git worktrees for concurrent work. Do not put secrets, personal data, local paths, sensitive prompts, or third-party information into versioned handoffs, tasks, or metrics. If the process becomes ceremonial, reduce task structure but preserve a useful note for the next session.
