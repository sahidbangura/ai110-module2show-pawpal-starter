import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# Streamlit reruns this script on every interaction, so keep the Owner in session_state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        elif owner.get_pet(pet_name.strip()):
            st.error(f"{pet_name} already exists.")
        else:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name}!")

st.subheader("Schedule a task")
if not owner.pets:
    st.info("Add a pet first.")
else:
    with st.form("add_task", clear_on_submit=True):
        target = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task", value="Morning walk")
        c1, c2, c3, c4 = st.columns(4)
        time_value = c1.time_input("Time")
        duration = c2.number_input("Minutes", min_value=1, max_value=240, value=20)
        priority = c3.selectbox("Priority", ["low", "medium", "high"], index=1)
        frequency = c4.selectbox("Repeats", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            owner.get_pet(target).add_task(Task(
                description, time_value.strftime("%H:%M"), frequency,
                duration_minutes=int(duration), priority=priority))
            st.success(f"Scheduled '{description}' for {target}.")

st.divider()
st.subheader("Today's schedule")

for warning in scheduler.detect_conflicts():
    st.warning(f"{warning}. Consider moving one of them.")

pet_filter = st.selectbox("Show pet", ["All"] + [p.name for p in owner.pets])
status_filter = st.radio("Status", ["Pending", "Completed", "All"], horizontal=True)

tasks = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All" else pet_filter,
    completed={"Pending": False, "Completed": True, "All": None}[status_filter],
)
tasks = scheduler.sort_by_time(tasks)

if tasks:
    st.table([
        {"Date": str(t.due_date), "Time": t.time, "Pet": t.pet_name, "Task": t.description,
         "Minutes": t.duration_minutes, "Priority": t.priority, "Repeats": t.frequency,
         "Done": "✅" if t.completed else ""}
        for t in tasks
    ])
else:
    st.info("No tasks to show.")

pending = scheduler.filter_tasks(completed=False)
if pending:
    st.markdown("**Mark a task complete**")
    labels = {f"{t.time} · {t.pet_name} · {t.description} ({t.due_date})": t
              for t in scheduler.sort_by_time(pending)}
    choice = st.selectbox("Task", list(labels))
    if st.button("Complete"):
        nxt = scheduler.mark_task_complete(labels[choice])
        st.success("Done!" + (f" Next one scheduled for {nxt.due_date}." if nxt else ""))
        st.rerun()
