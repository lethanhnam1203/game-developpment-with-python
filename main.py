from asyncio import Condition
import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ship Game")
WHITE = (255, 255, 255)  # passinto WIN.fill() a 3-element tupple for RGB
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
LIVES_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FRAME_PER_SECOND = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_IS_HIT = pygame.USEREVENT + 1
RED_IS_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)
ROTATED_YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)
ROTATED_RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)
VELOCITY = 5
BULLET_VELOCITY = VELOCITY * 1.5
MAX_BULLETS = 3
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives):
    """_summary_
    """
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_lives_text = LIVES_FONT.render("Lives: " + str(red_lives), 1, WHITE)
    yellow_lives_text = LIVES_FONT.render("Lives: " + str(yellow_lives), 1, WHITE)
    WIN.blit(red_lives_text, (WIDTH - red_lives_text.get_width() - 10, 10))
    WIN.blit(yellow_lives_text, (10, 10))
    WIN.blit(ROTATED_YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(ROTATED_RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def move_yellow(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY >= 0:  # LEFT
        yellow.x -= VELOCITY
    if (
        keys_pressed[pygame.K_d] and yellow.x + yellow.width + VELOCITY <= BORDER.x
    ):  # RIGHTT
        yellow.x += VELOCITY
    if (
        keys_pressed[pygame.K_s] and yellow.y + yellow.height + VELOCITY <= HEIGHT - 15
    ):  # DOWN
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY >= 0:  # UP
        yellow.y -= VELOCITY


def move_red(keys_pressed, red):
    if (
        keys_pressed[pygame.K_LEFT] and red.x - VELOCITY >= BORDER.x + BORDER.width
    ):  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.diwth + VELOCITY <= WIDTH:  # RIGHT
        red.x += VELOCITY
    if (
        keys_pressed[pygame.K_DOWN] and red.y + red.height + VELOCITY <= HEIGHT - 15
    ):  # DOWN
        red.y += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY >= 0:  # UP
        red.y -= VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):  # check for collision
            pygame.event.post(pygame.event.Event(RED_IS_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x >= WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):  # check for collision
            pygame.event.post(pygame.event.Event(YELLOW_IS_HIT))
            red_bullets.remove(bullet)
        elif bullet.x <= 0:
            red_bullets.remove(bullet)


def main():
    """_summary_
    """
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets, yellow_bullets = [], []
    red_lives, yellow_lives = 10, 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FRAME_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width - 5,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_IS_HIT:
                red_lives -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_IS_HIT:
                yellow_lives -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_lives <= 0 and yellow_lives >= 1:
            winner_text = "Congrats! Yellow wins"
        elif yellow_lives <= 0 and red_lives >= 1:
            winner_text = "Congrats! Red wins"
        elif red_lives <= 0 and yellow_lives <= 0:
            winner_text = "Congrats on both of you. Draw!"

        if winner_text != "":
            annouence_winner(winner_text)

        keys_pressed = pygame.key.get_pressed()
        move_yellow(keys_pressed, yellow)
        move_red(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives)

    main()


def annouence_winner(text):
    winner_annoucement_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        winner_annoucement_text,
        (
            WIDTH // 2 - winner_annoucement_text.get_width() / 2,
            HEIGHT - winner_annoucement_text.get_width() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


if __name__ == "__main__":
    main()
