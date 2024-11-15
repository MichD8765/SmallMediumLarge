import streamlit as st
import os
from datetime import datetime

# Define the file where tasks will be saved
TODO_FILE = 'todo_list.txt'

# Load tasks from the file
def load_tasks():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r') as file:
                tasks = [line.strip() for line in file.readlines()]
        except IOError as e:
            st.error(f"Error reading file {TODO_FILE}: {e}")
            tasks = []
    else:
        tasks = []
    return tasks

# Save tasks to the file
def save_tasks(tasks):
    try:
        with open(TODO_FILE, 'w') as file:
            for task in tasks:
                file.write(task + '\n')
    except IOError as e:
        st.error(f"Error writing to file {TODO_FILE}: {e}")

# Add task with date, size, and category
def add_task(task, size_tag, category):
    if task and size_tag and category:
        current_date = datetime.now().strftime("%Y-%m-%d")
        task_with_date = f"{current_date} - {task} [{size_tag}] ({category})"
        tasks = load_tasks()
        tasks.append(task_with_date)
        save_tasks(tasks)
        st.success("Task added successfully!")
    else:
        st.warning("Please enter a task, select a size tag, and choose a category.")

# Display tasks in the appropriate sections
def display_tasks():
    tasks = load_tasks()
    personal_tasks = {"Small": [], "Medium": [], "Large": []}
    business_tasks = {"Small": [], "Medium": [], "Large": []}

    for task in tasks:
        if "(Personal)" in task:
            if "[Small]" in task:
                personal_tasks["Small"].append(task)
            elif "[Medium]" in task:
                personal_tasks["Medium"].append(task)
            elif "[Large]" in task:
                personal_tasks["Large"].append(task)
        elif "(Business)" in task:
            if "[Small]" in task:
                business_tasks["Small"].append(task)
            elif "[Medium]" in task:
                business_tasks["Medium"].append(task)
            elif "[Large]" in task:
                business_tasks["Large"].append(task)

    # Display personal tasks
    st.subheader("Personal Tasks")
    for size, task_list in personal_tasks.items():
        st.write(f"**{size} Tasks**")
        for task in task_list:
            st.write(task)
            if st.button(f"Complete {task}", key=task):
                mark_completed(task)

    # Display business tasks
    st.subheader("Business Tasks")
    for size, task_list in business_tasks.items():
        st.write(f"**{size} Tasks**")
        for task in task_list:
            st.write(task)
            if st.button(f"Complete {task}", key=task):
                mark_completed(task)

# Mark task as completed and remove it from the file
def mark_completed(task_text):
    tasks = load_tasks()
    tasks.remove(task_text)
    save_tasks(tasks)
    st.success("Task marked as completed and removed!")

# Streamlit app layout
st.title("To-Do List App with Complete Buttons")

# Input fields for adding a task
st.header("Add a New Task")
task = st.text_input("Enter the task")
size_tag = st.selectbox("Select task size", ["Small", "Medium", "Large"])
category = st.selectbox("Select task category", ["Personal", "Business"])

# Add task button
if st.button("Add Task"):
    add_task(task, size_tag, category)

# Display tasks in the correct listboxes
st.header("Current Tasks")
display_tasks()
