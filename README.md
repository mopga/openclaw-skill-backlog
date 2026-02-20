# OpenClaw Backlog Skill

Task orchestration system for autonomous AI agents.

## Quick Start

### 1. Install
```bash
cp -r backlog %OPENCLAW_HOME%/workspace/skills/
```

### 2. Configure HEARTBEAT
Add to `HEARTBEAT.md`:
```
CHECK: Every heartbeat → Run: python3 %OPENCLAW_HOME%/workspace/backlog/src/agent_pm.py
```

### 3. Create First Task
Add to `backlog/2026-02-19.md`:
```markdown
- [ ] Автономность: Почистить Chromium профиль
  - status: backlog
  - priority: 1
```

## Usage

### Add Task
Just create/edit any `YYYY-MM-DD.md` file in backlog directory:
```markdown
- [ ] Скиллы: Добавить новый скилл
  - status: backlog
  - priority: 4
```

### Check Status
```bash
python3 %OPENCLAW_HOME%/workspace/backlog/src/agent_pm.py --status
```

### Manual Scan
```bash
python3 %OPENCLAW_HOME%/workspace/backlog/src/agent_pm.py --scan
```

## Configuration

Edit `backlog-config.json` or environment:
- `BACKLOG_DIR` — Directory for backlog files (default: `%OPENCLAW_HOME%/workspace/backlog`)
- `HEARTBEAT_INTERVAL` — How often to check (default: 600 seconds)

## Example Output

```
🎯 Backlog PM started
📁 Scanning: %OPENCLAW_HOME%/workspace/backlog/
📋 Found 3 tasks (2 backlog, 1 in_progress)
  
▶️ Task: "Почистить Chromium профиль"
  Status: in_progress → done
  Result: Освобождено 92MB
```

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Full documentation |
| `README.md` | This file |
| `src/agent_pm.py` | Main script |
| `templates/task.md` | Task template |

## Requirements

- Python 3.8+
- OpenClaw (for sub-agent spawning)
- Beads (optional, for dependencies)

## License

MIT
