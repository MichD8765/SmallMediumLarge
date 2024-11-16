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

# Custom CSS for styling
st.markdown("""
    <style>
        /* Center align content */
        .stApp {
            background-color: #f7f7f7;
            padding: 2rem;
        }
        
        /* Title styling */
        h1 {
            color: #4CAF50;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
        }

        /* Form styling */
        .task-form {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        /* Task display container */
        .task-container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Task text styling */
        .task-text {
            font-size: 1rem;
            color: #333333;
        }

        /* Complete button styling */
        .complete-button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            cursor: pointer;
        }

        /* Footer styling */
        .footer {
            margin-top: 2rem;
            text-align: center;
            color: #777777;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit App Layout
st.title("📋 To-Do List")

# Form to add new tasks
st.markdown('<div class="task-form">', unsafe_allow_html=True)
with st.form("Add Task Form"):
    task = st.text_input("Task")
    size = st.selectbox("Size", ["Small", "Medium", "Large"])
    category = st.selectbox("Category", ["Personal", "Business"])
    submitted = st.form_submit_button("Add Task")
    if submitted:
        add_task(task, size, category)
st.markdown('</div>', unsafe_allow_html=True)

# Display Current Tasks
tasks = load_tasks()
if tasks:
    st.subheader("Your Tasks")
    for task in tasks:
        st.markdown('<div class="task-container">', unsafe_allow_html=True)
        st.write(f'<span class="task-text">{task}</span>', unsafe_allow_html=True)
        complete_button = st.button("✔ Complete", key=task)
        if complete_button:
            remove_task(task)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No tasks added yet. Start by adding a task above!")

# Footer
st.markdown('<div class="footer">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)
