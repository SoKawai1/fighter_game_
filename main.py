import pygame
from pygame import *
from random import randint
clock = time.Clock()
#---------------------------------------------------Global-Variables--------------------------------------------------------------------------------
fps = 60
SCREEN_HEIGHT = 600
SCREEN_WIDHT = 1200
game = True
window = display.set_mode((SCREEN_WIDHT,SCREEN_HEIGHT))
display.set_caption('')
GREEN = (0,255,127)
DARK_GREEN = (0,128,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0] # Очки игрока №1 и №2
round_over = False
ROUND_OVER_COOLDOWN = 2000
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WARRIOR_ANIMATION_STEPS = [10,8,1,7,7,3,7] 
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]
WIZARD_ANIMATION_STEPS = [8,8,1,8,8,3,7] 
pygame.font.init()
events = event.get()
events[0].type 
mixer.init()
mixer.music.load('Sprites\Sounf_effects\epic_battle_music_1-6275.ogg')
mixer.music.play()

magic_attack1 = mixer.Sound('Sprites\Sounf_effects\ES_Magic-Spell-Explode-SFX-Producer.ogg')
magic_attack2 = mixer.Sound('Sprites\Sounf_effects\ES_Magic-Spell-Impact-SFX-Producer.ogg')
magic_attack3 = mixer.Sound('Sprites\Sounf_effects\ES_Magic-Spell-Whoosh-22-SFX-Producer.ogg')
#mixer.magic_attack1.load('')
#---------------------------------------------------Sprites-Import----------------------------------------------------------------------------------
menu_img = pygame.image.load('Sprites\Backgrounds\_background.jpg')
warrior_sheet = pygame.image.load('Sprites\Player_sprite\warrior1.png').convert_alpha()
wizard_sheet = pygame.image.load('Sprites\Player_sprite\wizard.png').convert_alpha()
count_font = pygame.font.Font('Sprites\Fonts\PixelFont.ttf', 80)
score_font = pygame.font.Font('Sprites\Fonts\PixelFont.ttf', 30)
warrior_win = pygame.image.load('Sprites\Player_sprite\warrior_win.png').convert_alpha()
wizard_win = pygame.image.load('Sprites\Player_sprite\wizard_win.png').convert_alpha()
#----------------------------------------------------Background--------------------------------------------------------------------------------
bck_1 = pygame.image.load('Sprites\Backgrounds\_background.jpg').convert_alpha()
bck_2 = pygame.image.load('Sprites\Backgrounds\dead_lands_bck.jpg').convert_alpha()
background_variant = 0
background_variant = randint(0,1)
#------------------------------------------------------Class--------------------------------------------------------------------------------------
class Fighter():
    def __init__ (self, player,x, y, flip,data,sprite_sheet,animation_steps):
        self.player = player
        self.size = data[0]    
        self.image_scale = data[1]              
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0-Стойка 1-Бег 2-Прыжок 3-Атака1 4-Атака2 5-ПолучениеУрона 6-Смерть
        self.frame_index = 0 
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.alive = True
        self.health = 100
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size,y * self.size,self.size,self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    def move(self, SCREEN_WIDHT, SCREEN_HEIGHT, surface, target):
        SPEED = 14
        GRAVITY = 1.5
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        key = pygame.key.get_pressed()
        if self.attacking == False and self.alive == True:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                        magic_attack2.play()
                    if key[pygame.K_KP2]:
                        self.attack_type = 2
                        magic_attack3.play()                        
        self.vel_y += GRAVITY
        dy += self.vel_y
        if target.alive == True:
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > SCREEN_WIDHT:
                dx = SCREEN_WIDHT - self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - 10:
            self.vel_y = 0
            self.jump = False
            dy = SCREEN_HEIGHT - 10 - self.rect.bottom
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)#Получение урона
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#Атака №1
            elif self.attack_type == 2:
                self.update_action(4)#Атака №2
        elif self.jump == True:
            self.update_action(2)#Прыжок
        elif self.running == True:
            self.update_action(1)#Бег
        else:
            self.update_action(0)#Стойка

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:  
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)                                                            
            if attacking_rect.colliderect(target.rect):
                dmg = randint(10,15)
                if dmg > 13:
                    print('Crit!')
                target.health -= dmg
                target.hit = True
            #pygame.draw.rect( surface, (0, 255, 0), attacking_rect)
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,0,0),self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
def draw_health_bar(health , x, y):
    ratio = health / 100
    pygame.draw.rect(window, BLACK, (x - 5, y - 5, 410, 40))    
    pygame.draw.rect(window, DARK_GREEN, (x, y, 400, 30))
    pygame.draw.rect(window, GREEN, (x, y, 400 * ratio, 30))
def warrior_won(warrior_win):
    window.blit(warrior_win,(340,-130))
def wizard_won(wizard_win):
    window.blit(wizard_win,(340,-130))
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))
#-------------------------------------------------Game-cycle------------------------------------------------------------------
fighter1 = Fighter(1,150, 350, False,WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter2 = Fighter(2,950, 350, True,WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
game = True
while game:
    clock.tick(fps)      
    if background_variant == 0:
        background = bck_1
    elif background_variant == 1:
        background = bck_2
    background = pygame.transform.scale(background, (1200, 600))
    window.blit(background,(0 ,0))
    draw_health_bar(fighter1.health, 20 , 20)
    draw_health_bar(fighter2.health, 770 , 20)
    if intro_count <= 0:
        fighter1.move(SCREEN_WIDHT, SCREEN_HEIGHT, window ,fighter2)
        fighter2.move(SCREEN_WIDHT, SCREEN_HEIGHT, window ,fighter1)
    else:
        draw_text(str(intro_count), count_font, RED , SCREEN_WIDHT / 2, SCREEN_HEIGHT /3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
    if round_over == False:
        if fighter1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()          
    elif fighter1.alive == False:
        warrior_won(wizard_win)
    elif fighter2.alive == False:  
        wizard_won(warrior_win)  
    else:
        pass     
    fighter1.update()
    fighter2.update()
    fighter1.draw(window)
    fighter2.draw(window)
    display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False
