let firstSubmission = true;

// Function to submit suggestion
const submitSuggestion = () => {
    const form = document.getElementById('suggestion-form');
    if (!form) return console.error('Form element not found');

    fetch('/submit-suggestion', {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(data => {
        const responseMessage = document.getElementById('response-message');
        if (!responseMessage) return console.error('Response message element not found');

        responseMessage.textContent = data.message;
        const addDeductionBtn = document.getElementById('add-deduction-btn');
        if (addDeductionBtn) {
            addDeductionBtn.style.display = data.correct ? 'none' : 'inline-block';
        }

        if (data.correct) {
            alert('Congratulations! Your suggestion is correct.');
            fetch('/refresh-session', { method: 'POST' })
                .then(() => window.location.href = '/');  // Navigate to the home page
        }

        firstSubmission = false;
    })
    .catch(error => console.error('Error:', error));
};

// Function to navigate to room selection
const navigateToRoom = () => window.location.href = '/choose-room';

document.addEventListener('DOMContentLoaded', () => {
    const addDeductionBtn = document.getElementById('add-deduction-btn');
    if (addDeductionBtn) {
        addDeductionBtn.addEventListener('click', () => {
            const deductionValue = document.getElementById('response-message').innerText;
            fetch('/add-deduction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ deduction: deductionValue })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                alert('Deduction saved. Please choose a new room.');
                navigateToRoom();
            })
            .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('Add Deduction button not found');
    }
});

// Function to view deductions
const viewDeductions = () => {
    fetch('/view-deductions')
        .then(response => response.json())
        .then(data => {
            const deductions = data.deductions.length ? data.deductions.join('\n') : 'No deductions saved.';
            alert(deductions);
        })
        .catch(error => console.error('Error fetching deductions:', error));
};

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('submit-suggestion-btn')?.addEventListener('click', submitSuggestion);
});