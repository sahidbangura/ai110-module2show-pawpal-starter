from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler():
    owner = Owner("Jordan")
    dog, cat = Pet("Mochi"), Pet("Whiskers", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return Scheduler(owner), dog, cat


def test_mark_complete_changes_status():
    task = Task("Walk", "08:00")
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi")
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.tasks) == 1
    assert pet.tasks[0].pet_name == "Mochi"


def test_get_all_tasks_spans_pets():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Walk", "08:00"))
    cat.add_task(Task("Feed", "09:00"))
    assert len(scheduler.get_all_tasks()) == 2


def test_sort_by_time_is_chronological():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Evening", "18:00"))
    cat.add_task(Task("Morning", "07:30"))
    dog.add_task(Task("Noon", "12:00"))
    assert [t.time for t in scheduler.sort_by_time()] == ["07:30", "12:00", "18:00"]


def test_daily_task_creates_next_day_occurrence():
    scheduler, dog, _ = make_scheduler()
    task = Task("Walk", "08:00", "daily", due_date=date(2030, 1, 1))
    dog.add_task(task)
    nxt = scheduler.mark_task_complete(task)
    assert nxt.due_date == date(2030, 1, 2) and not nxt.completed
    assert nxt in dog.tasks and nxt is not task


def test_weekly_task_recurs_in_seven_days():
    task = Task("Bath", "10:00", "weekly", due_date=date(2030, 1, 1))
    assert task.mark_complete().due_date == date(2030, 1, 1) + timedelta(days=7)


def test_one_off_task_does_not_recur():
    scheduler, dog, _ = make_scheduler()
    task = Task("Vet", "10:00")
    dog.add_task(task)
    assert scheduler.mark_task_complete(task) is None
    assert len(dog.tasks) == 1


def test_conflict_detected_for_same_time_across_pets():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Walk", "08:00"))
    cat.add_task(Task("Feed", "08:00"))
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1 and "08:00" in warnings[0]


def test_no_conflict_for_different_times_or_completed_tasks():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Walk", "08:00"))
    done = Task("Feed", "08:00")
    cat.add_task(done)
    done.mark_complete()
    cat.add_task(Task("Play", "09:00"))
    assert scheduler.detect_conflicts() == []


def test_filter_by_pet_and_status():
    scheduler, dog, cat = make_scheduler()
    walk = Task("Walk", "08:00")
    dog.add_task(walk)
    cat.add_task(Task("Feed", "09:00"))
    walk.mark_complete()
    assert [t.description for t in scheduler.filter_tasks(pet_name="Whiskers")] == ["Feed"]
    assert scheduler.filter_tasks(completed=True) == [walk]


def test_pet_with_no_tasks():
    scheduler, _, _ = make_scheduler()
    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_completing_twice_does_not_duplicate_recurring_task():
    scheduler, dog, _ = make_scheduler()
    task = Task("Walk", "08:00", "daily")
    dog.add_task(task)
    scheduler.mark_task_complete(task)
    assert scheduler.mark_task_complete(task) is None
    assert len(dog.tasks) == 2


def test_invalid_time_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        Task("Walk", "8am")
