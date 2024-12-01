// Initial setup
let currentPlayer = 'red';
let diceValue = 0;

// Function to roll the dice
document.getElementById('roll-dice').addEventListener('click', function() {
  diceValue = Math.floor(Math.random() * 6) + 1; // Dice value from 1 to 6
  document.getElementById('dice-value').textContent = 'Dice: ' + diceValue;
  moveToken(currentPlayer, diceValue);
  changePlayer();
});

// Function to move player token
function moveToken(player, dice) {
  const token = document.querySelector('.token.' + player);
  const tokenPos = token.getBoundingClientRect();

  // Example logic for moving (change top and left to simulate movement)
  if (dice > 0) {
    token.style.left = (tokenPos.left + dice * 20) + 'px';
    token.style.top = (tokenPos.top + dice * 20) + 'px';
  }
}

// Function to change the current player
function changePlayer() {
  if (currentPlayer === 'red') {
    currentPlayer = 'blue';
  } else if (currentPlayer === 'blue') {
    currentPlayer = 'green';
  } else if (currentPlayer === 'green') {
    currentPlayer = 'yellow';
  } else {
    currentPlayer = 'red';
  }
  console.log('Current Player:', currentPlayer);
}
