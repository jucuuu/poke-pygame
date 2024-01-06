import pygame
import random
from collections import OrderedDict
from mechanics import *

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
        
        self.name = "Playerette"
        
        self.animals = []
    
    def get_animals(self):
        return self.animals
    
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
    
    def set_x_y(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def add_animals(self, animal):
        self.animals.append(animal)
    
    def update(self):
        self.player_input()

class NPC(pygame.sprite.Sprite):
    def __init__(self, animation_list, x, y, name):
        super().__init__()
        
        self.name = name

        self.animation_frames = animation_list
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
        
        self.icon = self.animation_frames[0]
        
        self.animals = []
    
    def get_animals(self):
        return self.animals
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]
    
    def get_icon(self):
        return self.icon
    
    def update(self):
        self.animation_state()
    
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

    #Ups shitas bus japartaisa jo shito tikai kurmam vajag
    def no_animation(self):
        self.image = self.animation_frames.pop()
        
    def update(self):
        self.animation_state()

class Animal(pygame.sprite.Sprite):
    def __init__(self, animation_list, x, y, name, type = "Lazy"):
        super().__init__()
        
        self.animation_frames = animation_list
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
        
        self.icon = self.animation_frames[0]
        
        self.name = name
        self.type = type
        
        if type == 'Lazy':
            self.max_hp = 175
        else: self.max_hp = 100
        self.alive = True
        self.curr_hp = self.max_hp
    
    def set_abilities(self, abilities): # abilities - dict with ability name as key, ability dmg as value
        self.abilities = OrderedDict(abilities)
        self.abilities["Basic"] = 10
        self.abilities.move_to_end("Basic", last = False)
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]
    
    def get_icon(self):
        return self.icon
    
    def set_x_y(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def flipped(self):
        for anim in self.animation_frames:
            anim = pygame.transform.flip(anim, True, False)
        self.image = self.animation_frames[int(self.animation_index)]
        self.update()

    def update(self):
        self.animation_state()

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, dmg, color):
        super().__init__()
        self.font = pygame.font.Font('font/kongtext.ttf', 14)
        self.image = self.font.render(dmg, False, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        
    def draw(self, screen, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, 'black', (self.x, self.y, 250, 20))
        pygame.draw.rect(screen, 'green', (self.x, self.y, 250 * ratio, 20))

class Fight():
    def __init__(self, player, enemy):
        self.small_font = pygame.font.Font('font/kongtext.ttf', 14)
        self.big_font = pygame.font.Font('font/kongtext.ttf', 20)
        
        self.action = 1
        
        self.player = player
        self.enemy = enemy
        
        self.pl_animals = player.animals
        self.enemy_animals = enemy.animals
        
        self.pl_curr_animal = player.animals[0]
        self.pl_standby = [anim for anim in self.pl_animals if anim.alive and anim != self.pl_curr_animal]
        self.enemy_curr_animal = enemy.animals[0]
        self.enemy_standby = [anim for anim in self.enemy_animals if anim.alive and anim != self.enemy_curr_animal]
        
        self.current_turn = True # Player starts
        self.can_pick = True
        self.ongoing = True
        self.intro_active = True
        self.victory = True
        
        self.ability_rects = []
        self.standby_rects = []
    
    def intro(self, screen, event):
        #self.draw_bg(screen)
        screen.fill((153, 255, 153))
        text_1 = f"Fight between {self.player.name} and the {self.enemy.name}!"
        render_wrapped_text(screen, text_wrap(text_1, self.big_font, 700), self.big_font, 20, 20, 'Black')
        text_2 = "Press SPACE to fight!"
        render_wrapped_text(screen, text_wrap(text_2, self.big_font, 700), self.big_font, 20, 350, 'Black')
        
        pl_icon = pygame.transform.rotozoom(self.player.icon, 0, 3.5)
        screen.blit(pl_icon, (100, 90))
        
        render_wrapped_text(screen, text_wrap("VS", self.big_font, 700), self.big_font, 400, 175, 'Black')
        
        en_icon = pygame.transform.rotozoom(self.enemy.icon, 0, 2.8)
        screen.blit(en_icon, (500, 90))
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.intro_active = False
        
        self.ongoing = False
        for anim in self.pl_animals:
            if anim.alive == True:
                self.ongoing = True
        for anim in self.enemy_animals:
            if anim.alive == True:
                self.ongoing = True
    
    def pick_animal(self, event):
        if event.type == pygame.K_1:
            self.pl_curr_animal = self.pl_standby[0]
        if event.type == pygame.K_2:
            self.pl_curr_animal = self.pl_standby[1]

    def draw_bg(self, screen):
        # Draw fight screen
        screen.fill((153, 255, 153))
        # Ellipses for the active animal to stand on (both player's and NPC's)
        pygame.draw.ellipse(screen,(36, 157, 30),(430,100,270,50))
        pygame.draw.ellipse(screen,(36, 157, 30),(100,200,270,50))
    
    def draw_icons(self, screen):
        # Player icon
        pl_icon = self.player.icon
        pl_icon_rect = pl_icon.get_rect(center = (30, 370))
        screen.blit(pl_icon, pl_icon_rect)
            
        # Shopkeeper icon
        shopk_icon = self.enemy.icon
        shopk_icon_rect = shopk_icon.get_rect(center = (770, 45))
        screen.blit(shopk_icon, shopk_icon_rect)
    
    def switch_if_dead(self):
        # Player
        if not self.pl_curr_animal.alive and len(self.pl_standby) != 0:
            self.pl_curr_animal = self.pl_standby.pop(0)
        # NPC
        if not self.enemy_curr_animal.alive and len(self.enemy_standby) != 0:
            self.enemy_curr_animal = self.enemy_standby.pop(0)
    
    def draw_animals(self, screen):
        self.switch_if_dead()
        # Player: Show current animal scaled on the ellipse, the list of their abilities + their damage
        icon = self.pl_curr_animal.get_icon()
        icon = pygame.transform.rotozoom(icon, 0, 3)
        icon = pygame.transform.flip(icon, True, False)
        icon_rect = icon.get_rect(center = (240, 180))
        screen.blit(icon, icon_rect)
            
        # NPC: Show current animal scaled on the ellipse, the list of their abilities + their damage
        icon_2 = self.enemy_curr_animal.get_icon()
        icon_2 = pygame.transform.rotozoom(icon_2, 0, 3)
        icon_2_rect = icon_2.get_rect(center = (560, 80))
        screen.blit(icon_2, icon_2_rect)
            
        # Show small icons of other animals - if dead, greyed out
        standby_text = self.small_font.render('on standby:', False, 'Black')
        screen.blit(standby_text, (70, 340))
        for i in range(len(self.player.animals)):
            anim = self.player.animals[i]
            if anim in self.pl_standby and anim.alive:
                small_icon = anim.get_icon()
                small_icon_rect = small_icon.get_rect(center = (40+i*40, 380))
                screen.blit(small_icon, small_icon_rect)
            
        # Show small icons of NPC's animals
        for i in range(len(self.enemy.animals)):
            anim = self.enemy.animals[i]
            if anim in self.enemy_standby:
                small_icon = anim.get_icon()
                small_icon_rect = small_icon.get_rect(center = (690+i*40, 100))
                screen.blit(small_icon, small_icon_rect)
    
    def draw_abilities(self, screen):
        self.ability_rects.clear()
        abilities = self.pl_curr_animal.abilities
        i = 0
        for k, v in abilities.items():
            text_rect = pygame.Surface((390, 35))
            text_rect.set_alpha(240)
            text_rect.fill((0,0,0))
            text_rect.fill((63,197,63), text_rect.get_rect().inflate(-2,-2))
            ab_rect = pygame.Rect(10,10+i,390,35)
            self.ability_rects.append(ab_rect)
            screen.blit(text_rect, (5, 5+i))
            render_wrapped_text(screen, text_wrap(str(k), self.big_font, 700), self.big_font, 10, 10+i, 'Black')
            render_wrapped_text(screen, text_wrap(str(v), self.big_font, 700), self.big_font, 350, 10+i, 'Red')
            i += 40
        
        abilities = self.enemy_curr_animal.abilities
        i = 0
        for k, v in abilities.items():
            text_rect = pygame.Surface((438, 35))
            text_rect.set_alpha(240)
            text_rect.fill((0,0,0))
            text_rect.fill((89,122,95), text_rect.get_rect().inflate(-2,-2))
            screen.blit(text_rect, (355, 275+i))
            render_wrapped_text(screen, text_wrap(str(k), self.big_font, 700), self.big_font, 360, 280+i, 'Black')
            render_wrapped_text(screen, text_wrap(str(v), self.big_font, 700), self.big_font, 745, 280+i, 'Red')
            i += 40
    
    # Hit
    def hit(self, group, ability = 0):
        if self.current_turn:
            # Input to pick abilities
            abilities = self.pl_curr_animal.abilities
            ability_dmg = list(abilities.values())
            damage = 0
            damage += ability_dmg[ability]
            
            crit = random.randint(-5,5) 
            self.enemy_curr_animal.curr_hp -= damage + crit
                
            dmg_num = DamageText(self.enemy_curr_animal.rect.centerx, self.enemy_curr_animal.rect.y, str(damage), 'Red')
            group.add(dmg_num)
        
            if self.enemy_curr_animal.curr_hp < 1:
                self.enemy_curr_animal.curr_hp = 0
                self.enemy_curr_animal.alive = False
                if self.enemy_standby:
                    self.switch_if_dead()
                else:
                    self.ongoing = False
                    self.victory = True
            self.current_turn = False
        else:
            # Input to pick abilities
            abilities = self.enemy_curr_animal.abilities
            ability_dmg = list(abilities.values())
            damage = 0
            
            ability = random.randint(0,2)
            damage += ability_dmg[ability]
            
            crit = random.randint(-5,5) 
            self.pl_curr_animal.curr_hp -= damage + crit
                
            dmg_num = DamageText(self.pl_curr_animal.rect.centerx, self.pl_curr_animal.rect.y, str(damage), 'Red')
            group.add(dmg_num)
        
            if self.pl_curr_animal.curr_hp < 1:
                self.pl_curr_animal.curr_hp = 0
                self.pl_curr_animal.alive = False
                if self.pl_standby:
                    self.switch_if_dead()
                else:
                    self.ongoing = False
                    self.victory = False
            self.current_turn = True
    
    def outro(self):
        if self.victory:
            # First, victory screen on top of the battle
            # Playerette with her animals on the screen, "victory" on top, Playerette talks about the power of friendship
            pass
        else:
            # First, defeat screen on top of the battle
            # Shopkeeper with his gang on the screen, "defeat" on top, he says something about not stepping foot into the wrong store
            pass
    
    def eradicate(self):
        self.kill()

class InfoText():
    pass

class InteractableText():
    def __init__(self, x, y):
        self.x = x - 50
        self.y = y - 30
        self.font = pygame.font.Font('font/kongtext.ttf', 14)
    
    def draw(self, screen):
        text = self.font.render('press e to interact', False, (255,255,255))
        screen.blit(text, (self.x, self.y))
    
    def eradicate(self):
        self.kill()

class TitleText():
    pass
