#!/usr/bin/env python3
"""
Backlog Agent PM - Entry Point

This script is designed to be run as a sub-agent via cron.
It picks a task and hands it off to the agent for real execution.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

BACKLOG_DIR = '%OPENCLAW_HOME%/workspace/backlog'


# Schema for task result validation (2.3.1)
TASK_RESULT_SCHEMA = {
    "required_fields": ["status", "result"],
    "valid_statuses": ["done", "backlog", "in_progress", "blocked"]
}


def validate_task_result(task_data: dict[str, Any]) -> tuple[bool, str]:
    """
    Validate task result against schema.
    Returns (is_valid, error_message).
    """
    # Check required fields
    for field in TASK_RESULT_SCHEMA["required_fields"]:
        if field not in task_data:
            return False, f"Missing required field: {field}"
    
    # Validate status
    status = task_data.get("status", "")
    if status not in TASK_RESULT_SCHEMA["valid_statuses"]:
        return False, f"Invalid status: {status}. Must be one of {TASK_RESULT_SCHEMA['valid_statuses']}"
    
    # Validate result is not empty for done tasks
    if status == "done" and not task_data.get("result", "").strip():
        return False, "Result cannot be empty for done tasks"
    
    return True, ""


def validate_output(output: Any) -> dict[str, Any]:
    """
    Validate subagent output.
    Part of 2.3.1 Subagent Quality Gates - Output Validation.
    """
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check output type
    if output is None:
        validation_result["valid"] = False
        validation_result["errors"].append("Output is None")
        return validation_result
    
    # If output is a dict, validate as task result
    if isinstance(output, dict):
        is_valid, error = validate_task_result(output)
        if not is_valid:
            validation_result["valid"] = False
            validation_result["errors"].append(error)
    
    # Check for empty output
    if isinstance(output, str) and not output.strip():
        validation_result["warnings"].append("Output is empty string")
    
    return validation_result


# Retry configuration (2.3.2)
MAX_RETRIES = 2
RETRY_DELAYS = [1, 2]  # seconds between retries


def retry_with_backoff(func, max_retries: int = MAX_RETRIES, retry_delays: list = RETRY_DELAYS):
    """
    Retry decorator with exponential backoff.
    Part of 2.3.2 Subagent Quality Gates - Retry Logic.
    """
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                result = func(*args, **kwargs)
                # Validate output before returning
                validation = validate_output(result)
                if validation["valid"]:
                    return result
                else:
                    print(f"⚠️ Output validation failed: {validation['errors']}")
                    if attempt < max_retries:
                        print(f"🔄 Retrying... (attempt {attempt + 1}/{max_retries})")
                    last_exception = Exception(f"Validation failed: {validation['errors']}")
            except Exception as e:
                last_exception = e
                print(f"❌ Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries:
                delay = retry_delays[min(attempt, len(retry_delays) - 1)]
                import time
                time.sleep(delay)
        
        raise last_exception
    return wrapper


# Timeout configuration (2.3.3)
DEFAULT_TIMEOUT = 30  # seconds


class TimeoutError(Exception):
    """Raised when function execution exceeds timeout."""
    pass


def timeout_handler(seconds: int = DEFAULT_TIMEOUT):
    """
    Timeout decorator using signal (Unix) or threading (Windows).
    Part of 2.3.3 Subagent Quality Gates - Timeout Handling.
    """
    import signal
    import threading
    
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError(f"Function {func.__name__} timed out after {seconds}s")
        
        def wrapper(*args, **kwargs):
            # Set the signal handler
            old_handler = signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            return result
        return wrapper
    return decorator


# Error recovery (2.3.4)
ERROR_RECOVERY_STRATEGIES = {
    "retry": lambda e: ("retry", str(e)),
    "fallback": lambda e: ("fallback", str(e)),
    "skip": lambda e: ("skip", str(e)),
    "abort": lambda e: ("abort", str(e))
}


def error_recovery(func, strategy: str = "retry", fallback_func=None):
    """
    Error recovery wrapper with configurable strategies.
    Part of 2.3.4 Subagent Quality Gates - Error Recovery.
    
    Strategies:
    - retry: Retry the operation (use with retry_with_backoff)
    - fallback: Use fallback_func if provided
    - skip: Return None on error
    - abort: Re-raise the exception
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error in {func.__name__}: {error_msg}")
            
            if strategy == "fallback" and fallback_func:
                print(f"🔄 Using fallback function...")
                return fallback_func(*args, **kwargs)
            elif strategy == "skip":
                print(f"⏭️ Skipping due to error")
                return None
            elif strategy == "abort":
                raise
            else:  # retry or default
                raise  # Let retry_with_backoff handle it
    return wrapper


def get_task_prompt() -> str:
    """Build prompt for the agent to execute a task."""
    return """Ты — Backlog Agent. Выполни одну задачу из бэклога.

1. Найди первую задачу со статусом [ ] в %OPENCLAW_HOME%/workspace/backlog/2026-02-19.md
2. Выполни её по-настоящему
3. Обнови статус в файле:
   - Замени [ ] на [x]
   - Добавь result: <что сделано>
   - Добавь completed_at: <ISO timestamp>

Важно:
- Не просто "требует проработки" — реально сделай
- Если задача сложная — декомпозируй и выполни хотя бы часть
- Используй доступные инструменты (exec, read, write, search)
- После выполнения обязательно обнови файл с задачей

Начни с чтения backlog файла."""
 

def main():
    print("🎯 Backlog Agent PM - Sub-Agent Mode")
    print(f"📁 Backlog: {BACKLOG_DIR}")
    print("\nЭтот скрипт должен вызываться как sub-agent с LLM.")
    print("Команда для cron:")
    print("openclaw sessions spawn --task 'Выполни задачу из бэклога...'")
    print("\nИли добавь в cron как agentTurn с этим промптом.")
    

if __name__ == '__main__':
    main()
