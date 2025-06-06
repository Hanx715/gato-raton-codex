import random
import pygame

TILE_SIZE = 20

MAZE = [
    "########################",
    "#........#.............#",
    "#.####.#.#.####.#####.#",
    "#.#  #.#.#.#  #.#   #.#",
    "#.#  #.#.#.#  #.#   #.#",
    "#.####.#.#.####.#####.#",
    "#......................#",
    "#.####.#########.####.#",
    "#......................#",
    "########################",
]

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.speed = 2

    def move(self, dx, dy, walls):
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)
        if not any(new_rect.colliderect(w) for w in walls):
            self.rect = new_rect

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)

class Ghost:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color

    def move(self, walls):
        direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        new_rect = self.rect.move(direction[0], direction[1])
        if not any(new_rect.colliderect(w) for w in walls):
            self.rect = new_rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.walls = []
        self.points = []
        for row_idx, row in enumerate(layout):
            for col_idx, ch in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if ch == '#':
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif ch == '.':
                    self.points.append(pygame.Rect(x + 8, y + 8, 4, 4))

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 255), wall)
        for point in self.points:
            pygame.draw.rect(screen, (255, 255, 255), point)

class Game:
    def __init__(self):
        pygame.init()
        width = len(MAZE[0]) * TILE_SIZE
        height = len(MAZE) * TILE_SIZE
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mini Pac-Man")
        self.clock = pygame.time.Clock()
        self.maze = Maze(MAZE)
        self.player = Player(TILE_SIZE, TILE_SIZE)
        self.ghosts = [Ghost(18*TILE_SIZE, TILE_SIZE, (255, 0, 0))]
        self.running = True
        self.victory = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        self.player.move(dx, dy, self.maze.walls)

    def update(self):
        for ghost in self.ghosts:
            ghost.move(self.maze.walls)
            if ghost.rect.colliderect(self.player.rect):
                self.running = False
        self.maze.points = [p for p in self.maze.points if not p.colliderect(self.player.rect)]
        if not self.maze.points:
            self.victory = True
            self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        if self.victory:
            print("\n\u2714 Juego completado!\n")
        else:
            print("\n\u274c Has sido atrapado!\n")

if __name__ == "__main__":
    Game().run()
    pygame.quit()
