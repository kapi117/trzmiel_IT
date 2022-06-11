from typing import Tuple

import pygame
from pygame.locals import *
import sys
import random

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
    sounds_on : bool
        True jeśli mają być dźwięki, w innym przypadku False
    click : bool
        True tylko raz przy naciśnięciu przycisku potem False
    open_settings : bool
        True jeśli ma być otwrte okno, w innym przypadku False
    start_disappear : bool
        True jeśli ma zaniknąć okno startowe
    pointget_acc : int
        służy do wywoływania funkcji pointget, domyślnie powinna zostać przeniesiona jako zmienna okna 1_player_mode
        lub jakkolwiek będzie się nazywać
"""
FPS = 60
src_width = 800
src_height = 600
display_screen_window = pygame.display.set_mode((src_width, src_height))
music_on = True
sounds_on = True
click = False
open_settings = False
open_results = False
start_disappear = False
one_player_mode = False
SCORE = 0
pointget_acc = 0
inactive_bool = False
game_highscores_file = open(r"data/highscores.txt", 'r+')
HIGHSCORE = None
gap = 147

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
    game_obstacle_image : string
        Adres obrazku przeszkody
    start_music : string
        Adres dźwięku melodii startowej
    start_click_sound : string
        Adres dźwięku kliknięcia przycisku
    on_hover_sound : string
        Adres dźwięku
"""
start_background_image = 'images/start/background.png'
start_title_image = 'images/start/title.png'
start_button_1_player_image = 'images/start/Przycisk single.png'
start_button_2_player_image = 'images/start/Przycisk multi.png'
start_button_settings_image = 'images/settings/settings_icon.png'
game_obstacle_image = 'images/game/rura.png'
start_inactive_button_image = 'images/start/inactive_button.png'
counter_background = 'images/counter_background.png'

icon_image = 'images/start/icon.png'
trzmiel_images = [f'images/start/Trzmiel{x}.png' for x in range(1, 5)]
number_table = [f'images/numbers/number_{x}.png' for x in range(10)]
start_music = 'audio/theme_music.mp3'
start_click_sound = 'sounds/click.wav'
on_hover_sound = 'sounds/on_hover.wav'
jumping_sound = 'sounds/jump.wav'
hit_sound = 'sounds/hit.wav'
point_get_sound = 'sounds/pointget.wav'

settings_background_image = 'images/settings/settings.background.png'
settings_title_image = 'images/settings/settings.title.png'
settings_button_pressed_image = 'images/settings/Nacisniety przycisk.png'
settings_button_not_pressed_image = 'images/settings/przycisk.png'
settings_speaker_image = 'images/settings/speaker.png'
settings_note_image = 'images/settings/note.png'

results_background_image = 'images/results/background_with_text.png'
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
counter_hundreds_position = (48, 50)
counter_tens_position = (85, 50)
counter_ones_position = (124, 50)
counter_background_positions = (10, 10)
results_background_position = (208, 108)
highscore_hundreds_position = (362, 315)
highscore_tens_position = (397, 315)
highscore_ones_position = (432, 315)
score_hundreds_position = (362, 225)
score_tens_position = (397, 225)
score_ones_position = (432, 225)

"""
    Rozmiary obrazków : Tuple[int, int]
    -----------------
"""
start_button_settings_size = (50, 50)
trzmiel_size = (60, 56)
icon_size = (64, 32)
settings_title_size = (305, 45)
settings_button_pressed_size = (100, 100)
settings_button_not_pressed_size = (100, 100)
settings_speaker_size = (100, 100)
settings_note_size = (100, 100)
inactive_button_size = (260, 120)
number_size = (30, 38)
counter_background_size = (150, 85)

