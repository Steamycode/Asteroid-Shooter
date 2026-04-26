import pygame


class AssetManager:
        
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):

        pygame.init()
        
        self._bg_img = pygame.image.load('assets/sprites/space.png')
        self._ship_img = pygame.image.load('assets/sprites/spaceship.png')
        self._medium_asteroid_img = pygame.image.load('assets/sprites/asteroid.png')
        self._big_asteroid_img = pygame.transform.scale(self._medium_asteroid_img, (150, 150))
        self._small_asteroid_img = pygame.transform.scale(self._medium_asteroid_img, (50, 50))
        
        self._shoot_sound = pygame.mixer.Sound('assets/sounds/laser.mp3')
        self._explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.mp3')
        self._shoot_sound.set_volume(0.25)
        self._explosion_sound.set_volume(0.25)

        self._screen_width = 1280
        self._screen_height = 720

    @property
    def WIDTH(self):
        return self._screen_width

    @property
    def HEIGHT(self):
        return self._screen_height
    
    @property
    def bg_img(self):
        return self._bg_img
    
    @property
    def ship_img(self):
        return self._ship_img
    
    @property
    def big_asteroid_img(self):
        return self._big_asteroid_img
    
    @property
    def medium_asteroid_img(self):
        return self._medium_asteroid_img
    
    @property
    def small_asteroid_img(self):
        return self._small_asteroid_img
    
    @property
    def shoot_sound(self):
        return self._shoot_sound
    
    @property
    def explosion_sound(self):
        return self._explosion_sound
