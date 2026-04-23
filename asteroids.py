import random
from assets import small_asteroid_img, medium_asteroid_img, big_asteroid_img, WIDTH, HEIGHT
from game_object import GameObject


class Asteroid(GameObject):
    def __init__(self):
        self.rank = 0
        self.image = None
        self.width = 0
        self.height = 0
        self.set_random_location()
        self.set_velocity()

    def set_random_location(self):
        self.ran_point = random.choice([
            (random.randrange(0, WIDTH - self.width),
             random.choice([-self.height - 5, HEIGHT + 5])),
            (random.choice([-self.width - 5, WIDTH + 5]),
             random.randrange(0, HEIGHT - self.height))])
        self.x, self.y = self.ran_point

    def set_velocity(self):
        if self.x < WIDTH // 2:
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self.y < HEIGHT // 2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.x_velocity = self.x_direction * random.randrange(1, 3)
        self.y_velocity = self.y_direction * random.randrange(1, 3)

    def draw(self, win):
        super().draw(win)
        win.blit(self.image, (self.x, self.y))


class BigAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.rank = 3
        self.image = big_asteroid_img
        self.width = 150
        self.height = 150


class MediumAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.rank = 2
        self.image = medium_asteroid_img
        self.width = 100
        self.height = 100


class SmallAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.rank = 1
        self.image = small_asteroid_img
        self.width = 50
        self.height = 50


class AsteroidFactory():
    @staticmethod
    def create_asteroid(rank):
        if rank == 3:
            return BigAsteroid()
        elif rank == 2:
            return MediumAsteroid()
        elif rank == 1:
            return SmallAsteroid()
