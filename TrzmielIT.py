import pygame
from pygame.locals import *
import sys

FPS = 32
src_width = 800
src_height = 600
display_screen_window = pygame.display.set_mode((src_width, src_height))
start_background_image = 'images/start/background.png'
start_title_image = 'images/start/title.png'
start_button_1_player_image = 'images/start/button_1_player.png'
start_button_2_player_image = 'images/start/button_2_player.png'
start_button_settings_image = 'images/start/button_settings.png'

start_title_position = (100, 100)
start_button_1_player_position = (400, 400)
start_button_2_player_position = (400, 450)
start_button_settings_position = (50, 600)

game_images = {}


def start_window():
    display_screen_window.blit(game_images['start_background'], (0, 0))
    display_screen_window.blit(game_images['start_title'], start_title_position)
    display_screen_window.blit(game_images['start_button_1_player'], start_button_1_player_position)
    display_screen_window.blit(game_images['start_button_2_player'], start_button_2_player_position)
    display_screen_window.blit(game_images['start_button_settings'], start_button_2_player_position)
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
    game_images['start_button_1_player'] = pygame.image.load(start_button_1_player_image).convert()
    game_images['start_button_2_player'] = pygame.image.load(start_button_2_player_image).convert()
    game_images['start_title'] = pygame.image.load(start_title_image).convert()
    game_images['start_button_settings'] = pygame.image.load(start_button_settings_image).convert()

    start_window()