"""
    Nr kanałów dla poszczególnych dźwięków
"""
start_music_channel = 0
start_click_sound_channel = 1
jumping_sound_channel = 2
point_get_sound_channel = 3

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

    def __init__(self, image, center, clicked=False):
        """
        :function: __init__(self, image, center)
        :param image: Obrazek do wyświetlania jako przycisk
        :type image: image.pyi
        :param center: Współrzędne środka
        :type center: Tuple[int, int]
        :param clicked: Początkowe wciśnięcie przycisku
        :type clicked: bool
        :ivar self.original_center: Początkowy środek obiektu
        :type self.original_center: Tuple[int, int]
        :ivar self.on_screen: True jeśli obiekt ma być na ekranie
        :type self.on_screen: bool
        :ivar self.disappeared: True jeśli obiekt osiągnął pożądaną pozycję opuszczenia ekranu
        :type self.disappeared: bool
        :ivar self.place_to_move: Miejsce do którego ma się przesunąć środek obiektu znikając z ekranu
        :type self.place_to_move: Tuple[int, int]
        :ivar self.disappear_speed: Prędkość chowania się elementu
        :type self.disappear_speed: int
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
        self.original_center = center
        self.on_screen = True
        self.disappeared = False
        self.place_to_move = center
        self.disappear_speed = 10

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
        """
        :function set_on_click: Funkcja przypisująca funkcję do uruchomienia przy naciśnięciu przycisku
        :param func: Funkcja która ma być zwracana przy kliknięciu na przycisk
        """
        self.on_click = func

    def set_image_clicked(self, image):
        """
        :function set_image_clicked: Funkcja przypisująca zdjęcie do pokazania przy naciśnięciu przycisku
        :param image: Zdjęcie które ma być wyświetlane po naciśnięciu przycisku
        """
        self.image_clicked = image

    def toggle_clicked(self):
        """
        :function toggle_clicked: Funkcja zmieniająca wartość self.clicked na przeciwną
        """
        self.clicked = not self.clicked

    def update(self):
        """
        :function update: Funkcja dziedziczona po pygame.sprite.Sprite, wywoływana co tyknięcie zegara
        """
        if self.on_screen:
            if check_if_clicked(pygame.mouse.get_pos(), self.pos):
                """ Jeśli najechany to powiększ i wydaj dźwięk (jeśli nie został zagrany wcześniej) """
                if not self.played:
                    pygame.mixer.Channel(start_click_sound_channel).play(game_sounds["on_hover_sound"])
                    self.played = True
                self.enlarge()
                if click and self.on_click:
                    self.on_click()
                    self.toggle_clicked()
            else:
                """ W przeciwnym razie oryginalny obrazek i nie zagrano jeszcze dźwięku """
                self.reset_image()
                self.played = False
        else:
            """ jeśli nie ma być na ekranie """
            self.disappeared = move_sprite_to([self], self.place_to_move, self.disappear_speed)


def swipe_out(sprites):
    """
    Funkcja ustawiająca on_screen na False oraz obliczająca pożądane miejsce wysunięcia (do najbliższej krawędzi)
    :param sprites: Lista Sprite do wysunięcia
    """
    for sprite in sprites:
        sprite.on_screen = False
        """ do której krawędzi najbliżej """
        closest_border = min(sprite.rect.centerx, src_width - sprite.rect.centerx, sprite.rect.centery,
                             src_height - sprite.rect.centery)
        if closest_border == sprite.rect.centerx:
            """ najbliżej w lewo """
            sprite.place_to_move = (-sprite.image.get_width(), sprite.rect.centery)
        elif closest_border == src_width - sprite.rect.centerx:
            """ najbliżej w prawo"""
            sprite.place_to_move = (src_width + sprite.image.get_width(), sprite.rect.centery)
        elif closest_border == sprite.rect.centery:
            """ najbliżej w górę """
            sprite.place_to_move = (sprite.rect.centerx, -sprite.image.get_height())
        else:
            """ najbliżej w dół """
            sprite.place_to_move = (sprite.rect.centerx, src_height + sprite.image.get_height())


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
    """
    :function toggle_settings_window: Funkcja zmieniająca stan zmiennej open_settings
    """
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
    """
    :function settings_window: Funkcja rysująca na ekranie okienko ustawień
    :return:
    """
    display_screen_window.blit(game_images['settings_background'], settings_window_position)
    display_screen_window.blit(game_images['settings_title'], settings_title_position)
    display_screen_window.blit(game_images['settings_speaker'], settings_speaker_position)
    display_screen_window.blit(game_images['settings_note'], settings_note_position)


def results_window():
    display_screen_window.blit(game_images['results_background'], results_background_position)
    HIGHSCORE.update(SCORE)
    show_number(highscore_ones_position, highscore_tens_position, highscore_hundreds_position, HIGHSCORE.read()[0])
    show_number(score_ones_position, score_tens_position, score_hundreds_position, SCORE)


class Numbers(pygame.sprite.Sprite):
    """
        :class Numbers: Klasa pochodna od klasy Sprite odpowiedzialna za utworzenie spriteów cyfr.
            :ivar self.number: Wyświetlana cyfra
            :type self.number: int
            :ivar self.images: Lista grafik numerów
            :type self.images: List[image.pyi]
            :ivar self.image: Aktualna grafika cyfry
            :type self.image: image.pyi
            :ivar self.rect: Prostokąt do wyświetlania cyfry
            :type self.rect: pygame.Surface

    """

    def __init__(self, center, images):
        super().__init__()
        self.number = 0
        self.images = images
        self.image = images[self.number]
        self.rect = self.image.get_rect(center=center)
        self.center = center


class ScoreCounterONES(Numbers):
    """
        :class ScoreCounterONES: Klasa pochodna od klasy Numbers,
        odpowiadzialna za wyświetlanie cyfr jedności wyniku.
    """

    def __init__(self, center, images):
        super().__init__(center, images)

    def update(self, score):
        """
            :function update: Funkcja dziedziczona po pygame.sprite.Sprite, wywoływana co tyknięcie zegara,
            odpowiedzialna za wydobywanie cyfry jedności ze zmiennej SCORE
        """
        if score < 10:
            self.rect = self.image.get_rect(center=(self.center[0] - 38, self.center[1]))
        if 10 <= score < 100:
            self.rect = self.image.get_rect(center=(self.center[0] - 19, self.center[1]))
        if 100 <= score < 1000:
            self.rect = self.image.get_rect(center=self.center)
        self.number = score % 10
        self.image = self.images[self.number]
        self.rect = self.image.get_rect(center=self.rect.center)


class ScoreCounterTENS(Numbers):
    """
        :class ScoreCounterTENS: Klasa pochodna od klasy Numbers,
        odpowiadzialna za wyświetlanie cyfr dziesiątek wyniku.
    """

    def __init__(self, center, images):
        super().__init__(center, images)

    def update(self, score):
        """
            :function update: Funkcja dziedziczona po pygame.sprite.Sprite, wywoływana co tyknięcie zegara,
            odpowiedzialna za wydobywanie cyfry dziesiątek ze zmiennej SCORE
        """
        if 10 <= score < 100:
            self.rect = self.image.get_rect(center=(self.center[0] - 19, self.center[1]))
            ones = score % 10
            self.number = int((score - ones) / 10)
            self.image = self.images[self.number]
            self.rect = self.image.get_rect(center=self.rect.center)
        if 100 <= score < 1000:
            self.rect = self.image.get_rect(center=self.center)
            ones = score % 10
            self.number = int(((score - ones) % 100) / 10)
            self.image = self.images[self.number]
            self.rect = self.image.get_rect(center=self.rect.center)


class ScoreCounterHUNDREDS(Numbers):
    """
        :class ScoreCounterHUNDREDS: Klasa pochodna od klasy Numbers,
        odpowiadzialna za wyświetlanie cyfr setek wyniku.
    """

    def __init__(self, center, images):
        super().__init__(center, images)

    def update(self, score):
        """
            :function update: Funkcja dziedziczona po pygame.sprite.Sprite, wywoływana co tyknięcie zegara,
            odpowiedzialna za wydobywanie cyfry setek ze zmiennej SCORE
        """
        if 100 <= score < 1000:
            ones = score % 10
            tens = int(((score - ones) % 100) / 10)
            self.number = int((score - ((tens * 10) + ones)) / 100)
            self.image = self.images[self.number]
            self.rect = self.image.get_rect(center=self.rect.center)


class TrzmielSprite(pygame.sprite.Sprite):
    """
        :class TrzmielSprite: Klasa odpowiedzialna za utworzenie i animacje trzmiela.
            :ivar self.original_images: Oryginalne obrazki przekazane przy wywołaniu
            :type self.original_images: List[image.pyi]
            :ivar self.image: Aktualny obrazek
            :type self.image: image.pyi
            :ivar self.rect: Prostokąt do wyświetlania obrazka
            :type self.rect: pygame.Surface
            :ivar self.mode: Kierunek zmiany wielkości (powiększanie[+] , zmniejszanie [-])
            :type self.mode: int
            :ivar self.grow: Parametr unoszenia co klatkę
            :type self.grow: int
            :ivar self.y_move: odległość uniesienia
            :type self.y_move: int
            :ivar self.y_velocity: prędkość w pionie
            :type self.y_velocity: int
        """

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
        self.y_velocity = 0
        self.if_jumped = False
        self.rotation = 0
        self.collision = False
        self.stop = False

    def gravitation_pull(self):
        """
        function gravitational_pull: funckja odpowiedzialna za grawitację - ściąganie trzmiela w dół
        """
        self.y_velocity += 1.5

    def change_image(self):
        """
        :function change_image: Funkcja zmieniająca obrazek na następny w liście, dodatkowo obracająca go
        """
        if not self.stop:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.image = pygame.transform.rotate(self.images[self.current_index], self.rotation)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, keys, move=False):
        """
            Funkcja wywoływana co tick zegara, ruch trzmiela góra dół (po osiągnięciu odpowiedniej szybkości zwalniamy)
            oraz możłiwość skoku trzmiela jeśli został odpalony tryb jednoosobowy,
            o zadaną wartość jeśli minęły 3 klatki od ostatniego skoku
        """
        self.change_image()
        if not move:
            if self.collision:
                if self.rect.centery < src_height - self.image.get_height() / 3:
                    """ animacja kolizji """
                    self.rotation += 10
                    self.gravitation_pull()
                    center = self.rect.center
                    self.rect = self.image.get_rect(center=(center[0], center[1] + self.y_velocity))
                else:
                    self.stop = True
                    global open_results
                    open_results = True
            else:
                """ animacja latania góra dół na oknie startowym i w oczekiwaniu na start """
                if self.grow > self.y_move:
                    self.mode = -1
                if self.grow < -self.y_move:
                    self.mode = 1
                    """ ^^^ sprawdzanie czy powiększenie osiągneło skalowana wartość """
                self.grow += 1 * self.mode
                center = self.rect.center
                self.rect = self.image.get_rect(center=(center[0], center[1] + self.grow))
        else:
            """ sprawdzenie czy nastąpił skok """
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not self.if_jumped:
                self.y_velocity = 0
                self.y_velocity -= 15
                pygame.mixer.Channel(jumping_sound_channel).play(game_sounds["jumping_sound"])
                pygame.mixer.Channel(jumping_sound_channel).set_volume(0.2)
                self.if_jumped = True
            elif not (keys[pygame.K_SPACE] or keys[pygame.K_UP]):
                self.if_jumped = False
            self.gravitation_pull()
            center = self.rect.center
            self.rect = self.image.get_rect(center=(center[0], center[1] + self.y_velocity))


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
        :ivar self.original_center: Początkowy środek obiektu
        :type self.original_center: Tuple[int, int]
        :ivar self.on_screen: True jeśli obiekt ma być na ekranie
        :type self.on_screen: bool
        :ivar self.disappeared: True jeśli obiekt osiągnął pożądaną pozycję opuszczenia ekranu
        :type self.disappeared: bool
        :ivar self.place_to_move: Miejsce do którego ma się przesunąć środek obiektu znikając z ekranu
        :type self.place_to_move: Tuple[int, int]
        :ivar self.disappear_speed: Prędkość chowania się elementu
        :type self.disappear_speed: int
    """

    def __init__(self, center, image, scale):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.mode = 1
        self.grow = 0
        self.scale = scale
        self.original_center = center
        self.on_screen = True
        self.disappeared = False
        self.place_to_move = center
        self.disappear_speed = 10

    def update(self):
        """ Function update: Funkcja odpowiedzzialna za powiększanie lub zmneijszanie obrazku co skok zegara """
        if self.on_screen:
            """ jeśli ma być na ekranie """
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
        else:
            """ jeśli nie ma być na ekranie """
            self.disappeared = move_sprite_to([self], self.place_to_move, self.disappear_speed)


