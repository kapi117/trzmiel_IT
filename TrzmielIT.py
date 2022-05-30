from typing import Tuple

import pygame
from pygame.locals import *
import sys

"""
    TrzmielIT
    =========
    Główny plik aplikacji TrzmielIT, służący do obsługi gry oraz wyświetlania okna starowego
"""

"""
    Stałe używane
    -------------
    FPS : int
        Ilośc klatek na sekundę
    src_width : int
        Szerokość ekranu startowego
    src_height : int
        Wysokość ekranu startowego
    display_screen_window : pygame.Surface
        Okno startowe z biblioteki pygame   
    music_on : bool
        True jeśli ma lecieć muzyka, w innym przypadku False
"""
FPS = 32
src_width = 800
src_height = 600
display_screen_window = pygame.display.set_mode((src_width, src_height))
music_on = True
sounds_on = True

"""
    Adresy obrazków i dźwięków
    ---------------
    start_background_image : string
        Adres obrazku tła
    start_title_image : string
        Adres obrazku tytułu
    start_button_1_player_image : string
        Adres obrazku przycisku gry jednoosobowej
    start_button_2_player_image : string
        Adres obrazku przycisku gry dwuosobowej
    start_button_settings_image : string
        Adres obrazku przycisku ustawień
    start_music : string
        Adres dźwięku melodii startowej
    start_click_sound : string
        Adres dźwięku kliknięcia przycisku
"""
start_background_image = 'images/start/background.png'
start_title_image = 'images/start/title.png'
start_button_1_player_image = 'images/start/Przycisk single.png'
start_button_2_player_image = 'images/start/Przycisk multi.png'
start_button_settings_image = 'images/settings/settings_icon.png'
start_music = 'sounds/music.wav'
start_click_sound = 'sounds/click.wav'
on_hover = 'sounds/on_hover.wav'

"""
    Pozycje obrazków
    ----------------
    start_title_position : Tuple [int, int]
        Pozycja (lewy górny róg) napisu tytułowego
    start_button_1_player_position : Tuple [int, int]
        Pozycja (środek) przycisku gry jednoosobowej
    start_button_2_player_position : Tuple [int, int]
        Pozycja (środek) przycisku gry dwuosobowej
    start_button_settings_position : Tuple [int, int]
        Pozycja (środek) przycisku ustawień
"""
start_title_position = (50, 50)
start_button_1_player_position = (400, 400)
start_button_2_player_position = (400, 500)
start_button_settings_position = (40, 560)

"""
    Rozmiary obrazków
    -----------------
    start_button_settings_size : Tuple [int, int]
        Rozmiar przycisku ustawień
"""
start_button_settings_size = (50, 50)

"""
    Nr kanałów dla poszczególnych dźwięków
"""
start_music_channel = 0
start_click_sound_channel = 1

""" game_images : Dict[string, image.pyi]
        Słownik przechowujący obrazki
    game_sounds : Dict[string, image.pyi]
        Słownik przechowujący dźwięki
"""
game_images = {}
game_sounds = {}


class ButtonSprite(pygame.sprite.Sprite):
    """
        :class ButtonSprite: Klasa odpowiedzialna za tworzenie przycisków i ich odpowiednie wyświetlanie.

        :ivar self.original_image: Oryginalny obrazek przekazany przy wywołaniu
        :type self.original_image: image.pyi

        :ivar self.image: Aktualny obrazek
        :type self.image: image.pyi

        :ivar self.center: Współrzędne środka
        :type self.center: Tuple[int, int]

        :ivar self.rect: Prostokąt do wyświetlania przycisku
        :type self.rect: pygame.Surface

        :ivar self.pos: Pozycja krawędzi elementów w formacie (x_min, x_max, y_min, y_max)
                       x_min         x_max
                       \\//          \\//
               y_min -> |-------------|
                        |             |
                        |             |
               y_max -> |-------------|
        :type self.pos: Tuple[int, int, int, int]

    """

    def __init__(self, image, center):
        """
        :function: __init__(self, image, center)
        :param image: Obrazek do wyświetlania jako przycisk
        :type image: image.pyi
        :param center: Współrzędne środka
        :type center: Tuple[int, int]
        """
        super().__init__()
        self.original_image = image
        self.image = image
        self.center = center
        self.rect = self.image.get_rect(center=center)
        """ Obliczenie krawędzie na podstawie środka i rozmiarów obrazka """
        self.pos = (self.center[0] - self.image.get_width() / 2,
                    self.center[0] + self.image.get_width() / 2,
                    self.center[1] - self.image.get_height() / 2,
                    self.center[1] + self.image.get_height() / 2)
        self.played = False

    def enlarge(self, scale_factor=1.1):
        """
        :function enlarge: Zmienia wymiary obecnego przycisku mnożąc je razy scale_factor
        :param scale_factor: Współczynnik zmiany rozmiaru
        :type scale_factor: float
        """
        orig_x, orig_y = self.original_image.get_size()
        """ Wymnażanie oryginalnych rozmiarów razy współczynnik """
        size_x = orig_x * scale_factor
        size_y = orig_y * scale_factor
        """ zmiana rozmiarów """
        self.image = pygame.transform.scale(self.original_image, (size_x, size_y))
        """ odnowienie prostokąta """
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_image(self):
        """
        :function reset_image: Funkcja przywracająca self.original_image jako self.image
        """
        self.image = pygame.transform.scale(self.original_image, self.original_image.get_size())
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """
        :function update: Funkcja dziedziczona po pygame.sprite.Sprite, wywoływana co tyknięcie zegara
        """
        if check_if_clicked(pygame.mouse.get_pos(), self.pos):
            """ Jeśli najechany to powiększ i wydaj dźwięk (jeśli nie został zagrany wcześniej) """
            if not self.played:
                pygame.mixer.Channel(start_click_sound_channel).play(game_sounds["on_hover"])
                self.played = True
            self.enlarge()
        else:
            """ W przeciwnym razie oryginalny obrazek i nie zagrano jeszcze dźwięku """
            self.reset_image()
            self.played = False


