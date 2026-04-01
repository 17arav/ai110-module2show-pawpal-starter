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

- I used GitHub Copilot and Claude throughout this project. For design brainstorming, I asked Copilot to generate a Mermaid.js UML diagram based on my class ideas. For implementation, I used Copilot's Agent Mode to flesh out class skeletons into full working code. For testing, I used Copilot to generate pytest cases covering sorting, recurring tasks, and conflict detection. The most helpful prompts were specific ones that referenced files directly using #file:pawpal_system.py and gave clear numbered instructions for what to implement.

**b. Judgment and verification**

- When Copilot first generated the class skeletons, it didn't include a pet_name attribute on Task or proper date handling for scheduling. I didn't accept the initial design as-is — instead I asked Copilot to review its own output and it suggested adding pet_name, changing time_slot to datetime, and adding due_date. I verified these changes by running the CLI demo script and checking that tasks correctly linked to pets and the scheduler could detect time conflicts.

---

## 4. Testing and Verification

**a. What you tested**

- I tested seven key behaviors: task completion toggling, task count after adding to a pet, sorting tasks by time (chronological order), sorting by priority (highest first), recurring task automation (new task created with next day's due date), conflict detection (overlapping time slots flagged), and scheduler handling pets with no tasks. These tests were important because they verify the core logic that makes PawPal+ reliable — if sorting or conflict detection breaks, the entire schedule becomes untrustworthy.

**b. Confidence**

- I'm fairly confident (4 out of 5) that my scheduler works correctly for typical use cases. All 7 tests pass and cover the main features. If I had more time, I would test edge cases like tasks with zero duration, a very large number of tasks that exceed available time, tasks with no time slot during conflict detection, and boundary conditions where total task duration exactly equals available time.

---

## 5. Reflection

**a. What went well**

- I'm most satisfied with the scheduling logic. The Scheduler class cleanly gathers tasks from pets, sorts by priority or time, detects conflicts, and explains its reasoning. The CLI demo script was especially helpful for verifying everything worked before connecting it to the UI.

**b. What you would improve**

- If I had another iteration, I would add the ability to edit and delete tasks from the UI, add user authentication so multiple owners can use the app, and improve the conflict detection to suggest alternative times instead of just warning about overlaps.

**c. Key takeaway**

- I learned that AI is a powerful coding partner, but I need to stay in the driver's seat. AI-generated code often needs human review — like when the initial skeletons were missing key attributes. The best workflow is to design first, use AI to scaffold and implement, then carefully verify the output before moving on.
