# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three things I wanted a user to be able to do were add a pet, schedule a task for that pet, and see today's tasks in time order. I split the system into four classes:

- `Task`: one activity (description, time, frequency, due date, duration, priority, whether it's done). I made it a dataclass because it's mostly data.
- `Pet`: a name, a species, and a list of tasks.
- `Owner`: holds the pets and has `get_all_tasks()`, which collects every pet's tasks into one list.
- `Scheduler`: the "brain." It takes an `Owner` and handles sorting, filtering, conflicts, and recurring tasks. It only reads tasks through the `Owner`, never from a single pet, so it works across all pets.

**b. Design changes**

Yes, the design changed. I asked for a review of my skeleton looking for missing relationships and bottlenecks, and a few things came out of it:

- The Scheduler works from one flat list of tasks, so it had no way to know which pet a task belonged to. I added `pet_name` to `Task`, set automatically in `Pet.add_task`.
- Recurring tasks need a date to move forward ("today + 1 day"), so I added `due_date`.
- I added `Owner.get_pet` so the Scheduler can put a new recurring task back on the right pet.
- Sorting uses "HH:MM" strings, which only sort correctly if they're well-formed, so `Task` now validates its time and raises an error on something like "8am".

The final diagram is `diagrams/uml_final.mmd`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler cares about date and time of day first. Duration and priority are stored and shown in the UI, but they don't change the order or the conflict checks yet. I put time first because a missed time slot (like a medication) is the most obvious way this app could let an owner down, and time is the easiest constraint to explain and test.

**b. Tradeoffs**

Conflict detection only flags tasks that have the exact same date and `HH:MM`. It ignores duration, so a 30-minute walk at 8:00 and a feeding at 8:15 won't be flagged even though they overlap. I accepted that because the exact-match check is a short, readable grouping of tasks by time slot, it's easy to test, and it returns a warning message instead of blocking the user. Real overlap detection is the next improvement.

When I asked how to simplify that method, one suggestion was a `defaultdict(list)` in place of `setdefault`, which I took because it reads the same or better. A shorter `itertools.groupby` version was also on the table, but it's harder to read at a glance, so I kept the dictionary version.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code for most of the build: drafting the UML, generating the dataclass skeleton, implementing the Scheduler, writing tests, and connecting the Streamlit app. It was also useful as a reviewer, both for the skeleton and for the finished algorithms. The prompts that worked best were specific about the behavior and the contract, for example "the Scheduler must get its tasks through `Owner.get_all_tasks`" or "marking a daily task complete should create a new task for the next day." Vague prompts gave me generic code.

I did this in one continuous session instead of a separate chat per phase. That worked, but I kept the phases organized through the commit history and the README sections. If I did it again I'd start a fresh chat for testing, because the same context that wrote the code tends to agree with it.

**b. Judgment and verification**

I didn't take everything as-is. Two examples:

- I kept the draft diagram at `diagrams/uml.mmd` instead of renaming it `uml_draft.mmd` as the project steps suggest, because the repo history shows it was deliberately renamed to `uml.mmd` for grading.
- I kept `Task` independent from `Pet`. `mark_complete()` just returns the next task, and the Scheduler decides where it goes. That's less compact but keeps each class focused.

For verification I didn't rely on the AI saying it worked. I ran the demo script, ran the pytest suite, and tried the Streamlit app in the browser. Reviewing the finished code also caught a real bug: completing a recurring task twice created duplicate future tasks. I fixed it so a completed task returns nothing, and added a test for it.

---

## 4. Testing and Verification

**a. What you tested**

The 13 tests cover: marking a task complete, adding a task to a pet, collecting tasks across multiple pets, chronological sorting, daily and weekly recurrence, one-off tasks not recurring, completing a task twice, conflict detection (including no false alarms for different times or finished tasks), filtering by pet and status, rejecting a bad time string, and a pet with no tasks. I picked these because each one backs up something the README says the scheduler does.

**b. Confidence**

About 4 out of 5. Everything I thought to test passes, and I also checked the UI by hand. What I haven't tested: overlapping durations, tasks that cross midnight, and month or year rollover for recurrence. Those would be next.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with keeping all the logic in `pawpal_system.py`. The CLI demo, the tests, and the Streamlit app all call the same `Scheduler`, so I never had to duplicate logic, and a bug fixed once was fixed everywhere.

**b. What you would improve**

I'd make conflict detection duration-aware, use priority when ordering tasks, save data to a JSON file so it survives restarts, and add more input validation in the UI.

**c. Key takeaway**

Being the lead architect means deciding the contracts between the classes (the Scheduler reads through the Owner, Task stays separate from Pet) and then checking the AI's output against them. The AI is very fast at producing code, but it won't tell you whether the design is right, and tests are how I found out the difference.
