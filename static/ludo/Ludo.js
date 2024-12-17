import {
  BASE_POSITIONS,
  HOME_ENTRANCE,
  HOME_POSITIONS,
  PLAYERS,
  SAFE_POSITIONS,
  START_POSITIONS,
  STATE,
  TURNING_POINTS,
} from "./constants.js";
import { UI } from "./UI.js";

export class Ludo {
  tempPositions = {
    P1: [],
    P2: [],
  };
  currentPositions = {
    P1: [],
    P2: [],
  };
  diceFace = [
    "../static/dice/dice1.png",
    "../static/dice/dice2.png",
    "../static/dice/dice3.png",
    "../static/dice/dice4.png",
    "../static/dice/dice5.png",
    "../static/dice/dice6.png",
  ];

  yourPlayer = null;
  opponentValue = {};
  opponentDATA = {};
  _diceValue;
  checkVariable;
  get diceValue() {

    return this._diceValue;
  }
  set diceValue(value) {
    this._diceValue = value;
    UI.setDiceValue(value);
  }

  _turn;
  get turn() {
    return this._turn;
  }
  set turn(value) {
    this._turn = value;
    UI.setTurn(value, this.yourPlayer, this.diceValue);
  }

  _state;
  get state() {
    return this._state;
  }
  set state(value) {
    this._state = value;
    if (value === STATE.DICE_NOT_ROLLED) {
      UI.enableDice();
      UI.unhighlightPieces();
    } else {
      UI.disableDice();
    }
  }

  constructor() {
    console.log("Hello World! Let's play Ludo!");
    this.yourPlayer = undefined;
    this.connectWebSocket();
    this.listenDiceClick();

    this.listenPieceClick();

    this.resetGame();



    // Call the initialization method
    this.init();

  }
  init() {
    // Simulating asynchronous variable assignment

    // Start the interval to check for yourPlayer
    this.checkVariable = setInterval(() => {
      console.log(this.yourPlayer + " ---------=");

      if (this.yourPlayer !== undefined) {
        console.log("Player is defined, showing content.");

        // Hide loader and show content
        document.getElementById("loader").style.display = "none";
        document.getElementById("content").style.display = "block";

        // Clear the interval
        clearInterval(this.checkVariable);

      }
    }, 1000);
  }

  listenDiceClick() {
    UI.listenDiceClick(this.onDiceClick.bind(this));
  }
  wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  async onDiceClick() {
    console.log("1");
    if (this.yourPlayer !== `P${this.turn + 1}`) {
      console.log(`${this.yourPlayer} == P${this.turn + 1}`);
      console.log("It is not your turn to roll the dice.");
      return;
    }

    console.log("dice clicked test");
    let randomValue;
    // 70% chance for 6, 30% chance for other values
    if (Math.random() < 0.7) {
      randomValue = 6; // 70% chance
    } else {
      randomValue = 1 + Math.floor(Math.random() * 5); // 30% chance for 1 to 5
    }
    this.diceValue = randomValue;

    this.state = STATE.DICE_ROLLED;
   
    this.checkForEligiblePieces();


    this.sendDataDiceTurn(this.diceValue, this.turn);
  }

  async checkForEligiblePieces() {
    console.log("2");
    const player = PLAYERS[this.turn];
    const eligiblePieces = this.getEligiblePieces(player);
    if (eligiblePieces.length) {
      UI.highlightPieces(player, eligiblePieces);
    } else {
      
      this.incrementTurn();
    }
  }

  incrementTurn() {
    console.log("3");
    this.turn = this.turn === 0 ? 1 : 0;
    this.state = STATE.DICE_NOT_ROLLED;
  }

  getEligiblePieces(player) {
    console.log("4");
    return [0, 1, 2, 3].filter((piece) => {
      const currentPosition = this.currentPositions[player][piece];
      if (currentPosition === HOME_POSITIONS[player]) {
        return false;
      }
      if (
        BASE_POSITIONS[player].includes(currentPosition) &&
        this.diceValue !== 6
      ) {
        return false;
      }
      if (
        HOME_ENTRANCE[player].includes(currentPosition) &&
        this.diceValue > HOME_POSITIONS[player] - currentPosition
      ) {
        return false;
      }
      return true;
    });
  }


  resetGame() {
    console.log("Reset game");
    this.currentPositions = structuredClone(BASE_POSITIONS);

    PLAYERS.forEach((player) => {
      [0, 1, 2, 3].forEach((piece) => {
        this.setPiecePosition(
          player,
          piece,
          this.currentPositions[player][piece]
        );
      });
    });

    this.turn = 0;
    this.state = STATE.DICE_NOT_ROLLED;
  }

  listenPieceClick() {
    console.log("5");
    UI.listenPieceClick(this.onPieceClick.bind(this));
  }

