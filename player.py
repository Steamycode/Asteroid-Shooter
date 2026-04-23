import pygame
import math
from assets import ship_img, WIDTH, HEIGHT
from bullet import Bullet
from game_object import GameObject

pygame.init()

class Player(GameObject):
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.img = ship_img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.angle = 0
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect(center = (self.x, self.y))
        self.update_direction()
        self.bullets = []

    def draw(self, win):
        super().draw(win)
        win.blit(self.rotated, self.rotated_rect)

    def fire(self):
        new_bullet = Bullet(self.head[0], self.head[1], self.cos, self.sin)
        self.bullets.append(new_bullet)

    def turn_left(self):
        self.angle += 5
        self.update_rotation()

    def turn_right(self):
        self.angle -= 5
        self.update_rotation()

    def move_forward(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.update_position()

    def update_rotation(self):
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

    def update_location(self):
        if self.x > WIDTH + 50:
            self.x = 0
        elif self.x < -self.width:
            self.x = WIDTH
        if self.y > HEIGHT + 50:
            self.y = HEIGHT
        elif self.y < -self.height:
            self.y = HEIGHT
