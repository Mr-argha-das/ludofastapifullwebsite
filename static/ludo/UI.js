import { COORDINATES_MAP, PLAYERS, STEP_LENGTH } from "./constants.js";

const diceButtonElement = document.querySelector("#p1-dice");
const playerPiecesElements = {
  P1: document.querySelectorAll('[player-id="P1"].player-piece'),
  P2: document.querySelectorAll('[player-id="P2"].player-piece'),
};

export class UI {
  static listenDiceClick(callback) {
    diceButtonElement.addEventListener("click", callback);
  }

  static listenPieceClick(callback) {
    document
      .querySelector(".player-pieces")
      .addEventListener("click", callback);
  }

  /**
   *
   * @param {string} player
   * @param {Number} piece
   * @param {Number} newPosition
   */
  static setPiecePosition(player, piece, newPosition) {
    if (!playerPiecesElements[player] || !playerPiecesElements[player][piece]) {
      console.error(
        `Player element of given player: ${player} and piece: ${piece} not found`
      );
      return;
    }

    const [x, y] = COORDINATES_MAP[newPosition];

    const pieceElement = playerPiecesElements[player][piece];
    pieceElement.style.top = y * STEP_LENGTH + "%";
    pieceElement.style.left = x * STEP_LENGTH + "%";
  }

  static setTurn(index, yourPlayer, dicevalue) {
    if (index < 0 || index >= PLAYERS.length) {
      console.error("index out of bound!");
      return;
    }

    const player = PLAYERS[index];

    // Display player ID

    const activePlayerBase = document.querySelector(".player-base.highlight");
    if (activePlayerBase) {
      activePlayerBase.classList.remove("highlight");
    }
    // highlight
    document
      .querySelector(`[player-id="${player}"].player-base`)
      .classList.add("highlight");
    console.log(`UI === ${player}`);

    console.log(dicevalue);
    let diceFace = [
      "../static/dice/dice1.png",
      "../static/dice/dice2.png",
      "../static/dice/dice3.png",
      "../static/dice/dice4.png",
      "../static/dice/dice5.png",
      "../static/dice/dice6.png",
    ];
    console.log(yourPlayer + "================== :) " + player);
    if (yourPlayer === player && yourPlayer !== undefined) {
      const div = document.getElementById("p1-dice");
      div.innerHTML = "";
      div.style.backgroundImage = `url('${
        diceFace[dicevalue === undefined ? 0 : dicevalue - 1]
      }')`;
      div.style.backgroundSize = "cover"; // Optional: cover the entire div
      div.style.backgroundPosition = "center";
    }

    if (yourPlayer !== player && yourPlayer === undefined) {
      const div = document.getElementById("p1-dice");
      div.style.backgroundImage = "none";
      div.innerHTML = "<p> Wait for opponent move </p>";
    }
  }

  static enableDice() {
    diceButtonElement.removeAttribute("disabled");
  }

  static disableDice() {
    diceButtonElement.setAttribute("disabled", "");
  }

  /**
   *
   * @param {string} player
   * @param {Number[]} pieces
   */
  static highlightPieces(player, pieces) {
    pieces.forEach((piece) => {
      const pieceElement = playerPiecesElements[player][piece];
      pieceElement.classList.add("highlight");
    });
  }

  static unhighlightPieces() {
    document.querySelectorAll(".player-piece.highlight").forEach((ele) => {
      ele.classList.remove("highlight");
    });
  }

  static setDiceValue(value, yourPlayer, turn) {
    let diceFace = [
      "../static/dice/dice1.png",
      "../static/dice/dice2.png",
      "../static/dice/dice3.png",
      "../static/dice/dice4.png",
      "../static/dice/dice5.png",
      "../static/dice/dice6.png",
    ];
    console.log(yourPlayer + "==========" + `P${turn + 1}`);
    if (yourPlayer === `P${turn + 1}`) {
      const div = document.getElementById("p1-dice");
      div.innerHTML = "";
      div.style.backgroundImage = `url('${diceFace[value - 1]}')`;
      div.style.backgroundSize = "cover"; // Optional: cover the entire div
      div.style.backgroundPosition = "center";
    } else {
      const div = document.getElementById("p1-dice");
      div.style.backgroundImage = "none";
      div.innerHTML = "<p> Wait for opponent move </p>";
    }
  }
}

// UI.setPiecePosition('P1', 0, 0);
// UI.setTurn(0);
// UI.setTurn(1);

// UI.disableDice();
// UI.enableDice();
// UI.highlightPieces('P1', [0]);
// UI.unhighlightPieces();
// UI.setDiceValue(5);
