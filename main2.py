import streamlit as st
import os
from datetime import datetime

# Define the file where tasks will be saved
TODO_FILE = 'todo_list.txt'

# Load tasks from the file
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

# Save tasks to the file
def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        file.writelines([task + '\n' for task in tasks])

# Add a task
def add_task(task, size, category):
    if task and size and category:
        current_date = datetime.now().strftime("%Y-%m-%d")
        formatted_task = f"{current_date} - {task} [{size}] ({category})"
        tasks = load_tasks()
        tasks.append(formatted_task)
        save_tasks(tasks)
        st.success("Task added successfully!")
    else:
        st.warning("Please complete all fields.")

# Remove a task
def remove_task(task_to_remove):
    tasks = load_tasks()
    if task_to_remove in tasks:
        tasks.remove(task_to_remove)
        save_tasks(tasks)
        st.success("Task removed successfully!")

# Streamlit App Layout
st.title("📋 To-Do List")

# Center-align the content for a better mobile experience
st.markdown("<style> .css-18e3th9 {padding: 0;} .css-1d391kg {padding: 0;} </style>", unsafe_allow_html=True)

# Task Input Form
with st.form("Add Task Form"):
    task = st.text_input("Task")
    size = st.selectbox("Size", ["Small", "Medium", "Large"])
    category = st.selectbox("Category", ["Personal", "Business"])
    submitted = st.form_submit_button("Add Task")
    if submitted:
        add_task(task, size, category)

# Display Current Tasks
tasks = load_tasks()
if tasks:
    st.subheader("Your Tasks")
    for task in tasks:
        with st.container():
            st.write(task)
            complete_button = st.button("✔ Complete", key=task)
            if complete_button:
                remove_task(task)
else:
    st.info("No tasks added yet. Start by adding a task above!")

# Footer
st.markdown("<br><center>Made with ❤️ in Streamlit</center>", unsafe_allow_html=True)
