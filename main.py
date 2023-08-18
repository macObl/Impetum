import pygame
from fighter import Fighter

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEGIHT = 600


screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEGIHT))
pygame.display.set_caption("Brawler")

clock = pygame.time.Clock()
FPS = 60


HEALTH_LOW = (76, 69, 102)
RED = (255, 0, 0)
HEALTH = (203, 69, 96)
BLACK = (0, 0, 0)

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False 
ROUND_OVER_COOLDOWN = 2000

WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]


bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

health_img = pygame.image.load("assets/images/icons/health.png").convert_alpha()
scaled_health = pygame.transform.scale(health_img, (364, 84))

victory_img =  pygame.image.load("assets/images/icons/you-win.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def darw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEGIHT))
    screen.blit(scaled_bg, (0,0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    screen.blit(scaled_health, (x, y))
    pygame.draw.rect(screen, HEALTH_LOW, (x+102, y+30, 205, 21))
    pygame.draw.rect(screen, HEALTH, (x+102, y+30, 205 * ratio, 21))

fighter_1 = Fighter(1, 200, 360, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 360, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

run = True
while run:

    clock.tick(FPS)

    darw_bg()

    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, BLACK, 140, 80)
    draw_text("P2: " + str(score[1]), score_font, BLACK, 680, 80)

    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEGIHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEGIHT, screen, fighter_1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEGIHT / 3)
        if(pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            

    fighter_1.update()
    fighter_2.update()
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (300, 50))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 200, 360, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
            fighter_2 = Fighter(2, 700, 360, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    pygame.display.update()

pygame.quit()