import math
import pygame
import random

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
score = 0

class Player(object):
    
    def __init__(self):
        self.img = ship_img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.angle = 0
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h //2)

    def draw(self, win):
        win.blit(self.rotated, self.rotated_rect)

    def turnLeft(self):
        self.angle += 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h//2)

    def moveForward(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.w//2, self.y - self.sin * self.h//2)
        

class Bullet(object):
    
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.cos = player.cos
        self.sin = player.sin
        self.x_velocity = self.cos * 10
        self.y_velocity = self.sin * 10

    def move(self):
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > WIDTH or self.y > HEIGHT or self.y < -50:
            return True

class Asteroid(object):

    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = small_asteroid_img
        elif self.rank == 2:
            self.image = medium_asteroid_img
        else:
            self.image = big_asteroid_img
        self.w = 50 * rank
        self.h = 50 * rank
        self.random_point = random.choice([(random.randrange(0, WIDTH - self.w), random.choice([-1*self.h - 5, HEIGHT + 5])), (random.choice([-1*self.w - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.h))])
        self.x, self.y = self.random_point
        if self.x < WIDTH//2:
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self.y < HEIGHT//2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.x_velocity = self.x_direction * random.randrange(1,3)
        self.y_velocity = self.y_direction * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


player = Player()
asteroids = []
bullets = []
count = 0

def draw_window():
    window.blit(bg_img, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    score_txt = font.render('Score: ' + str(score), 1, (255,255,255))
    
    player.draw(window)

    for a in asteroids:
        a.draw(window)
    for b in bullets:
        b.draw(window)

    window.blit(score_txt, (WIDTH - score_txt.get_width() - 25, 25))
    
    pygame.display.update()

while run:
    clock.tick(60)
    count += 1

    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))

        for b in bullets:
            b.move()
            if b.checkOffScreen():
                bullets.pop(bullets.index(b))

        for a in asteroids:
            a.x += a.x_velocity
            a.y += a.y_velocity

            # bullet collision
            for b in bullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                        asteroids.pop(asteroids.index(a))
                        bullets.pop(bullets.index(b))
                        break
        
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
