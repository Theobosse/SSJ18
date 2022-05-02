#
# Untitled Space Score Jam 18 Game
# By Arkanyota, Gouspourd, Theobosse & Yolwoocle
#  

from telnetlib import theNULL
import pygame
import math
import random
import time

from vector import Vect2


def keydown(*keys):
    pressed = pygame.key.get_pressed()
    for k in keys:
        if pressed[k]:
            return True
    return False


def keypressed(*keys):
    pressed = pygame.key.get_pressed()
    for k in keys:
        if pressed[k] and not Globals.oldpressed[k]:
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
    NORMAL = pygame.font.Font('./resources/fonts/Calibri_Regular.ttf', 64)

def display_text(screen, text, pos, color=pygame.Color(0, 0, 0)):
    if type(pos) == Vect2: 
        pos = pos.tuple()
    screen.blit(Fonts.NORMAL.render(text, True, color), pos)


class Actor(Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple, size: tuple, name: str = ''):
        super().__init__(image, pos, name)
        self.type = "undefined"
        self.pos = Vect2(*pos)
        self.vel = Vect2()
        self.gravity = 2
        self.w = size[0]
        self.h = size[1]
        self.state = "Falling"
        self.flip_x = False
        self.friction = .90

        self.is_magnetic = False

        self.is_deleted = False

    def update(self):
        self.update_pos()
        self.collision()
        self.pos += self.vel

    def update_pos(self):
        self.vel.y += self.gravity
        self.vel *= self.friction

    def collision(self):
        if self.pos.y > Globals.window_height - self.h - self.vel.y:
            self.vel.y -= self.vel.y
            self.state = "Grounded"

        xmod = pygame.rect.Rect(self.pos.x + self.vel.x, self.pos.y, self.rect.width, self.rect.height)
        ymod = pygame.rect.Rect(self.pos.x, self.pos.y + self.vel.y, self.rect.width, self.rect.height)
        xymod = pygame.rect.Rect(self.pos.x + self.vel.x, self.pos.y + self.vel.y, self.rect.width, self.rect.height)
        b = True
        if xmod.collidelist(Globals.GAME.map.sprites()) >= 0:
            self.vel.x *= -0.0001
            b = False
        if ymod.collidelist(Globals.GAME.map.sprites()) >= 0:
            self.vel.y *= -0.0001
            if self.vel.y < 0:
                self.state = "Grounded"
            b = False
        if b and xymod.collidelist(Globals.GAME.map.sprites()) >= 0:
            self.vel.x *= -0.0001
            self.vel.y *= -0.0001
            if self.vel.y < 0:
                self.state = "Grounded"

    def draw(self, screen: pygame.surface.Surface):
        image = pygame.transform.flip(self.image, self.flip_x, False)
        screen.blit(image, self.pos.tuple())


class Player(Actor):
    def __init__(self, name="Steve", x=0, y=0):
        super().__init__(image('magnet_blue', (64, 64)), (x, y), (64, 64), name)
        self.type = "player"
        self.name = name
        self.pos = Vect2(x, y)
        self.vel = Vect2(0, 0)
        self.dir = Vect2(0, 0)
        self.w = 64
        self.h = 64
        self.pole = "-"
        self.gravity = 1.5

        self.image_blue = image('magnet_blue', (64, 64))
        self.image_red = image('magnet_red', (64, 64))

        self.is_magnetic = True
        self.is_active = False

        self.magneticField = MagneticField(x, y, 3, self.pole, 400)
        Globals.GAME.new_actor(self.magneticField)

        self.flip_x = False

        self.speed = 1
        self.jump_speed = 40
        self.max_jump_nb = 3
        self.jump_nb = self.max_jump_nb

        self.state = "Falling"

    def update(self):
        self.movement()
        super().update()
        self.do_magnetism()
        if self.pole == "-":
            self.image = self.image_red
        else:
            self.image = self.image_blue
    
        if self.state == "Grounded":
            self.jump_nb = self.max_jump_nb

    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)

    def movement(self):
        xdir = 0
        dir = Vect2(0,0)
        if keydown(pygame.K_LEFT, pygame.K_q, pygame.K_a):
            xdir -= 1
            dir.x -= 1
        if keydown(pygame.K_RIGHT, pygame.K_d):
            xdir += 1
            dir.x += 1
        if keydown(pygame.K_UP, pygame.K_z, pygame.K_w):
            dir.y -= 1
        if keydown(pygame.K_DOWN, pygame.K_s):
            dir.y += 1

        if keypressed(pygame.K_SPACE,pygame.K_c):
            self.jump()

        dir.normalize()
        self.vel.x += xdir * self.speed
        self.flip_x = self.vel.x < 0
        if dir.x or dir.y:
            self.dir = Vect2(dir.x, dir.y)
    
    def do_magnetism(self):
        self.is_active = keypressed(pygame.K_x,pygame.K_RSHIFT)
        if self.is_active:
            if self.pole == "+":
                self.pole = "-"
            else:
                self.pole = "+"    

        self.magneticField.pos = self.pos
        self.magneticField.pole = self.pole
        #if self.is_active :
        #    Globals.GAME.new_actor(MagneticField(self.pos.x, self.pos.y, "-", 200))

    def jump(self):
        if self.jump_nb > 0:
            self.vel.y = -self.jump_speed
            self.jump_nb -= 1
            self.state = "Jumping"


