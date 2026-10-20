# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- **Owner / Pet / Task model** built with dataclasses; one owner manages many pets, each with many tasks.
- **Sorting by time** (`Scheduler.sort_by_time`) – chronological by date then `HH:MM`.
- **Filtering** (`Scheduler.filter_tasks`) – by pet name and/or completion status.
- **Conflict warnings** (`Scheduler.detect_conflicts`) – flags incomplete tasks at the same date and time, for one pet or several. Returns messages; never raises.
- **Recurring tasks** (`Task.mark_complete`, `Scheduler.mark_task_complete`) – completing a daily/weekly task creates the next occurrence (`+1` / `+7` days via `timedelta`).
- **Streamlit UI** (`app.py`) – add pets, schedule tasks, view a sorted/filtered table, see conflict warnings, and mark tasks complete.

## Implementation summary

`pawpal_system.py` holds four classes. `Task` is a dataclass (description, `HH:MM` time, frequency, due date, duration, priority, completed, pet name). `Pet` stores tasks, `Owner` stores pets and exposes `get_all_tasks()`, and `Scheduler` takes an `Owner` and reads every pet's tasks through that method. `main.py` is the CLI demo; `app.py` keeps one `Owner` in `st.session_state` and calls the same `Scheduler` methods. UML: `diagrams/uml.mmd` (initial draft) and `diagrams/uml_final.mmd` (final).

## 🖥️ Sample Output

Output of `python main.py` (tasks are added out of order; two share 08:00):

```
Today's Schedule
----------------
  [ ] 08:00  Mochi    Morning walk      30 min  high   daily
  [ ] 08:00  Whiskers Breakfast         10 min  high   daily
  [ ] 12:30  Whiskers Flea medicine      5 min  medium weekly
  [ ] 18:00  Mochi    Evening walk      30 min  medium daily

Conflict check
--------------
  Warning: 2 tasks at 08:00 on 2026-10-20: Morning walk (Mochi), Breakfast (Whiskers)

Completed 'Breakfast'; next occurrence created for 2026-10-21.

Whiskers' tasks (filtered by pet)
---------------------------------
  [x] 08:00  Whiskers Breakfast         10 min  high   daily
  [ ] 12:30  Whiskers Flea medicine      5 min  medium weekly
  [ ] 08:00  Whiskers Breakfast         10 min  high   daily

Completed tasks (filtered by status)
------------------------------------
  [x] 08:00  Whiskers Breakfast         10 min  high   daily
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The suite (`tests/test_pawpal.py`) covers task completion, task addition, multi-pet task retrieval, chronological sorting, daily and weekly recurrence, one-off tasks not recurring, conflict detection (same time across pets; no false positives for different times or completed tasks), filtering by pet/status, and a pet with no tasks.

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\user\OneDrive - Radford University\Desktop\Code Path\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0, asyncio-1.3.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 11 items

tests\test_pawpal.py ...........                                         [100%]

============================= 11 passed in 0.10s ==============================
```

**Confidence level:** ★★★★☆ (4/5). Core behaviors pass; durations/overlaps, invalid time strings, and month-end edge cases are untested.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time()` | `sorted()` with key `(due_date, time)`; zero-padded `HH:MM` strings sort correctly |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Either or both filters; `None` means no filter |
| Today's plan | `Scheduler.get_todays_schedule()` | Incomplete tasks due today, sorted |
| Conflict handling | `Scheduler.detect_conflicts()` | Exact date+time match only; returns warning strings |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.mark_task_complete()` | `daily` = +1 day, `weekly` = +7 days; new task added to the same pet |

## 📸 Demo Walkthrough

1. Launch with `streamlit run app.py`. The owner is created once and kept in `st.session_state`.
2. Under **Add a pet**, enter a name and species (e.g. Mochi, dog) and submit; a `Pet` is added to the `Owner`.
3. Under **Schedule a task**, choose the pet, description, time, duration, priority and repeat (once/daily/weekly) and submit.
4. **Today's schedule** shows a table sorted by time. Use the pet and status filters to narrow it.
5. If two tasks share a date and time (for any pets), a yellow `st.warning` names them.
6. Pick a task and press **Complete**; daily/weekly tasks get a new instance for the next day/week.

**Screenshot or video** *(optional)*: not included.

CLI output from `python main.py` is shown in the Sample Output section above.
