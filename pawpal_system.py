from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional


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

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def is_overdue(self) -> bool:
        """Return whether this task is overdue."""
        if self.completed or self.due_date is None:
            return False
        return date.today() > self.due_date


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

    def sort_by_priority(self) -> None:
        """Sort tasks with highest priority first."""
        self.tasks.sort(key=lambda task: task.priority, reverse=True)

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
