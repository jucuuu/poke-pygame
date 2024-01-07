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
    
    def animation_state(self):
        self.image = self.player_walk[int(self.animation_index)]
    
    def player_input(self):
        """
        Moves the player character according to player input.
        """
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

    def player_interaction(self):
        """
        Returns interaction input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            return 'interact'
        if keys[pygame.K_SPACE]:
            return 'next'
        if keys[pygame.K_y]:
            return 'yes'
        if keys[pygame.K_n]:
            return 'no'
    
    def set_x_y(self, x, y):
        """
        Sets a new position for the player.
        """
        self.rect.x = x
        self.rect.y = y
    
    def add_animals(self, animal):
        """
        Adds an animal to the player's animal list.
        """
        self.animals.append(animal)
    
    def update(self):
        """
        Updates player's animation on the screen.
        """
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
    
    def animation_state(self):
        """
        Changes NPC's animation frame.
        """
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]
    
    def update(self):
        """
        Updates NPC's animation.
        """
        self.animation_state()

class Static(pygame.sprite.Sprite):
    def __init__(self, animation_list, x, y):
        super().__init__()
        
        self.animation_frames = animation_list
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
    
    def animation_state(self):
        """
        Changes the static sprite's animation frame.
        """
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]

    def no_animation(self):
        """
        Turns off a static sprite's animation.
        """
        self.image = self.animation_frames.pop()
        
    def update(self):
        """
        Updates static sprite's animation.
        """
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
        
        if type == 'Lazy': # Different HP according to type.
            self.max_hp = 175
        else: self.max_hp = 100
        self.curr_hp = self.max_hp
        self.alive = True
    
    def set_abilities(self, abilities): # abilities - dict with ability name as key, ability dmg as value
        self.abilities = OrderedDict(abilities)
        self.abilities["Basic"] = 10
        self.abilities.move_to_end("Basic", last = False) # Basic attack - every animal's first ability
    
    def animation_state(self):
        """
        Changes the animal's animation frame.
        """
        self.animation_index += 0.1
        if self.animation_index >= len(self.animation_frames): self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]
    
    def switch_image(self, frame):
        """
        Switches the animal's image to a set frame.
        """
        self.image = self.animation_frames[frame]
    
    def set_x_y(self, x, y):
        """
        Changes animal's position.
        """
        self.rect.x = x
        self.rect.y = y
    
    def flipped(self):
        """
        Flips all animal's animation frames vertically.
        """
        for anim in self.animation_frames:
            anim = pygame.transform.flip(anim, True, False)
        self.image = self.animation_frames[int(self.animation_index)]

    def flip_current_img(self):
        """
        Flips animal's image vertically.
        """
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        """
        Updates animal's animation every frame.
        """
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
        """
        Damage numbers float up and disappear.
        """
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
        """
        A healthbar is drawn at a given position using animal's current and max health stats.
        """
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, 'black', (self.x, self.y, 250, 20))
        pygame.draw.rect(screen, 'green', (self.x, self.y, 250 * ratio, 20))

class Fight():
    def __init__(self, player, enemy, screen):
        self.screen = screen
        self.small_font = pygame.font.Font('font/kongtext.ttf', 14)
        self.big_font = pygame.font.Font('font/kongtext.ttf', 20)
        self.even_bigger_font = pygame.font.Font('font/kongtext.ttf', 30)
        self.action = 1
        self.player = player
        self.enemy = enemy
        
        self.pl_animals = player.animals
        self.enemy_animals = enemy.animals
        if self.pl_animals:
            self.pl_curr_animal = player.animals[0]
            self.pl_standby = [anim for anim in self.pl_animals if (anim.alive and anim != self.pl_curr_animal)]
        self.enemy_curr_animal = enemy.animals[0]
        self.enemy_standby = [anim for anim in self.enemy_animals if (anim.alive and anim != self.enemy_curr_animal)]
        
        self.current_turn = True # Player starts
        self.can_pick = True
        self.ongoing = True
        self.intro_active = True
        self.victory = True
        
        self.ability_rects = []
        self.standby_rects = []
    
    def renew_animals(self):
        """
        Adds player's newly acquired animals to the Fight object.
        """
        if len(self.pl_animals) == 1: self.pl_curr_animal = self.pl_animals[0]
        self.pl_animals = self.player.animals
        self.pl_standby = [anim for anim in self.pl_animals if anim.alive and anim != self.pl_curr_animal]
    
    def intro(self, screen, event):
        """
        Displays a fight intro screen.
        """
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
    
    def pick_animal(self, i):
        """
        Picks the animal at index i in the player's standby animal list.
        """
        anim = self.pl_standby[i]
        self.pl_curr_animal = anim
        self.pl_standby.clear()
        self.pl_standby = [anim for anim in self.pl_animals if anim is not self.pl_curr_animal]

    def draw_bg(self, screen):
        """
        Displays the fight's background on the surface.
        """
        # Draw fight screen
        screen.fill((153, 255, 153))
        # Ellipses for the active animal to stand on (both player's and NPC's)
        pygame.draw.ellipse(screen,(36, 157, 30),(430,100,270,50))
        pygame.draw.ellipse(screen,(36, 157, 30),(100,200,270,50))
    
    def draw_icons(self, screen):
        """
        Displays the player's and enemy's icons in the corners of the fight screen.
        """
        # Player icon
        pl_icon = self.player.icon
        pl_icon_rect = pl_icon.get_rect(center = (30, 370))
        screen.blit(pl_icon, pl_icon_rect)
            
        # Shopkeeper icon
        shopk_icon = self.enemy.icon
        shopk_icon_rect = shopk_icon.get_rect(center = (770, 45))
        screen.blit(shopk_icon, shopk_icon_rect)
    
    def switch_if_dead(self):
        """
        Switches to the first animal in standby if the current animal dies.
        """
        # Player
        if not self.pl_curr_animal.alive and len(self.pl_standby) != 0:
            self.pl_curr_animal = self.pl_standby.pop(0)
        # NPC
        if not self.enemy_curr_animal.alive and len(self.enemy_standby) != 0:
            self.enemy_curr_animal = self.enemy_standby.pop(0)
    
    def draw_animals(self, screen):
        """
        Displays the current animal and standby animals on the screen.
        """
        self.standby_rects.clear()
        self.switch_if_dead()
        # Player: Show current animal scaled on the ellipse
        icon = self.pl_curr_animal.icon
        icon = pygame.transform.rotozoom(icon, 0, 3)
        icon = pygame.transform.flip(icon, True, False)
        icon_rect = icon.get_rect(center = (240, 180))
        screen.blit(icon, icon_rect)
            
        # NPC: Show current animal scaled on the ellipse
        icon_2 = self.enemy_curr_animal.icon
        icon_2 = pygame.transform.rotozoom(icon_2, 0, 3)
        icon_2_rect = icon_2.get_rect(center = (560, 80))
        screen.blit(icon_2, icon_2_rect)
            
        # Show small icons of standby animals
        if self.ongoing:
            standby_text = self.small_font.render('on standby:', False, 'Black')
            screen.blit(standby_text, (70, 340))
        for i in range(len(self.pl_standby)):
            anim = self.pl_standby[i]
            if anim in self.pl_standby and anim.alive:
                small_icon = anim.icon
                small_icon_rect = small_icon.get_rect(center = (80+i*40, 380))
                standby_rect = pygame.Rect(60+i*40,360,40,40)
                self.standby_rects.append(standby_rect)
                screen.blit(small_icon, small_icon_rect)
            
        # Show small icons of NPC's standby animals
        for i in range(len(self.enemy.animals)):
            anim = self.enemy.animals[i]
            if anim in self.enemy_standby:
                small_icon = anim.icon
                small_icon_rect = small_icon.get_rect(center = (690+i*40, 100))
                screen.blit(small_icon, small_icon_rect)
    
    def draw_abilities(self, screen):
        """
        Displays the player's and enemy's current animal abilities and their damage.
        """
        self.ability_rects.clear()
        abilities = self.pl_curr_animal.abilities
        i = 0
        for k, v in abilities.items():
            text_rect = pygame.Surface((390, 35))
            text_rect.set_alpha(240)
            text_rect.fill((0,0,0))
            text_rect.fill((63,197,63), text_rect.get_rect().inflate(-2,-2))
            ab_rect = pygame.Rect(10,10+i,390,35) # Ability rectangle to track clicks on abilities
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
    
    def hit(self, group, ability = 0):
        """
        Uses an ability to damage the target with an applied critical damage, lowering its health and switching animals if the current one's health goes below 1.
        """
        if self.current_turn:
            # Input to pick abilities
            abilities = self.pl_curr_animal.abilities
            ability_dmg = list(abilities.values())
            damage = 0
            damage += ability_dmg[ability]
            
            crit = random.randint(-7,7) 
            self.enemy_curr_animal.curr_hp -= (damage + crit)

            curr_an_rect = pygame.Surface((300,200))
            curr_an_rect.set_alpha(0)
            curr_an_rect.fill((255,255,255))
            self.screen.blit(curr_an_rect, (560,60))
            
            dmg_num = DamageText(560, 60, f'-{(damage+crit)}', 'Red')
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
            abilities = self.enemy_curr_animal.abilities
            ability_dmg = list(abilities.values())
            damage = 0
            
            ability = random.randint(0,2) # Enemy picks an ability randomly
            damage += ability_dmg[ability]
            
            crit = random.randint(-5,5) 
            self.pl_curr_animal.curr_hp -= (damage + crit)
            
            curr_an_rect = pygame.Surface((300,200))
            curr_an_rect.set_alpha(0)
            curr_an_rect.fill((255,255,255))
            self.screen.blit(curr_an_rect, (240,160))
            
            dmg_num = DamageText(240, 180, f'-{(damage+crit)}', 'Red')
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
    
    def outro_text(self, screen):
        """
        Displays "victory" or "defeat" text once the fight is over (all player's or NPC's animals' health is 0).
        """
        pygame.draw.rect(screen, (0,0,0,128), (0,150,800,100))
        if self.victory:
            render_wrapped_text(screen, ["VICTORY"], self.even_bigger_font, 300, 175, 'White')
        else:
            render_wrapped_text(screen, ["DEFEAT"], self.even_bigger_font, 300, 175, 'Red')
        render_wrapped_text(screen, ["press SPACE to continue"], self.small_font, 230, 215, 'White')
    
    def outro(self, screen):
        """
        Displays an ending screen depending on whether the player won or lost the fight.
        """
        if self.victory:
            screen.fill((153, 255, 153))
            render_wrapped_text(screen, ['VICTORY'], self.even_bigger_font, 300, 30, 'Black')
            
            # Playerette
            pl_icon = self.player.icon
            pl_icon = pygame.transform.rotozoom(pl_icon, 0, 3)
            pl_icon_rect = pl_icon.get_rect(center = (400, 200))
            screen.blit(pl_icon, pl_icon_rect)
            
            # Her animals in front
            for i in range(len(self.pl_animals)):
                anim = self.pl_animals[len(self.pl_animals)-1-i]
                anim_icon = anim.icon
                anim_icon = pygame.transform.rotozoom(anim_icon, 0, 2)
                anim_icon_rect = anim_icon.get_rect(center = (200+200*i, 300))
                screen.blit(anim_icon, anim_icon_rect)
            
            # Playerette's text
            pygame.draw.rect(screen, 'White', (80,120,235,100),0,15)
            pygame.draw.polygon(screen, 'White', ((315,140),(315,170),(330,155)))
            for anim in self.pl_animals:
                if anim.name == 'Pom-pom':
                    pl_text = "The power of friendship won yet again! Right, Pom-Pom?"
                else: pl_text =  "The power of friendship won yet again!"
            wrap_pl_text = text_wrap(pl_text, self.small_font, 210)
            render_wrapped_text(screen, wrap_pl_text, self.small_font, 90, 135, 'Black', 3)
            
            # Pom-pom's text
            for anim in self.pl_animals:
                if anim.name == 'Pom-pom':
                    pygame.draw.rect(screen, 'White', (490,180,275,55),0,6)
                    pygame.draw.polygon(screen, 'White', ((725,235),(685,235),(665,260)))
                    render_wrapped_text(screen, ['I have no time for', 'your foolishness.'], self.small_font, 500, 190, 'Black', 5)
        else:
            screen.fill((126,54,54))
            render_wrapped_text(screen, ['DEFEAT'], self.even_bigger_font, 310, 30, 'Black')
            
            # Shopkeeper
            en_icon = self.enemy.icon
            en_icon = pygame.transform.rotozoom(en_icon, 0, 3)
            en_icon_rect = en_icon.get_rect(center = (400, 200))
            screen.blit(en_icon, en_icon_rect)
            
            # His animals in front
            for i in range(len(self.enemy_animals)):
                anim = self.enemy_animals[i]
                anim_icon = anim.icon
                anim_icon = pygame.transform.rotozoom(anim_icon, 0, 2)
                anim_icon_rect = anim_icon.get_rect(center = (200+200*i, 300))
                screen.blit(anim_icon, anim_icon_rect)
            
            # Shopkeeper's text
            pygame.draw.rect(screen, 'Black', (490,80,270,175),0,15)
            pygame.draw.polygon(screen, 'Black', ((490,190),(490,225),(470,205)))
            shopkeeper_text = "Never should have come here. Now you'll think twice before stepping foot into the wrong shop."
            wrap_shopk_text = text_wrap(shopkeeper_text, self.small_font, 240)
            render_wrapped_text(screen, wrap_shopk_text, self.small_font, 510, 100, 'White', 5)

            # Raccoon's text
            pygame.draw.rect(screen, 'Black', (145,225,150,30),0,6)
            pygame.draw.polygon(screen, 'Black', ((240,255),(270,255),(212,270)))
            render_wrapped_text(screen, ['lol loser'], self.small_font, 155, 234, 'White', 5)

