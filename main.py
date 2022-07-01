import pygame
from sys import exit
from random import randint, choice

#global variables
started_time = 0
x_position = 0
y_position = 0
boss_alive = True


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
        
    def display_score(self):
        self.score_surf = test_font.render('Score: ' + f'{self.score}', False, "White")   
        self.score_rect = self.score_surf.get_rect(topleft = (40,30))
        screen.blit(self.score_surf, self.score_rect)
        
    def display_wave(self, passed_time):
        if passed_time > 10000:
            self.level = 2
        if passed_time > 20000:
            self.level = 3
        if passed_time > 28000:
            self.level = 4

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
    def collision_sprite(self):
        if pygame.sprite.spritecollide(player.sprite, obstacle_group,True):
            obstacle_group.empty()
            return False
        else:
            return True

    # if shooting obstacle, kill obstacle + score
    def collision_sprite_munition(self):
        if pygame.sprite.groupcollide(munition_group, obstacle_group,True, True):
            explosion_sound.play()
            self.score += 100

    def add_score_boss(self):
        self.score += 100
    
    def collision_player_munition(self):
        if pygame.sprite.groupcollide(player, boss_munition, False, True):
            boss_munition.empty()
            return False
        else:
            return True

    def update (self):
        self.display_score()
        self.display_wave(passed_time)
        self.collision_sprite()
        self.collision_sprite_munition()
        self.collision_player_munition()

class Start_screen:
    def __init__(self):
        self.start_surf = pygame.image.load('Graphics/space_cat.jpg').convert_alpha()
        self.start_surf_scaled = pygame.transform.scale(self.start_surf, (1020, 700))
        self.start_cat_rectangle = self.start_surf_scaled.get_rect(topleft = (0,0))
        self.start_text = test_font.render("Welcome to catheaven! Press space to continue", False, "White").convert_alpha()
        self.start_rect = self.start_text.get_rect(center = (200, 50))

    def text_movement(self):
        self.start_rect.x += 4
        if self.start_rect.x > 800:
            self.start_rect.x = -600
        screen.blit(self.start_surf, self.start_cat_rectangle)
        screen.blit(self.start_text, self.start_rect)
        
class End_screen():
    def __init__(self):
        self.game_status = "You loose!"
        if boss_alive == False:
            self.game_status = "You won!"
        self.endimg_surf = pygame.image.load('Graphics/intro_cat.jpeg')
        self.endtext_surf = test_font.render(self.game_status +" Press space to continue", False, "White")
        self.endtext_rect = self.endtext_surf.get_rect(center = (400,100))
        
        self.endimg_surf_scaled = pygame.transform.scale(self.endimg_surf, (200,200))
        self.endimg_rect = self.endimg_surf_scaled.get_rect(center = (400, 250))

        screen.blit(self.endtext_surf, self.endtext_rect)
        screen.blit(self.endimg_surf_scaled,self.endimg_rect)

        self.score_message = test_font.render('Your Score: ' + f'{main_game.score}', False, "White")
        self.score_rect = self.score_message.get_rect(center = (400, 50))
        screen.blit(self.score_message, self.score_rect)
        

class Boss (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        boss_surf1 = pygame.image.load('Graphics/fly1.png').convert_alpha()
        boss_surf2 = pygame.image.load('Graphics/fly2.png').convert_alpha()
        self.frames = [boss_surf1, boss_surf2]
        self.health = 100
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (700, 300))
        self.move_down = True

        self.damage = False
        self.damage_count = 0

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def boss_position(self):
        if self.move_down == True:
            self.rect.y += 4
        if self.move_down == False:
            self.rect.y -= 4
        if self.rect.y >= 300:
            self.move_down = False
        if self.rect.y <= 60:
            self.move_down = True

        global x_position
        x_position = self.rect.x
        global y_position
        y_position = self.rect.y
        
    def health_bar (self):
        self.health_surf = pygame.Surface((40,4))
        self.health_surf.fill((0,255,127))
        self.health_bar_rect = self.health_surf.get_rect(topleft = (self.rect.x +30, self.rect.y -15))
        screen.blit(self.health_surf, self.health_bar_rect)

        self.damage_surf = pygame.Surface((self.damage_count,4))
        self.damage_surf.fill((255,100,127))
        self.damage_rect = self.damage_surf.get_rect(topleft = (self.rect.x +30, self.rect.y -15))
        screen.blit(self.damage_surf, self.damage_rect)
     
    def collision_sprite_munition(self):
        if pygame.sprite.groupcollide(boss, munition_group, False, True):
            self.damage_count += 5 
            explosion_sound.play()
            main_game.add_score_boss()

        if self.damage_count >= 40:
            boss.empty()
            boss_munition.empty()
            global boss_alive
            boss_alive = False
      
    def update(self):
        self.animation_state()
        self.boss_position()
        self.health_bar()
        self.collision_sprite_munition()

class Boss_Munition (pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.img = pygame.image.load('Graphics/bullet.png').convert_alpha()
        self.image = pygame.transform.rotate(self.img, 180)
        self.rect = self.image.get_rect(topleft = (x_position, y_position))

    def bullet_movement(self):
        self.rect.x -= 6
        screen.blit(self.image, self.rect)
    
    def update(self):
        self.bullet_movement()

#initial statements and settings for game
pygame.init()
game_running = True
game_started = False
game_end = False
game_difficulty = 900
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Simple Shooter <3')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 40)

#groups and classes initalisation
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
munition_group = pygame.sprite.Group()
start_screen = Start_screen()
main_game = Main_game()
boss = pygame.sprite.Group()
boss.add(Boss()) 
boss_munition = pygame.sprite.Group()

#background
sky_surf = pygame.image.load('Graphics/space_background.jpg').convert_alpha()
ground_surf = pygame.image.load('Graphics/ground.png').convert_alpha()

# timers
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 900)
obstacle_timer2 = pygame.USEREVENT +2
pygame.time.set_timer(obstacle_timer2, 600)
obstacle_timer3 = pygame.USEREVENT +3
pygame.time.set_timer(obstacle_timer3, 300)
obstacle_timer4 = pygame.USEREVENT +4
pygame.time.set_timer(obstacle_timer4, 100)
obstacle_timer5 = pygame.USEREVENT +5
pygame.time.set_timer(obstacle_timer5, randint(1000, 3000))

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

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True

        if game_started == True and game_running == True:
            global passed_time
            passed_time = pygame.time.get_ticks() - started_time
           
            if passed_time > 28000:
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
    if game_running == True and game_started == False:
        start_screen.text_movement()
        main_game.score = 0
        main_game.level = 1
        started_time = pygame.time.get_ticks()
     
    #gamemode
    if game_started == True:
        if game_running == True:
            pygame.draw.line(screen, "Black", (0,350), (800,350), width = 3)
            screen.blit(sky_surf,(0,0))
            screen.blit(ground_surf,(0,350))
            main_game.update()
            player.draw(screen)
            player.update()
            obstacle_group.draw(screen)
            obstacle_group.update()
            munition_group.draw(screen)
            munition_group.update()

            if passed_time > 35000:
                boss.draw(screen)
                boss.update()
                if event.type == obstacle_timer5 and boss_alive == True:
                    boss_munition.add(Boss_Munition(x_position, y_position))

            boss_munition.draw(screen)
            boss_munition.update()
            if main_game.collision_sprite() == False or main_game.collision_player_munition() == False:
                game_running = False

        else:
            pygame.draw.rect(screen, "Black", pygame.Rect(0, 0, 800, 400))
            end_screen = End_screen()
            boss.empty()
            boss.add(Boss()) 
            player_gravity = 0

            

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



