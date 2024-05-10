// Function to fetch tasks from the server
async function fetchTasks() {
    try {
        const response = await fetch('/api/tasks');
        if (response.ok) {
            const tasks = await response.json();
            renderTasks(tasks);
        } else {
            console.error('Failed to fetch tasks:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to render tasks
function renderTasks(tasks) {
    const tasksList = document.getElementById('tasks-list');
    tasksList.innerHTML = '';
    tasks.forEach(task => {
        const taskElement = document.createElement('li');
        taskElement.textContent = task.name;
        console.log(task.name);
        tasksList.appendChild(taskElement);
    });
}

// Call the fetchTasks function when the page loads
document.addEventListener('DOMContentLoaded', fetchTasks);