def move_sprite_to(sprite, destination, speed):
    """
    :function move_sprite_to: Funkcja przesuwająca stopniowo Sprite do miejsca docelowego
    :param sprite: Obiekt do przesuwania
    :param destination: Miejsce docelowe
    :param speed: Prędkość (dotyczy mniejszej wartości)
    :return: True jeśli jest już na miejscu
    """

    """ Pobierz środek i oblicz odległości do pokonania """
    center = sprite[0].rect.center
    to_travel = (destination[0] - center[0], destination[1] - center[1])
    if to_travel != (0, 0):
        """ Jeśli nie jest na odpowiednim miejscu to przesun w odpowiedni sposob"""
        if to_travel[0] == 0:
            if speed < abs(to_travel[1]):
                movement = [0, speed * to_travel[1] / abs(to_travel[1])]
            else:
                movement = to_travel
        elif to_travel[1] == 0:
            if speed < abs(to_travel[0]):
                movement = [speed * to_travel[0] / abs(to_travel[0]), 0]
            else:
                movement = to_travel
        else:
            closer = min(to_travel)
            speed_x = (speed if speed < abs(to_travel[0]) else to_travel[0])
            speed_y = (speed if speed < abs(to_travel[1]) else to_travel[1])
            movement = [speed_x * to_travel[0] / abs(closer), speed_y * to_travel[1] / abs(closer)]
        """ Przypisz środek po przesunięciu """
        sprite[0].rect = sprite[0].image.get_rect(center=(center[0] + movement[0], center[1] + movement[1]))
        return False
    else:
        return True


