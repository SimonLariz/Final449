async function getTasks() {
    try {
        const response = await fetch('/api/tasks', {
            method: 'GET',
            credentials: 'same-origin',
        });

        if (response.ok) {
            const data = await response.json();
            const tasks = data.tasks;
            const taskList = document.getElementById('taskList');

            // Clear existing task items
            taskList.innerHTML = '';

            // Add each task as a list item
            tasks.forEach((task) => {
                const listItem = document.createElement('li');
                listItem.textContent = `${task.title} - ${task.description} - Due: ${task.due_date}`;
                taskList.appendChild(listItem);
            });
        } else {
            // Handle error case
            console.error('Error retrieving tasks');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


document.addEventListener('DOMContentLoaded', () => {
    getTasks();
});