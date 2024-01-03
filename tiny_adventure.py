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

tree_1 = pygame.image.load('graphics/tree.png').convert_alpha()
tree_frames = [tree_1]

# Animals
dog = pygame.image.load('graphics/animals/doggo_1.png').convert_alpha()
dog_frames = [dog]
dog_moved = False
dog_moving = False
frames_to_complete_movement = 3 * 60  # 3 seconds at 60 FPS

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player(400, 200))

bush = pygame.sprite.GroupSingle()
bush.add(Static(bush_frames, 250, 175))

tree_group_upper = pygame.sprite.Group()
for i in range(17):
    tree_instance = Static(tree_frames, 0 + i * 50, 50)
    tree_group_upper.add(tree_instance)

tree_group_lower = pygame.sprite.Group()
for i in range(17):
    tree_instance = Static(tree_frames, 0 + i * 50, 346)
    tree_group_lower.add(tree_instance)

tree_group_left = pygame.sprite.Group()
for i in range(5):
    tree_instance = Static(tree_frames, 0, 50 + i * 70)
    tree_group_left.add(tree_instance)

dog = pygame.sprite.GroupSingle()
dog.add(Animal(dog_frames, 250, 180))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(bgs[bg_index],(0,0))
    if bg_index == 0:
        player.draw(screen)
        player.update()
        
        tree_group_upper.draw(screen)
        tree_group_upper.update()

        tree_group_left.draw(screen)
        tree_group_left.update()

        tree_group_lower.draw(screen)
        tree_group_lower.update()

        dog.draw(screen)
        dog.update()
        
        bush.draw(screen)
        bush.update()
        
        dist = math.sqrt((player.sprite.x_pos() - dog.sprite.x_pos())**2 + (player.sprite.y_pos() - dog.sprite.y_pos())**2)
        if dist < 100:
            speech('Terrible misfortunes are upon us...', dog.sprite, dialogue_font, screen)

        if not dog_moved:
            dist = math.sqrt((player.sprite.x_pos() - dog.sprite.x_pos())**2 + (player.sprite.y_pos() - dog.sprite.y_pos())**2)
            if dist < 50:
                dog_moving = True
                movement_distance = 300 / frames_to_complete_movement
                dog.sprite.rect.x -= movement_distance
                frames_to_complete_movement -= 1
                if dog.sprite.x_pos() <= 170:
                    dog_moved = True
                    dog.sprite.flipped()
                    bush.sprite.no_animation()
        
        for tree in tree_group_left:
            if player.sprite.rect.colliderect(tree.rect):
                player_x_limit = tree.rect.right -20
                if player.sprite.x_pos() < player_x_limit:
                    player.sprite.set_x_y(player_x_limit, player.sprite.y_pos())

        for tree in tree_group_upper:
            if player.sprite.rect.colliderect(tree.rect):
                player_y_limit = tree.rect.bottom
                if player.sprite.y_pos() < tree.rect.bottom:
                    player.sprite.set_x_y(player.sprite.x_pos(), player_y_limit)

        if player.sprite.y_pos() > 350:
            player.sprite.set_x_y(player.sprite.x_pos(), 350)
        
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
