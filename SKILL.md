# Backlog — Task Orchestration System

**Manage tasks, decompose goals, and coordinate sub-agents autonomously.**

## Overview

Backlog is a task management system for AI agents. It tracks incoming tasks, decomposes them into subtasks, and executes them via sub-agents — all autonomously.

## Key Features

- 📋 **Backlog Management** — All tasks in structured daily files
- 🔄 **Auto-Decomposition** — Breaks complex tasks into actionable subtasks  
- 🤖 **Sub-Agent Coordination** — Spawns and monitors sub-agents
- 📊 **Beads Integration** — Task dependencies via DAG
- 🎯 **Priority System** — Autonomy, Stability, Optimization, Skills, Security

## Concept

### Directory Structure
```
backlog/
├── BACKLOG.md           # Methodology + global tasks
├── 2026-02-19.md        # Daily task file
├── src/
│   └── agent_pm.py       # Main PM agent
├── templates/            # Task templates
└── examples/            # Usage examples
```

### Task Format
```markdown
- [ ] Автономность: Научиться запускать Chromium без напоминаний
  - status: backlog → in_progress → done|failed
  - subtasks: [...]
  - assignee: agent_pm | subagent
```

### Workflow
1. **HEARTBEAT** triggers agent_pm every ~10 minutes
2. agent_pm scans `/backlog/*.md` files for `backlog` tasks
3. Decomposes complex tasks → subtasks
4. Spawns sub-agents via `sessions_spawn`
5. Sub-agent completes → updates status in file
6. Cycle repeats

## Installation

```bash
# Copy to skills directory
cp -r backlog %OPENCLAW_HOME%/workspace/skills/

# Configure (optional)
# Edit backlog-config.json for paths and priorities
```

## Commands

### From HEARTBEAT
Add to `HEARTBEAT.md`:
```
CHECK: Every heartbeat → Run: python3 %OPENCLAW_HOME%/workspace/backlog/src/agent_pm.py
```

### Manual Run
```bash
python3 %OPENCLAW_HOME%/workspace/backlog/src/agent_pm.py --scan
```

## Priority Directions

1. **Автономность (Autonomy)** — Self-management, proactive actions
2. **Стабильность (Stability)** — Reliability, error recovery
3. **Оптимизация (Optimization)** — Performance, cost, efficiency
4. **Скиллы (Skills)** — New capabilities, integrations
5. **Безопасность (Security)** — Protection, access control

## Integration with Beads

Backlog uses Beads for task dependency tracking:

```python
# Tasks with dependencies
- [ ] Deploy: Задеплоить новую версию
  - depends_on: ["build:1.2.3"]  # Beads reference
```

## Files

- `BACKLOG.md` — Methodology and global tasks
- `YYYY-MM-DD.md` — Daily task files
- `agent_pm.py` — Main orchestration script
- `templates/task.md` — Task template

## Example

### Creating a Task
```markdown
# In 2026-02-19.md
- [ ] Оптимизация: Сжать логи при заполнении диска
  - status: backlog
  - priority: 2
  - assignee: agent_pm
```

### Agent PM Execution
```
🎯 HEARTBEAT → Scanning backlog...
📋 Found 1 backlog task: "Сжать логи при заполнении диска"
🔄 Decomposing → ["Найти большие логи", "Сжать архив", "Удалить старые"]
▶️ Spawning sub-agent for: "Найти большие логи"
```

## Output

Results are written back to the daily file:
```markdown
- [x] Оптимизация: Сжать логи при заполнении диска
  - status: done
  - result: Освобождено 2GB, удалены логи старше 30 дней
  - completed_at: 2026-02-19T10:30:00Z
```

---

**Part of OpenClaw ecosystem** — Made by Kleshnya 🦞