# TODO : MARCELI SKOMENTUJ


def show_number(ones_position, tens_position, hundreds_position, score):
    """ Utworzenie liczników """
    ones = ScoreCounterONES(ones_position, game_images['numbers'])
    tens = ScoreCounterTENS(tens_position, game_images['numbers'])
    hundreds = ScoreCounterHUNDREDS(hundreds_position, game_images['numbers'])
    group_ones = pygame.sprite.Group(ones)
    group_tens = pygame.sprite.Group(tens)
    group_hundreds = pygame.sprite.Group(hundreds)
    if score > 999:
        score = 0
    group_ones.update(score)
    group_ones.draw(display_screen_window)
    if score > 9:
        group_tens.update(score)
        group_tens.draw(display_screen_window)
    if score > 99:
        group_hundreds.update(score)
        group_hundreds.draw(display_screen_window)


def start_1_player_mode(**info):
    """
    :function start_1_player_mode:
    :param info: Słownik argumentów potrzebnych przy rozpoczynaniu gry jednoosobowej
        'acc' : wartość acc animacji tła
        'main_screeen_motion' : wartość przesunięcia tła
        'trzmiel' : TrzmielSprite
    :return:
    """

    """ to się tyczy przygotowania (zanikanie okna startowego) """
    global start_disappear
    start_disappear = True
    if one_player_mode:
        """ Tu już się zaczyna konkretny kod dla gry jednoosobowej"""

        """ Poniżej tworze 4 obiekty klasy obstacle, odległe od siebie o 400 px pojawiające się za ekranem
        obiekty te są dodawane do grupy także można je wszystkie wywoływać i wpływać na nie za pomocą pojedynczych poleceń
        """
        obstacle_group = pygame.sprite.Group()
        for obst in range(3):
            new_obst = Obstacle([1000 + obst * 400, random.randrange(80, 520)], "images/game/rura.png")
            obstacle_group.add(new_obst)

        """ move_trzmiel przybiera wartość True kiedy ma zacząć się ruszać """
        move_trzmiel = False
        """ start_game przybiera wartość True gdy rozpoczęto grę"""
        start_game = False
        """Wielkość szczeliny"""
        gap = 147
        """ grupa trzmiela """
        trzmiel_group = pygame.sprite.Group(info['trzmiel'])
        while True:
            global SCORE, click
            """ naciśnięte klawisze """
            keys = pygame.key.get_pressed()
            if not move_trzmiel and not info['trzmiel'].collision and (keys[K_SPACE] or keys[K_UP]):
                """ rozpocznij ruch trzmiela po naciśnięciu spacji """
                move_trzmiel = True
                start_game = True
            click = False
            for event in pygame.event.get():
                """ sprawdzanie czy nie użytkownik nie chce wyjść lub czy nie nacisnął myszki """
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    click = True
            """ Animacja tła oraz umiejscowienie tytułu """
            info['acc'] += time_clock.tick(FPS)
            while info['acc'] >= 1:
                info['acc'] -= 1
                if not info['trzmiel'].collision:
                    info['main_screen_motion'] += 0.1
                    if info['main_screen_motion'] >= 3202.0:
                        info['main_screen_motion'] = 0
                display_screen_window.blit(game_images['start_background'], (-info['main_screen_motion'], 0))
            """ Rysowanie rur """
            if start_game:
                obstacle_group.draw(display_screen_window)
            if move_trzmiel:
                obstacle_group.update()
                """sprawdzanie czy gracz zdobył punkt"""
                for el in obstacle_group:
                    pointget(el, info['trzmiel'])
            """ Trzmiel """
            trzmiel_group.update(keys, move_trzmiel)
            trzmiel_group.draw(display_screen_window)
            """ sprawdzanie wyniku oraz odpowienie wyświetlanie """
            display_screen_window.blit(game_images['counter_background'], counter_background_positions)
            show_number(counter_ones_position, counter_tens_position, counter_hundreds_position, SCORE)

            if open_results:
                results_window()

            """Kolizja"""
            obstacle = pygame.sprite.spritecollideany(info['trzmiel'], obstacle_group, check_collision)
            if obstacle:
                move_trzmiel = False
                info['trzmiel'].collision = True

            """ Uaktualnienie widoku """
            pygame.display.flip()
            time_clock.tick(FPS)


