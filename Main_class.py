import pygame
from sys import exit
from random import randint, choice


#global variables
score_shooting = 0
passed_time = 0
started_time = 0

class Munition (pygame.sprite.Sprite):
    def __init__(self,player_pos_y):
        super().__init__()
        self.player_bullet = pygame.image.load('Graphics/bullet.png').convert_alpha()
        self.image = self.player_bullet
        self.rect = self.image.get_rect(midright = (130, player_pos_y +50))
        self.bullet_state = False

    def shoot_bullet(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.bullet_state = True

    def bullet_movement(self):
        if self.bullet_state == True:
            self.rect.x += 10
        if self.rect.x >= 800:
            self.bullet_state = False

    def destroy(self):
        if self.rect.x >= 820:
            self.kill()
            
    def update(self):
        self.shoot_bullet()
        self.bullet_movement()
        self.destroy()

class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Graphics/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('Graphics/jump.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
    
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(topleft = (80,266))
        self.gravity = 0
        self.double_jump = True
        self.jump_sound_possible = True

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.double_jump == True:
            self.gravity = -10
        
            if self.jump_sound_possible:
                self.jump_sound.play()
                self.jump_sound_possible = False
            
            if self.rect.y <= 180:
                self.jump_sound.play()
                self.jump_sound_possible = False

            
    def apply_gravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.y >= 266:
            self.rect.y = 266
            self.double_jump = True
            self.jump_sound_possible = True
        if self.rect.y < 50:
            self.double_jump = False
        
        # player position for the bullet shooting
        global player_pos_y
        player_pos_y = self.rect.y

    def animation_state(self):
        if self.rect.y <266:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle (pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('Graphics/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Graphics/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            list_y_pos = [230, 150, 100, 50]
            y_pos = choice(list_y_pos)
            self.type = "fly"
        
        else:
            snail_1 = pygame.image.load('Graphics/snail.png').convert_alpha()
            snail_2 = pygame.image.load('Graphics/snail2.png').convert_alpha()
            self.frames= [snail_1, snail_2]
            y_pos = 300
            self.type = "snail"

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (randint(900, 1400), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class Main_game:
    def __init__(self):

        self.score = 0
        self.level = 1
        
    def display_score(self, score_shooting):
    
        self.score += score_shooting
        self.score_surf = test_font.render('Score: ' + f'{self.score}', False, "White")   
        self.score_rect = self.score_surf.get_rect(topleft = (40,30))
        screen.blit(self.score_surf, self.score_rect)
        
    def display_wave(self, passed_time):
        
        if passed_time > 10000:
            self.level = 2
        if passed_time > 20000:
            self.level = 3

        self.level_surf = test_font.render('Level: ' + f'{self.level}', False, "White")
        self.level_rect = self.level_surf.get_rect(topleft = (650,30))
        screen.blit(self.level_surf, self.level_rect)
        
        if passed_time >= 31000:
            wave = "Final battle!"
            wave_surf = test_font.render(wave, False, "White")
            wave_rect = wave_surf.get_rect(topleft = (220, 30))
            screen.blit(wave_surf, wave_rect)
        if passed_time >= 100000:
            wave2 = "Concrats! You won!"
            wave2_surf = test_font.render(wave2, False, "White")
            wave2_rect = wave2_surf.get_rect(topleft = (220, 30))
            screen.blit(wave2_surf, wave2_rect)
    
# end game if collision with obstacle
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,True):
        obstacle_group.empty()
        return False
    else:
        return True

# if shooting obstacle, kill obstacle
def collision_sprite_munition():
    if pygame.sprite.groupcollide(munition_group, obstacle_group,True, True):
        explosion_sound.play()
        global score_shooting
        score_shooting += 100
        
#initial statements and settings for game
pygame.init()
game_running = True
game_started = False
game_end = False
game_difficulty = 900
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Cat game <3')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 40)

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
munition_group = pygame.sprite.Group()

#background
sky_surf = pygame.image.load('Graphics/space_background.jpg').convert_alpha()
ground_surf = pygame.image.load('Graphics/ground.png').convert_alpha()

# EndScreen
endtext_surf = test_font.render("You lost! Press space to continue", False, "White")
endtext_rect = endtext_surf.get_rect(center = (400,100))
endimg_surf = pygame.image.load('Graphics/intro_cat.jpeg')
endimg_surf_scaled = pygame.transform.scale(endimg_surf, (200,200))
endimg_rect = endimg_surf_scaled.get_rect(center = (400, 250))

# Startscreen
start_surf = pygame.image.load('Graphics/space_cat.jpg')
start_surf_scaled = pygame.transform.scale(start_surf, (1020, 700))
start_cat_rectangle = start_surf_scaled.get_rect(topleft = (0,0))
start_text = test_font.render("Welcome to catheaven! Press space to continue", False, "White")
start_rect = start_text.get_rect(center = (-500, 50))

# timers
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 900)

obstacle_timer2 = pygame.USEREVENT +2
pygame.time.set_timer(obstacle_timer2, 600)

obstacle_timer3 = pygame.USEREVENT +3
pygame.time.set_timer(obstacle_timer3, 300)

obstacle_timer4 = pygame.USEREVENT +4
pygame.time.set_timer(obstacle_timer4, 100)

# sounds
explosion_sound = pygame.mixer.Sound('Audio/explosion.wav')
explosion_sound.set_volume(0.2)

#Eventhandler
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 

        if game_running == False: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = True
                    started_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True

        if game_started == True and game_running == True:
            passed_time = pygame.time.get_ticks() - started_time
            if passed_time > 100000:
                pass
            elif passed_time > 40000 and event.type == obstacle_timer4:
                obstacle_group.add(Obstacle(choice(['fly', 'snail'])))
            elif passed_time > 30000:
                pass
            elif passed_time > 20000 and event.type == obstacle_timer3:
                obstacle_group.add(Obstacle(choice(['fly', 'snail'])))
            elif passed_time > 10000 and event.type == obstacle_timer2:
                obstacle_group.add(Obstacle(choice(['fly', 'snail'])))
            elif passed_time < 10000 and event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail'])))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    munition_group.add(Munition(player_pos_y))

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_end == True:
                        game_end = False
                        game_running = True
                        game_started = False
                        passed_time = 0
    
    #intro
    if game_running == True:
        screen.blit(start_surf, start_cat_rectangle)
        screen.blit(start_text, start_rect)

        # introscreen movement
        start_rect.x += 4
        if start_rect.x > 800:
            start_rect.x = -600
        level = 1
        score = 0
     
    #gamemode
    if game_started == True:
        if game_running == True:
            pygame.draw.line(screen, "Black", (0,350), (800,350), width = 3)
            screen.blit(sky_surf,(0,0))
            screen.blit(ground_surf,(0,350))
            main_game = Main_game()
            main_game.display_score(score_shooting)
            main_game.display_wave(passed_time)
            player.draw(screen)
            player.update()
            obstacle_group.draw(screen)
            obstacle_group.update()
            munition_group.draw(screen)
            munition_group.update()
            game_running = collision_sprite()
            collision_sprite_munition()
        else:
            pygame.draw.rect(screen, "Black", pygame.Rect(0, 0, 800, 400))
            screen.blit(endtext_surf, endtext_rect)
            screen.blit(endimg_surf_scaled, endimg_rect)
            player_gravity = 0
            score_shooting = 0

            #display score
            score_message = test_font.render('Your Score: ' + f'{main_game.score}', False, "White")
            score_rect = score_message.get_rect(center = (400, 50))
            screen.blit(score_message, score_rect)
            game_end = True
            
    pygame.display.update()
    clock.tick(60)

































""""
# objects
snail_frame1 = pygame.image.load('Graphics/snail.png').convert_alpha()
snail_frame2 = pygame.image.load('Graphics/snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load('Graphics/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Graphics/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# player rectangle
player_walk1 = pygame.image.load('Graphics/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('Graphics/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0 
player_jump = pygame.image.load('Graphics/jump.png').convert_alpha()
player_surf = player_walk[player_index]

player_surf = pygame.image.load('Graphics/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(topleft = (50,266))
player_gravity = -20
"""



