import pygame
import math
from classes import *

def sprite_dist(sprite_1, sprite_2):
    """
    Calculates the distance between two given sprites.
    """
    return math.sqrt((sprite_1.rect.left - sprite_2.rect.left)**2 + (sprite_1.rect.top - sprite_2.rect.top)**2)

def text_wrap(text, font, width): # Line width
    """
    Breaks text into lines within the provided width.
    """
    words = text.split()
    
    lines = []
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > width:
                break
        
        line = ' '.join(line_words)
        lines.append(line)
    return lines

def render_wrapped_text(screen, lines, font, x, y, color, line_y = 0, y_offset = 0): # (x,y) - position of text
    """
    Render lines of text.
    """
    for line in lines:
        fw, fh = font.size(line)
        fh += line_y
        
        tx = x
        ty = y + y_offset
        
        font_surf = font.render(line, False, color)
        screen.blit(font_surf, (tx, ty))
        
        y_offset += fh
    return y_offset

def speech(text, sprite, font, screen):
    """
    Dialogue mechanic.
    """
    icon = sprite.icon
    icon = pygame.transform.rotozoom(icon, 0, 1.5)
    icon_rect = icon.get_rect(center = (95, 300))
    
    text_rect = pygame.Surface((700, 120))
    text_rect.set_alpha(240)
    text_rect.fill((0,0,0))
    screen.blit(text_rect, (50, 250))
    pygame.draw.rect(screen, (239, 232, 76), ((60, 260), (80, 100)))
    screen.blit(icon, icon_rect)
    
    lines = text_wrap(text, font, 575)
    render_wrapped_text(screen, lines, font, 150, 270, 'White')
        
def confirmation(option1, option2, font, screen):
    """
    Render player input options.
    """
    text_rect = pygame.Surface((700, 120))
    text_rect.set_alpha(240)
    text_rect.fill((0,0,0))
    screen.blit(text_rect, (50, 250))
    pygame.draw.rect(screen, (239, 232, 76), ((60, 260), (80, 100)))
    lines = [option1, option2]
    render_wrapped_text(screen, lines, font, 150, 270, (255,255,255))

def hint(text, sprite, font, screen):
    """
    Render informational text on the screen.
    """
    wrapped_text = text_wrap(text, font, 4*sprite.rect.width)
    render_wrapped_text(screen, wrapped_text, font, sprite.rect.left-30, sprite.rect.top-30, (255,255,255))

def sprite_movement(sprite, target_x, frames_to_complete_movement, dist, speed):
    """
    Running animation.
    """
    if dist < 100:
        movement_distance = (target_x - sprite.rect.x) / frames_to_complete_movement
        sprite.rect.x += speed * movement_distance
        frames_to_complete_movement -= 1
