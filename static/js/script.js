const board = document.getElementById("board");
      const boardSize = 15;
      const players = [
        { color: "red", path: [], position: -1, token: null },
        { color: "green", path: [], position: -1, token: null },
        { color: "blue", path: [], position: -1, token: null },
        { color: "yellow", path: [], position: -1, token: null },
      ];
      let currentPlayerIndex = 0;

      // Generate the board dynamically
      function generateBoard() {
        for (let i = 0; i < boardSize * boardSize; i++) {
          const cell = document.createElement("div");
          cell.classList.add("cell");
          board.appendChild(cell);
        }

        // Define paths for each player
        const cells = document.querySelectorAll(".cell");
        players[0].path = definePath(cells, 105, -15, 1); // Red
        players[1].path = definePath(cells, 165, 15, -1); // Green
        players[2].path = definePath(cells, 195, -15, -1); // Blue
        players[3].path = definePath(cells, 255, 15, 1); // Yellow
      }

      // Define paths dynamically
      function definePath(cells, start, increment, step) {
        const path = [];
        for (let i = 0; i < 56; i++) {
          const pos = start + (i % 7) * step + Math.floor(i / 7) * increment;
          path.push(cells[pos]);
          cells[pos].classList.add(`path-${players[currentPlayerIndex].color}`);
        }
        return path;
      }

      // Roll Dice
      document.getElementById("rollDice").addEventListener("click", () => {
        const dice = Math.floor(Math.random() * 6) + 1;
        document.getElementById("diceResult").textContent = `Dice: ${dice}`;
        const player = players[currentPlayerIndex];

        // Move token
        if (player.position === -1 && dice === 6) {
          player.position = 0; // Enter board
        } else if (player.position !== -1) {
          player.position += dice;
          if (player.position >= player.path.length) {
            alert(`${capitalize(player.color)} wins!`);
            resetGame();
            return;
          }
        }

        // Update token position
        updateToken(player);

        // Next turn
        currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
        document.getElementById(
          "turn"
        ).textContent = `Player Turn: ${capitalize(
          players[currentPlayerIndex].color
        )}`;
      });

      // Update token position visually
      function updateToken(player) {
        if (player.token) player.token.remove();
        if (player.position !== -1) {
          const cell = player.path[player.position];
          const token = document.createElement("div");
          token.classList.add("token", `token-${player.color}`);
          cell.appendChild(token);
          player.token = token;
        }
      }

      // Reset the game
      function resetGame() {
        players.forEach((player) => {
          player.position = -1;
          if (player.token) player.token.remove();
        });
        currentPlayerIndex = 0;
        document.getElementById("diceResult").textContent = "Dice: ";
        document.getElementById("turn").textContent = "Player Turn: Red";
      }

      // Capitalize player color for display
      function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
      }

      // Initialize the game
      generateBoard();

 