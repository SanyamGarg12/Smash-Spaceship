import pygame
import os
import sys
import random
import time
# Initializing
pygame.font.init()
pygame.mixer.init()
# Defined some basic parameters
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load(os.path.join("Assets1","S_icon.png"))
pygame.display.set_caption("Smash Spaceship!")
pygame.display.set_icon(icon)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)
# Sound effect
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets1/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets1/Gun+Silencer.mp3')
HEAL_SOUND = pygame.mixer.Sound('Assets1/heal.mp3')
loss_SOUND = pygame.mixer.Sound('Assets1/loss.mp3')
# All font used to display
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
M_BULLET_FONT = pygame.font.SysFont('comicsans', 40)
time_font = pygame.font.SysFont('comicsans', 30)
mystery_width = 50
mystery_height = 40
FPS = 60
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
# Making userevents
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RED_HEART = pygame.USEREVENT + 3
YELLOW_HEART = pygame.USEREVENT + 4

# importing and tranforming images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets1', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets1', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)
mystery_image1 = pygame.image.load(os.path.join('Assets1', 'star.png'))
mystery_image2 = pygame.image.load(os.path.join('Assets1', 'another_star.png'))
mystery_box1 = pygame.transform.scale(
    mystery_image1, (mystery_width, mystery_height))
mystery_box2 = pygame.transform.scale(
    mystery_image2, (mystery_width+20, mystery_height+20))
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets1', 'earth.jpeg')), (WIDTH, HEIGHT))
green_screen = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets1', 'earth.jpeg')), (WIDTH, HEIGHT))
instruct = pygame.font.SysFont('comicsans', 50)


# Starting Display
def game_start():
    WIN.blit(green_screen, (0, 0))
    WIN.blit(instruct.render('Press ANY key to play', 1, WHITE), (200, 200))
    pygame.display.update()


