import pygame
import math

from assets import ship_img, WIDTH, HEIGHT


class Player():
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.width = ship_img.get_width()
        self.height = ship_img.get_height()
        self.img = ship_img
        self.angle = 0
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width // 2,
                     self.y - self.sin * self.height // 2)

    def draw(self, win):
        win.blit(self.rotated, self.rotated_rect)

    def turnLeft(self):
        self.angle += 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width // 2,
                     self.y - self.sin * self.height // 2)

    def turnRight(self):
        self.angle -= 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width // 2,
                     self.y - self.sin * self.height // 2)

    def moveForward(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width // 2,
                     self.y - self.sin * self.height // 2)

    def updateLocation(self):
        if self.x > WIDTH + 50:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = WIDTH
        elif self.y < -50:
            self.y = HEIGHT
        elif self.y > HEIGHT + 50:
            self.y = 0