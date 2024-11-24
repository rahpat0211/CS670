function showCharacterSelection() {
    const mainContent = document.getElementById('mainContent');
    const characterSelection = document.getElementById('characterSelection');

    if (mainContent && characterSelection) {
        // Hide the main content
        mainContent.style.display = 'none';

        // Show the character selection
        characterSelection.style.display = 'block';
    } else {
        console.error('One or both elements not found');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[action="/download-layout"]');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission

            fetch('/download-layout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.opened) {
                    // Alert if the layout is already opened
                    alert(data.message);
                } else {
                    // Handle successful layout download
                    alert('Game layout downloaded successfully.');
                }
            })
            .catch(error => {
                // Handle any errors that occur during the fetch
                console.error('Error:', error);
                alert('Please close the xlsx file before downloading again');
            });
        });
    } else {
        console.error('Form element not found');
    }
});
