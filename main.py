import math
import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720

bg_img = pygame.image.load('assets/sprites/space.png')
ship_img = pygame.image.load('assets/sprites/spaceship.png')
medium_asteroid_img = pygame.image.load('assets/sprites/asteroid.png')
big_asteroid_img = pygame.transform.scale(medium_asteroid_img, (150, 150))
small_asteroid_img = pygame.transform.scale(medium_asteroid_img, (50, 50))

shoot_sound = pygame.mixer.Sound('assets/sounds/laser.mp3')
explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.mp3')
shoot_sound.set_volume(.25)
explosion_sound.set_volume(.25)

pygame.display.set_caption('Asteroids')

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

run = True
gameover = False

class Player(object):
    
    def __init__(self):
        self.img = ship_img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.angle = 0
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotated.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h //2)

    def draw(self, win):
        win.blit(self.rotated, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotated.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotated.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h//2)

    def moveForward(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotated.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h//2)

class Bullet(object):
    
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cos
        self.s = player.sin
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > WIDTH or self.y > HEIGHT or self.y < -50:
            return True

player = Player()
bullets = []

def draw_window():
    window.blit(bg_img, (0, 0))
    
    player.draw(window)

    for b in bullets:
        b.draw(window)
    
    pygame.display.update()

while run:
    clock.tick(60)
    
    if not gameover:
        for b in bullets:
            b.move()
            if b.checkOffScreen():
                bullets.pop(bullets.index(b))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    bullets.append(Bullet())
                    

    draw_window()

pygame.quit()
