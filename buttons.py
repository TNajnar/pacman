import pygame
from constants import *


class Button:
    def __init__(self, color, height, width, text=''):
        self.color = color
        self.height = height
        self.width = width
        self.text = text

    # toto je metoda která mi vykreslí buttony
    def draw_text(self, screen):
            font = pygame.font.SysFont(TITLE_FONT, TITLE_TEXT_SIZE)
            text = font.render(self.text, True, self.color)
            text_rect = text.get_rect()
            text_rect.center = (self.height, self.width)
            screen.blit(text, text_rect)






