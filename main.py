"""CLI demo for the PawPal+ logic layer."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title, tasks):
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("  (none)")
    for t in tasks:
        mark = "x" if t.completed else " "
        print(f"  [{mark}] {t.time}  {t.pet_name:<8} {t.description:<16} "
              f"{t.duration_minutes:>3} min  {t.priority:<6} {t.frequency}")


def main():
    owner = Owner("Jordan")
    mochi, whiskers = Pet("Mochi", "dog"), Pet("Whiskers", "cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # Added deliberately out of order; two tasks share 08:00 to trigger a conflict.
    mochi.add_task(Task("Evening walk", "18:00", "daily", duration_minutes=30))
    mochi.add_task(Task("Morning walk", "08:00", "daily", duration_minutes=30, priority="high"))
    whiskers.add_task(Task("Breakfast", "08:00", "daily", duration_minutes=10, priority="high"))
    whiskers.add_task(Task("Flea medicine", "12:30", "weekly", duration_minutes=5))

    scheduler = Scheduler(owner)
    print_tasks("Today's Schedule", scheduler.get_todays_schedule())

    print("\nConflict check")
    print("--------------")
    for warning in scheduler.detect_conflicts() or ["No conflicts."]:
        print(f"  {warning}")

    breakfast = scheduler.filter_tasks(pet_name="Whiskers")[0]
    nxt = scheduler.mark_task_complete(breakfast)
    print(f"\nCompleted '{breakfast.description}'; next occurrence created for {nxt.due_date}.")

    print_tasks("Whiskers' tasks (filtered by pet)", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Whiskers")))
    print_tasks("Completed tasks (filtered by status)", scheduler.filter_tasks(completed=True))


if __name__ == "__main__":
    main()
