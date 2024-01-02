import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
        self.image = pygame.image.load('graphics/player1.png')
        self.rect = self.image.get_rect(midbottom = (200, 300))
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_d]:
            self.rect.x += 5
    
    def update(self):
        self.player_input()

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
    
    def dialogue(self):
        pass

class Static(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()

class Animal(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()