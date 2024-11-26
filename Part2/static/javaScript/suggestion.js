// Variable to track if it's the first submission
let firstSubmission = true;

function submitSuggestion() {
    const form = document.getElementById('suggestion-form');
    if (form) {
        const formData = new FormData(form);

        fetch('/submit-suggestion', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const responseMessage = document.getElementById('response-message');
            if (responseMessage) {
                responseMessage.textContent = data.message;

                // Show the Add To Deduction button if the suggestion is incorrect
                const addDeductionBtn = document.getElementById('add-deduction-btn');
                if (addDeductionBtn) {
                    if (!data.correct) {
                        addDeductionBtn.style.display = 'inline-block';
                    } else {
                        // If the suggestion is correct, hide the button
                        addDeductionBtn.style.display = 'none';
                    }
                }

                // Check if the suggestion is correct
                if (data.correct) {
                    // Show a popup message
                    alert('Congratulations! Your suggestion is correct.');

                    // Refresh the session by making a request to a session refresh endpoint
                    fetch('/refresh-session', {
                        method: 'POST'
                    })
                    .then(() => {
                        // Navigate to the home page after refreshing the session
                        window.location.href = '/';  // Navigate to the home page
                    });
                }

                // Mark that the first submission has been made
                firstSubmission = false;
            } else {
                console.error('Response message element not found');
            }
        });
    } else {
        console.error('Form element not found');
    }
}

function navigateToRoom() {
    window.location.href = '/choose-room';
}

document.addEventListener('DOMContentLoaded', function() {
    const addDeductionBtn = document.getElementById('add-deduction-btn');
    if (addDeductionBtn) {
        addDeductionBtn.addEventListener('click', function() {
            const deductionValue = document.getElementById('response-message').innerText;

            fetch('/add-deduction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ deduction: deductionValue }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message); // Handle success message

                // Show popup notification
                alert('Deduction saved. Please choose a new room.');

                // Navigate to choose room
                navigateToRoom();
            })
            .catch((error) => {
                console.error('Error:', error); // Handle error
            });
        });
    } else {
        console.error('Add Deduction button not found');
    }
});

// Function to view deductions saved by the user
function viewDeductions() {
    fetch('/view-deductions')
        .then(response => response.json())
        .then(data => {
            console.log("Deductions fetched:", data.deductions); // Log fetched deductions
            const deductions = data.deductions.length > 0 ? data.deductions.join('\n') : 'No deductions saved.';
            alert(deductions);
        })
        .catch(error => console.error('Error fetching deductions:', error));
}

document.addEventListener('DOMContentLoaded', function() { function submitSuggestion() { console.log("Submitting suggestion..."); } document.getElementById('submit-suggestion-btn').addEventListener('click', function() { submitSuggestion(); }); });