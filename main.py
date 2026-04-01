from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

# Create an owner
owner = Owner(name="Alex", available_time=120, preferences=["walks", "playtime"])

# Create two pets
dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5, special_needs="Indoor only")

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create tasks for Buddy
walk = Task(name="Morning Walk", task_type="walk", duration=30, priority=5, recurring=True, pet_name="Buddy",
            time_slot=datetime(2026, 3, 31, 8, 0), due_date=date.today())
feed_dog = Task(name="Breakfast", task_type="feeding", duration=10, priority=4, recurring=True, pet_name="Buddy",
                time_slot=datetime(2026, 3, 31, 7, 0), due_date=date.today())
meds = Task(name="Flea Medication", task_type="meds", duration=5, priority=3, recurring=False, pet_name="Buddy",
            time_slot=datetime(2026, 3, 31, 9, 0), due_date=date.today())

# Create tasks for Whiskers
feed_cat = Task(name="Breakfast", task_type="feeding", duration=10, priority=4, recurring=True, pet_name="Whiskers",
                time_slot=datetime(2026, 3, 31, 7, 0), due_date=date.today())
grooming = Task(name="Brushing", task_type="grooming", duration=15, priority=2, recurring=False, pet_name="Whiskers",
                time_slot=datetime(2026, 3, 31, 10, 0), due_date=date.today())
playtime = Task(name="Laser Pointer Play", task_type="enrichment", duration=20, priority=1, recurring=True, pet_name="Whiskers",
                time_slot=datetime(2026, 3, 31, 11, 0), due_date=date.today())

# Add tasks to pets
dog.add_task(walk)
dog.add_task(feed_dog)
dog.add_task(meds)

cat.add_task(feed_cat)
cat.add_task(grooming)
cat.add_task(playtime)

# Create scheduler and generate plan
scheduler = Scheduler(owner=owner)
scheduler.generate_plan()

# Print the plan
print("=" * 50)
print("       TODAY'S PET CARE SCHEDULE")
print("=" * 50)
print(scheduler.explain_plan())
print("=" * 50)
