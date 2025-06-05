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

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function drawBoard(tempCat = cat, tempRat = rat) {
  console.clear();
  for (let y = 0; y < BOARD_SIZE; y++) {
    let row = '';
    for (let x = 0; x < BOARD_SIZE; x++) {
      if (tempCat.x === x && tempCat.y === y) {
        row += '🐱';
      } else if (tempRat.x === x && tempRat.y === y) {
        row += '🐭';
      } else {
        row += '⬜';
      }
    }
    console.log(row);
  }
  console.log('Usa W/A/S/D para mover al gato. Ctrl+C para salir.');
}

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

let ratInterval;

async function dropFromTop(entity) {
  const finalY = entity.y;
  entity.y = 0;
  for (let y = 0; y <= finalY; y++) {
    entity.y = y;
    drawBoard();
    await sleep(100);
  }
  entity.y = finalY;
}

function onKeyPress(str, key) {
  if (key.sequence === '\u0003') {
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
}

async function startGame() {
  readline.emitKeypressEvents(process.stdin);
  process.stdin.setRawMode(true);

  await dropFromTop(cat);
  await dropFromTop(rat);
  drawBoard();

  ratInterval = setInterval(() => {
    moveRat();
    if (checkWin()) {
      endGame();
    } else {
      drawBoard();
    }
  }, 1000);

  process.stdin.on('keypress', onKeyPress);
}

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

startGame();
