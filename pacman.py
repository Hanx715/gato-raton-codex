import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 2

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Mini Pac-Man")
        self.clock = pygame.time.Clock()
        self.player = Player(40, 40)
        self.running = True

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
        self.player.move(dx, dy)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.handle_input()
            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
    pygame.quit()
