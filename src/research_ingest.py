#!/usr/bin/env python3
"""
Backlog Research Ingest - Adds research tasks to backlog

Runs periodically, executes research, and adds findings as backlog tasks.
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

BACKLOG_DIR = '%OPENCLAW_HOME%/workspace/backlog'
TODAY = datetime.now().strftime('%Y-%m-%d')
BACKLOG_FILE = f'{BACKLOG_DIR}/{TODAY}.md'

TOPICS = {
    'moltbook': 'Исследовать Moltbook для идей по улучшению агента',
    'reddit': 'Исследовать Reddit (r/LocalLLaMA, r/ArtificialIntelligence) для трендов',
    'hn': 'Исследовать Hacker News для AI/ML трендов',
}


def get_research(topic: str) -> list:
    """Run research and return findings."""
    # Simple duck-search based research
    queries = {
        'moltbook': 'AI agents self-improvement best practices 2026',
        'reddit': 'LLM agents architecture trends 2026',
        'hn': 'AI agent memory management 2026'
    }
    
    findings = []
    try:
        result = subprocess.run(
            ['python3', '-c', f'''
import subprocess
result = subprocess.run(
    ["duck-search", "--query", "{queries.get(topic, topic)}", "--count", "3"],
    capture_output=True, text=True, timeout=30
)
print(result.stdout)
'''],
            capture_output=True, text=True, timeout=35
        )
        
        # Parse results - simple extraction
        for line in result.stdout.split('\n')[:5]:
            if 'http' in line:
                findings.append(line.strip())
                
    except Exception as e:
        print(f"Research error for {topic}: {e}")
        
    return findings


def add_to_backlog(task_title: str, priority: int = 3) -> bool:
    """Add a task to today's backlog file."""
    
    # Create file if doesn't exist
    if not os.path.exists(BACKLOG_FILE):
        with open(BACKLOG_FILE, 'w') as f:
            f.write(f"# {TODAY} — Daily Backlog\n\n")
    
    # Check for duplicates
    with open(BACKLOG_FILE, 'r') as f:
        content = f.read()
    
    if task_title.lower() in content.lower():
        print(f"  ⏭️ Duplicate skipped: {task_title[:40]}...")
        return False
    
    # Add task
    with open(BACKLOG_FILE, 'a') as f:
        f.write(f"\n- [ ] {priority}. Автономность: {task_title}\n")
        f.write(f"  - status: backlog\n")
        f.write(f"  - priority: {priority}\n")
        f.write(f"  - source: research_ingest\n")
        f.write(f"  - added_at: {datetime.now().isoformat()}Z\n")
    
    return True


def main():
    print(f"🎯 Backlog Research Ingest")
    print(f"   Date: {TODAY}")
    print(f"   File: {BACKLOG_FILE}")
    
    added = 0
    
    for topic, task in TOPICS.items():
        print(f"\n📡 Research: {topic}")
        findings = get_research(topic)
        
        if findings:
            # Add main task
            if add_to_backlog(task, priority=3):
                added += 1
                print(f"   ✅ Added: {task[:40]}...")
            
            # Add findings as subtasks or related tasks
            for i, finding in enumerate(findings[:2]):
                related_task = f"{topic}: {finding[:50]}"
                if add_to_backlog(related_task, priority=4):
                    added += 1
        else:
            print(f"   ⚠️ No findings")
    
    print(f"\n✅ Done: {added} tasks added to backlog")


if __name__ == '__main__':
    main()
