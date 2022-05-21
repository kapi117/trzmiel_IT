import pygame
from pygame.locals import *
import sys

src_width = 400
src_height = 300
display_screen_window = pygame.display.set_mode((src_width, src_height))

def start_window():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
            sys.exit()


if __name__ == "__main__":
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('TrzmielIT')
    while True:
        start_window()
