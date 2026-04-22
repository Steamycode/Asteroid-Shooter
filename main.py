import pygame
import random

from assets import WIDTH, HEIGHT, bg_img, shoot_sound, explosion_sound
from asteroids import AsteroidFactory, MediumAsteroid, SmallAsteroid
from bullet import Bullet
from player import Player


pygame.init()

pygame.display.set_caption('Asteroids')

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class GameState():
    def __init__(self):
        self.run = True
        self.gameover = False
        self.lives = 3
        self.score = 0
        self.sound_on = True
        self.high_score = 0

    def add_score(self, points):
        self.score += points

    def lose_life(self):
        self.lives -= 1
        if self.sound_on:
            explosion_sound.play()
        if self.lives <= 0:
            self.gameover = True

    def toggle_sound(self):
        self.sound_on = not self.sound_on

    def change_gameover(self, value):
        self.gameover = value

    def reset(self):
        self.run = True
        self.gameover = False
        self.lives = 3
        self.score = 0
        self.sound_on = True

count = 0
variables = GameState()
asteroids = []
bullets = []
player = Player()

try:
    with open('scores.txt', 'r') as fr:
        variables.high_score = int(fr.read())
except (FileNotFoundError, ValueError):
    print('Error loading scores file')
    variables.high_score = 0


def draw_window():
    font = pygame.font.SysFont('arial', 30)
    lives_txt = font.render('Lives: ' + str(variables.lives), 1, (255, 255, 255))
    restart_txt = font.render('Press Tab to Play Again', 1, (255,255,255))
    score_txt = font.render('Score: ' + str(variables.score), 1, (255,255,255))
    high_score_txt = font.render('High Score: ' + str(variables.high_score), 1, (255, 255, 255))

    restart_x = WIDTH // 2 - restart_txt.get_width() // 2
    restart_y = HEIGHT // 2 - restart_txt.get_height() // 2
    score_x = WIDTH - score_txt.get_width() - 25
    score_y = 25
    high_score_x = WIDTH - high_score_txt.get_width() - 25
    high_score_y = 35 + score_txt.get_height()

    window.blit(bg_img, (0, 0))

    player.draw(window)
    
    for asteroid in asteroids:
        asteroid.draw(window)

    for bullet in bullets:
        bullet.draw(window)

    if variables.gameover:
        window.blit(restart_txt, (restart_x, restart_y))

    window.blit(score_txt, (score_x, score_y))
    window.blit(high_score_txt, (high_score_x, high_score_y))
    window.blit(lives_txt, (25, 25))
    
    pygame.display.update()


def handle_bullet_asteroid_collision(bullet, asteroid):
    if asteroid.rank == 3:
        if variables.sound_on:
            explosion_sound.play()
        variables.add_score(10)
        na1 = MediumAsteroid()
        na2 = MediumAsteroid()
        na1.x, na1.y = asteroid.x, asteroid.y
        na2.x, na2.y = asteroid.x, asteroid.y
        asteroids.append(na1)
        asteroids.append(na2)
    elif asteroid.rank == 2:
        if variables.sound_on:
            explosion_sound.play()
        variables.add_score(20)
        na1 = SmallAsteroid()
        na2 = SmallAsteroid()
        na1.x, na1.y = asteroid.x, asteroid.y
        na2.x, na2.y = asteroid.x, asteroid.y
        asteroids.append(na1)
        asteroids.append(na2)
    else:
        variables.add_score(30)
        if variables.sound_on:
            explosion_sound.play()
    asteroids.pop(asteroids.index(asteroid))
    bullets.pop(bullets.index(bullet))


def check_collisions():
    for asteroid in asteroids:
        asteroid.x += asteroid.x_velocity
        asteroid.y += asteroid.y_velocity

        # Check player collision
        player_left = player.x - player.width // 2
        player_right = player.x + player.width // 2
        player_top = player.y - player.height // 2
        player_bottom = player.y + player.height // 2

        if ((asteroid.x >= player_left and
             asteroid.x <= player_right) or
            (asteroid.x + asteroid.width <= player_right and
             asteroid.x + asteroid.width >= player_left)):
            if ((asteroid.y >= player_top and
                 asteroid.y <= player_bottom) or
                (asteroid.y + asteroid.height >= player_top and
                 asteroid.y + asteroid.height <= player_bottom)):
                variables.lose_life()
                asteroids.pop(asteroids.index(asteroid))
                break

        # Check bullet collision
        for bullet in bullets:
            if ((bullet.x >= asteroid.x and
                 bullet.x <= asteroid.x + asteroid.width) or
                (bullet.x + bullet.width >= asteroid.x and
                 bullet.x + bullet.width <= asteroid.x + asteroid.width)):
                if ((bullet.y >= asteroid.y and
                     bullet.y <= asteroid.y + asteroid.height) or
                    (bullet.y + bullet.height >= asteroid.y and
                     bullet.y + bullet.height <= asteroid.y + asteroid.height)):
                    handle_bullet_asteroid_collision(bullet, asteroid)
                    break


def update_game_state():
    player.updateLocation()

    for bullet in bullets:
        bullet.move()
        if bullet.checkOffScreen():
            bullets.pop(bullets.index(bullet))

    check_collisions()


def game_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score on quit
            if variables.score > variables.high_score:
                with open('scores.txt', 'w') as fw:
                    fw.write(str(variables.score))
                variables.high_score = variables.score
            variables.run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not variables.gameover:
                    bullets.append(Bullet(player.head[0], player.head[1], player.cos, player.sin))
                    if variables.sound_on:
                        shoot_sound.play()

            if event.key == pygame.K_m:
                variables.toggle_sound()

            if event.key == pygame.K_TAB:
                if variables.score > variables.high_score:
                        with open('scores.txt', 'w') as fw:
                            fw.write(str(variables.score))
                        variables.high_score = variables.score
                        
                if variables.gameover:
                    variables.reset()
                    asteroids.clear()
                    bullets.clear()


def handle_player_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.turnLeft()
    if keys[pygame.K_RIGHT]:
        player.turnRight()
    if keys[pygame.K_UP]:
        player.moveForward()

if __name__ == '__main__':
    while variables.run:
        clock.tick(60)
        count += 1

        if not variables.gameover:
            if count % 50 == 0:
                rank = random.choice([1, 1, 1, 2, 2, 3])
                new_asteroid = AsteroidFactory.createAsteroid(rank)
                asteroids.append(new_asteroid)

            update_game_state()
            handle_player_input()

        game_events()
        draw_window()

    pygame.quit()
