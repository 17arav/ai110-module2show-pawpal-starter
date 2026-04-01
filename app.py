import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
# Initialize session state with Owner object
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
    

st.title("🐾 PawPal+")
st.caption("A smart pet care management system")

# --- Owner Setup ---
st.subheader("👤 Owner Setup")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_time = st.number_input("Available time (minutes)", min_value=10, max_value=480, value=120)

if st.button("Create Owner"):
    st.session_state.owner = Owner(name=owner_name, available_time=available_time)
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.success(f"Owner '{owner_name}' created with {available_time} minutes available!")

if st.session_state.owner is None:
    st.info("Please create an owner to get started.")
    st.stop()

st.divider()

# --- Add Pet ---
st.subheader("🐾 Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Fish", "Other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

special_needs = st.text_input("Special needs (optional)", value="")

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species, age=age, special_needs=special_needs)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added {pet_name} the {species}!")

# Show current pets
pets = st.session_state.owner.get_pets()
if pets:
    st.write(f"**Current pets ({len(pets)}):**")
    for p in pets:
        st.write(f"- {p.name} ({p.species}, age {p.age})")
else:
    st.info("No pets added yet.")

st.divider()

# --- Add Task ---
st.subheader("📋 Add a Task")
if not pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in pets]
    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("For which pet?", pet_names)
        task_name = st.text_input("Task name", value="Morning Walk")
        task_type = st.selectbox("Task type", ["walk", "feeding", "meds", "grooming", "enrichment", "other"])
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
        priority = st.slider("Priority (1=low, 5=high)", min_value=1, max_value=5, value=3)
        recurring = st.checkbox("Recurring daily?")

    if st.button("Add Task"):
        task = Task(
            name=task_name,
            task_type=task_type,
            duration=duration,
            priority=priority,
            recurring=recurring,
            pet_name=selected_pet,
        )
        for p in pets:
            if p.name == selected_pet:
                p.add_task(task)
                st.success(f"Added '{task_name}' for {selected_pet}!")
                break

    # Show tasks per pet
    for p in pets:
        tasks = p.get_tasks()
        if tasks:
            st.write(f"**{p.name}'s tasks ({len(tasks)}):**")
            for t in tasks:
                status = "✅" if t.completed else "⬜"
                st.write(f"  {status} {t.name} ({t.task_type}, {t.duration}min, priority {t.priority})")

st.divider()

# --- Generate Schedule ---
st.subheader("📅 Generate Daily Schedule")

if st.button("Generate Schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    scheduler.generate_plan()
    st.session_state.scheduler = scheduler

    explanation = scheduler.explain_plan()
    st.text(explanation)

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(f"⚠️ {len(conflicts)} task conflicts detected!")
