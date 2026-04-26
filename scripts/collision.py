from scripts.asteroids import AsteroidFactory
from scripts.assets import AssetManager


class Collision:
    
    def __init__(self):
        self._assets = AssetManager()
        self._asteroid_factory = AsteroidFactory()

    @property
    def assets(self):
        return self._assets

    @property
    def asteroid_factory(self):
        return self._asteroid_factory
    

    def check_player_collision(self, asteroid, player):
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
                return True
        return False

    def check_bullet_collision(self, asteroid, player):
        for bullet in player.bullets:
            if ((bullet.x >= asteroid.x and
                 bullet.x <= asteroid.x + asteroid.width) or
                (bullet.x + bullet.width >= asteroid.x and
                 bullet.x + bullet.width <= asteroid.x + asteroid.width)):
                if ((bullet.y >= asteroid.y and
                     bullet.y <= asteroid.y + asteroid.height) or
                    (bullet.y + bullet.height >= asteroid.y and
                     bullet.y + bullet.height <= asteroid.y + asteroid.height)):
                    return bullet
        return None

    def handle_bullet_asteroid_collision(self, player, bullet, asteroid, asteroids, game_state):
        if asteroid.rank == 3:
            if game_state.sound_on:
                self.assets.explosion_sound.play()
            game_state.add_score(10)
            na1 = self.asteroid_factory.create_asteroid(2)
            na2 = self.asteroid_factory.create_asteroid(2)
            na1.x, na1.y = asteroid.x, asteroid.y
            na2.x, na2.y = asteroid.x, asteroid.y
            asteroids.extend([na1, na2])
        elif asteroid.rank == 2:
            if game_state.sound_on:
                self.assets.explosion_sound.play()
            game_state.add_score(20)
            na1 = self.asteroid_factory.create_asteroid(1)
            na2 = self.asteroid_factory.create_asteroid(1)
            na1.x, na1.y = asteroid.x, asteroid.y
            na2.x, na2.y = asteroid.x, asteroid.y
            asteroids.extend([na1, na2])
        else:
            game_state.add_score(30)
            if game_state.sound_on:
                self.assets.explosion_sound.play()

        asteroids.pop(asteroids.index(asteroid))
        player.bullets.pop(player.bullets.index(bullet))
