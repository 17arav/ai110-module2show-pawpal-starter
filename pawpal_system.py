from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional


class Owner:
    """Represents a pet owner and their care preferences."""

    def __init__(self, name: str, available_time: int, preferences: List[str] | None = None) -> None:
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
        self.owner = owner
        self.tasks = tasks or []
        self.planning_date = planning_date or date.today()
        self.daily_plan: Dict[str, List[Task]] = {}

    def generate_plan(self) -> None:
        """Generate a daily care plan based on owner availability and tasks."""
        self.tasks = [task for pet in self.owner.get_pets() for task in pet.get_tasks()]
        self.daily_plan = {}

    def detect_conflicts(self) -> List[Task]:
        """Detect scheduling conflicts within the current plan."""
        return []

    def sort_by_priority(self) -> None:
        """Sort tasks by priority for planning."""
        self.tasks.sort(key=lambda task: task.priority, reverse=True)

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        return ""