def check_collision(trzmiel, obstacle):
    obstacle_borders = (
        obstacle.rect.centerx - obstacle.image.get_width() / 2, obstacle.rect.centerx + obstacle.image.get_width() / 2)
    return obstacle_borders[0] < trzmiel.rect.centerx + trzmiel.image.get_width() / 2 < obstacle_borders[1] and abs(
        trzmiel.rect.center[1] - obstacle.rect.center[1]) > gap / 2 + trzmiel_size[1] / 2


class Obstacle(pygame.sprite.Sprite):
    """Klasa odpowiedzialna za pojawianie się na ekranie i animację przeszkody
        oprócz tego pojawia niewidzialny próg na środku przeszkody, którego przekroczenie ma powodować zdobycie punktu
        (zaimplementowane w funkcji pointget)"""

    def __init__(self, pos, picture_path):
        super().__init__()
        self.pos = pos
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (100, 1150))
        self.rect = self.image.get_rect(center=self.pos)
        """threshold to rectangle służący do sprawdzania czy gracz zdobył punkt
        po wyśrodkowaniu grafiki poniżej wartość (self.pos[0],self.pos[1]-53) nalezy zastąpić
        poprostu self.pos i analogicznie w update center"""
        self.threshold = pygame.Rect(self.pos, (1, self.image.get_height())).move(0, -self.image.get_height() / 2)

    """funkcja update powoduje pomniejszenie położenia x przeszkody o 5 pikseli zgodnie z zegarem"""

    def update(self):
        center = self.rect.center
        self.rect = self.image.get_rect(center=(center[0] - 5, center[1]))
        self.threshold = pygame.Rect(center, (1, self.image.get_height())).move(0, -self.image.get_height() / 2)
        """poniższy if zapewnia przenoszenie przeszkód spowrotem na początek po osiągnięciu odległości -200 x"""
        if center[0] == -200:
            """ reset położenia x-owego przeszkody musi sie odbywać za pomocą wartości liczbowej, ponieważ przywrócenie
             oryginalnej wartości powoduje konflikty ze sposobem tworzenia grupy obiektów"""
            self.rect = self.image.get_rect(center=(1000, random.randrange(80, 520)))


