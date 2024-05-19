import pygame
import sys
import random
from src.player_class import Player
from src.coin_class import Coin
from src.spike_classes import East_Wall_Spike, West_Wall_Spike, Ceilling_Spike, Floor_Spike
from pygame import mixer

pygame.init()

scale = 2
user_x = 288 * scale
user_y = 352 * scale
screen = pygame.display.set_mode((user_x, user_y))
pygame.display.set_caption("Beware of the skewers!")

with open("data/high_score.txt") as file:
    high_score = file.read()
start_high_score = high_score
with open("data/total_coins.txt") as file:
    coin_total = file.read()
coin_total = int(coin_total)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("font\\Pixeltype.ttf", size)
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def high_score_check(high_score, score):
    if int(high_score) < int(score):
        return score
    else:
        return high_score

floor_rect = pygame.Rect(0, round(user_y * (0.9)), user_x, user_y)
floor_spikes = [Floor_Spike(scale) for _ in range(0, 9)]
floor_spikes = [spike.set_position(i * scale * 32, round(user_y * (0.9)) - spike.rect.height) for i, spike in enumerate(floor_spikes)]

ceilling_rect = pygame.Rect(0, -user_y, user_x, user_y + round(user_y * (0.1)))
ceilling_spikes = [Ceilling_Spike(scale) for _ in range(0, 9)]
ceilling_spikes = [spike.set_position(i * scale * 32, round(user_y * (0.1))) for i, spike in enumerate(ceilling_spikes)]

def randomise_spikes(score, flag, scale):
    if flag != 0:
        if score < 5:
            count = 2
        elif score < 10:
            count = 3
        elif score < 20:
            count = 4
        else:
            count = 5
        if flag == 1:
            return [East_Wall_Spike(scale) for _ in range(0, count)], [], count
        return [], [West_Wall_Spike(scale) for _ in range(0, count)], count
    return [], [], 0

def generate_spikes(scale, score):
    east_spikes, west_spikes, count = randomise_spikes(score, player.check_wall_collision(), scale)
    pos_list = [i for i in range(2, 9)]
    pos_list = random.sample(pos_list, count)
    west_spikes = [spike.set_position(0, pos_list.pop() * 32 * scale) for spike in west_spikes]
    east_spikes = [spike.set_position(user_x - spike.rect.width, pos_list.pop() * 32 * scale) for spike in east_spikes]
    return east_spikes, west_spikes

def menage_spikes(east_spikes, west_spikes, player):
    for spike in east_spikes + west_spikes:
        screen.blit(spike.image, spike.rect)
        if spike.rect.colliderect(player.rect):
            player.death()

def generate_coins(coin_list, scale):
    if coin_list == []:
        coin = Coin(scale)
        coin_list = [coin.set_position(random.randint(round(0.2 * user_x), round(0.8 * user_x)), random.randint(round(0.2 * user_y), round(0.8 * user_y)))]
    return coin_list

def menage_coins(coin_list, coin_total, player):
    for coin in coin_list:
        screen.blit(coin.image, coin.rect)
        if coin.rect.colliderect(player.rect):
            coin_sound.play()
            coin_list = []
            coin_total += 1
    return coin_list, coin_total

running = False
player = Player(scale, user_x, user_y)
east_spikes = []
west_spikes = []
coin_list = []
coin_sound = mixer.Sound("aduio/coin_collect.mp3")
clock = pygame.time.Clock()
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if int(start_high_score) < int(high_score):
                with open("data/high_score.txt", "w") as file:
                    file.write(f"{high_score}")
            with open("data/total_coins.txt", "w") as file:
                file.write(f"{coin_total}")
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
        if player.dead:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (user_x // 3 < event.pos[0] < user_x // 3 * 2) and (user_y // 5 * 2 < event.pos[1] < user_y // 5 * 2 + user_y // 6):
                    player.defult_pos()
                    player.dead = False
                    coin_list = []
                    score = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.defult_pos()
                    player.dead = False
                    coin_list = []
                    score = 0
        elif not running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                    player.jump()
    screen.fill("#c3c3c3")

    pygame.draw.rect(screen, "#5c5c5c", floor_rect)

    for spike in floor_spikes:
        screen.blit(spike.image, spike.rect)

    pygame.draw.rect(screen, "#5c5c5c", ceilling_rect)

    for spike in ceilling_spikes:
        screen.blit(spike.image, spike.rect)

    draw_text(screen, f"Score: {score}", 40 * scale, user_x // 2, user_y // 3 - 12 * scale)
    draw_text(screen, f"High Score: {high_score}", 40 * scale, user_x // 2, user_y // 5 - 12 * scale)
    draw_text(screen, f"Coins: {coin_total}", 40 * scale, user_x // 2, user_y // 4 * 3)
    if not player.dead:
        if running:
            for spike in floor_spikes + ceilling_spikes:
                if spike.rect.colliderect(player.rect):
                    player.death()

            if player.check_wall_collision() != 0:
                player.after_collision()
                score += 1
                coin_list = generate_coins(coin_list, scale)
                east_spikes, west_spikes = generate_spikes(scale, score)

            coin_list, coin_total = menage_coins(coin_list, coin_total, player)
            menage_spikes(east_spikes, west_spikes, player)

            player.update()

            if player.dead:
                west_spikes = []
                east_spikes = []
                running = False

        else:
            player.defult_pos()
            player.start_screen_animation()
            draw_text(screen, "Press SPACE to start", 40 * scale, user_x // 2, user_y // 2 + 30 * scale)

    else:
        pygame.draw.rect(screen, "#fd5f5f", pygame.Rect(user_x // 3, user_y // 5 * 2, user_x // 3, user_y // 6), 90, 30)
        pygame.draw.rect(screen, "#bf5959", pygame.Rect(user_x // 3, user_y // 5 * 2, user_x // 3, user_y // 6), 10, 30)
        draw_text(screen, "Retry", 40 * scale, user_x // 2, user_y // 2 - 16 * scale)
    screen.blit(player.image, player.rect)
    high_score = high_score_check(high_score, score)

    pygame.display.update()
    clock.tick(30)
