from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
import json
from typing import Any, Dict, List, Optional


class Owner:
    """Represents a pet owner and their care preferences."""

    def __init__(self, name: str, available_time: int, preferences: List[str] | None = None) -> None:
        """Initialize a pet owner with availability and preferences."""
        self.name = name
        self.available_time = available_time
        self.preferences = preferences or []
        self._pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self._pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection."""
        if pet in self._pets:
            self._pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return the list of pets owned by this owner."""
        return list(self._pets)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the owner and all pets to a dictionary."""
        return {
            "name": self.name,
            "available_time": self.available_time,
            "preferences": self.preferences,
            "pets": [pet.to_dict() for pet in self._pets],
        }

    def save_to_json(self, filepath: str) -> None:
        """Save the owner, pets, and tasks to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str) -> "Owner":
        """Load an Owner and all nested pets/tasks from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        owner = cls(
            name=data["name"],
            available_time=data["available_time"],
            preferences=data.get("preferences", []),
        )

        for pet_data in data.get("pets", []):
            pet = Pet.from_dict(pet_data)
            owner.add_pet(pet)

        return owner


@dataclass
class Pet:
    """Represents a pet and its associated care tasks."""

    name: str
    species: str
    age: int
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's schedule."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's schedule."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return the list of tasks assigned to this pet."""
        return list(self.tasks)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this pet to a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_needs": self.special_needs,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        """Deserialize a pet and its tasks from a dictionary."""
        pet = cls(
            name=data["name"],
            species=data["species"],
            age=data["age"],
            special_needs=data.get("special_needs", ""),
        )

        for task_data in data.get("tasks", []):
            pet.add_task(Task.from_dict(task_data))

        return pet


@dataclass
class Task:
    """Represents a pet care task."""

    name: str
    task_type: str
    duration: int
    priority: int
    recurring: bool
    pet_name: str
    time_slot: Optional[datetime] = None
    due_date: Optional[date] = None
    completed: bool = False

    def mark_complete(self) -> Optional[Task]:
        """Mark this task as complete.

        For recurring tasks, create and return the next occurrence with the due date
        moved forward by one day. Non-recurring tasks are just marked complete.
        """
        self.completed = True

        if self.recurring:
            next_due_date = self.due_date + timedelta(days=1) if self.due_date else None
            return Task(
                name=self.name,
                task_type=self.task_type,
                duration=self.duration,
                priority=self.priority,
                recurring=self.recurring,
                pet_name=self.pet_name,
                time_slot=None,
                due_date=next_due_date,
                completed=False,
            )

        return None

    def is_overdue(self) -> bool:
        """Return whether this task is overdue."""
        if self.completed or self.due_date is None:
            return False
        return date.today() > self.due_date

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the task to a dictionary."""
        return {
            "name": self.name,
            "task_type": self.task_type,
            "duration": self.duration,
            "priority": self.priority,
            "recurring": self.recurring,
            "pet_name": self.pet_name,
            "time_slot": self.time_slot.isoformat() if self.time_slot else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Deserialize a task from a dictionary."""
        return cls(
            name=data["name"],
            task_type=data["task_type"],
            duration=data["duration"],
            priority=data["priority"],
            recurring=data["recurring"],
            pet_name=data["pet_name"],
            time_slot=datetime.fromisoformat(data["time_slot"]) if data.get("time_slot") else None,
            due_date=date.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            completed=data.get("completed", False),
        )


class Scheduler:
    """Generates and explains a pet care plan for an owner."""

    def __init__(self, owner: Owner, tasks: List[Task] | None = None, planning_date: Optional[date] = None) -> None:
        """Initialize the scheduler with an owner and optional tasks."""
        self.owner = owner
        self.tasks = tasks or []
        self.planning_date = planning_date or date.today()
        self.daily_plan: Dict[str, List[Task]] = {}

    def generate_plan(self) -> None:
        """Generate a daily care plan based on owner availability and tasks."""
        self.tasks = [task for pet in self.owner.get_pets() for task in pet.get_tasks()]
        self.sort_by_priority()

        self.daily_plan = {}
        remaining_time = self.owner.available_time
        total_scheduled = 0

        for task in self.tasks:
            if task.duration <= 0:
                continue

            if total_scheduled + task.duration > self.owner.available_time:
                break

            self.daily_plan.setdefault(task.pet_name, []).append(task)
            total_scheduled += task.duration
            remaining_time = self.owner.available_time - total_scheduled

    def detect_conflicts(self) -> List[Task]:
        """Detect scheduling conflicts within the current plan."""
        conflicts: List[Task] = []
        scheduled_tasks = [task for tasks in self.daily_plan.values() for task in tasks]

        for i, task_a in enumerate(scheduled_tasks):
            if task_a.time_slot is None:
                continue
            end_a = task_a.time_slot + timedelta(minutes=task_a.duration)

            for task_b in scheduled_tasks[i + 1 :]:
                if task_b.time_slot is None:
                    continue
                start_b = task_b.time_slot
                end_b = task_b.time_slot + timedelta(minutes=task_b.duration)

                if task_a.time_slot < end_b and start_b < end_a:
                    if task_a not in conflicts:
                        conflicts.append(task_a)
                    if task_b not in conflicts:
                        conflicts.append(task_b)

        return conflicts

    def find_next_available_slot(self, duration: int) -> Optional[datetime]:
        """Find the next available slot between 8:00 AM and 8:00 PM for a given duration."""
        if duration <= 0:
            return None

        day_start = datetime.combine(self.planning_date, datetime.min.time()).replace(hour=8, minute=0)
        day_end = datetime.combine(self.planning_date, datetime.min.time()).replace(hour=20, minute=0)

        scheduled = [
            task
            for tasks in self.daily_plan.values()
            for task in tasks
            if task.time_slot is not None
        ]

        if not scheduled:
            return day_start if day_start + timedelta(minutes=duration) <= day_end else None

        scheduled.sort(key=lambda task: task.time_slot)
        candidate = day_start

        for task in scheduled:
            task_start = task.time_slot
            task_end = task_start + timedelta(minutes=task.duration)

            if candidate + timedelta(minutes=duration) <= task_start:
                return candidate

            if task_end > candidate:
                candidate = task_end

        return candidate if candidate + timedelta(minutes=duration) <= day_end else None

    def sort_by_priority(self) -> None:
        """Sort tasks with highest priority first."""
        self.tasks.sort(key=lambda task: task.priority, reverse=True)

    def sort_by_time(self) -> None:
        """Sort tasks by their scheduled time slot.

        Tasks without a time_slot are placed after scheduled tasks.
        """
        self.tasks.sort(key=lambda task: (task.time_slot is None, task.time_slot))

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        filtered = self.tasks
        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name == pet_name]
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        return filtered

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        if not self.daily_plan:
            return (
                f"No tasks are currently scheduled for {self.owner.name} on {self.planning_date}. "
                "Use generate_plan() to create a plan from your pets' tasks."
            )

        lines = [
            f"Daily plan for {self.owner.name} on {self.planning_date}:"
        ]

        total_duration = 0
        for pet_name, tasks in self.daily_plan.items():
            lines.append(f"\n{pet_name}:")
            for index, task in enumerate(tasks, start=1):
                time_str = task.time_slot.isoformat() if task.time_slot else "unscheduled time"
                lines.append(
                    f"  {index}. {task.name} ({task.task_type}, priority {task.priority}) at {time_str}"
                )
                total_duration += task.duration

        lines.append(
            f"\nTasks are ordered by priority so the most important care happens first. "
            f"The schedule fits within {self.owner.name}'s available time of {self.owner.available_time} minutes."
        )
        lines.append(f"Total scheduled duration: {total_duration} minutes.")

        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("\nWarning: some tasks overlap in time_slot and may conflict:")
            for task in conflicts:
                lines.append(f"  - {task.name} for {task.pet_name} at {task.time_slot}")
        else:
            lines.append("\nNo detected task time conflicts.")

        return "\n".join(lines)
