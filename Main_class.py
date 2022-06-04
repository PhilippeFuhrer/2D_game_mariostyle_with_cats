import pygame
from sys import exit
from random import randint, choice

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/10)
    score_surf = test_font.render('Score: ' + f'{current_time}', False, "White")
    score_rect = score_surf.get_rect(topleft = (40,40))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6

            if obstacle_rect.y == 290:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        #remove the obstacles from the list, to reduce memory
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True



pygame.init()
game_running = True
game_started = False
game_end = False
start_time = 0
score = 0
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Cat game <3')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 40)

#background
sky_surf = pygame.image.load('Graphics/space_background.jpg').convert_alpha()
ground_surf = pygame.image.load('Graphics/ground.png').convert_alpha()

# player rectangle
player_surf = pygame.image.load('Graphics/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(topleft = (50,266))
player_gravity = -20

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

# objects
snail_surf = pygame.image.load('Graphics/snail.png').convert_alpha()
obstacle_rect_list = []
fly_surf = pygame.image.load('Graphics/fly1.png').convert_alpha()


# timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 900)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_started == True and game_running == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.y > 50:
                        player_gravity = -20
                        print(player_rect.y)

        if game_running == False: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = True
                    start_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True

        if event.type == obstacle_timer and game_started == True and game_running == True:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(topleft = (randint(900,1400), 290)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(topleft = (randint(900,1400), 210)))

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_end == True:
                        game_end = False
                        game_running = True
                        game_started = False
        
        #if event.type == pygame.MOUSEMOTION:
            #player_rect.collidepoint(event.pos)

    
    if game_running == True:
        screen.blit(start_surf, start_cat_rectangle)
        screen.blit(start_text, start_rect)

        # introscreen movement
        start_rect.x += 4
        if start_rect.x > 800:
            start_rect.x = -600

    if game_started == True:
        if game_running == True:
            pygame.draw.line(screen, "Black", (0,350), (800,350), width = 3)
            screen.blit(sky_surf,(0,0))
            screen.blit(ground_surf,(0,350))
            #screen.blit(snail_surf,snail_rect)

            #obstacle movement
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            #display score while gamge_started == true
            score = display_score()

            # draw player + gravity
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.top > 266:
                player_rect.top = 266
            screen.blit(player_surf, player_rect)

            #collisions
            game_running = collision(player_rect, obstacle_rect_list)

        else:
            pygame.draw.rect(screen, "Black", pygame.Rect(0, 0, 800, 400))
            screen.blit(endtext_surf, endtext_rect)
            screen.blit(endimg_surf_scaled, endimg_rect)
            player_rect.midbottom = (80,266)
            player_gravity = 0

            #display score
            score_message = test_font.render('Your Score: ' + f'{score}', False, "White")
            score_rect = score_message.get_rect(center = (400, 50))

            if score > 0:
                screen.blit(score_message, score_rect)
            
            obstacle_rect_list.clear()
            game_end = True


    pygame.display.update()
    clock.tick(60)





