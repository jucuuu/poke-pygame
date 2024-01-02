import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
    
    def player_input(self):
        keys = pygame.key.get_pressed()

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()

class Static(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()

class Animal(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()