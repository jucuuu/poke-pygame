import pygame
from sys import exit
from classes import *
from mechanics import *

pygame.init() 
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Tiny Adventures')
clock = pygame.time.Clock()

# Fonts
dialogue_font = pygame.font.Font('font/kongtext.ttf', 20)

# Backgrounds
bg_forest = pygame.image.load('graphics/background1.png').convert_alpha()
bg_shop_outside = pygame.image.load('graphics/background1.png').convert_alpha()
bg_shop_inside = pygame.image.load('graphics/background1.png').convert_alpha()
bgs = [bg_forest, bg_shop_outside, bg_shop_outside]
bg_index = 0
current_bg = bgs[bg_index]

# Object surfaces
bush_1 = pygame.image.load('graphics/bush/bush_1.png').convert_alpha()
bush_1 = pygame.transform.rotozoom(bush_1, 0, 1.5)
bush_2 = pygame.image.load('graphics/bush/bush_2.png').convert_alpha()
bush_2 = pygame.transform.rotozoom(bush_2, 0, 1.5)
bush_frames = [bush_1, bush_2]

# Animals
dog = pygame.image.load('graphics/animals/doggo_1.png').convert_alpha()
dog_frames = [dog]

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player(400, 200))

bush = pygame.sprite.GroupSingle()
bush.add(Static(bush_frames, 250, 175))

dog = pygame.sprite.GroupSingle()
dog.add(Animal(dog_frames, 250, 170))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(bgs[bg_index],(0,0))
    if bg_index == 0:
        player.draw(screen)
        player.update()
        
        dog.draw(screen)
        dog.update()
        
        bush.draw(screen)
        bush.update()
        
        speech('Terrible misfortunes are upon us...', dog.sprite, dialogue_font, screen)
        
        if player.sprite.x_pos() >= 850:
            bg_index = 1
            player.sprite.set_x_y(100, 200)
    if bg_index == 1:
        player.draw(screen)
        player.update()
        
        if player.sprite.x_pos() <= -50:
            bg_index = 0
            player.sprite.set_x_y(750, 200)
    #if bg_index == 2:
    
    pygame.display.update()
    clock.tick(60) # Max framerate
