import pygame
from sys import exit
from classes import *

pygame.init() 
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Tiny Adventures')
clock = pygame.time.Clock()

# Surfaces
bg_forest = pygame.image.load('graphics/background1.png').convert_alpha()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(bg_forest,(0,0))
    
    player.draw(screen)
    player.update()
        
    pygame.display.update()
    clock.tick(60) # Max framerate
