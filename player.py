import pygame
import math
from assets import AssetManager
from game_object import GameObject


class Player(GameObject):
    
    def __init__(self):
        self._assets = AssetManager()
        self._x = self._assets._screen_width // 2
        self._y = self._assets._screen_height // 2
        self._img = self._assets.ship_img
        self._width = self._img.get_width()
        self._height = self._img.get_height()
        self._angle = 0
        self._rotated = pygame.transform.rotate(self._img, self._angle)
        self._rotated_rect = self._rotated.get_rect(center=(self._x, self._y))
        self._bullets = []
        self.update_direction()

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
    def angle(self):
        return self._angle

    def draw(self, win):
        super().draw(win)
        win.blit(self._rotated, self._rotated_rect)

    def fire(self, bullet):
        self._bullets.append(bullet)

    def turn_left(self):
        self.update_rotation(5)

    def turn_right(self):
        self.update_rotation(-5)

    def move_forward(self):
        self._x += self._cos * 6
        self._y -= self._sin * 6
        self.update_position()

    def update_rotation(self, angle):
        self._angle += angle
        self._rotated = pygame.transform.rotate(self._img, self._angle)
        self._rotated_rect = self._rotated.get_rect(center=(self._x, self._y))
        self.update_direction()

    def update_position(self):
        self._rotated_rect = self._rotated.get_rect(center=(self._x, self._y))
        self.update_direction()

    def update_direction(self):
        self._cos = math.cos(math.radians(self._angle + 90))
        self._sin = math.sin(math.radians(self._angle + 90))
        self._head = (self._x + self._cos * self._width // 2,
                      self._y - self._sin * self._height // 2)

    def update_location(self, width, height):
        if self._x > width + 50:
            self._x = 0
        elif self._x < -50:
            self._x = width
        if self._y > height + 50:
            self._y = 0
        elif self._y < -50:
            self._y = height
