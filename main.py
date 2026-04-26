import pygame
import random
from assets import AssetManager
from asteroids import AsteroidFactory
from bullet import Bullet
from player import Player
from collision import Collision
from game_state import GameState

pygame.display.set_caption('Asteroid Shooter')

class Game:

    def __init__(self):
        self._assets = AssetManager()
        self._game_state = GameState()
        self._asteroids = []
        self._player = Player()
        self._collision = Collision()
        self._asteroid_factory = AsteroidFactory()
        self._window = pygame.display.set_mode((self._assets._screen_width, self._assets._screen_height))
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

    def load_high_score(self):
        try:
            with open('scores.csv', 'r') as score_file:
                self._game_state._high_score = int(score_file.readline().strip())
        except (FileNotFoundError, ValueError):
            print('Error loading scores file')
            self._game_state._high_score = 0

    def save_high_score(self, score):
        try:
            with open('scores.csv', 'w') as score_file:
                score_file.write(str(score))
                self._game_state._high_score = score
        except (FileNotFoundError, ValueError):
            print(f'Error saving high score: {score}')

    def update_gui(self):
        self._lives_txt = self._font.render(f'Lives: {self._game_state.lives}', 1, (255, 255, 255))
        self._restart_txt = self._font.render('Press Tab to Play Again', 1, (255, 255, 255))
        self._score_txt = self._font.render(f'Score: {self._game_state.score}', 1, (255, 255, 255))
        self._high_score_txt = self._font.render(f'High Score: {self._game_state.high_score}', 1, (255, 255, 255))
        self._restart_position = (self._assets._screen_width // 2 - self._restart_txt.get_width() // 2,
                                  self._assets._screen_height // 2 - self._restart_txt.get_height() // 2)
        self._high_score_position = (self._assets._screen_width - self._high_score_txt.get_width() - 25,
                                     35 + self._score_txt.get_height())
        self._score_position = (self._assets._screen_width - self._score_txt.get_width() - 25, 25)

    def draw_window(self):
        self._window.blit(self._assets.bg_img, (0, 0))
        self._player.draw(self._window)
        
        for asteroid in self._asteroids:
            asteroid.draw(self._window)

        for bullet in self._player.bullets:
            bullet.draw(self._window)

        if self._game_state.gameover:
            self._window.blit(self._restart_txt, self._restart_position)

        self._window.blit(self._score_txt, self._score_position)
        self._window.blit(self._high_score_txt, self._high_score_position)
        self._window.blit(self._lives_txt, (25, 25))
        
        pygame.display.update()

    def update_game_state(self):
        self._player.update_location(self._assets._screen_width, self._assets._screen_height)

        for bullet in self._player.bullets:
            bullet.move()
            if bullet.check_off_screen():
                self._player.bullets.pop(self._player.bullets.index(bullet))
        
        for asteroid in self._asteroids:
            asteroid.move()
            if self._collision._check_player_collision(asteroid, self._player):
                self._game_state.lose_life()
                self._asteroids.pop(self._asteroids.index(asteroid))
                break
            if self._collision._check_bullet_collision(asteroid, self._asteroids, self._player, self._game_state):
                self._collision._handle_bullet_asteroid_collision(self._player, bullet, asteroid, self._asteroids, self._game_state)
                break

    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self._game_state.score > self._game_state.high_score:
                    self.save_high_score(self._game_state.score)
                self._game_state.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self._game_state.gameover:
                    self._player.fire(Bullet(self._player._head[0], self._player._head[1], self._player._cos, self._player._sin))
                    if self._game_state.sound_on:
                        self._assets.shoot_sound.play()

                if event.key == pygame.K_m:
                    self._game_state.toggle_sound()

                if event.key == pygame.K_TAB:
                    if self._game_state.gameover:
                        if self._game_state.score > self._game_state.high_score:
                            self.save_high_score(self._game_state.score)
                        self._player._x = self._assets._screen_width // 2
                        self._player._y = self._assets._screen_height // 2
                        self._player._angle = 0
                        self._player.update_rotation(0)
                        self._game_state.restart()
                        self._asteroids.clear()
                        self._player.bullets.clear()

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._player.turn_left()
        if keys[pygame.K_RIGHT]:
            self._player.turn_right()
        if keys[pygame.K_UP]:
            self._player.move_forward()

    def spawn_asteroid(self):
        rank = random.choice([1, 1, 1, 2, 2, 3])
        new_asteroid = self._asteroid_factory.create_asteroid(rank)
        self._asteroids.append(new_asteroid)

    def run(self):
        while self._game_state.run:
            self._clock.tick(60)
            self._game_state.count += 1

            if not self._game_state.gameover:
                if self._game_state.count % 50 == 0:
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
