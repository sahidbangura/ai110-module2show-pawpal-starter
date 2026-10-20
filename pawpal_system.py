"""PawPal+ logic layer: Task, Pet, Owner and Scheduler."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Optional

RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str  # "HH:MM", 24-hour
    frequency: str = "once"  # "once", "daily" or "weekly"
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> Optional["Task"]:
        """Mark done and return the next occurrence for recurring tasks, else None."""
        self.completed = True
        days = RECURRENCE_DAYS.get(self.frequency)
        if days is None:
            return None
        return replace(self, completed=False, due_date=self.due_date + timedelta(days=days))


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """A person who owns one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None."""
        return next((p for p in self.pets if p.name == name), None)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Organizes, filters and checks tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Fetch all tasks via the Owner so every pet is included."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by date, then by "HH:MM" time (zero-padded strings sort correctly)."""
        tasks = self.get_all_tasks() if tasks is None else tasks
        return sorted(tasks, key=lambda t: (t.due_date, t.time))

    def filter_tasks(self, pet_name: Optional[str] = None,
                     completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status (None means no filter)."""
        return [
            t for t in self.get_all_tasks()
            if (pet_name is None or t.pet_name == pet_name)
            and (completed is None or t.completed == completed)
        ]

    def get_todays_schedule(self, on_date: Optional[date] = None) -> List[Task]:
        """Return incomplete tasks due on the given date (default today), sorted by time."""
        on_date = on_date or date.today()
        due = [t for t in self.filter_tasks(completed=False) if t.due_date == on_date]
        return self.sort_by_time(due)

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for incomplete tasks sharing the same date and time."""
        slots = {}
        for t in self.filter_tasks(completed=False):
            slots.setdefault((t.due_date, t.time), []).append(t)
        return [
            f"Warning: {len(group)} tasks at {time} on {day}: "
            + ", ".join(f"{t.description} ({t.pet_name})" for t in group)
            for (day, time), group in sorted(slots.items())
            if len(group) > 1
        ]

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task and, if it recurs, add the next occurrence to its pet."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(next_task)
        return next_task
