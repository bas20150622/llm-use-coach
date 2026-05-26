# LLM Use Coach

## What this is

A coaching system that helps you become a better LLM collaborator. After a Claude Code session, you invoke `/coach` and an AI coach analyzes *your* side of the conversation — how you prompted, steered, corrected, and directed the work. It gives you specific, evidence-based feedback grounded in what actually happened.

This is not a tool for improving the LLM's responses. It's a tool for improving *you*.

## Why it exists

Working with LLMs is a skill. Like any skill, it improves faster with deliberate practice and honest feedback. Most people develop prompting habits unconsciously — some effective, some wasteful. Without a feedback loop, bad habits persist and good instincts go unrecognized.

The transcripts of your sessions contain a complete record of how you collaborate with LLMs. This system reads that record and coaches you on it.

## The coaching model

Three psychological principles drive the design:

### 1. Deliberate practice loop

Passive feedback doesn't change behavior. Each coaching session ends with situational advice — "next time you're in a situation like X, try Y." This is guidance, not homework. If the advice doesn't align with what you're working on in your next session, it's irrelevant and should be ignored. The coach checks whether a relevant situation arose and whether the advice applied — not whether you forced it into an unrelated task. Improvement happens through real project work, not contrived exercises.

### 2. Blind spot surfacing

The most valuable feedback is what you can't see yourself. The coach looks for situational triggers — patterns that correlate with specific conditions (task ambiguity, frustration, unfamiliar domain, time pressure) rather than just naming behaviors. "You always underspecify scope when starting a side task" is more useful than "you sometimes underspecify scope."

### 3. Designed for obsolescence

The explicit goal is that you internalize the coaching and stop needing it. When a dimension reaches "resolved" (consistently high scores, no regressions), it drops out of active coaching. The coach then pushes you toward harder challenges — expanding your range rather than fixing weaknesses. If you're getting the same feedback after 20 sessions, the system has failed.

## Analysis dimensions

Each session is analyzed on five dimensions, scored 1-5:

### Precision (did your prompts land?)
- 5: Every prompt produced useful work on the first try
- 3: Some correction rounds needed, but recoveries were quick
- 1: Multiple prompts required rework, redirects, or interruptions

What to look for: ratio of productive exchanges (approval, forward movement) to correction exchanges (interruptions, negations, redirects). Also: whether corrections were about substance (the LLM did the wrong thing) or communication (the LLM misunderstood what you wanted).

### Context-setting (did you set up success?)
- 5: Constraints, scope, and relevant background stated before the request
- 3: Some context given, but key constraints emerged mid-task
- 1: The LLM had to guess most of the context, leading to rework

What to look for: whether constraints appeared before or after the request. Whether the LLM had to ask clarifying questions that you could have anticipated. Whether you referenced relevant prior work or decisions.

### Scope clarity (did the LLM know the boundaries?)
- 5: Clear boundaries on what to do and what not to do
- 3: Scope was mostly clear but some ambiguity caused drift
- 1: The LLM had to guess scope, built the wrong thing or overbuilt

What to look for: requests where the LLM extended beyond what was asked. Moments where you had to pull it back. Whether "subproject" vs. "extension" type distinctions were made explicit.

### Mode signaling (did you communicate what kind of interaction you wanted?)
- 5: Clear transitions between exploration and execution, appropriate depth at each stage
- 3: Modes were mostly implicit but the LLM adapted
- 1: Mismatch between what you wanted (quick answer vs. deep dive) and what you got

What to look for: whether you signaled intent ("let's explore this" vs. "just do it"). Whether the LLM over-explained during execution or under-explored during design. Whether output format expectations were stated.

### Question quality (did your questions move the work forward?)
- 5: Questions were precise, opened new ground, and shaped decisions
- 3: Questions were reasonable but some were redundant or unfocused
- 1: Questions were vague, leading to generic responses that didn't advance the work

What to look for: questions that triggered architectural insights or pivots (high value). Questions that restated what was already established (low value). Whether compound questions caused confused responses.

## How lessons evolve

Observations follow a lifecycle:

```
observation -> pattern -> principle -> resolved
```

- **Observation**: noted in a single coaching session. "You didn't specify output format in exchange 7."
- **Pattern**: same observation recurs across 3+ sessions. Promoted to a lesson file with score tracking.
- **Principle**: a pattern you've internalized with consistent improvement. Still tracked but no longer actively coached.
- **Resolved**: consistently high scores (4-5) for 5+ sessions. Drops out of active coaching. The coach pushes you toward new challenges.

## Data structure

```
~/.local/share/llm-use-coach/
    README.md              # this file (coaching philosophy)
    state.yaml             # tracks which sessions have been analyzed
    profile.md             # current strengths, growth areas, trajectory
    debriefs/              # per-session coaching output
        YYYY-MM-DD-project-sessionid.md
    lessons/               # promoted patterns with score history
        dimension-slug.md
    scores/                # raw dimension scores per session
        YYYY-MM-DD-project-sessionid.yaml
```

### state.yaml format

```yaml
analyzed:
  session-uuid-1:
    project: second-brain
    date: 2026-05-25
    debrief: 2026-05-25-second-brain-session-uuid-1.md
  session-uuid-2:
    ...
advice_next: "Specify output format before requesting explanations"
```

### Score file format

```yaml
session: session-uuid
project: second-brain
date: 2026-05-25
dimensions:
  precision: 3
  context-setting: 4
  scope-clarity: 2
  mode-signaling: 3
  question-quality: 4
notes: "Scope clarity dropped due to subproject ambiguity in exchange 1"
```

### Lesson file format

```yaml
---
name: scope-clarity-side-tasks
dimension: scope-clarity
status: pattern           # observation | pattern | principle | resolved
occurrences: 3
scores: [2, 2, 3]
first_seen: 2026-05-24
last_seen: 2026-05-26
---

When requesting work that is separate from the current project,
explicitly state that it is a new/separate thing with its own scope.

**Trigger:** tends to happen when branching from an ongoing project
into a side task or subproject.

**Why it matters:** without the boundary, the LLM defaults to extending
the current project, which wastes a correction round.
```

### Profile format

```markdown
# Prompting Profile

## Current strengths
- Question quality: consistently drives architectural decisions
- Context-setting: strong on constraints, improving

## Active growth areas
- Scope clarity: improving (2 -> 3 trend), focus on side-task boundaries
- Mode signaling: stagnant (3 -> 3), experiment with explicit mode declarations

## Resolved
(none yet)

## Trajectory
| Date       | Project      | Prec | Ctx | Scope | Mode | Quest |
|------------|--------------|------|-----|-------|------|-------|
| 2026-05-24 | second-brain |    3 |   4 |     2 |    3 |     4 |
| 2026-05-25 | second-brain |    4 |   4 |     3 |    3 |     4 |

## Advice log
| Date       | Advice given                                              | Situation arose? | Result        |
|------------|-----------------------------------------------------------|------------------|---------------|
| 2026-05-24 | When starting a side task, state it's separate from current scope | Yes              | Improved to 3 |
```

## How to use

From any Claude Code session:

```
/coach
```

The coach analyzes the current project's session transcripts, compares against your history, and produces a coaching session. Run it at the end of a work session, or periodically during long projects.

The output is a coaching dialogue, not a report. It tells you what to do more of, what to do less of, whether you're improving, and what to focus on next.
