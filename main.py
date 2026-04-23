import pygame
import random
from assets import WIDTH, HEIGHT, bg_img, shoot_sound, explosion_sound
from asteroids import AsteroidFactory
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
        self._high_score = 0
        self._count = 0

    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self, value):
        self._count = value
        
    @property
    def high_score(self):
        return self._high_score
    
    @high_score.setter
    def high_score(self, value):
        self._high_score = value

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

    def reset(self):
        self.run = True
        self.gameover = False
        self.lives = 3
        self.score = 0
        self.sound_on = True
        self.count = 0

game_state = GameState()
asteroids = []
player = Player()

try:
    with open('scores.txt', 'r') as fr:
        game_state.high_score = int(fr.read())
except (FileNotFoundError, ValueError):
    print('Error loading scores file')
    game_state.high_score = 0


def draw_window():
    font = pygame.font.SysFont('arial', 30)
    lives_txt = font.render('Lives: ' + str(game_state.lives), 1, (255, 255, 255))
    restart_txt = font.render('Press Tab to Play Again', 1, (255,255,255))
    score_txt = font.render('Score: ' + str(game_state.score), 1, (255,255,255))
    high_score_txt = font.render('High Score: ' + str(game_state.high_score), 1, (255, 255, 255))

    restart_position = (WIDTH // 2 - restart_txt.get_width() // 2,
                        HEIGHT // 2 - restart_txt.get_height() // 2)
    high_score_position = (WIDTH - high_score_txt.get_width() - 25,
                           35 + score_txt.get_height())
    score_position = (WIDTH - score_txt.get_width() - 25, 25)

    window.blit(bg_img, (0, 0))
    player.draw(window)
    
    for asteroid in asteroids:
        asteroid.draw(window)

    for bullet in player.bullets:
        bullet.draw(window)

    if game_state.gameover:
        window.blit(restart_txt, restart_position)

    window.blit(score_txt, score_position)
    window.blit(high_score_txt, high_score_position)
    window.blit(lives_txt, (25, 25))
    
    pygame.display.update()


def handle_bullet_asteroid_collision(bullet, asteroid):
    if asteroid.rank == 3:
        if game_state.sound_on:
            explosion_sound.play()
        game_state.add_score(10)
        na1 = AsteroidFactory.create_asteroid(2)
        na2 = AsteroidFactory.create_asteroid(2)
        na1.x, na1.y = asteroid.x, asteroid.y
        na2.x, na2.y = asteroid.x, asteroid.y
        asteroids.extend([na1, na2])
    elif asteroid.rank == 2:
        if game_state.sound_on:
            explosion_sound.play()
        game_state.add_score(20)
        na1 = AsteroidFactory.create_asteroid(1)
        na2 = AsteroidFactory.create_asteroid(1)
        na1.x, na1.y = asteroid.x, asteroid.y
        na2.x, na2.y = asteroid.x, asteroid.y
        asteroids.extend([na1, na2])
    else:
        game_state.add_score(30)
        if game_state.sound_on:
            explosion_sound.play()

    asteroids.pop(asteroids.index(asteroid))
    player.bullets.pop(player.bullets.index(bullet))


def check_collisions():
    for asteroid in asteroids: #list(asteroids): Use a copy to modify list during iteration
        asteroid.x += asteroid.x_velocity
        asteroid.y += asteroid.y_velocity

        # Check player collision
        player_left = player.x - player.width // 2
        player_right = player.x + player.width // 2
        player_top = player.y - player.height // 2
        player_bottom = player.y + player.height // 2

        if ((asteroid.x >= player_left and
             asteroid.x <= player_right) or
            ((asteroid.x + asteroid.width) <= player_right and
             (asteroid.x + asteroid.width) >= player_left)):
            if ((asteroid.y >= player_top and
                 asteroid.y <= player_bottom) or
                (asteroid.y + asteroid.height >= player_top and
                 asteroid.y + asteroid.height <= player_bottom)):
                game_state.lose_life()
                asteroids.pop(asteroids.index(asteroid))
                break

        # Check bullet collision
        for bullet in player.bullets:
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
    player.update_location()

    for bullet in player.bullets:
        bullet.move()
        if bullet.check_off_screen():
            player.bullets.pop(player.bullets.index(bullet))

    check_collisions()


def game_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game_state.score > game_state.high_score:
                with open('scores.txt', 'w') as fw:
                    fw.write(str(game_state.score))
                game_state.high_score = game_state.score
            game_state.run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_state.gameover:
                player.fire()
                if game_state.sound_on:
                    shoot_sound.play()

            if event.key == pygame.K_m:
                game_state.toggle_sound()

            if event.key == pygame.K_TAB:
                if game_state.score > game_state.high_score:
                        with open('scores.txt', 'w') as fw:
                            fw.write(str(game_state.score))
                        game_state.high_score = game_state.score
                        
                if game_state.gameover:
                    game_state.reset()
                    asteroids.clear()
                    player.bullets.clear()


def handle_player_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.turn_left()
    if keys[pygame.K_RIGHT]:
        player.turn_right()
    if keys[pygame.K_UP]:
        player.move_forward()

if __name__ == '__main__':
    while game_state.run:
        clock.tick(60)
        game_state.count += 1

        if not game_state.gameover:
            if game_state.count % 50 == 0:
                rank = random.choice([1, 1, 1, 2, 2, 3])
                new_asteroid = AsteroidFactory.create_asteroid(rank)
                asteroids.append(new_asteroid)

            update_game_state()
            handle_player_input()

        game_events()
        draw_window()

    pygame.quit()
