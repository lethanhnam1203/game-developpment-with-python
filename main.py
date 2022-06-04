from asyncio import Condition
import pygame
import os
import pandas as pd

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
WHITE = (255, 255, 255)  # passinto WIN.fill() a 3-element tupple for RGB
FRAME_PER_SECOND = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
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


def draw_window(red, yellow):
    """_summary_
    """
    WIN.fill(WHITE)
    WIN.blit(ROTATED_YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(ROTATED_RED_SPACESHIP, (red.x, red.y))
    pygame.display.update()


def move_yellow(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d]:  # RIGHTT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_s]:  # DOWN
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_w]:  # UP
        yellow.y -= VELOCITY


def move_red(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT]:  # RIGHTT
        red.x += VELOCITY
    if keys_pressed[pygame.K_DOWN]:  # DOWN
        red.y += VELOCITY
    if keys_pressed[pygame.K_UP]:  # UP
        red.y -= VELOCITY


def main():
    """_summary_
    """
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FRAME_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        move_yellow(keys_pressed, yellow)
        move_red(keys_pressed, red)
        draw_window(red, yellow)

    pygame.quit()


if __name__ == "__main__":
    main()