"""
    funkcja pointget przyjmuje:
     obst : Obstacle - przeszkoda, w której znajduje sie pole threshold
     trzmiel : TrzmielSprite - grywalny ptak lotny
     SCORE - globalna zmienna przechowująca liczbę puntków gracza
     pointget_acc - akumulator globalny
     
     Okazuje się że trzmiel koliduje z threshold dokładnie 24 razy przy przelocie przez jedną przeszkodę,
     w związku z tym funkcja liczy do 24 za pomocą funkcji pointget, aby następnie powiększyć SCORE o 1
"""


def pointget(obst, trzmiel: TrzmielSprite):
    global SCORE
    global pointget_acc
    if obst.threshold.colliderect(trzmiel):
        pointget_acc += 1
        if pointget_acc >= 12:
            SCORE += 1
            pointget_acc = 0
            pygame.mixer.Channel(point_get_sound_channel).set_volume(0.5)
            pygame.mixer.Channel(point_get_sound_channel).play(game_sounds["point_get_sound"])


"""Klasa umożliwiająca zapisywanie i wyświetlanie 10 najlepszych wyników"""


class HighscoresList:
    """
    :class Highscores_list: Klasa nadpisująca i wyświetlająca 10 najlepszych wyników
    :ivar self.best_ten: Lista przechowująca 10 najlepszych wyników
    :type self.best_ten: List[integer]
    """

    def __init__(self, game_highscores):
        self.best_ten = []
        self.game_highscores = game_highscores
        for i, line in enumerate(game_highscores):
            if i in range(10):
                if line != 0:
                    self.best_ten.append(int(line.strip()))
            elif i > 9:
                break

    def update(self, new_score):
        """
        :function update: Sprawdza czy nowy wynik nie jest wyższy od któregoś z najlepszych i jeśli tak to go wpisuje
        :param new_score: Nowy osiągnięty wynik
        :type new_score: integer
        """
        if not self.best_ten:
            self.best_ten.append(new_score)
        else:
            for i, elem in enumerate(self.best_ten):
                if new_score > elem:
                    lower_scores = [x for x in self.best_ten[i:8]]
                    self.best_ten[i] = new_score
                    self.best_ten += lower_scores
                    print(self.best_ten)

    def read(self):
        """
        :function read: Odczyt 10 najlepszych wyników
        """
        return self.best_ten

    def reset(self):
        """
        :function reset: Wymazanie zawartości pliku z wynikami
        """
        self.game_highscores.truncate(0)


