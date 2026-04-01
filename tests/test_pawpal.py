from pawpal_system import Owner, Pet, Task

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
