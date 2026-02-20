# Задача

## Заголовок
- [ ] Приоритет: Краткое описание задачи

## Атрибуты
- status: backlog | in_progress | done | failed
- priority: 1-5
- assignee: agent_pm | subagent
- depends_on: [task_id]  # Опционально, для зависимостей

## Подзадачи
- - [ ] Подзадача 1
- - [ ] Подзадача 2

## Результат (заполняется после выполнения)
- result: Описание результата
- completed_at: YYYY-MM-DDTHH:MM:SSZ

## Пример
```markdown
- [ ] 1. Автономность: Научиться чистить Chromium без напоминаний
  - status: in_progress
  - priority: 1
  - assignee: agent_pm
  - subtasks:
    - - [ ] Проверить размер профиля
    - - [ ] Удалить старые файлы
    - - [ ] Проверить результат
```
