import pygame
import random
from scripts.assets import AssetManager
from scripts.asteroids import AsteroidFactory
from scripts.bullet import Bullet
from scripts.player import Player
from scripts.collision import Collision
from scripts.game_state import GameState

pygame.display.set_caption('Asteroid Shooter')

class Game:

    def __init__(self):
        self._assets = AssetManager()
        self._game_state = GameState()
        self._asteroids = []
        self._player = Player()
        self._collision = Collision()
        self._asteroid_factory = AsteroidFactory()
        self._window = pygame.display.set_mode((self.assets.screen_width, self.assets.screen_height))
        self._clock = pygame.time.Clock()
        self.load_high_score()
        self._font = pygame.font.SysFont('calibri', 30)
        self.update_gui()

    @property
    def asteroids(self):
        return self._asteroids
    
    @property
    def player(self):
        return self._player
    
    @property
    def game_state(self):
        return self._game_state
    
    @property
    def collision(self):
        return self._collision
    
    @property
    def assets(self):
        return self._assets
    
    @property
    def window(self):
        return self._window

    @property
    def clock(self):
        return self._clock
    
    @property
    def asteroid_factory(self):
        return self._asteroid_factory
    
    @property
    def lives_txt(self):
        return self._lives_txt

    @property
    def restart_txt(self):
        return self._restart_txt

    @property
    def score_txt(self):
        return self._score_txt

    @property
    def high_score_txt(self):
        return self._high_score_txt
    
    @property
    def font(self):
        return self._font
    
    @property
    def restart_position(self):
        return self._restart_position
    
    @property
    def high_score_position(self):
        return self._high_score_position
    
    @property
    def score_position(self):
        return self._score_position

    def load_high_score(self):
        try:
            with open('scores.csv', 'r') as score_file:
                self.game_state.high_score = int(score_file.readline().strip())
        except (FileNotFoundError, ValueError):
            print('Error loading scores file')
            self.game_state.high_score = 0

    def save_high_score(self, score):
        try:
            with open('scores.csv', 'w') as score_file:
                score_file.write(str(score))
                self.game_state.high_score = score
        except (FileNotFoundError, ValueError):
            print(f'Error saving high score: {score}')

    def update_gui(self):
        self._lives_txt = self.font.render(f'Lives: {self.game_state.lives}', 1, (255, 255, 255))
        self._restart_txt = self.font.render('Press Tab to Play Again', 1, (255, 255, 255))
        self._start_txt = self.font.render('Press Space to Start', 1, (255, 255, 255))
        self._mute_txt = self.font.render('Mute', 1, (255, 255, 255))
        self._score_txt = self.font.render(f'Score: {self.game_state.score}', 1, (255, 255, 255))
        self._high_score_txt = self.font.render(f'High Score: {self.game_state.high_score}', 1, (255, 255, 255))
        self._restart_position = (self.assets.screen_width // 2 - self.restart_txt.get_width() // 2,
                                  self.assets.screen_height // 2 - self.restart_txt.get_height() // 2)
        self._high_score_position = (self.assets.screen_width - self.high_score_txt.get_width() - 25,
                                     35 + self.score_txt.get_height())
        self._score_position = (self.assets.screen_width - self.score_txt.get_width() - 25, 25)

    def draw_window(self):
        self.window.blit(self.assets.bg_img, (0, 0))
        self.player.draw(self.window)
        
        for asteroid in self.asteroids:
            asteroid.draw(self.window)

        for bullet in self.player.bullets:
            bullet.draw(self.window)

        if self.game_state.gameover:
            self.window.blit(self.restart_txt, self.restart_position)

        if self.game_state.first_launch:
            self.window.blit(self._start_txt, self.restart_position)

        if not self.game_state.sound_on:
           self.window.blit(self._mute_txt, (25, 50))

        self.window.blit(self.score_txt, self.score_position)
        self.window.blit(self.high_score_txt, self.high_score_position)
        self.window.blit(self.lives_txt, (25, 25))
        
        
        pygame.display.update()

    def update_game_state(self):
        self.player.check_off_screen(self.assets.screen_width, self.assets.screen_height)

        for bullet in self.player.bullets:
            bullet.move()
            if bullet.check_off_screen(self.assets.screen_width, self.assets.screen_height):
                self.player.bullets.pop(self.player.bullets.index(bullet))
                continue
        
        for asteroid in self.asteroids:
            asteroid.move()
            colliding_bullet = self.collision.check_bullet_collision(asteroid, self.player)
            if colliding_bullet:
                self.collision.handle_bullet_asteroid_collision(self.player, colliding_bullet, asteroid, self.asteroids, self.game_state)
                continue
            elif self.collision.check_player_collision(asteroid, self.player):
                self.game_state.lose_life()
                self.asteroids.pop(self.asteroids.index(asteroid))
                continue
            elif asteroid.check_off_screen(self.assets.screen_width, self.assets.screen_height):
                self.asteroids.pop(self.asteroids.index(asteroid))
                continue

    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.game_state.score > self.game_state.high_score:
                    self.save_high_score(self.game_state.score)
                self.game_state.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_state.gameover:
                    self.player.fire(Bullet(self.player.head[0], self.player.head[1], self.player.cos, self.player.sin))
                    if self.game_state.sound_on:
                        self.assets.shoot_sound.play()

                if event.key == pygame.K_m:
                    self.game_state.toggle_sound()

                if event.key == pygame.K_TAB:
                    if self.game_state.gameover:
                        if self.game_state.score > self.game_state.high_score:
                            self.save_high_score(self.game_state.score)
                        self.player.x = self.assets.screen_width // 2
                        self.player.y = self.assets.screen_height // 2
                        self.player.angle = 0
                        self.player.update_rotation(0)
                        self.game_state.restart()
                        self.asteroids.clear()
                        self.player.bullets.clear()

                if event.key == pygame.K_SPACE and self.game_state.first_launch:
                    self.game_state.first_launch = False

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.turn_left()
        if keys[pygame.K_RIGHT]:
            self.player.turn_right()
        if keys[pygame.K_UP]:
            self.player.move()

    def spawn_asteroid(self):
        rank = random.choice([1, 1, 1, 2, 2, 3])
        new_asteroid = self.asteroid_factory.create_asteroid(rank)
        self.asteroids.append(new_asteroid)

    def run(self):
        while self.game_state.run:
            self.clock.tick(60)
            self.game_state.count += 1

            if not self.game_state.gameover and not self.game_state.first_launch:
                if self.game_state.count % 50 == 0:
                    self.spawn_asteroid()

                self.update_game_state()
                self.handle_player_input()

            self.update_gui()
            self.game_events()
            self.draw_window()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
