let playerCards = {}; // Store player's cards

// Function to load player's cards
const loadPlayerCards = () => {
    fetch('/get-player-cards')
        .then(response => response.json())
        .then(data => {
            console.log('Player cards response:', data);
            playerCards = data.cards;

            const playerCardsDiv = document.getElementById('player-cards');
            playerCardsDiv.innerHTML = `
                <p>Character: ${playerCards.character}</p>
                <p>Room: ${playerCards.room}</p>
                <p>Weapon: ${playerCards.weapon}</p>
            `;
        })
        .catch(error => console.error('Error fetching player cards:', error));
};

// Load player cards on page load
document.addEventListener('DOMContentLoaded', loadPlayerCards);

// Function to save deductions
const saveDeductions = () => {
    const deductions = document.getElementById('deductions').value;
    fetch('/save-deductions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deductions })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
};

// Function to clear deductions
const clearDeductions = () => {
    fetch('/clear-deductions', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('deductions').value = ''; // Clear the textarea
    })
    .catch(error => console.error('Error:', error));
};

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

// Function to refute suggestion
const refuteSuggestion = () => {
    document.getElementById('refute-suggestion-section').style.display = 'block';
};