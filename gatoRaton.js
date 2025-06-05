const readline = require('readline');

const BOARD_SIZE = 10;

function randomPosition() {
  return {
    x: Math.floor(Math.random() * BOARD_SIZE),
    y: Math.floor(Math.random() * BOARD_SIZE)
  };
}

let cat = randomPosition();
let rat = randomPosition();
while (cat.x === rat.x && cat.y === rat.y) {
  rat = randomPosition();
}

readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

function drawBoard() {
  console.clear();
  for (let y = 0; y < BOARD_SIZE; y++) {
    let row = '';
    for (let x = 0; x < BOARD_SIZE; x++) {
      if (cat.x === x && cat.y === y) {
        row += '🐱';
      } else if (rat.x === x && rat.y === y) {
        row += '🐭';
      } else {
        row += '⬜';
      }
    }
    console.log(row);
  }
  console.log('Usa W/A/S/D para mover al gato. Ctrl+C para salir.');
}

drawBoard();

function move(entity, dx, dy) {
  entity.x = Math.min(BOARD_SIZE - 1, Math.max(0, entity.x + dx));
  entity.y = Math.min(BOARD_SIZE - 1, Math.max(0, entity.y + dy));
}

function moveRat() {
  const dirs = [
    { dx: 0, dy: -1 },
    { dx: 0, dy: 1 },
    { dx: -1, dy: 0 },
    { dx: 1, dy: 0 }
  ];
  const dir = dirs[Math.floor(Math.random() * dirs.length)];
  move(rat, dir.dx, dir.dy);
}

function checkWin() {
  return cat.x === rat.x && cat.y === rat.y;
}

const ratInterval = setInterval(() => {
  moveRat();
  if (checkWin()) {
    endGame();
  } else {
    drawBoard();
  }
}, 1000);

process.stdin.on('keypress', (str, key) => {
  if (key.sequence === '\u0003') { // Ctrl+C
    endGame(true);
    return;
  }
  switch (key.name) {
    case 'w':
      move(cat, 0, -1);
      break;
    case 's':
      move(cat, 0, 1);
      break;
    case 'a':
      move(cat, -1, 0);
      break;
    case 'd':
      move(cat, 1, 0);
      break;
  }
  if (checkWin()) {
    endGame();
  } else {
    drawBoard();
  }
});

function endGame(exitOnly = false) {
  clearInterval(ratInterval);
  process.stdin.setRawMode(false);
  process.stdin.pause();
  if (!exitOnly) {
    drawBoard();
    console.log('¡El gato atrapó al ratón!');
  }
  process.exit();
}

