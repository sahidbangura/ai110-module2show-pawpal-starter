# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions: add a pet, schedule a task for a pet, and see today's tasks in time order. Classes: `Task` (a dataclass holding description, time, frequency, due date, duration, priority, completion, pet name), `Pet` (name, species, its tasks), `Owner` (holds pets; `get_all_tasks()` gathers every pet's tasks), and `Scheduler` (the "brain": sorting, filtering, conflicts, recurrence, reading tasks only through the Owner).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. Tasks gained a `pet_name` (set in `Pet.add_task`) so the Scheduler can filter by pet and attach a recurring task to the right pet from a flat task list. I also gave `Task` a `due_date` so recurrence ("today + 1 day") has something to advance, and added `Owner.get_pet`. Final diagram: `diagrams/uml_final.mmd`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers date and time of day first. Duration and priority are stored and shown but do not yet affect ordering or conflicts. I put time first because a missed time slot is the most concrete failure for a pet owner.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Conflict detection only flags tasks with the exact same date and `HH:MM`; it ignores duration, so a 30-minute walk at 08:00 and a feeding at 08:15 are not flagged. That keeps the logic to a dictionary grouping that is easy to read and test, and returns warnings rather than blocking the user. Overlap detection would be the next step.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude Code in a single session to draft the UML, generate the dataclass skeleton, implement the Scheduler, write the tests, and wire up Streamlit. The most helpful prompts named the specific behavior and the contract (e.g. the Scheduler must read through `Owner.get_all_tasks`). *(Edit this to reflect your own experience, including whether you used separate chat sessions per phase.)*

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I kept the draft diagram at `diagrams/uml.mmd` rather than renaming it `uml_draft.mmd` as the instructions suggest, because the repo history shows it was deliberately renamed for grading. I also made `mark_complete()` return the next task instead of having Task know about Pet, keeping Task decoupled. I verified by running `main.py`, the pytest suite, and a headless Streamlit `AppTest` that added a pet and a task.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Completion, task addition, multi-pet retrieval, chronological sorting, daily/weekly/one-off recurrence, conflict detection (including no false positives), filtering, and the empty-pet case. These cover each algorithm the scheduler claims to provide.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

About 4/5. All 11 tests pass. Next I would test overlapping durations, malformed time strings, month/year rollover for recurrence, and completing the same task twice (which currently creates a second next occurrence).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Keeping all logic in `pawpal_system.py` meant the CLI demo, tests, and Streamlit app share the same code with no duplication.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Add duration-aware conflict detection, use priority in ordering, persist data to JSON, and validate time input.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is fast at scaffolding, but the human has to own the architecture: decide the contracts between classes, check them against the repo's constraints, and verify with tests rather than trusting output.

