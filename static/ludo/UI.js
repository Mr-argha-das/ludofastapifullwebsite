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

    let blueFace = [
      "../static/dice/blue/dice1.png",
      "../static/dice/blue/dice2.png",
      "../static/dice/blue/dice3.png",
      "../static/dice/blue/dice4.png",
      "../static/dice/blue/dice5.png",
      "../static/dice/blue/dice6.png",
    ];
    let greenFace = [
      "../static/dice/green/dice1.png",
      "../static/dice/green/dice2.png",
      "../static/dice/green/dice3.png",
      "../static/dice/green/dice4.png",
      "../static/dice/green/dice5.png",
      "../static/dice/green/dice6.png",
    ];
    if (yourPlayer === "P1" && yourPlayer !== undefined) {
      const div = document.getElementById("p1-dice");
      div.innerHTML = "";
      div.style.backgroundImage = `url('${
        blueFace[dicevalue === undefined ? 0 : dicevalue - 1]
      }')`;
      div.style.backgroundSize = "cover"; // Optional: cover the entire div
      div.style.backgroundPosition = "center";
    } else {
      const div = document.getElementById("p1-dice");
      div.innerHTML = "";
      div.style.backgroundImage = `url('${
        greenFace[dicevalue === undefined ? 0 : dicevalue - 1]
      }')`;
      div.style.backgroundSize = "cover"; // Optional: cover the entire div
      div.style.backgroundPosition = "center";
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
    let logicbool = false;
    let blueFace = [
      "../static/dice/blue/dice1.png",
      "../static/dice/blue/dice2.png",
      "../static/dice/blue/dice3.png",
      "../static/dice/blue/dice4.png",
      "../static/dice/blue/dice5.png",
      "../static/dice/blue/dice6.png",
    ];
    let greenFace = [
      "../static/dice/green/dice1.png",
      "../static/dice/green/dice2.png",
      "../static/dice/green/dice3.png",
      "../static/dice/green/dice4.png",
      "../static/dice/green/dice5.png",
      "../static/dice/green/dice6.png",
    ];

    if (yourPlayer === "P1") {
      const div = document.getElementById("p1-dice");
      div.innerHTML = "";
      div.style.backgroundImage = `url('${blueFace[value - 1]}')`;
      div.style.backgroundSize = "cover"; // Optional: cover the entire div
      div.style.backgroundPosition = "center";
    } else {
      const div = document.getElementById("p1-dice");
      div.innerHTML = "";
      div.style.backgroundImage = `url('${greenFace[value - 1]}')`;
      div.style.backgroundSize = "cover"; // Optional: cover the entire div
      div.style.backgroundPosition = "center";
    }
  }
}
