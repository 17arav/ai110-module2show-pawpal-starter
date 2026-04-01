from datetime import date, datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task

def test_mark_complete():
    task = Task(name="Walk", task_type="walk", duration=30, priority=5, recurring=True, pet_name="Buddy")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True

def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.get_tasks()) == 0
    task = Task(name="Walk", task_type="walk", duration=30, priority=5, recurring=True, pet_name="Buddy")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_sort_by_time():
    owner = Owner(name="Ava", available_time=120)
    scheduler = Scheduler(owner=owner)

    task_early = Task(
        name="Morning walk",
        task_type="walk",
        duration=30,
        priority=3,
        recurring=False,
        pet_name="Buddy",
        time_slot=datetime(2026, 4, 1, 8, 0),
    )
    task_late = Task(
        name="Evening play",
        task_type="play",
        duration=30,
        priority=2,
        recurring=False,
        pet_name="Buddy",
        time_slot=datetime(2026, 4, 1, 18, 0),
    )
    task_unscheduled = Task(
        name="Unscheduled grooming",
        task_type="groom",
        duration=20,
        priority=1,
        recurring=False,
        pet_name="Buddy",
    )

    scheduler.tasks = [task_late, task_unscheduled, task_early]
    scheduler.sort_by_time()

    assert scheduler.tasks[0] is task_early
    assert scheduler.tasks[1] is task_late
    assert scheduler.tasks[2] is task_unscheduled


def test_sort_by_priority():
    owner = Owner(name="Ava", available_time=120)
    scheduler = Scheduler(owner=owner)

    low_priority = Task(
        name="Low",
        task_type="care",
        duration=15,
        priority=1,
        recurring=False,
        pet_name="Buddy",
    )
    high_priority = Task(
        name="High",
        task_type="care",
        duration=15,
        priority=10,
        recurring=False,
        pet_name="Buddy",
    )
    medium_priority = Task(
        name="Medium",
        task_type="care",
        duration=15,
        priority=5,
        recurring=False,
        pet_name="Buddy",
    )

    scheduler.tasks = [low_priority, high_priority, medium_priority]
    scheduler.sort_by_priority()

    assert scheduler.tasks[0] is high_priority
    assert scheduler.tasks[1] is medium_priority
    assert scheduler.tasks[2] is low_priority


def test_recurring_task():
    original_due = date(2026, 4, 1)
    task = Task(
        name="Daily meds",
        task_type="medication",
        duration=10,
        priority=5,
        recurring=True,
        pet_name="Buddy",
        due_date=original_due,
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == original_due + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.time_slot is None


def test_conflict_detection():
    owner = Owner(name="Ava", available_time=120)
    scheduler = Scheduler(owner=owner)

    task_one = Task(
        name="Morning walk",
        task_type="walk",
        duration=30,
        priority=3,
        recurring=False,
        pet_name="Buddy",
        time_slot=datetime(2026, 4, 1, 9, 0),
    )
    task_two = Task(
        name="Vet check",
        task_type="vet",
        duration=30,
        priority=4,
        recurring=False,
        pet_name="Buddy",
        time_slot=datetime(2026, 4, 1, 9, 0),
    )

    scheduler.daily_plan = {"Buddy": [task_one, task_two]}
    conflicts = scheduler.detect_conflicts()

    assert task_one in conflicts
    assert task_two in conflicts
    assert len(conflicts) == 2


def test_empty_pet_schedule():
    owner = Owner(name="Ava", available_time=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    scheduler.generate_plan()

    assert scheduler.daily_plan == {}
