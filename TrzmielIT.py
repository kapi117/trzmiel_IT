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
trzmiel_images = [f'images/start/Trzmiel{x}.png' for x in range(1, 5)]
start_music = 'sounds/music.wav'
start_click_sound = 'sounds/click.wav'
on_hover = 'sounds/on_hover.wav'

settings_background_image = 'images/settings/settings.background.png'
settings_title_image = 'images/settings/settings.title.png'
settings_button_pressed_image = 'images/settings/Nacisniety przycisk.png'
settings_button_not_pressed_image = 'images/settings/przycisk.png'
settings_speaker_image = 'images/settings/speaker.png'
settings_note_image = 'images/settings/note.png'
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
animation_title_position = (400, 120)
start_button_1_player_position = (400, 400)
start_button_2_player_position = (400, 500)
start_button_settings_position = (40, 560)
start_trzmiel_position = (150, 280)
settings_window_position = (95, 100)
settings_title_position = (247, 120)
settings_button_position_1 = (500, 250)
settings_button_position_2 = (500, 400)
settings_speaker_position = (250, 200)
settings_note_position = (250, 350)

"""
    Rozmiary obrazków
    -----------------
    start_button_settings_size : Tuple [int, int]
        Rozmiar przycisku ustawień
"""
start_button_settings_size = (50, 50)
trzmiel_size = (120, 60)
settings_title_size = (305, 45)
settings_button_pressed_size = (100, 100)
settings_button_not_pressed_size = (100, 100)
settings_speaker_size = (100, 100)
settings_note_size = (100, 100)

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

