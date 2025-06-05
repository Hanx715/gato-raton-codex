const readline = require('readline');

const ROWS = 6;
const COLS = 7;

const board = Array.from({ length: ROWS }, () => Array(COLS).fill(' '));
let currentPlayer = 'X';

function printBoard() {
  console.clear();
  for (let row = 0; row < ROWS; row++) {
    let line = '';
    for (let col = 0; col < COLS; col++) {
      line += `|${board[row][col]}`;
    }
    line += '|';
    console.log(line);
  }
  console.log(' ' + Array.from({ length: COLS }, (_, i) => i + 1).join(' '));
}

function dropPiece(col, piece) {
  for (let row = ROWS - 1; row >= 0; row--) {
    if (board[row][col] === ' ') {
      board[row][col] = piece;
      return row;
    }
  }
  return -1;
}

function countDirection(row, col, dx, dy, piece) {
  let r = row + dy;
  let c = col + dx;
  let count = 0;
  while (r >= 0 && r < ROWS && c >= 0 && c < COLS && board[r][c] === piece) {
    count++;
    r += dy;
    c += dx;
  }
  return count;
}

function checkWin(row, col, piece) {
  const directions = [
    [1, 0], // horizontal
    [0, 1], // vertical
    [1, 1], // diagonal down-right
    [1, -1] // diagonal up-right
  ];
  for (const [dx, dy] of directions) {
    const total =
      1 + countDirection(row, col, dx, dy, piece) + countDirection(row, col, -dx, -dy, piece);
    if (total >= 4) return true;
  }
  return false;
}

function boardFull() {
  return board.every(row => row.every(cell => cell !== ' '));
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

function askMove() {
  printBoard();
  rl.question(`Player ${currentPlayer}, choose column (1-${COLS}): `, answer => {
    const col = parseInt(answer, 10) - 1;
    if (!Number.isInteger(col) || col < 0 || col >= COLS) {
      console.log('Invalid column.');
      return askMove();
    }
    const row = dropPiece(col, currentPlayer);
    if (row === -1) {
      console.log('Column full. Try another one.');
      return askMove();
    }
    if (checkWin(row, col, currentPlayer)) {
      printBoard();
      console.log(`Player ${currentPlayer} wins!`);
      return rl.close();
    }
    if (boardFull()) {
      printBoard();
      console.log("It's a draw!");
      return rl.close();
    }
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    askMove();
  });
}

askMove();
