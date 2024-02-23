# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
from sys import exit
import time

import random
import unicodedata

import numpy as np


# קצב עידכון המסך 60 פעמים בשנייה
FRAME_RATE = 60

# גובה המסך
HIGHT = 400
# אורך המסך
WIDTH = 800

# גובה כרטיס
CARD_WIDTH = 60

# רוחב כרטיס
CARD_HIGHT = 50

# צבע של הרקע
# COLOR R, G, B   כחול, ירוק, אדום 0-255
BG_COLOR = 'darkgreen'

COLORS = {
  "red": "אדום",
  "orange": "כתום",
  "yellow": "צהוב",
  "green": "ירוק",
  "blue": "כחול",
  "purple": "סגול",
  "pink": "ורוד",
  "brown": "חום",
  "black": "שחור",
  "white": "לבן",
  "gray": "אפור"
}

JOBS = {
  "doctor": "רופא",
  "teacher": "מורה",
  "engineer": "מהנדס",
  "lawyer": "עורך דין",
  "chef": "שף",
  "artist": "אמן",
  "police officer": "שוטר",
  "firefighter": "כבאי",
  "accountant": "רואה חשבון",
  "mechanic": "מכונאי"
}

ANIMALS = {
  "dog": "כלב",
  "cat": "חתול",
  "horse": "סוס",
  "cow": "פרה",
  "sheep": "כבשה",
  "goat": "עז",
  "pig": "חזיר",
  "chicken": "תרנגול",
  "duck": "ברווז",
  "rabbit": "ארנב"
}

DIRECTIONS = {
  "up": "למעלה",
  "down": "למטה",
  "back": "אחורה",
  "near": "קרוב",
  "far": "רחוק",
  "left": "שמאלה",
  "right": "ימינה",
  "inside": "בפנים",
  "outside": "מחוץ לבית",
  "top": "למעלה",
  "bottom": "למטה",
  "front": "קדימה",
  "behind": "מאחורי"
}

HOUSE = {
  "table": "שולחן",
  "chair": "כיסא",
  "bed": "מיטה",
  "sofa": "ספה",
  "lamp": "מנורה",
  "clock": "שעון",
  "mirror": "מראה",
  "plate": "צלחת",
  "fork": "מזלג",
  "knife": "סכין",
  "spoon": "כף",
  "cup": "כוס",
  "bowl": "קערה",
  "television": "טלוויזיה",
  "computer": "מחשב",
  "telephone": "טלפון",
  "refrigerator": "מקרר",
  "oven": "תנור",
  "microwave": "מיקרוגל",
  "washing machine": "מכונת כביסה",
  "vacuum cleaner": "שואב אבק"
}

class Card:
    def __init__(self, face_value, back_value):
        self.face_value = face_value
        self.back_value = back_value

