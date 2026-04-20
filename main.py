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
lives = 3
score = 0
sound_on = True

try:
    with open('scores.txt', 'r') as fr:
        high_score = int(fr.read())
except:
    print('Error loading scores file')
    high_score = 0

print('High Score: ' + str(high_score))

class Player(object):

    def __init__(self):
        self.img = ship_img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.angle = 0
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos*self.width//2, self.y - self.sin*self.height//2)

    def draw(self, win):
        win.blit(self.rotated, self.rotated_rect)

    def turnLeft(self):
        self.angle += 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos*self.width//2, self.y - self.sin*self.height//2)

    def turnRight(self):
        self.angle -= 5
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos*self.width//2, self.y - self.sin*self.height//2)

    def moveForward(self):
        self.x += self.cos*6
        self.y -= self.sin*6
        self.rotated = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos*self.width//2, self.y - self.sin*self.height//2)

    def updateLocation(self):
        if self.x > WIDTH + 50:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = WIDTH
        elif self.y < -50:
            self.y = HEIGHT
        elif self.y > HEIGHT + 50:
            self.y = 0

class Bullet(object):
        
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.width = 4
        self.height = 4
        self.cos = player.cos
        self.sin = player.sin
        self.x_velocity = self.cos*10
        self.y_velocity = self.sin*10

    def move(self):
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.width, self.height])

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
        self.width = 50*rank
        self.height = 50*rank
        self.ran_point = random.choice([(random.randrange(0, WIDTH - self.width), random.choice([-self.height - 5, HEIGHT + 5])), (random.choice([-self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))])
        self.x, self.y = self.ran_point
        if self.x < WIDTH//2:
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self.y < HEIGHT//2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.x_velocity = self.x_direction*random.randrange(1,3)
        self.y_velocity = self.y_direction*random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

player = Player()
asteroids = []
bullets = []
count = 0

def draw_window():

    window.blit(bg_img, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    lives_txt = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    restart_txt = font.render('Press Tab to Play Again', 1, (255,255,255))
    score_txt = font.render('Score: ' + str(score), 1, (255,255,255))
    high_score_txt = font.render('High Score: ' + str(high_score), 1, (255, 255, 255))

    player.draw(window)
    
    for a in asteroids:
        a.draw(window)

    for b in bullets:
        b.draw(window)

    if gameover:
        window.blit(restart_txt, (WIDTH//2 - restart_txt.get_width()//2, HEIGHT//2 - restart_txt.get_height()//2))
        
    window.blit(score_txt, (WIDTH - score_txt.get_width() - 25, 25))
    window.blit(lives_txt, (25, 25))
    window.blit(high_score_txt, (WIDTH - high_score_txt.get_width() - 25, 35 + score_txt.get_height()))
    
    pygame.display.update()

while run:
    clock.tick(60)
    count += 1
    
    if not gameover:

        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))

        player.updateLocation()
        
        for b in bullets:
            b.move()
            if b.checkOffScreen():
                bullets.pop(bullets.index(b))

        for a in asteroids:
            a.x += a.x_velocity
            a.y += a.y_velocity

            # player collision
            if (a.x >= player.x - player.width//2 and a.x <= player.x + player.width//2) or (a.x + a.width <= player.x + player.width//2 and a.x + a.width >= player.x - player.width//2):
                if(a.y >= player.y - player.height//2 and a.y <= player.y + player.height//2) or (a.y + a.height >= player.y - player.height//2 and a.y + a.height <= player.y + player.height//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if sound_on:
                        explosion_sound.play()
                    break

            # bullet collision
            for b in bullets:
                if (b.x >= a.x and b.x <= a.x + a.width) or b.x + b.width >= a.x and b.x + b.width <= a.x + a.width:
                    if (b.y >= a.y and b.y <= a.y + a.height) or b.y + b.height >= a.y and b.y + b.height <= a.y + a.height:
                        if a.rank == 3:
                            if sound_on:
                                explosion_sound.play()
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
                            if sound_on:
                                explosion_sound.play()
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
                            if sound_on:
                                explosion_sound.play()
                        asteroids.pop(asteroids.index(a))
                        bullets.pop(bullets.index(b))
                        break

        if lives <= 0:
            gameover = True

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
                    if sound_on:
                        shoot_sound.play()

            if event.key == pygame.K_m:
                sound_on = not sound_on

            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    
                    if score > high_score:
                        with open('scores.txt', 'w') as fw:
                            fw.write(str(score))
                        high_score = score
                    score = 0
    draw_window()

pygame.quit()