def toggle_music():
    """
    :function toggle_music: Funkcja zmieniająca stan zmiennej music_on na przeciwny
    """
    global music_on
    music_on = not music_on
    if music_on:
        """ Jeśli zmieniona muzykę na on to zacznij grać muzykę"""
        pygame.mixer.Channel(start_music_channel).play(game_sounds['start_music'], -1)
    else:
        pygame.mixer.Channel(start_music_channel).stop()


def toggle_sounds():
    """
    :function toggle_sounds: Funkcja zmieniająca stan zmiennej sounds_on na przeciwny
    """
    global sounds_on
    sounds_on = not sounds_on
    if sounds_on:
        pygame.mixer.Channel(start_click_sound_channel).set_volume(1.0)
    else:
        pygame.mixer.Channel(start_click_sound_channel).set_volume(0.0)


def check_if_clicked(mouse_pos: Tuple[int, int], bounds: Tuple[int, int, int, int]) -> bool:
    """
    :function check_if_clicked: Funkcja sprawdzająca czy współrzędne myszki znajdują się w ramach podanych krawędzi
    :param mouse_pos: Współrzędne myszki
    :type mouse_pos: Tuple[int, int]
    :param bounds: Krawędzie obiektu
    :type bounds: Tuple[int, int, int, int]
    :return: True jeśli znajduje się, False w przeciwnym razie
    :rtype: bool
    """
    return bounds[0] <= mouse_pos[0] <= bounds[1] and bounds[2] <= mouse_pos[1] <= bounds[3]


def start_window():
    """
    :function start_window: Funkcja odpowiedzialna za działanie okna startowego

    button_* : ButtonSprite
        Zmienne przechowujące przyciski jako obiekty ButtonSprite (domyślnie powiększające się przy najechaniu)

    group : pygame.sprite.Group
        Grupa przycisków w celu łatwego wywołanie update() na wszystkich

    """
    button_1_player = ButtonSprite(game_images['start_button_1_player'], start_button_1_player_position)
    button_2_player = ButtonSprite(game_images['start_button_2_player'], start_button_2_player_position)
    button_settings = ButtonSprite(game_images['start_button_settings'], start_button_settings_position)
    buttons = pygame.sprite.Group(button_1_player, button_settings, button_2_player)
    """ Rozpoczęcie grania muzyczki w nieskończonej pętli """
    pygame.mixer.Channel(start_music_channel).play(game_sounds["start_music"], -1)
    while True:
        """ Dla każdego eventu, jeśli krzyżyk lub ESC to wyjście z gry"""
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        """ Umiejscowienie tła oraz tytułu """
        display_screen_window.blit(game_images['start_background'], (0, 0))
        display_screen_window.blit(game_images['start_title'], start_title_position)
        """ update() przyciski oraz wyrysowanie ich na ekran """
        buttons.update()
        buttons.draw(display_screen_window)
        """ Uaktualnienie widoku """
        pygame.display.flip()
        time_clock.tick(FPS)


if __name__ == "__main__":
    """ Inicjalizacja gry oraz dźwięków"""
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.init()
    time_clock = pygame.time.Clock()
    """ Napis na okienku """
    pygame.display.set_caption('TrzmielIT')
    """ Przypisanie obrazków do game_images na podstawie ich ścieżek """
    game_images['start_background'] = pygame.image.load(start_background_image).convert()
    game_images['start_button_1_player'] = pygame.image.load(start_button_1_player_image).convert_alpha()
    game_images['start_button_2_player'] = pygame.image.load(start_button_2_player_image).convert_alpha()
    game_images['start_title'] = pygame.image.load(start_title_image).convert_alpha()
    """ Dodatkowo przeskalowanie ikony ustawień """
    game_images['start_button_settings'] = pygame.transform.scale(
        pygame.image.load(start_button_settings_image).convert_alpha(), start_button_settings_size)

    """ Przypisanie dźwięków do game_sounds na podstawie ich ścieżek """
    game_sounds["start_music"] = pygame.mixer.Sound(start_music)
    game_sounds["click_sound"] = pygame.mixer.Sound(start_click_sound)
    game_sounds["on_hover"] = pygame.mixer.Sound(on_hover)

    """ Okno startowe """
    start_window()