class MagneticField:
    def __init__(self, x=0, y=0, strength=5, pole="+", radius=100):
        self.pos = Vect2(x, y)
        self.strength = strength
        self.radius = radius
        self.is_magnetic = False
        self.pole = pole

        self.is_deleted = False

    def update(self):
        # TODO
        for actor in Globals.GAME.actors:
            if math.dist(self.pos.tuple(), actor.pos.tuple()) <= self.radius:
                if actor.is_magnetic:
                    diff = (actor.pos - self.pos).normalized()
                    actor.vel += diff * self.strength * (
                                (self.pole != actor.pole) * 2 - 1)

    def draw(self, surface: pygame.surface.Surface):
        if self.pole == "+":
            color = Colors.BLUE
        else:
            color = Colors.RED
        pygame.draw.circle(surface, color, self.pos.tuple(), self.radius)
    


class Enemy(Actor):
    def __init__(self, x=0, y=0, name:str='enemy'):
        super().__init__(image('can', (64, 64)), (x,y), (64, 64), name)
        self.type = "enemy"
        self.pos = Vect2(x,y)
        self.is_stuck = False
        self.is_magnetic = True
        self.pole = "+"

        self.friction = .95
        self.gravity = 1

        self.radius = 32


    def update(self):
        super().update()
        self.do_magnetism()
        self.do_stuck()
        self.enemy_collision()

    def draw(self, screen):
        image = pygame.transform.flip(self.image, False, False)
        screen.blit(image, self.pos.tuple())
        if self.is_stuck:
            display_text(screen, "STUCK", self.pos)

    def do_magnetism(self):
        player = Globals.GAME.player

        if player.is_active:
            # Attraction to player
            diff = (player.pos - self.pos).normalized()
            self.vel += diff * 3
            # counter gravity
            self.vel.y -= self.gravity
        
    def do_stuck(self):
        player = Globals.GAME.player
        dist = self.pos.dist(player.pos)
        old_stuck = self.is_stuck

        # Stuck if player active and close enough
        if player.is_active:
            if dist < self.radius:
                self.is_stuck = True
        else:
            self.is_stuck = False

        if self.is_stuck:
            self.pos = player.pos
        else:
            # If stuckness has just been deactivated, launch 
            if old_stuck:
                self.vel = player.dir + (Vect2(random.random(),random.random())*.5) * 20
                player.vel -= player.dir * 10
    
    def enemy_collision(self):
        for actor in Globals.GAME.actors:
            if type(actor) == Enemy and actor != self:
                dist = self.pos.dist(actor.pos)
                if dist <= self.radius + actor.radius and not actor.is_stuck and not self.is_stuck:
                    self.collision_reaction(actor)

    def collision_reaction(self, actor):
        are_not_stuck = not actor.is_stuck and not self.is_stuck
        if actor.vel.norm() > 10 and are_not_stuck:
            ...
            #self.is_deleted = True
            #actor.is_deleted = True
        
        # Repulsion
        diff = (actor.pos - self.pos).normalized()
        self.vel += -diff * 3
        actor.vel += diff * 3


class Game:
    def __init__(self, window_width, window_height):

        self.window_width = window_width
        self.window_height = window_height
        self.actors = []
        self.map = pygame.sprite.Group()

    def update(self, screen):
        if Globals.frame == 1:
            self.player = Player()

            self.new_wall(400, 500, 100, 100, Colors.GREEN)
            self.new_wall(200, 400, 100, 100, Colors.GREEN)
            self.new_wall(150, 200, 100, 100, Colors.GREEN)
            self.new_wall(700, 500, 100, 100, Colors.GREEN)
            self.new_wall(600, 400, 100, 100, Colors.GREEN)
            self.new_wall(450, 200, 100, 100, Colors.GREEN)

            self.new_actor(MagneticField(300, 300, 3, "+", 100))
            self.new_actor(MagneticField(600, 200, 3, "-", 100))
            self.new_actor(MagneticField(800, 500, 3, "-", 100))
            self.new_actor(MagneticField(1100, 0, 3, "+", 400))
            
            self.new_actor(self.player)

            for i in range(10):
                x = random.randint(0, self.window_width)
                y = random.randint(0, self.window_height)
                self.new_actor(Enemy(x, y))
                self.new_actor(Enemy(400, 50))

        Globals.frame += 1
        screen.fill(Colors.BG)
        screen.blit(Fonts.TITLE.render("Hello", True, Colors.BLUE), (10, 10))
        for a in self.actors:
            a.update()
        for a in self.actors:
            if a.is_deleted:
                self.actors.remove(a)

        for a in self.actors:
            a.draw(screen)
        self.map.draw(screen)
        # Sprite(image())
        Globals.oldpressed = pygame.key.get_pressed()

    def new_actor(self, actor):
        self.actors.append(actor)

    def new_wall(self, x, y, w, h, color):
        rect = pygame.rect.Rect(x, y, w, h)
        surf = pygame.Surface(rect.size)
        surf.fill(color)
        self.map.add(Sprite(surf, (x, y)))


class Globals:
    window_width = int(1366 * 1.25)
    window_height = int(768 * 1.25)

    GAME = Game(window_width, window_height)
    FPS = 60
    frame = 0

    oldpressed = []
    magnetic_fields = []

    GRAVITY = 3


def main():
    pygame.init()
    screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
    pygame.display.set_caption("Little PI²")

    # Game Loop
    running = True
    t = 0
    oldtime = time.time()

    while running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Stop game
                if event.key == pygame.K_F12:
                    running = False

        #print(time.time(), "diff=", 1000*(oldtime-time.time()))
        t -= 1000 * (time.time() - oldtime)
        limit = 10
        while t < 0 and limit > 0:
            limit -= 1
            t += 1000 // Globals.FPS
            # Update & Draw
            Globals.GAME.update(screen)
            pygame.display.flip()
            #pygame.time.delay(1000 // Globals.FPS)

        oldtime = time.time()

    pygame.quit()


if __name__ == "__main__":
    main()
