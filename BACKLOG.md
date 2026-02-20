# Backlog Methodology

## Overview

Backlog is a task management system for autonomous AI agents. All tasks are stored in structured files, the PM agent decomposes them and coordinates sub-agents.

## Core Principles

### 1. Declarativeness
- Tasks describe **what to do**, not how
- Agent decides how to execute

### 2. Autonomy
- Agent finds tasks in backlog itself
- Decomposes and executes
- Reports results itself

### 3. Transparency
- All tasks in files (readable, versionable)
- Easy to view history and progress

### 4. Portability
- System not tied to a specific agent
- Can be copied and used elsewhere

## Directory Structure

```
backlog/
├── BACKLOG.md              # This file - methodology
├── YYYY-MM-DD.md          # Daily task files
├── src/
│   └── agent_pm.py       # Main PM agent
├── templates/
│   └── task.md           # Task template
└── examples/
    └── usage.md          # Usage examples
```

## Task Format

```markdown
- [ ] Priority: Task description
  - status: backlog | in_progress | done | failed
  - priority: 1-5
  - assignee: agent_pm | subagent
```

### Checkbox States
- `[ ]` — backlog (new task)
- `[~]` — in_progress (working)
- `[x]` — done (completed)
- `[-]` — failed

## Priority Directions

| # | Direction | Description |
|---|-----------|-------------|
| 1 | Autonomy | Self-management without reminders |
| 2 | Stability | Reliability, error recovery |
| 3 | Optimization | Performance, cost, efficiency |
| 4 | Skills | New capabilities, integrations |
| 5 | Security | Protection, access control |

## Workflow

### 1. HEARTBEAT (~every 10 minutes)
```
HEARTBEAT → agent_pm.scan() → Find backlog tasks
```

### 2. Decomposition
```
For each backlog task:
  → If has subtasks: go to execution
  → If not: decompose into subtasks
```

### 3. Execution
```
If subtasks:
  → Spawn sub-agent for each subtask
  → sub-agent executes → updates status

If no subtasks:
  → agent_pm executes itself
  → Updates status in file
```

### 4. Result
```
- [x] Priority: Task completed
  - status: done
  - result: Freed 92MB
  - completed_at: 2026-02-20T10:30:00Z
```

## Integration

### With OpenClaw
Add to `HEARTBEAT.md`:
```markdown
CHECK: Every heartbeat → Run: python3 %OPENCLAW_HOME%/workspace/backlog/src/agent_pm.py --heartbeat
```

### With Beads (dependencies)
```python
# In task specify dependency
- [ ] Deploy: Deploy new version
  - depends_on: ["build:1.2.3"]  # Beads ID
```

### With GSD (sub-agent context)
Each sub-agent receives context via GSD-like prompt:
```
Context: Task X from backlog
Goal: Execute subtask Y
Constraints: [constraints]
Expected: [expected result]
```

## Task Lifecycle

```
backlog → in_progress → done
    ↓           ↓          ↓
  new     executing   completed
           (or failed)
```

## Best Practices

1. **One task — one day file** — don't mix dates
2. **Use priorities** — 1 is most important
3. **Write results** — future you will thank you
4. **Decompose** — small tasks are easier to execute
5. **Version** — git for backlog is good

---

**Part of OpenClaw ecosystem** 🦞
