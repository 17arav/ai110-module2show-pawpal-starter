from datetime import datetime, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

# Create an owner
owner = Owner(name="Alex", available_time=120, preferences=["walks", "playtime"])

# Create two pets
dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5, special_needs="Indoor only")

owner.add_pet(dog)
owner.add_pet(cat)

# Add tasks OUT OF ORDER to test sorting
walk = Task(name="Morning Walk", task_type="walk", duration=30, priority=5, recurring=True, pet_name="Buddy",
            time_slot=datetime(2026, 4, 1, 8, 0), due_date=date.today())
feed_dog = Task(name="Breakfast", task_type="feeding", duration=10, priority=4, recurring=True, pet_name="Buddy",
                time_slot=datetime(2026, 4, 1, 7, 0), due_date=date.today())
meds = Task(name="Flea Medication", task_type="meds", duration=5, priority=3, recurring=False, pet_name="Buddy",
            time_slot=datetime(2026, 4, 1, 9, 0), due_date=date.today())

feed_cat = Task(name="Cat Breakfast", task_type="feeding", duration=10, priority=4, recurring=True, pet_name="Whiskers",
                time_slot=datetime(2026, 4, 1, 7, 0), due_date=date.today())
grooming = Task(name="Brushing", task_type="grooming", duration=15, priority=2, recurring=False, pet_name="Whiskers",
                time_slot=datetime(2026, 4, 1, 10, 0), due_date=date.today())

dog.add_task(walk)
dog.add_task(feed_dog)
dog.add_task(meds)
cat.add_task(feed_cat)
cat.add_task(grooming)

scheduler = Scheduler(owner=owner)
scheduler.generate_plan()

# Test sorting by time
print("=" * 50)
print("  TASKS SORTED BY TIME")
print("=" * 50)
scheduler.sort_by_time()
for t in scheduler.tasks:
    time_str = t.time_slot.strftime("%H:%M") if t.time_slot else "No time"
    print(f"  {time_str} - {t.name} ({t.pet_name})")

# Test filtering
print("\n" + "=" * 50)
print("  BUDDY'S TASKS ONLY")
print("=" * 50)
buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
for t in buddy_tasks:
    print(f"  {t.name} ({t.task_type}, priority {t.priority})")

# Test recurring task
print("\n" + "=" * 50)
print("  RECURRING TASK TEST")
print("=" * 50)
print(f"  Before: {walk.name} due {walk.due_date}, completed={walk.completed}")
next_task = walk.mark_complete()
print(f"  After:  {walk.name} due {walk.due_date}, completed={walk.completed}")
if next_task:
    print(f"  Next:   {next_task.name} due {next_task.due_date}, completed={next_task.completed}")

# Test conflict detection
print("\n" + "=" * 50)
print("  CONFLICT DETECTION")
print("=" * 50)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        time_str = c.time_slot.strftime("%H:%M") if c.time_slot else "No time"
        print(f"  ⚠️ Conflict: {c.name} ({c.pet_name}) at {time_str}")
else:
    print("  No conflicts detected.")

# Full schedule
print("\n" + "=" * 50)
print("  FULL SCHEDULE")
print("=" * 50)
print(scheduler.explain_plan())