def inactive():
    global inactive_bool
    inactive_bool = True


def start_window():
    """
    :function start_window: Funkcja odpowiedzialna za działanie okna startowego
    all_sprites : List[pygame.sprite.Sprite]
        Tablica przechowywująca wszystkie interaktywne elementy ekranu startowego które mają zniknąć
    button_* : ButtonSprite
        Zmienne przechowujące przyciski jako obiekty ButtonSprite (domyślnie powiększające się przy najechaniu)
    buttons_* : pygame.sprite.Group
        Grupa przycisków w celu łatwego wywołanie update() na wszystkich
    """
    all_sprites = []
    button_1_player = ButtonSprite(game_images['start_button_1_player'], start_button_1_player_position)
    button_2_player = ButtonSprite(game_images['start_button_2_player'], start_button_2_player_position)
    button_settings = ButtonSprite(game_images['start_button_settings'], start_button_settings_position)
    all_sprites.extend([button_1_player, button_2_player, button_settings])
    button_sound = ButtonSprite(game_images['settings_button_not_pressed'], settings_button_position_1, sounds_on)
    button_music = ButtonSprite(game_images['settings_button_not_pressed'], settings_button_position_2, music_on)
    """ Przypisanie reakcji na nacisniecie """
    button_settings.set_on_click(toggle_settings_window)
    button_music.set_image_clicked(game_images['settings_button_pressed'])
    button_sound.set_image_clicked(game_images['settings_button_pressed'])
    button_music.set_on_click(toggle_music)
    button_sound.set_on_click(toggle_sounds)
    button_1_player.set_on_click(start_1_player_mode)

    """ Utworzenie trzmiela """
    trzmiel = TrzmielSprite(start_trzmiel_position, game_images['trzmiel'])
    trzmiel_group = pygame.sprite.Group(trzmiel)

    """ Utworzenie animacji tytułu """
    title_animation = AnimateSprite(animation_title_position,
                                    pygame.image.load(start_title_image), 40)
    all_sprites.append(title_animation)
    buttons = pygame.sprite.Group(button_1_player, button_2_player, title_animation)
    group_button_settings = pygame.sprite.Group(button_settings)
    buttons_settings = pygame.sprite.Group(button_music, button_sound)
    """ Rozpoczęcie grania muzyczki w nieskończonej pętli """
    pygame.mixer.Channel(start_music_channel).play(game_sounds["start_music"], -1)
    pygame.mixer.Channel(start_music_channel).set_volume(0.2)
    """ akumulator wykorzystywany w animacji tła, oraz zmienna wyrażająca szybkość poruszania się tła"""
    acc = 0.0
    main_screen_motion = 1
    """ akumulator wykorzystywany przy wyświetlaniu nieaktywnego przycisku"""
    inactive_acc = 0
    while True:
        """ Dla każdego eventu, jeśli krzyżyk lub ESC to wyjście z gry"""
        global click, start_disappear, SCORE, one_player_mode, inactive_bool
        keys = pygame.key.get_pressed()
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
        trzmiel_group.update(keys)
        trzmiel_group.draw(display_screen_window)
        if start_disappear:
            swipe_out(all_sprites)
            start_disappear = False
        if open_settings:
            """ jeśli okienko ma być otwarte narysuj je i załącz przyciski od ustawień """
            settings_window()
            buttons_settings.update()
            buttons_settings.draw(display_screen_window)
        else:
            buttons.update()

        """ Sprawdzam czy wszystkie obrazki wysunięte """
        end_start = True
        for sprite in all_sprites:
            end_start = end_start and sprite.disappeared
        """ Jeśli wszystkie zniknęły to mamy tryb jednoosobowy """
        if end_start:
            one_player_mode = True
            return acc, main_screen_motion, trzmiel

        """Nieaktywny przycisk"""
        if inactive_bool and inactive_acc < 40:
            display_screen_window.blit(game_images['inactive_button'], pygame.mouse.get_pos())
            inactive_acc += 1
        else:
            inactive_bool = False
            inactive_acc = 0

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
    game_images['inactive_button'] = pygame.transform.scale(
        pygame.image.load(start_inactive_button_image).convert_alpha(), inactive_button_size)
    game_images['trzmiel'] = [
        pygame.transform.smoothscale(pygame.image.load(trzmiel_images[x]).convert_alpha(), trzmiel_size) for x in
        range(4)]
    game_images['icon'] = pygame.transform.smoothscale(pygame.image.load(icon_image).convert_alpha(), icon_size)
    game_images['numbers'] = [
        pygame.transform.smoothscale(pygame.image.load(number_table[x]).convert_alpha(), number_size) for x in
        range(10)]
    game_images['counter_background'] = pygame.transform.scale(
        pygame.image.load(counter_background).convert_alpha(), counter_background_size)
    game_images['results_background'] = pygame.image.load(results_background_image).convert_alpha()

    """ Przypisanie dźwięków do game_sounds na podstawie ich ścieżek """
    game_sounds["start_music"] = pygame.mixer.Sound(start_music)
    game_sounds["click_sound"] = pygame.mixer.Sound(start_click_sound)
    game_sounds["on_hover_sound"] = pygame.mixer.Sound(on_hover_sound)
    game_sounds["jumping_sound"] = pygame.mixer.Sound(jumping_sound)
    game_sounds["point_get_sound"] = pygame.mixer.Sound(point_get_sound)
    game_sounds["hit_sound"] = pygame.mixer.Sound(hit_sound)

    """Wczytanie najwiekszego wyniku z pliku"""
    HIGHSCORE = HighscoresList(game_highscores_file)

    """ Zmiana ikony programu """
    pygame.display.set_icon(game_images['icon'])

    """ Okno startowe """
    acc, main_screen_motion, trzmiel = start_window()

    """ Gra jednoosobowa """
    if one_player_mode:
        start_1_player_mode(acc=acc, main_screen_motion=main_screen_motion, trzmiel=trzmiel)

"""
 :game_highscores: Obiekt typu file odczytujący plik txt z wynikami
"""
