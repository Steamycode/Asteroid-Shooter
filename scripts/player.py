import pygame
import math
from scripts.assets import AssetManager
from scripts.game_object import GameObject


class Player(GameObject):
    
    def __init__(self):
        self._assets = AssetManager()
        self._x = self.assets.screen_width // 2
        self._y = self.assets.screen_height // 2
        self._img = self.assets.ship_img
        self._width = self.img.get_width()
        self._height = self.img.get_height()
        self._angle = 0
        self._rotated = pygame.transform.rotate(self.img, self.angle)
        self._rotated_rect = self.rotated.get_rect(center=(self.x, self.y))
        self._bullets = []
        self.update_direction()

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    @property
    def bullets(self):
        return self._bullets
    
    @property
    def head(self):
        return self._head
    
    @head.setter
    def head(self, value):
        self._head = value
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def cos(self):
        return self._cos
    
    @cos.setter
    def cos(self, value):
        self._cos = value
    
    @property
    def sin(self):
        return self._sin
    
    @sin.setter
    def sin(self, value):
        self._sin = value
    
    @property
    def rotated(self):
        return self._rotated
    
    @rotated.setter
    def rotated(self, value):
        self._rotated = value
    
    @property
    def rotated_rect(self):
        return self._rotated_rect
    
    @rotated_rect.setter
    def rotated_rect(self, value):
        self._rotated_rect = value

    @property
    def assets(self):
        return self._assets

    @property
    def img(self):
        return self._img
    
    def draw(self, win):
        super().draw(win)
        win.blit(self.rotated, self.rotated_rect)

    def fire(self, bullet):
        self.bullets.append(bullet)

    def turn_left(self):
        self.update_rotation(5)

    def turn_right(self):
        self.update_rotation(-5)

    def move(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.update_position()

    def update_rotation(self, angle):
        self.angle += angle
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect(center=(self.x, self.y))
        self.update_direction()

    def update_position(self):
        self.rotated_rect = self.rotated.get_rect(center=(self.x, self.y))
        self.update_direction()

    def update_direction(self):
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width // 2,
                     self.y - self.sin * self.height // 2)

    def check_off_screen(self, width, height):
        if self.x > width + 50:
            self.x = 0
        elif self.x < -50:
            self.x = width
        if self.y > height + 50:
            self.y = 0
        elif self.y < -50:
            self.y = height