click = False
open_settings = False


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

    def __init__(self, image, center, clicked=False):
        """
        :function: __init__(self, image, center)
        :param image: Obrazek do wyświetlania jako przycisk
        :type image: image.pyi
        :param center: Współrzędne środka
        :type center: Tuple[int, int]
        :param clicked: Początkowe wciśnięcie przycisku
        :type clicked: bool
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
        self.on_click = None
        self.image_clicked = None
        self.clicked = clicked

    def enlarge(self, scale_factor=1.1):
        """
        :function enlarge: Zmienia wymiary obecnego przycisku mnożąc je razy scale_factor
        :param scale_factor: Współczynnik zmiany rozmiaru
        :type scale_factor: float
        """
        """ Wybór obrazka na podstawie kliknięcia"""
        image_to_show = self.original_image
        if self.clicked and self.image_clicked:
            image_to_show = self.image_clicked
        orig_x, orig_y = image_to_show.get_size()
        """ Wymnażanie oryginalnych rozmiarów razy współczynnik """
        size_x = orig_x * scale_factor
        size_y = orig_y * scale_factor
        """ zmiana rozmiarów """
        self.image = pygame.transform.scale(image_to_show, (size_x, size_y))
        """ odnowienie prostokąta """
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_image(self):
        """
        :function reset_image: Funkcja przywracająca self.original_image jako self.image
        """
        image_to_show = self.original_image
        if self.clicked and self.image_clicked:
            image_to_show = self.image_clicked
        self.image = pygame.transform.scale(image_to_show, image_to_show.get_size())
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_on_click(self, func):
        self.on_click = func

    def set_image_clicked(self, image):
        self.image_clicked = image

    def toggle_clicked(self):
        self.clicked = not self.clicked

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
            if click and self.on_click:
                self.on_click()
                self.toggle_clicked()
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


def toggle_settings_window():
    global open_settings
    open_settings = not open_settings


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


def settings_window():
    display_screen_window.blit(game_images['settings_background'], settings_window_position)
    display_screen_window.blit(game_images['settings_title'], settings_title_position)
    display_screen_window.blit(game_images['settings_speaker'], settings_speaker_position)
    display_screen_window.blit(game_images['settings_note'], settings_note_position)


class TrzmielSprite(pygame.sprite.Sprite):
    def __init__(self, center, images):
        super().__init__()
        self.original_images = images
        self.images = images
        self.current_index = 0
        self.image = images[self.current_index]
        self.rect = self.image.get_rect(center=center)
        self.grow = 0
        self.mode = 1
        self.y_move = 5

    def change_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self.image = self.images[self.current_index]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.change_image()
        if self.grow > self.y_move:
            self.mode = -1
        if self.grow < -self.y_move:
            self.mode = 1
            """ ^^^ sprawdzanie czy powiększenie osiągneło skalowana wartość """
        self.grow += 1 * self.mode
        center = self.rect.center
        self.rect = self.image.get_rect(center = (center[0], center[1]+self.grow))


class AnimateSprite(pygame.sprite.Sprite):
    """
    :class AnimateSprite: Klasa odpowiedzialna za animacje pulsowania.
        :ivar self.original_image: Oryginalny obrazek przekazany przy wywołaniu
        :type self.original_image: image.pyi
        :ivar self.image: Aktualny obrazek
        :type self.image: image.pyi
        :ivar self.rect: Prostokąt do wyświetlania obrazka
        :type self.rect: pygame.Surface
        :ivar self.mode: Kierunek zmiany wielkości (powiększanie[+] , zmniejszanie [-])
        :type self.image: int
        :ivar self.grow: Parametr zwiększania co klatkę
        :type self.grow: int
        :ivar self.scale: Skala powiększenia
        :type self.scale: int

    """

    def __init__(self, center, image, scale):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.mode = 1
        self.grow = 0
        self.scale = scale

    def update(self):
        """ Function update: Funkcja odpowiedzzialna za powiększanie lub zmneijszanie obrazku co skok zegara """
        if self.grow > self.scale:
            self.mode = -1
        if self.grow < 1:
            self.mode = 1
            """ ^^^ sprawdzanie czy powiększenie osiągneło skalowana wartość """
        self.grow += 1 * self.mode

        orig_x, orig_y = self.original_image.get_size()
        size_x = orig_x + round(self.grow)
        size_y = orig_y + (round(self.grow) * 0.5)
        """ Mechanizm powiększania poprzez dodawanie wartości do rozmiarów obrazka """
        self.image = pygame.transform.scale(self.original_image, (size_x, size_y))
        self.rect = self.image.get_rect(center=self.rect.center)


def start_window():
    """
    :function start_window: Funkcja odpowiedzialna za działanie okna startowego
    button_* : ButtonSprite
        Zmienne przechowujące przyciski jako obiekty ButtonSprite (domyślnie powiększające się przy najechaniu)
    buttons_* : pygame.sprite.Group
        Grupa przycisków w celu łatwego wywołanie update() na wszystkich
    """
    button_1_player = ButtonSprite(game_images['start_button_1_player'], start_button_1_player_position)
    button_2_player = ButtonSprite(game_images['start_button_2_player'], start_button_2_player_position)
    button_settings = ButtonSprite(game_images['start_button_settings'], start_button_settings_position)
    button_settings.set_on_click(toggle_settings_window)
    button_sound = ButtonSprite(game_images['settings_button_not_pressed'], settings_button_position_1, sounds_on)
    button_music = ButtonSprite(game_images['settings_button_not_pressed'], settings_button_position_2, music_on)
    button_music.set_image_clicked(game_images['settings_button_pressed'])
    button_sound.set_image_clicked(game_images['settings_button_pressed'])
    button_music.set_on_click(toggle_music)
    button_sound.set_on_click(toggle_sounds)

    trzmiel = TrzmielSprite(start_trzmiel_position, game_images['trzmiel'])
    trzmiel_group = pygame.sprite.Group(trzmiel)

    title_animation = AnimateSprite(animation_title_position,
                                    pygame.image.load(start_title_image), 40)
    buttons = pygame.sprite.Group(button_1_player, button_2_player, title_animation)
    group_button_settings = pygame.sprite.Group(button_settings)
    buttons_settings = pygame.sprite.Group(button_music, button_sound)
    """ Rozpoczęcie grania muzyczki w nieskończonej pętli """
    pygame.mixer.Channel(start_music_channel).play(game_sounds["start_music"], -1)
    pygame.mixer.Channel(start_music_channel).set_volume(0.2)
    """ akumulator wykorzystywany w animacji tła, oraz zmienna wyrażająca szybkość poruszania się tła"""
    acc = 0.0
    main_screen_motion = 1
    while True:
        """ Dla każdego eventu, jeśli krzyżyk lub ESC to wyjście z gry"""
        global click
        click = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                click = True
        """ Animacja tła oraz umiejscowienie tytułu """
        acc += time_clock.tick(FPS)
        while acc >= 1:
            acc -= 1
            main_screen_motion += 0.1
            if main_screen_motion >= 3202.0:
                main_screen_motion = 0
            display_screen_window.blit(game_images['start_background'], (-main_screen_motion, 0))
        """ update() przyciski oraz wyrysowanie ich na ekran """
        group_button_settings.update()
        group_button_settings.draw(display_screen_window)
        buttons.draw(display_screen_window)
        trzmiel_group.update()
        trzmiel_group.draw(display_screen_window)
        if open_settings:
            settings_window()
            buttons_settings.update()
            buttons_settings.draw(display_screen_window)
        else:
            buttons.update()
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
    game_images['settings_background'] = pygame.image.load(settings_background_image).convert()
    """ Dodatkowo przeskalowanie ikon w ustawieniach """
    game_images['start_button_settings'] = pygame.transform.scale(
        pygame.image.load(start_button_settings_image).convert_alpha(), start_button_settings_size)
    game_images['settings_title'] = pygame.transform.scale(
        pygame.image.load(settings_title_image).convert_alpha(), settings_title_size)
    game_images['settings_button_pressed'] = pygame.transform.scale(
        pygame.image.load(settings_button_pressed_image).convert_alpha(), settings_button_pressed_size)
    game_images['settings_button_not_pressed'] = pygame.transform.scale(
        pygame.image.load(settings_button_not_pressed_image).convert_alpha(), settings_button_not_pressed_size)
    game_images['settings_speaker'] = pygame.transform.scale(
        pygame.image.load(settings_speaker_image).convert_alpha(), settings_speaker_size)
    game_images['settings_note'] = pygame.transform.scale(
        pygame.image.load(settings_note_image).convert_alpha(), settings_note_size)
    game_images['trzmiel'] = [
        pygame.transform.smoothscale(pygame.image.load(trzmiel_images[x]).convert_alpha(), trzmiel_size) for x in
        range(4)]

    """ Przypisanie dźwięków do game_sounds na podstawie ich ścieżek """
    game_sounds["start_music"] = pygame.mixer.Sound(start_music)
    game_sounds["click_sound"] = pygame.mixer.Sound(start_click_sound)
    game_sounds["on_hover"] = pygame.mixer.Sound(on_hover)

    """ Okno startowe """
    start_window()
