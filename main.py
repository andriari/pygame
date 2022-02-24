import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.2)
        self.walk = [player_walk_1, player_walk_2]
        self.index = 0
        self.jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.keyboard_pressed = False
        self.game_active = True

    def player_input(self):
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        left_click_pressed = pygame.mouse.get_pressed()[0]
        if keys[pygame.K_SPACE] and not self.keyboard_pressed:
            self.keyboard_pressed = True
            if self.rect.bottom >= 300:
                self.gravity = -20
                self.jump_sound.play()
        elif not keys[pygame.K_SPACE]:
            self.keyboard_pressed = False

        if left_click_pressed:
            if self.rect.collidepoint(pos):
                if self.rect.bottom >= 300:
                    self.gravity = -20
                    self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.index += 0.1
            if self.index >= len(self.walk):
                self.index = 0
            self.image = self.walk[int(self.index)]

    def animation_reset(self, game_active):
        if not game_active:
            self.rect.bottom = 300

    def update(self, game_active):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.animation_reset(game_active)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'snail':
            # snail
            frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            y_pos = 300
            self.rate_speed = 0.1
        else:
            # fly
            frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            y_pos = 210
            self.rate_speed = 0.2

        self.frames = [frame_1, frame_2]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(randint(850, 1050), y_pos))

    def animation_state(self):
        self.frame_index += self.rate_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -150:
            self.kill()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 100)
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else:
        return True


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
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops=-1)
# obstacle Group
obstacle = pygame.sprite.Group()

# player Group
player = pygame.sprite.GroupSingle()
player.add(Player())

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
                obstacle.add(Obstacle(choice(['snail', 'fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        bg_music.set_volume(0.1)
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        game_score = display_score()

        player.draw(screen)
        player.update(game_active)

        obstacle.draw(screen)
        obstacle.update()

        # collision
        game_active = collision()

    else:
        bg_music.set_volume(0)
        player.update(game_active)
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
