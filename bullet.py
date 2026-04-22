import pygame

from assets import WIDTH, HEIGHT


class Bullet():
    def __init__(self, x, y, cos, sin):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 4
        self.cos = cos
        self.sin = sin
        self.x_velocity = self.cos * 10
        self.y_velocity = self.sin * 10

    def move(self):
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.width, self.height])

    def checkOffScreen(self):
        if (self.x < -50 or self.x > WIDTH or self.y > HEIGHT or self.y < -50):
            return True