# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:
1. Add a pet — The user can enter basic pet info like name, species, age, and any special needs.
2. Schedule a task — The user can add care tasks like walks, feeding, medications, grooming, and enrichment with a duration and priority level.
3. Generate a daily plan — The system creates a daily schedule based on task priorities, time constraints, and owner preferences, and explains why tasks were ordered that way.

Initial UML Design:
I designed four classes for PawPal+:

1. Owner — Represents the pet owner. Holds their name, available time per day, and preferences. Responsible for managing their list of pets (add, remove, get pets).
2. Pet — Represents a pet using a Python dataclass. Holds name, species, age, and special needs. Responsible for managing its own tasks (add, remove, get tasks).
3. Task — Represents a care task using a Python dataclass. Holds name, task type (walk, feeding, meds, etc.), duration, priority, whether it's recurring, and a time slot. Can be marked complete and checked if overdue.
4. Scheduler — The brain of the system. Takes an Owner and their tasks, then generates a daily plan by sorting tasks by priority, detecting conflicts, and explaining the reasoning behind the schedule.
Relationships: An Owner owns many Pets, each Pet has many Tasks, and the Scheduler manages Tasks for one Owner.

**b. Design changes**

After asking Copilot to review my class skeleton, I made several changes:

1. Added a pet_name attribute to Task so each task knows which pet it belongs to.
2. Changed time_slot from a plain string to an optional datetime field for more reliable scheduling and conflict detection.
3. Added a due_date attribute to Task so the is_overdue() method can work with real dates.
4. Added a planning_date attribute to Scheduler to give context for daily plan generation.
5. Updated generate_plan() to automatically gather tasks from the owner's pets instead of requiring tasks to be passed in manually.

These changes were made because Copilot pointed out that the original skeleton had weak connections between classes and lacked proper date handling for scheduling.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers three main constraints: time (owner's available minutes per day), priority (tasks with higher priority get scheduled first), and time slot conflicts (tasks shouldn't overlap). I decided priority mattered most because critical tasks like medications should always happen, even if it means skipping lower-priority tasks like grooming when time is limited.

**b. Tradeoffs**

- One tradeoff my scheduler makes is that it checks for time conflicts using overlapping durations rather than just exact time matches. This is more accurate but means two tasks scheduled at 7:00 AM will always conflict even if the owner could handle them simultaneously (like feeding two pets at once). This tradeoff is reasonable because in most real-world scenarios, an owner can only focus on one pet care task at a time, so flagging overlaps helps them plan realistically.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- I tested seven key behaviors: task completion toggling, task count after adding to a pet, sorting tasks by time (chronological order), sorting by priority (highest first), recurring task automation (new task created with next day's due date), conflict detection (overlapping time slots flagged), and scheduler handling pets with no tasks. These tests were important because they verify the core logic that makes PawPal+ reliable — if sorting or conflict detection breaks, the entire schedule becomes untrustworthy.

**b. Confidence**

- I'm fairly confident (4 out of 5) that my scheduler works correctly for typical use cases. All 7 tests pass and cover the main features. If I had more time, I would test edge cases like tasks with zero duration, a very large number of tasks that exceed available time, tasks with no time slot during conflict detection, and boundary conditions where total task duration exactly equals available time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
