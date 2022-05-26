from typing import Tuple

import pygame
from pygame.locals import *
import sys

FPS = 32
src_width = 800
src_height = 600
display_screen_window = pygame.display.set_mode((src_width, src_height))
start_background_image = 'images/start/background.png'
start_title_image = 'images/start/title.png'
start_button_1_player_image = 'images/start/Przycisk single.png'
start_button_2_player_image = 'images/start/Przycisk multi.png'
start_button_settings_image = 'images/settings/settings_icon.png'

start_title_position = (50, 50)
start_button_1_player_position = (400, 400)
start_button_2_player_position = (400, 500)
start_button_settings_position = (40, 560)
start_button_settings_size = (50, 50)

game_images = {}


class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, image, center):
        super().__init__()
        self.original_image = image
        self.image = image
        self.center = center
        self.rect = self.image.get_rect(center=center)
        self.pos = (self.center[0] - self.image.get_width() / 2,
                    self.center[0] + self.image.get_width() / 2,
                    self.center[1] - self.image.get_height() / 2,
                    self.center[1] + self.image.get_height() / 2)

    def enlarge(self, scale_factor=1.1):
        orig_x, orig_y = self.original_image.get_size()
        size_x = orig_x * scale_factor
        size_y = orig_y * scale_factor
        self.image = pygame.transform.scale(self.original_image, (size_x, size_y))
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_image(self):
        self.image = pygame.transform.scale(self.original_image, self.original_image.get_size())
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if check_if_clicked(pygame.mouse.get_pos(), self.pos):
            self.enlarge()
        else:
            self.reset_image()


def check_if_clicked(mouse_pos: Tuple[int, int], bounds: Tuple[int, int, int, int]) -> bool:
    return bounds[0] <= mouse_pos[0] <= bounds[1] and bounds[2] <= mouse_pos[1] <= bounds[3]


def start_window():
    display_screen_window.blit(game_images['start_title'], start_title_position)
    # display_screen_window.blit(game_images['start_button_1_player'], start_button_1_player_position)
    # display_screen_window.blit(game_images['start_button_2_player'], start_button_2_player_position)
    # display_screen_window.blit(game_images['start_button_settings'], start_button_2_player_position)
    button_1_player = ButtonSprite(game_images['start_button_1_player'], start_button_1_player_position)
    button_2_player = ButtonSprite(game_images['start_button_2_player'], start_button_2_player_position)
    button_settings = ButtonSprite(game_images['start_button_settings'], start_button_settings_position)
    group = pygame.sprite.Group(button_1_player, button_settings, button_2_player)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        group.update()
        display_screen_window.blit(game_images['start_background'], (0, 0))
        display_screen_window.blit(game_images['start_title'], start_title_position)
        group.draw(display_screen_window)
        pygame.display.flip()
        time_clock.tick(FPS)
        '''
        mouse = pygame.mouse.get_pos()
        button_1_player_bounds = (start_button_1_player_position[0],
                                  start_button_1_player_position[0] + game_images['start_button_1_player'].get_width(),
                                  start_button_1_player_position[1],
                                  start_button_1_player_position[1] + game_images['start_button_1_player'].get_height())
        button_2_player_bounds = (start_button_2_player_position[0],
                                  start_button_2_player_position[0] + game_images['start_button_2_player'].get_width(),
                                  start_button_2_player_position[1],
                                  start_button_2_player_position[1] + game_images['start_button_2_player'].get_height())
        button_settings_bounds = (start_button_settings_position[0],
                                  start_button_settings_position[0] + game_images['start_button_settings'].get_width(),
                                  start_button_settings_position[1],
                                  start_button_settings_position[1] + game_images['start_button_settings'].get_height())
                                  '''


if __name__ == "__main__":
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('TrzmielIT')
    game_images['start_background'] = pygame.image.load(start_background_image).convert()
    game_images['start_button_1_player'] = pygame.image.load(start_button_1_player_image).convert_alpha()
    game_images['start_button_2_player'] = pygame.image.load(start_button_2_player_image).convert_alpha()
    game_images['start_title'] = pygame.image.load(start_title_image).convert_alpha()
    game_images['start_button_settings'] = pygame.transform.scale(
        pygame.image.load(start_button_settings_image).convert_alpha(), start_button_settings_size)

    start_window()
