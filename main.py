import pygame
import math

from vector import Vect2

def keydown(*keys):
    pressed = pygame.key.get_pressed()
    for k in keys:
        if pressed[k]:
            return True
    return False


def image(name: str, size: tuple, angle: int = 0, x_flip: bool = False, y_flip: bool = False):
    return pygame.transform.flip(pygame.transform.scale(pygame.transform.rotate(
        pygame.image.load(f'./resources/images/{name}.png'), angle), size), x_flip, y_flip)


class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple, name: str = ''):
        super(Sprite, self).__init__()
        self.name = name
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self, pos: tuple):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Colors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    BG = pygame.Color(200, 200, 200)


class Fonts:
    pygame.font.init()
    TITLE = pygame.font.Font('./resources/fonts/Calibri_Bold.TTF', 64)


class Player(Sprite):
    def __init__(self, name="Steve", x=0, y=0):
        super().__init__(image('magnet', (64, 64)), (x, y), name)
        self.name = name
        self.pos = Vect2(x, y)
        self.vel = Vect2(0, 0)
        self.w = 32
        self.h = 32
        
        self.speed = 0.5
        self.jump_speed = 20
        self.gravity = 3

        self.is_jumping = False
        self.is_falling = False

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.pos.tuple())

    def update(self):
        self.movement()
        self.update_pos()

        self.vel *= .90
        self.vel.y += self.gravity
        self.collision()

    def movement(self):
        dir = Vect2(0, 0)
        if keydown(pygame.K_LEFT, pygame.K_q):
            dir.x -= 1
        if keydown(pygame.K_RIGHT, pygame.K_d):
            dir.x += 1
        if keydown(pygame.K_UP, pygame.K_z):
            self.vel.y = -self.jump_speed

        dir.normalize()
        self.vel += dir * self.speed
        
    def update_pos(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
    
    def collision(self):
        # Théodore, bonne chance :3
        if self.pos.y > Globals.window_height - self.h:
            self.pos.y = Globals.window_height - self.h


class Game:
    def __init__(self):
        self.player = Player()
        self.actors = [self.player]

    # Game.update.getlook.fertilize.elevat.add.divide.getpos.x.world.sup.label.groud.is_maj()

    def update(self, screen):
        Globals.frame += 1
        screen.fill(Colors.BG)
        screen.blit(Fonts.TITLE.render("Hello", True, Colors.BLUE), (10, 10))
        for a in self.actors:
            a.update()
        for a in self.actors:
            a.draw(screen)
        # Sprite(image())


class Globals:
    window_width = 800
    window_height = 600
    GAME = Game()
    FPS = 60
    frame = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
    pygame.display.set_caption("Little PI²")
    
    # Game Loop
    running = True

    while running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Hey, you pressed the key {event.key}!")
                # Stop game
                if event.key == pygame.K_F12:
                    running = False

        # Update & Draw
        Globals.GAME.update(screen)
        pygame.display.flip()
        pygame.time.delay(1000 // Globals.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()