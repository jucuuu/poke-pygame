import pygame
from sys import exit
from classes import *

pygame.init() 
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Tiny Adventures')
clock = pygame.time.Clock()

# Backgrounds
bg_forest = pygame.image.load('graphics/background1.png').convert_alpha()

# Object surfaces
bush_1 = pygame.image.load('graphics/bush/bush_1.png').convert_alpha()
bush_1 = pygame.transform.rotozoom(bush_1, 0, 1.5)
bush_2 = pygame.image.load('graphics/bush/bush_2.png').convert_alpha()
bush_2 = pygame.transform.rotozoom(bush_2, 0, 1.5)
bush_frames = [bush_1, bush_2]

# Animals
dog = pygame.image.load('graphics/animals/dogg_1.png').convert_alpha()
dog_frames = [dog]

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

bush = pygame.sprite.GroupSingle()
bush.add(Static(bush_frames, 250, 175))

dog = pygame.sprite.GroupSingle()
dog.add(Animal(dog_frames, 250, 170))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(bg_forest,(0,0))
    
    player.draw(screen)
    player.update()
    
    bush.draw(screen)
    bush.update()
    
    dog.draw(screen)
    dog.update()
        
    pygame.display.update()
    clock.tick(60) # Max framerate