  onPieceClick(event) {
    console.log("6.0");
    const target = event.target;
    if (
      !target.classList.contains("player-piece") ||
      !target.classList.contains("highlight")
    ) {
      return;
    }

    if (this.yourPlayer !== `P${this.turn + 1}`) {
      console.log("It is not your turn to move a piece.");
      return;
    }

    console.log("Piece clicked");
    const player = target.getAttribute("player-id");
    const piece = target.getAttribute("piece");
    console.log(piece + " = " + player);
    this.handlePieceClick(player, piece);
  }

  handlePieceClick(player, piece) {
    console.log("6");
    console.log(player, piece);
    const currentPosition = this.currentPositions[player][piece];

    if (BASE_POSITIONS[player].includes(currentPosition)) {
      this.setPiecePosition(player, piece, START_POSITIONS[player]);
      this.state = STATE.DICE_NOT_ROLLED;
      return;
    }

    UI.unhighlightPieces();
    this.movePiece(player, piece, this.diceValue);
  }

  setPiecePosition(player, piece, newPosition) {
    console.log("7");

    this.currentPositions[player][piece] = newPosition;
    console.log(newPosition);

    UI.setPiecePosition(player, piece, newPosition);
    console.log(
      this.tempPositions + " ================= " + this.currentPositions
    );
    console.log(this.tempPositions);
    console.log(this.currentPositions);
    if (
      this.tempPositions[player][piece] !== this.currentPositions[player][piece]
    ) {
      this.sendGameData(
        piece,
        this.diceValue,
        this.currentPositions,
        this.turn
      );
    }
  }

  movePiece(player, piece, moveBy) {
    console.log("8");
    const interval = setInterval(() => {
      this.incrementPiecePosition(player, piece);
      moveBy--;

      if (moveBy === 0) {
        clearInterval(interval);

        if (this.hasPlayerWon(player)) {
          //// put here winere api
          alert(`Player: ${player} has won!`);
          if (this.yourPlayer === player) {
            /// call here winner api
            /// i win
            // this.sendWiningDAta()
          } else {
          }
          this.resetGame();
          return;
        }

        const isKill = this.checkForKill(player, piece);

        if (isKill || this.diceValue === 6) {
          this.state = STATE.DICE_NOT_ROLLED;
          // Send game data to server after the move
          this.sendGameData(
            piece,
            this.diceValue,
            this.currentPositions,
            this.turn
          );
          return;
        }

        this.incrementTurn();

        // Send game data to server after the turn has been incremented
        this.sendGameData(
          piece,
          this.diceValue,
          this.currentPositions,
          this.turn
        );
      }
    }, 200);
  }

  checkForKill(player, piece) {
    console.log("9");
    const currentPosition = this.currentPositions[player][piece];
    const opponent = player === "P1" ? "P2" : "P1";
    let kill = false;

    [0, 1, 2, 3].forEach((opponentPiece) => {
      const opponentPosition = this.currentPositions[opponent][opponentPiece];
      if (
        currentPosition === opponentPosition &&
        !SAFE_POSITIONS.includes(currentPosition)
      ) {
        this.setPiecePosition(
          opponent,
          opponentPiece,
          BASE_POSITIONS[opponent][opponentPiece]
        );
        /// here is you have to add senddata
        this.sendKillData(
          opponent,
          this.diceValue,
          this.turn,
          opponentPiece,
          BASE_POSITIONS[opponent][opponentPiece]
        );

        kill = true;
      }
    });

    return kill;
  }

  hasPlayerWon(player) {
    console.log("10");
    return [0, 1, 2, 3].every(
      (piece) => this.currentPositions[player][piece] === HOME_POSITIONS[player]
    );
  }

  incrementPiecePosition(player, piece) {
    console.log("11");
    this.setPiecePosition(
      player,
      piece,
      this.getIncrementedPosition(player, piece)
    );
  }

  sendIncremnet(player, piece, postion) {
    console.log("11");
    this.setPiecePosition(player, piece, postion);
  }

  getIncrementedPosition(player, piece) {
    console.log("12");
    const currentPosition = this.currentPositions[player][piece];
    console.log(currentPosition);
    if (currentPosition === TURNING_POINTS[player]) {
      return HOME_ENTRANCE[player][0];
    } else if (currentPosition === 51) {
      return 0;
    }
    return currentPosition + 1;
  }

