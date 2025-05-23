import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_RETURN

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)
BIG_FONT = pygame.font.SysFont("Verdana", 60)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load("player.png").convert_alpha()
player_rect = player.get_rect()
player_rect.center = main_display.get_rect().center

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

boom_image = BIG_FONT.render("BOOM!", True, COLOR_RED)
game_over_image = BIG_FONT.render("GAME OVER", True, COLOR_BLACK)
restart_image = FONT.render("Натисни ENTER щоб почати знову", True, COLOR_BLACK)

life = 3
timer = 0

pygame.mixer.init()
try:
    pygame.mixer.music.load("AmIWrong.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Фонова музика не знайдена або не може бути відтворена")

def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(), HEIGHT - enemy.get_height()), *enemy.get_size())
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width), -bonus.get_height(), *bonus.get_size())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)
TIMER_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(TIMER_EVENT, 1000)

def game_loop():
    global player, player_rect, image_index, score, life, timer, bg_X1, bg_X2

    enemies = []
    bonuses = []
    score = 0
    life = 3
    timer = 0
    image_index = 0
    playing = True
    boom_timer = 0

    bg_X1 = 0
    bg_X2 = bg.get_width()

    player_rect.center = main_display.get_rect().center

    while playing:
        FPS.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index = (image_index + 1) % len(PLAYER_IMAGES)
            if event.type == TIMER_EVENT:
                timer += 1

        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)
        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        bg_X1 -= bg_move
        bg_X2 -= bg_move

        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))

        for enemy in enemies[:]:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                boom_timer = 30
                life -= 1
                enemies.remove(enemy)

        for bonus in bonuses[:]:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.remove(bonus)

        if boom_timer > 0:
            main_display.blit(boom_image, (WIDTH//2 - 100, HEIGHT//2))
            boom_timer -= 1

        main_display.blit(player, player_rect)
        main_display.blit(FONT.render(f"Бонуси: {score}", True, COLOR_BLACK), (WIDTH - 200, 20))
        main_display.blit(FONT.render(f"Життя: {life}", True, COLOR_BLACK), (WIDTH - 200, 50))
        main_display.blit(FONT.render(f"Час: {timer}с", True, COLOR_BLACK), (WIDTH - 200, 80))

        pygame.display.flip()

        for enemy in enemies[:]:
            if enemy[1].right < 0:
                enemies.remove(enemy)

        for bonus in bonuses[:]:
            if bonus[1].top > HEIGHT:
                bonuses.remove(bonus)

        if life <= 0:
            end_game()
            return

def end_game():
    while True:
        main_display.blit(game_over_image, (WIDTH//2 - 200, HEIGHT//2 - 50))
        main_display.blit(restart_image, (WIDTH//2 - 200, HEIGHT//2 + 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    return

while True:
    game_loop()