// Function to toggle character selection visibility
const showCharacterSelection = () => {
    const mainContent = document.getElementById('mainContent');
    const characterSelection = document.getElementById('characterSelection');

    if (mainContent && characterSelection) {
        mainContent.style.display = 'none';  // Hide the main content
        characterSelection.style.display = 'block';  // Show character selection
    } else {
        console.error('One or both elements not found');
    }
};

// Add event listener for form submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form[action="/download-layout"]');
    if (!form) {
        return console.error('Form element not found');
    }

    form.addEventListener('submit', event => {
        event.preventDefault();  // Prevent default submission

        fetch('/download-layout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.opened ? data.message : 'Game layout downloaded successfully.');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Please close the xlsx file before downloading again');
        });
    });
});