class CardView:
    def __init__(self, card = None, pos = None, color='lightyellow', up=True):
        self.pos = pos
        self.text_rect = None
        self.card = card
        self.color = color
        self.up = up
        self.flip_back_ts = None
        font_size = CARD_WIDTH // 2
        self.front_font = pygame.font.SysFont('Ariel', font_size)
        self.back_font = pygame.font.Font('..\Assets\Fonts\GveretLevinAlefAlefAlef\GveretLevinAlefAlefAlef\otf\GveretLevinAlefAlefAlef-Regular.otf', font_size)

    def set_pos(self, pos):
        self.pos = pos

    def set_card(self, card: Card, up: bool = False):
        self.card = card
        self.up = up

    def flip(self):
        self.up = not self.up

    def draw(self, screen=None):
        if self.up:
            font = self.front_font
            value = self.card.face_value
        else:
            font = self.back_font
            value = self.card.back_value[::-1]


        text = font.render(value, False, 'black')
        margin = 10
        text_rect = text.get_rect(topleft=(self.pos[0] + margin, self.pos[1] + margin))
        self.text_rect = text_rect.inflate(2*margin, 2*margin)

        if screen:
            pygame.draw.rect(screen, self.color, self.text_rect, border_radius=self.text_rect.height // 4)
            screen.blit(text, text_rect)

class Score:
    def __init__(self, score: int = 0, rect: pygame.Rect = None, msg:str = "{}"):
        self.score = score
        self.rect = rect if rect is not None else pygame.Rect(0, 0, 100, 100)
        self.msg = msg
        self.font = pygame.font.SysFont('Ariel', self.rect.height)
        # self.font = pygame.font.Font(
        #     '..\Assets\Fonts\GveretLevinAlefAlefAlef\GveretLevinAlefAlefAlef\otf\GveretLevinAlefAlefAlef-Regular.otf',
        #     self.rect.height)

    def __iadd__(self, other: int):
        if isinstance(other, Score):
            self.score += other.score
        else:
            self.score += other
        return self

    def __isub__(self, other: int):
        if isinstance(other, Score):
            self.score -= other.score
        else:
            self.score -= other

        return self

    def draw(self, screen):
        text = self.font.render(self.msg.format(self.score), False, 'lightblue')
        text_rect = text.get_rect(topleft=self.rect.topleft)
        #self.text_rect = text_rect.inflate(20, 20)

        screen.blit(text, text_rect)



class Board:
    def __init__(self):
        self._options = []
        self._words = []
        self.set_words([HOUSE, COLORS, ANIMALS, DIRECTIONS, JOBS])
        self.set_words([JOBS])
        self._option = None
        self.clear()
        self._card_views = [CardView(self) for _ in range(4)]
        self._score = Score(0, pygame.Rect(300, 50, 40, 100))
        self._lock = None
        self._callbacks = []

    def set_words(self, list_of_dicts: list[dict]):
        self._words = {}
        for dict in list_of_dicts:
            self._words.update(dict)

    def clear(self):
        self._options = []
        self._option = None

    def set_option(self, card: CardView):
        self._option = card

    def set_options(self, cards: list[Card]):
        self._options = cards

    def lock(self, duration: int = 2):
        self._lock = time.time() + duration

    def locked(self) -> bool:
        if self._lock is None:
            return False

        if time.time() < self._lock:
            return True

        self._lock = None

        return False

    def deal(self):
        random_elements = random.sample(self._words.keys(), 4)
        self._options = [Card(key, self._words[key]) for key in random_elements]
        self._option = self._options[random.randint(0, 3)]

        x = 100
        y = 200

        for i, card in enumerate(self._options):
            self._card_views[i].set_card(card, True)
            self._card_views[i].set_pos((x, y))
            self._card_views[i].draw()
            x += self._card_views[i].text_rect.width + CARD_WIDTH // 5

    def press(self, pos):
        if self.locked():
            return

        for card_view in self._card_views:
            if card_view.text_rect.collidepoint(pos):
                card_view.flip()
                self._callbacks.append((time.time() + 1, card_view.flip))
                self.lock(duration=1)
                if card_view.card == self._option:
                    self._score += 1
                    self._callbacks.append((time.time() + 1, self.deal))
                else:
                    self._score -= 1

    def draw(self, screen):
        pos = None
        for card_view in self._card_views:
            if pos is not None:
                card_view.set_pos(pos)
            card_view.draw(screen)
            pos = card_view.text_rect.topright[0] + 10, card_view.text_rect.topright[1]


        CardView(card=self._option, up=False, pos=(200, 100)).draw(screen)
        self._score.draw(screen)

    def update(self):
        now = time.time()
        callbacks = []
        for (ts, callback) in self._callbacks:
            if now > ts:
                callback()
            else:
                callbacks.append((ts, callback))

        self._callbacks = callbacks


def main(name):
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HIGHT))

    # כותרת
    pygame.display.set_caption('Learn English / לימוד אנגלית')
    clock = pygame.time.Clock()

    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



    #for words in WORDS:

    board = Board()
    board.deal()


    while True:
        screen.fill(BG_COLOR)

        board.update()

        board.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_d:
                    board.deal()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    board.press(pos)



        # תעדכן את התמונה על המסך
        pygame.display.update()
        # תחכה שייעבור זמן לעידכון נוסף
        clock.tick(FRAME_RATE)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('Ben')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
