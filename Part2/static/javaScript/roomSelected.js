let playerCards = {}; // Store player's cards

function loadPlayerCards() {
    fetch('/get-player-cards')
        .then(response => response.json())
        .then(data => {
            console.log('Player cards response:', data);
            playerCards = data.cards; // Store the player's cards

            // Display the player's cards directly instead of using radio buttons
            const playerCardsDiv = document.getElementById('player-cards');
            playerCardsDiv.innerHTML = ''; // Clear previous cards

            // Display the player's cards in a readable format
            playerCardsDiv.innerHTML += `<p>Character: ${playerCards.character}</p>`;
            playerCardsDiv.innerHTML += `<p>Room: ${playerCards.room}</p>`;
            playerCardsDiv.innerHTML += `<p>Weapon: ${playerCards.weapon}</p>`;
        })
        .catch(error => console.error('Error fetching player cards:', error));
}

// Call loadPlayerCards when the page loads
document.addEventListener('DOMContentLoaded', loadPlayerCards);

function saveDeductions() {
    const deductions = document.getElementById('deductions').value;

    fetch('/save-deductions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ deductions: deductions })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function clearDeductions() {
    fetch('/clear-deductions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('deductions').value = ''; // Clear the textarea
    })
    .catch(error => console.error('Error:', error));
}

function viewDeductions() {
    fetch('/view-deductions')
        .then(response => response.json())
        .then(data => {
            const deductions = data.deductions.length > 0 ? data.deductions.join('\n') : 'No deductions saved.';
            alert(deductions);

        })
        .catch(error => console.error('Error fetching deductions:', error));
}

function refuteSuggestion() {
            // Show the refute suggestion section
            document.getElementById('refute-suggestion-section').style.display = 'block';
}