# Main window display
def draw_window(red, yellow, red_bullets, yellow_bullets, n_red_bullets, n_yellow_bullets, red_health, yellow_health, Y_MAX_BULLETS, R_MAX_BULLETS, box1, box2, TIME):
    WIN.blit(SPACE, (0, 0))
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, YELLOW)
    red_bullets_text = M_BULLET_FONT.render(
        'Bullets left: '+str(R_MAX_BULLETS), 1, RED)
    yellow_bullets_text = M_BULLET_FONT.render(
        'Bullets left: '+str(Y_MAX_BULLETS), 1, YELLOW)
    time_text = time_font.render("Time left : "+str(TIME), 1, BROWN)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_bullets_text, (WIDTH - red_bullets_text.get_width()-10, 45))
    WIN.blit(yellow_bullets_text, (10, 45))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(mystery_box1, (box1.x, box1.y))
    WIN.blit(time_text, (WIDTH//2 - 100, 10))
    WIN.blit(mystery_box2, (box2.x, box2.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in n_yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in n_red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


# Yellow Controls -> w,a,s,d to move
def yellow_handle_movement(keys_pressed, yellow, box1, box2):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < WIDTH:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL
    if abs(yellow.x-box1.x) <= mystery_width and abs(yellow.y-box1.y) <= mystery_height:
        a, b = random.randrange(0, 860), random.randrange(40, 460)
        box1.x = a
        box1.y = b
        pygame.event.post(pygame.event.Event(YELLOW_HEART))
        HEAL_SOUND.play()
    if abs(yellow.x-box2.x) <= mystery_width and abs(yellow.y-box2.y) <= mystery_height:
        a, b = random.randrange(0, 860), random.randrange(40, 460)
        box2.x = a
        box2.y = b
        pygame.event.post(pygame.event.Event(RED_HEART))
        loss_SOUND.play()


# Red Controls ->  arrow keys to move
def red_handle_movement(keys_pressed, red, box1, box2):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL
    if abs(red.x - box1.x) <= mystery_width and abs(red.y-box1.y) <= mystery_height:
        a, b = random.randrange(0, 860), random.randrange(40, 460)
        box1.x = a
        box1.y = b
        pygame.event.post(pygame.event.Event(YELLOW_HEART))
        loss_SOUND.play()
    if abs(red.x - box2.x) <= mystery_width and abs(red.y-box2.y) <= mystery_height:
        a, b = random.randrange(0, 860), random.randrange(40, 460)
        box2.x = a
        box2.y = b
        pygame.event.post(pygame.event.Event(RED_HEART))
        HEAL_SOUND.play()


def y_handle_bullets(yellow_bullets, red, BULLET_VEL_Y):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL_Y
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH or bullet.x < 0:
            yellow_bullets.remove(bullet)


def ny_handle_bullets(n_yellow_bullets, red, BULLET_VEL_Y):
    for bullet in n_yellow_bullets:
        bullet.x += BULLET_VEL_Y
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            n_yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH or bullet.x < 0:
            n_yellow_bullets.remove(bullet)


def r_handle_bullets(red_bullets, yellow, BULLET_VEL_R):
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL_R
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0 or bullet.x > WIDTH:
            red_bullets.remove(bullet)


def nr_handle_bullets(n_red_bullets, yellow, BULLET_VEL_R):
    for bullet in n_red_bullets:
        bullet.x -= BULLET_VEL_R
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            n_red_bullets.remove(bullet)
        elif bullet.x < 0 or bullet.x > WIDTH:
            n_red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    R_MAX_BULLETS = 50
    Y_MAX_BULLETS = 50
    max_time = 41
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    box1 = pygame.Rect(800, 100, mystery_width, mystery_height)
    box2 = pygame.Rect(5, 100, mystery_width+20, mystery_height+20)
    WIN.blit(mystery_box2, (5, 100))
    WIN.blit(mystery_box1, (800, 100))
    pygame.display.update()
    red_bullets = []
    yellow_bullets = []
    n_red_bullets = []
    n_yellow_bullets = []

    red_health = 20
    yellow_health = 20

    clock = pygame.time.Clock()
    run = True
    BULLET_VEL_R = 20
    BULLET_VEL_Y = 20
    while True:
        game_start()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            break
    t2 = time.time()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < Y_MAX_BULLETS: # left control to fire in +ve direction for yellow
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    Y_MAX_BULLETS -= 1
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_q and len(yellow_bullets) < Y_MAX_BULLETS: # q to fire in -ve direction for yellow
                    bullet = pygame.Rect(
                        yellow.x + yellow.width-10, yellow.y + yellow.height//2 - 2, 10, 5)
                    n_yellow_bullets.append(bullet)
                    Y_MAX_BULLETS -= 1
                    BULLET_FIRE_SOUND.play()

                if (event.key == pygame.K_RCTRL or event.key == pygame.K_RETURN) and len(red_bullets) < R_MAX_BULLETS: # red fires in -ve direction on right control(Windows users) or return(Mac OS users)
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    R_MAX_BULLETS -= 1
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_p and len(red_bullets) < R_MAX_BULLETS: # red fires in -ve directon when p pressed
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    n_red_bullets.append(bullet)
                    R_MAX_BULLETS -= 1
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HEART:
                red_health += 1
            if event.type == YELLOW_HEART:
                yellow_health += 1

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, box1, box2)
        ny_handle_bullets(n_yellow_bullets, red, -BULLET_VEL_Y)
        nr_handle_bullets(n_red_bullets, yellow, -BULLET_VEL_R)
        y_handle_bullets(yellow_bullets, red, BULLET_VEL_Y)
        r_handle_bullets(red_bullets, yellow, BULLET_VEL_R)
        red_handle_movement(keys_pressed, red, box1, box2)
        t1 = time.time()
        draw_window(red, yellow, red_bullets, yellow_bullets, n_red_bullets, n_yellow_bullets,
                    red_health, yellow_health, Y_MAX_BULLETS, R_MAX_BULLETS, box1, box2, int(max_time-(t1-t2)))
        winner_text = ""
        if (red_health == yellow_health and red_bullets == yellow_bullets == 0):
            winner_text = "DRAW!!!!"
        elif red_health <= 0:
            winner_text = "Yellow Wins!"

        elif yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        if int(max_time-(t1-t2)) == 0:
            if (red_health < yellow_health):
                winner_text = "Yellow wins!"
            elif (yellow_health < red_health):
                winner_text = "Red wins!"
            else:
                winner_text = "Draw!!!"
            draw_winner(winner_text)
            break
    main()


if __name__ == "__main__":
    main()
