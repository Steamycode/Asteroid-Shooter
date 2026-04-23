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
