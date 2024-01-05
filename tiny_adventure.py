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
bg_shop_outside = pygame.image.load('graphics/background2.png').convert_alpha()
bg_shop_inside = pygame.image.load('graphics/background3.png').convert_alpha()
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

trash_front = pygame.image.load('graphics/trashcan/trash_front.png').convert_alpha()
trash_back = pygame.image.load('graphics/trashcan/trash_back.png').convert_alpha()
trash_front_frames = [trash_front]
trash_back_frames = [trash_back]

table = pygame.image.load('graphics/table.png').convert_alpha()
table_frames = [table]

# Animals
dog = pygame.image.load('graphics/animals/doggo_1.png').convert_alpha()
dog_frames = [dog]
dog_moved = False
frames_to_complete_movement = 3 * 60  # 3 seconds at 60 FPS

cat_1 = pygame.image.load('graphics/animals/cat_1.png').convert_alpha()
cat_trashcan= pygame.image.load('graphics/trashcan/cat_trashcan.png').convert_alpha()
cat_frames = [cat_1]
cat_trashcan_frames = [cat_trashcan]

birb_1 = pygame.image.load('graphics/animals/birb_1.png').convert_alpha()
birb_frames = [birb_1]
# NPC
shopkeep = pygame.image.load('graphics/npcs/shopkeeper_1.png').convert_alpha()
shopkeep_frames = [shopkeep]

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

tree_group_right = pygame.sprite.Group()
for i in range(5):
    tree_instance = Static(tree_frames, 800, 50 + i * 70)
    tree_group_right.add(tree_instance)

trash_front = pygame.sprite.GroupSingle()
trash_front.add(Static(trash_front_frames, 680, 180))

trash_back = pygame.sprite.GroupSingle()
trash_back.add(Static(trash_back_frames, 680, 180))

table = pygame.sprite.GroupSingle()
table.add(Static(table_frames, 400, 100))

dog = pygame.sprite.GroupSingle()
dog.add(Animal(dog_frames, 250, 180))

cat_trashcan = pygame.sprite.GroupSingle()
cat_trashcan.add(Animal(cat_trashcan_frames, 680, 180))

cat = pygame.sprite.GroupSingle()
cat.add(Animal(cat_frames, 680, 180))

birb = pygame.sprite.GroupSingle()
birb.add(Animal(birb_frames,460,180))

shop_entrance = pygame.Rect(600,200,100,100)

shopkeeper = pygame.sprite.GroupSingle()
shopkeeper.add(NPC(shopkeep_frames, 400, 50))

fighting = False

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
            elif event.key == pygame.K_e and bg_index == 2:
                # Switch to shop outside area if press E next to shop left wall
                if player.sprite.rect.x <= 10:
                    bg_index = 1
                    player.sprite.set_x_y(400,220)
                if sprite_dist(shopkeeper.sprite, player.sprite) <= 20:
                    fighting = True
    
    screen.blit(bgs[bg_index],(0,0))
    if fighting == True:
        fight(screen, player.sprite, shopkeeper.sprite)
    elif bg_index == 0:
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
        
        dist = sprite_dist(player.sprite, dog.sprite)
        if dist < 100:
            speech('Terrible misfortunes are upon us...', dog.sprite, dialogue_font, screen)

        if not dog_moved:
            if dist < 50:
                movement_distance = 300 / frames_to_complete_movement
                dog.sprite.rect.x -= movement_distance
                frames_to_complete_movement -= 1
                if dog.sprite.rect.left <= 170:
                    dog_moved = True
                    dog.sprite.flipped()
                    bush.sprite.no_animation()
                if dog.sprite not in player.sprite.animals: player.sprite.add_animals(dog.sprite)
        
        for tree in tree_group_left:
            if player.sprite.rect.colliderect(tree.rect):
                player_x_limit = tree.rect.right -20
                if player.sprite.rect.left < player_x_limit:
                    player.sprite.set_x_y(player_x_limit, player.sprite.rect.top)

        for tree in tree_group_upper:
            if player.sprite.rect.colliderect(tree.rect):
                player_y_limit = tree.rect.bottom
                if player.sprite.rect.top < tree.rect.bottom:
                    player.sprite.set_x_y(player.sprite.rect.left, player_y_limit)

        if player.sprite.rect.top > 350:
            player.sprite.set_x_y(player.sprite.rect.left, 350)
        
        if player.sprite.rect.left >= 850:
            bg_index = 1
            player.sprite.set_x_y(100, 200)

    elif bg_index == 1:
        tree_group_right.draw(screen)
        tree_group_right.update()

        tree_group_upper.draw(screen)
        tree_group_upper.update()

        player.draw(screen)
        player.update()

        tree_group_lower.draw(screen)
        tree_group_lower.update()
        
        trash_back.draw(screen)
        trash_back.update()
        
        cat_trashcan.draw(screen)
        cat_trashcan.update()

        trash_front.draw(screen)
        trash_front.update()
        #screen.blit(shop_entr, (600,200))
        pygame.draw.rect(screen, 'red', shop_entrance)
        
        for tree in tree_group_upper:
            if player.sprite.rect.colliderect(tree.rect):
                player_y_limit = tree.rect.bottom
                if player.sprite.rect.top < tree.rect.bottom:
                    player.sprite.set_x_y(player.sprite.rect.left, player_y_limit)

        for tree in tree_group_right:
            if player.sprite.rect.colliderect(tree.rect):
                player_x_limit = tree.rect.left -45
                if player.sprite.rect.left > player_x_limit:
                    player.sprite.set_x_y(player_x_limit, player.sprite.rect.top)

        if player.sprite.rect.top > 350:
            player.sprite.set_x_y(player.sprite.rect.left, 350)

        if player.sprite.rect.left <= -50:
            bg_index = 0
            player.sprite.set_x_y(750, 200)
        
        if shop_entrance.colliderect(player.sprite.rect):
            speech('A shop with a trash cat outside! This must be a bad omen...', dog.sprite, dialogue_font, screen)
    elif bg_index == 2:
        screen.fill((0,0,255))

        shopkeeper.draw(screen)
        shopkeeper.update()

        birb.draw(screen)
        birb.update()

        table.draw(screen)
        table.update()
        
        player.draw(screen)
        player.update()
        
        speech('velkam bruh', shopkeeper.sprite, dialogue_font, screen)
        
        if player.sprite.rect.y >= 450:
            player.sprite.set_x_y(100, 200)
        #if player.sprite.x_pos() <= -50:
        #    bg_index = 1
        #    player.sprite.set_x_y(400, 200)
        if sprite_dist(shopkeeper.sprite, player.sprite) <= 20 and fighting == False:
            speech("Let's mess him up!", dog.sprite, dialogue_font, screen)
        
    pygame.display.update()
    clock.tick(60) # Max framerate
