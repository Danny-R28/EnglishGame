# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
from sys import exit
import numpy as np


# קצב עידכון המסך 60 פעמים בשנייה
FRAME_RATE = 60

# גובה המסך
HIGHT = 400
# אורך המסך
WIDTH = 800

# גובה כרטיס
CARD_WIDTH = 30

# רוחב כרטיס
CARD_HIGHT = 50

# צבע של הרקע
# COLOR R, G, B   כחול, ירוק, אדום 0-255
BG_COLOR = 'darkgreen'



class CardView:
    def __init__(self, card, pos = [0,0], color='red', up=True):
        self.rect = pygame.Rect(pos[0], pos[1], CARD_HIGHT, CARD_HIGHT)
        self.card = card
        self.color = color
        self.up = up

    def set_pos(self, pos):
        self.rect.pos = pos

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        text = test_font.render(self., False, 'blue')
        text_rect = score_message.get_rect(center=self.rect.center)
        screen.blit(score_message, score_message_rect)


class Card:
    def __init__(self, face_value, back_value):
        self.face_value = face_value
        self.back_value = back_value


def main(name):
    pygame.init()
    test_font = pygame.font.SysFont('impact', CARD_WIDTH)
    screen = pygame.display.set_mode((WIDTH, HIGHT))

    # כותרת
    pygame.display.set_caption('Learn English / לימוד אנגלית')
    clock = pygame.time.Clock()

    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


    cards = [CardView(Card('name', 'danny'), [int(WIDTH / 2), int(HIGHT / 2)])]

    while True:
        screen.fill(BG_COLOR)


        for card in cards:
            card.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()



        # תעדכן את התמונה על המסך
        pygame.display.update()
        # תחכה שיעעבור זמן לעידכון נוסף
        clock.tick(FRAME_RATE)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('Ben')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
