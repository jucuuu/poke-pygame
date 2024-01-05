import pygame
import math
from sys import exit
from classes import *

def sprite_dist(sprite_1, sprite_2):
    """
    Calculates the distance between the centers of two given sprites.
    """
    #return math.sqrt((sprite_1.x_pos() - sprite_2.x_pos())**2 + (sprite_1.y_pos() - sprite_2.y_pos())**2)
    return math.sqrt((sprite_1.rect.left - sprite_2.rect.left)**2 + (sprite_1.rect.top - sprite_2.rect.top)**2)

def speech(text, sprite, font, screen):
    icon = sprite.get_icon()
    icon = pygame.transform.rotozoom(icon, 0, 1.5)
    icon_rect = icon.get_rect(center = (95, 300))
    
    text_rect = pygame.Surface((700, 120))
    text_rect.set_alpha(240)
    text_rect.fill((0,0,0))
    screen.blit(text_rect, (50, 250))
    pygame.draw.rect(screen, (239, 232, 76), ((60, 260), (80, 100)))
    screen.blit(icon, icon_rect)
    
    words = text.split()
    
    lines = []
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > 575:
                break
        
        line = ' '.join(line_words)
        lines.append(line)
    
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)
        
        tx = 150
        ty = 270 + y_offset
        
        font_surf = font.render(line, False, (255,255,255))
        screen.blit(font_surf, (tx, ty))
        
        y_offset += fh
        
def fight(screen, player, npc):
    # Player starts
    current_turn = True
    chosen = False # True as soon as player makes any move (switch animal/attack)
    if player.animals and chosen == False:
        current_animal = player.animals[0]
    
    # Draw fight screen
    screen.fill((153, 255, 153))
    # Ellipses for the active animal to stand on (both player's and NPC's)
    pygame.draw.ellipse(screen,(36, 157, 30),(430,100,270,50))
    pygame.draw.ellipse(screen,(36, 157, 30),(100,200,270,50))
    
    # Show current animal scaled, the list of their abilities + their damage
    icon = current_animal.get_icon()
    icon = pygame.transform.rotozoom(icon, 0, 3)
    icon = pygame.transform.flip(icon, True, False)
    icon_rect = icon.get_rect(center = (240, 180))
    screen.blit(icon, icon_rect)
    
    # Show small icons of other animals
    
    # Show small icons of NPC's animals
