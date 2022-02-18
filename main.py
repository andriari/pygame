import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("fat runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
score_surface = test_font.render("Score : ", False, (64, 64, 64))
score_rect = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (750, 300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #if event.type == pygame.MOUSEBUTTONUP:
        #   if(player_rect.collidepoint(event.pos)): print("collide")

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)

    screen.blit(score_surface, score_rect)

    snail_rect.x -= 3
    if(snail_rect.right <= -10):
        snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    #if(player_rect.colliderect(snail_rect)):
    #   print("collide!")

    #mouse_pos = pygame.mouse.get_pos()
    #if(player_rect.collidepoint(mouse_pos)):
    #  print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)