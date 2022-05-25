import pygame
from pygame.locals import *
import sys

FPS = 32
src_width = 800
src_height = 600
display_screen_window = pygame.display.set_mode((src_width, src_height))
start_background_image = 'images/start/background.png'
game_images = {}


def start_window():
    display_screen_window.blit(game_images['start_background'], (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('TrzmielIT')
    game_images['start_background'] = pygame.image.load(start_background_image).convert()

    while True:
        start_window()