  sendKillData(opponent, diceValue, nextTurn, opponentPiece, newPosition) {
    console.log("data sensd");
    const dataToSend = {
      message: "kill",
      diceValue: diceValue,
      opponent: opponent,
      nextTurn: nextTurn,
      opponentPiece: opponentPiece,
      newPosition: newPosition,
    };
    console.log("Sended data");
    console.log(dataToSend);
    try {
      this.socket.send(JSON.stringify(dataToSend));
      console.log("done");
    } catch (e) {
      console.log(e);
    }
  }
  // WebSocket Integration
  connectWebSocket() {
    const urlParams = new URLSearchParams(window.location.search);
    const userid = urlParams.get("userid");
    const priceid = urlParams.get("priceid");
    this.socket = new WebSocket(
      `ws://127.0.0.1:8080/find-opponent/${userid}/${priceid}`
    );

    this.socket.onopen = () => {
      console.log("WebSocket connection established");
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received WebSocket message:", data);

      if (data.message === "game data" && data.data_received) {
        if (data.data_received.message === "next turn") {
          this.turn = data.data_received.nextTurn;
          this.diceValue = data.data_received.diceValue;
          // if (this.yourPlayer === "P2") {
          //   const div = document.getElementById("p1-dice");
          //   div.style.backgroundImage = `url('${
          //     this.diceFace[this.diceValue - 1]
          //   }')`;
          //   div.style.backgroundSize = "cover"; // Optional: cover the entire div
          //   div.style.backgroundPosition = "center";
          // } else {
          //   const div = document.getElementById("p2-dice");
          //   div.style.backgroundImage = `url('${
          //     this.diceFace[this.diceValue - 1]
          //   }')`;
          //   div.style.backgroundSize = "cover"; // Optional: cover the entire div
          //   div.style.backgroundPosition = "center";
          // }
        } else if (data.data_received.message == "kill") {
          this.turn = data.data_received.nextTurn;
          this.setPiecePosition(
            data.data_received.opponent,
            Number(data.data_received.opponentPiece),
            BASE_POSITIONS[data.data_received.opponent][
            Number(data.data_received.opponentPiece)
            ]
          );
        } else {
          this.handleGameData(data.data_received);
        }
      }

      if (data.message === "Connected with opponent") {
        this.yourPlayer = data.your_player;
        console.log(this.yourPlayer + "======== here is player");
        this.opponentDATA = data.opponent_data;
        console.log("User Data:", userdata);
        if (this.yourPlayer === "P1") {
          document.getElementById("p1-player").textContent = userdata.name;
          document.getElementById("p2-player").textContent =
            data.opponent_data.name;
        } else {
          document.getElementById("p1-player").textContent =
            data.opponent_data.name;
          document.getElementById("p2-player").textContent = userdata.name;
        }
      }
    };

    this.socket.onclose = () => {
      console.log("WebSocket connection closed");
    };
  }

  handleGameData(dataReceived) {
    console.log("13");
    this.tempPositions = dataReceived.currentPosition;
    this.diceValue = dataReceived.diceValue;
    this.turn = dataReceived.nextTurn;
    this.piece = dataReceived.piece;
    const data = dataReceived.currentPosition;
    console.log(data);
    // if (this.yourPlayer === "P2") {
    //   const div = document.getElementById("p1-dice");
    //   div.style.backgroundImage = `url('${this.diceFace[this.diceValue - 1]}')`;
    //   div.style.backgroundSize = "cover"; // Optional: cover the entire div
    //   div.style.backgroundPosition = "center";
    // } else {
    //   const div = document.getElementById("p2-dice");
    //   div.style.backgroundImage = `url('${this.diceFace[this.diceValue - 1]}')`;
    //   div.style.backgroundSize = "cover"; // Optional: cover the entire div
    //   div.style.backgroundPosition = "center";
    // }
    this.setPiecePosition(
      `P${dataReceived.nextTurn + 1}`,
      Number(dataReceived.piece),
      data[`P${dataReceived.nextTurn + 1}`][Number(dataReceived.piece)]
    );

    // Set the role for your player (P1 or P2)

    // Optionally, set up the UI or handle opponent data
    if (dataReceived.opponent_data) {
      console.log("Opponent data:", dataReceived.opponent_data);
    }
  }

  // Method to send game data via WebSocket
  sendGameData(piece, diceValue, currentPosition, nextTurn, killID) {
    console.log("data sensd");
    const dataToSend = {
      message: "move",
      piece: piece,
      diceValue: diceValue,
      currentPosition: currentPosition,
      nextTurn: nextTurn,
      killId: killID,
    };
    console.log("Sended data");
    console.log(dataToSend);

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(dataToSend));

    } else {
      console.error("WebSocket is not open.");
    }
  }
  sendDataDiceTurn(diceValue, nextTurn) {
    console.log("data sensd");
    const dataToSend = {
      message: "next turn",
      diceValue: diceValue,
      nextTurn: nextTurn,
    };
    console.log("Sended data");
    console.log(dataToSend);
    try {
      this.socket.send(JSON.stringify(dataToSend));
      console.log("done");
    } catch (e) {
      console.log(e);
    }
  }
  sendWiningDAta(whowin, wholose) {
    console.log("data sensd");
    const dataToSend = {
      message: "Who win",
      whowin: whowin,
      wholose: wholose,
    };
    console.log("Sended data");
    console.log(dataToSend);
    try {
      this.socket.send(JSON.stringify(dataToSend));
      console.log("done");

    } catch (e) {
      console.log(e);
    }
  }
}
