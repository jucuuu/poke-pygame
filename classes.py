import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        player_walk_s = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        player_walk_w = pygame.image.load('graphics/player/player_up.png').convert_alpha()
        player_walk_a = pygame.image.load('graphics/player/player_left.png').convert_alpha()
        player_walk_d = pygame.image.load('graphics/player/player_right.png').convert_alpha()
        self.player_walk = [player_walk_s, player_walk_w, player_walk_a, player_walk_d]
        self.animation_index = 0
        
        self.image = self.player_walk[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
        self.icon = self.player_walk[0]
        
        self.animals = []
    
    def animation_state(self):
        self.image = self.player_walk[int(self.animation_index)]
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 5
            self.animation_index = 1
            self.animation_state()
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.animation_index = 2
            self.animation_state()
        if keys[pygame.K_s]:
            self.rect.y += 5
            self.animation_index = 0
            self.animation_state()
        if keys[pygame.K_d]:
            self.rect.x += 5
            self.animation_index = 3
            self.animation_state()
    
    def x_pos(self):
        return self.rect.x

    def y_pos(self):
        return self.rect.y
    
    def set_x_y(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def add_animals(self, animal):
        self.animals.append(animal)
    
    def update(self):
        self.player_input()

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
    def dialogue(self):
        pass

class Static(pygame.sprite.Sprite):
    def __init__(self, animation_list, x, y):
        super().__init__()
        
        self.animation_frames = animation_list
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()

class Animal(pygame.sprite.Sprite):
    def __init__(self, animation_list, x, y):
        super().__init__()
        
        self.animation_frames = animation_list
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
        
        self.icon = self.animation_frames[0]
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]
    
    def get_icon(self):
        return self.icon

    def x_pos(self):
        return self.rect.x

    def y_pos(self):
        return self.rect.y
    
    def set_x_y(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def flipped(self):
        for anim in self.animation_frames:
            anim = pygame.transform.flip(anim, True, False)
        self.image = self.animation_frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.flipped()