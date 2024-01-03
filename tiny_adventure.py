import pygame
import math
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

# NPC
shopkeep = pygame.image.load('graphics/npcs/shopkeeper_1.png').convert_alpha()
shopkeep_frames = [shopkeep]

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player(400, 200))

bush = pygame.sprite.GroupSingle()
bush.add(Static(bush_frames, 250, 175))

dog = pygame.sprite.GroupSingle()
dog.add(Animal(dog_frames, 250, 170))

shop_entrance = pygame.Rect(600,200,100,100)

shopkeeper = pygame.sprite.GroupSingle()
shopkeeper.add(NPC(shopkeep_frames, 400, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e and bg_index == 1:
                # Switch to shop area if press E next to shop
                if shop_entrance.colliderect(player.sprite.rect):
                    bg_index = 2
    
    screen.blit(bgs[bg_index],(0,0))
    if bg_index == 0:
        player.draw(screen)
        player.update()
        
        dog.draw(screen)
        dog.update()
        
        bush.draw(screen)
        bush.update()
        
        dist = sprite_dist(player.sprite, dog.sprite)
        if dist < 100:
            speech('Terrible misfortunes are upon us...', dog.sprite, dialogue_font, screen)
        
        if player.sprite.x_pos() >= 850:
            bg_index = 1
            player.sprite.set_x_y(100, 200)
    if bg_index == 1:
        player.draw(screen)
        player.update()
        
        #screen.blit(shop_entr, (600,200))
        pygame.draw.rect(screen, 'red', shop_entrance)
        
        if player.sprite.x_pos() <= -50:
            bg_index = 0
            player.sprite.set_x_y(750, 200)
        
        if shop_entrance.colliderect(player.sprite.rect):
            speech('A shop with a trash cat outside! This must be a bad omen...', dog.sprite, dialogue_font, screen)
    if bg_index == 2:
        screen.fill((0,0,255))
        player.draw(screen)
        player.update()
        
        shopkeeper.draw(screen)
        shopkeeper.update()
        
        speech('velkam bruh', shopkeeper.sprite, dialogue_font, screen)
        
        if player.sprite.rect.x <= -50 or player.sprite.rect.x >= 450:
            player.sprite.set_x_y(100, 200)
    
    pygame.display.update()
    clock.tick(60) # Max framerate
