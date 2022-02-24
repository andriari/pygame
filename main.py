import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/100)
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def jump(rect):
    if rect.bottom >= 300:
        gravity = -20
    else:
        gravity = 0
    return gravity


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -150]
        return obstacle_list
    else:
        return []


def collision(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if obstacle_rect.colliderect(player):
                return False
            else:
                return True
    else:
        return True


def player_animation():
    global player_rect, player_surface, player_walk, player_index, player_jump
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
game_active = False
game_score = 0
start_time = 0
title = "Fat Runner"
pygame.display.set_caption(title)
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# player
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# intro
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title_surface = test_font.render(title, False, (111, 196, 169))
title_surface = pygame.transform.rotozoom(title_surface, 0, 2)
title_rect = title_surface.get_rect(center=(400, 50))

instruct_surface = test_font.render("Press space to START", False, (64, 64, 64))
instruct_rect = instruct_surface.get_rect(center=(400, 340))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # obstacle generator
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomleft=(randint(850, 1050), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomleft=(randint(850, 1050), 210)))

            # obstacle animation
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0

                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0

                fly_surface = fly_frames[fly_frame_index]

            # jumping mechanism
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gravity = jump(player_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and event.button == pygame.BUTTON_LEFT:
                    player_gravity = jump(player_rect)
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        game_score = display_score()

        # snail
        # snail_rect.x -= 6
        # if snail_rect.right <= -10:
        #    snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision(player_rect, obstacle_rect_list)

    else:
        obstacle_rect_list.clear()
        player_rect.bottom = 300
        player_gravity = 0

        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your Score: {game_score}', False, (64, 64, 64))
        score_rect = score_message.get_rect(center=(400, 340))
        if game_score > 0:
            screen.blit(score_message, score_rect)
        else:
            screen.blit(instruct_surface, instruct_rect)
        screen.blit(title_surface, title_rect)

    pygame.display.update()
    clock.tick(60)