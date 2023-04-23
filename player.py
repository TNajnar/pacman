import pygame
from constants import *
from app import *

vector = pygame.math.Vector2


class Player:
    def __init__(self, app, pos, color, size):
        self.color = color
        self.size = size
        self.app = app
        self.grid_position = vector(pos[0], pos[1])
        self.index_position = self.get_index_position()
        self.direction = vector(1, 0)
        self.stored_direction = None
        self.speed = 2
        self.able_to_move = True
        self.score = 0
        self.lives = 3

    # hráčův pohyb, rozeznání zdí
    def player_update(self):
        if self.able_to_move:
            self.index_position += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # nastavuji grid pozici která odkazuje na index pozici a centruje enemy ke gridu
        # index pozice hráče, mapovač, pohyb po ose x[0], y[1], nastavuje grid pozici která odkazuje na index pozici
        # trakuje můj pohyb a pozici
        # snaží se centrovat hráče
        self.grid_position[0] = (self.index_position[0] - MARGIN) // CELL_WIDTH + 1
        self.grid_position[1] = (self.index_position[1] - MARGIN) // CELL_HEIGHT + 1

        if self.eat_food():
            return True

    # vykreslení hráče
    def draw_player(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.index_position.x), int(self.index_position.y)), self.size)
        #vykreslení mapovače jestli je naše index pos správná
        #pygame.draw.rect(screen, BLUE, (self.grid_position[0] * CELL_WIDTH + MARGIN // 2, self.grid_position[1] * CELL_HEIGHT + MARGIN // 2, CELL_WIDTH, CELL_HEIGHT), 1)

        # životy pacmana
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, YELLOW, (125 + 20 * x, WIDTH + 45), 8)

    # hráčův pohyb
    def player_movement(self, direction):
        self.stored_direction = direction

    # zajišťuje plynulý pohyb hráče po gridu, po 1 px místo skáníní např. po 30
    # vycentruje do gridu
    def get_index_position(self):
        return vector((self.grid_position.x * CELL_WIDTH) + MARGIN // 2 + CELL_WIDTH // 2,
                      (self.grid_position.y * CELL_HEIGHT) + MARGIN // 2 + CELL_HEIGHT // 2)

    #nepohybuju se mimo grid, centruje pohyb doprostřed cell, nejdu mezi buňkama
    def time_to_move(self):
        if int(self.index_position.x + MARGIN // 2) % CELL_WIDTH == 0:
            if self.direction == vector(1, 0) or self.direction == vector(-1, 0):
                return True
        if int(self.index_position.y + MARGIN // 2) % CELL_HEIGHT == 0:
            if self.direction == vector(0, 1) or self.direction == vector(0, -1):
                return True

    # pokud narazím do zdi zůstanu stát
    def can_move(self):
        for wall in self.app.walls:
            if vector(self.grid_position + self.direction) == wall:
                return False
        return True

    # pacman jí jídlo a přičítá se mu score
    def eat_food(self):
        if self.grid_position in self.app.food:
            self.app.food.remove(self.grid_position)
            self.score += 1
        if self.grid_position in self.app.cherry:
            self.app.cherry.remove(self.grid_position)
            self.score += 10
        if self.grid_position in self.app.banana:
            self.app.banana.remove(self.grid_position)
            self.score += 50
        if self.grid_position in self.app.ananas:
            self.app.ananas.remove(self.grid_position)
            self.score += 150
