import os
import pygame
from game_assets.game_methods import collide

RED_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
PLAYER_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

WIDTH, HEIGHT = 650, 650


class Ship:
    MAX_COOLDOWN = 30

    def __init__(self, x_pos, y_pos, health=100):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down = 0

    def draw(self, window):
        # draw ship at specified location
        window.blit(self.ship_img, (self.x_pos, self.y_pos))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offscreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down >= self.MAX_COOLDOWN:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def shoot(self):
        if self.cool_down == 0:
            laser = Laser(self.x_pos - 15, self.y_pos, self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1

    def collision(self, obj):
        return collide(obj, self)

    # determine the location of the ship
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x_pos, y_pos, health=100):
        super().__init__(x_pos, y_pos, health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)  # create mask to show true collision of ship
        self.max_health = health
        self.score = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offscreen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.score += 25
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        green_health = self.health/self.max_health
        pygame.draw.rect(window, (255, 0, 0), (self.x_pos, self.y_pos + self.ship_img.get_height() + 15,
                                               self.ship_img.get_width(), 15))
        pygame.draw.rect(window, (0, 255, 0), (self.x_pos, self.y_pos + self.ship_img.get_height() + 15,
                                               self.ship_img.get_width() * green_health, 15))


class Enemy(Ship):
    COLOR_MAP = {
        'red': (RED_SHIP, RED_LASER),
        'green': (GREEN_SHIP, GREEN_LASER),
        'blue': (BLUE_SHIP, BLUE_LASER)
    }

    def __init__(self, x_pos, y_pos, color, health = 100):
        super().__init__(x_pos, y_pos, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y_pos += vel


class Laser:
    def __init__(self, x_pos, y_pos, img):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x_pos, self.y_pos))

    def move(self, vel):
        self.y_pos += vel

    def offscreen(self, height):
        return not height >= self.y_pos >= 0

    def collision(self, obj):
        return collide(obj, self)
