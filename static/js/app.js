async function createTask(event){
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/api/tasks/create', {
            method: 'POST',
            credentials: 'same-origin',
            body: formData,
        });

        if (response.ok) {
            form.reset();
            getTasks();
        } else {
            // Handle error case
            console.error('Error creating task');
        }
    }
    catch (error) {
        console.error('Error:', error);
    }
    
}

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
        // Add each task as a Bootstrap card
        tasks.forEach((task) => {
          const card = createTaskCard(task);
          taskList.appendChild(card);
        });
      } else {
        // Handle error case
        console.error('Error retrieving tasks');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  function createTaskCard(task) {
    const card = document.createElement('div');
    card.classList.add('card', 'bg-dark', 'text-white', 'mb-3', 'shadow-lg');
  
    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');
  
    const title = document.createElement('h5');
    title.classList.add('card-title');
    title.textContent = task.title;
  
    const description = document.createElement('p');
    description.classList.add('card-text');
    description.textContent = task.description;
  
    const dueDate = document.createElement('p');
    dueDate.classList.add('card-text');
    dueDate.textContent = `Due Date: ${task.due_date}`;
  
    const completeButton = document.createElement('button');
    completeButton.classList.add('btn', 'btn-sm', 'btn-success', 'delete-task');
    completeButton.dataset.taskId = task._id;
    completeButton.textContent = 'Mark Complete';
  
    cardBody.appendChild(title);
    cardBody.appendChild(description);
    cardBody.appendChild(dueDate);
    cardBody.appendChild(completeButton);
  
    card.appendChild(cardBody);
  
    return card;
  }

async function deleteTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/delete/${taskId}`, {
            method: 'DELETE',
            credentials: 'same-origin',
        });

        if (response.ok) {
            getTasks();
        } else {
            // Handle error case
            console.error('Error deleting task');
        }
    }
    catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Listen for task submit event
    const taskForm = document.getElementById('taskForm');
    taskForm.addEventListener('submit', createTask);

    // Listen for task delete event
    const taskList = document.getElementById('taskList');
    taskList.addEventListener('click', handleTaskDelete);

    getTasks();
});

function handleTaskDelete(event) {
    if (event.target.classList.contains('delete-task')) {
        const taskId = event.target.dataset.taskId;
        deleteTask(taskId);
    }
}
