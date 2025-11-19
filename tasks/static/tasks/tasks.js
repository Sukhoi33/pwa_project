// Function to display tasks on the home screen
function displayTasksOnHomeScreen() {
    const taskList = document.querySelector('#task-list');
    taskList.innerHTML = ''; // Clear existing tasks
    loadTaskList(); // Load tasks from server or IndexedDB
}

// Function to view task details
function viewTaskDetails(task) {
    const detailsContainer = document.querySelector('#task-details');
    detailsContainer.innerHTML = `
        <h2>Task Details</h2>
        <p>Name: ${task.name}</p>
        <p>Status: ${task.completed ? 'Completed' : 'Incomplete'}</p>
    `;
}

// Modify the addTaskToPage function to include a click event for viewing details
function addTaskToPage(task) {
    const taskList = document.querySelector('#task-list');
    const taskElement = document.createElement('li');
    taskElement.textContent = `${task.name} - ${task.completed ? 'Completed' : 'Incomplete'}`;
    
    // Add click event to view task details
    taskElement.addEventListener('click', () => viewTaskDetails(task));
    
    taskList.appendChild(taskElement);
}

// Call displayTasksOnHomeScreen when the home screen is loaded
document.addEventListener('DOMContentLoaded', function() {
    displayTasksOnHomeScreen();
    // Other existing code...
});
