import pygame
import random

from constants import *

vector = pygame.math.Vector2


# def __init__(self, app, pos, color, size, speed, personality):
class Enemy:
    def __init__(self, app, pos, type_enemy):
        self.app = app
        self.grid_position = pos
        self.index_position = self.get_index_position()
        self.type_enemy = type_enemy
        self.colour = self.set_colour_enemy()
        self.direction = vector(0, 0)
        self.personality_enemy = self.set_personality_enemy()
        self.speed = self.set_speed()
        self.radius = int(CELL_WIDTH // 2.3)
        self.target = None
        self.starting_position = [pos.x, pos.y]

    # pohyb enemy, umí poznat zdi a nastavení cíle
    def update_enemy(self):
        self.target = self.set_target()
        if self.target != self.grid_position:
            self.index_position += self.direction * self.speed
            if self.time_to_move():
                self.move_enemy()

        # nastavuji grid pozici která odkazuje na index pozici a centruje enemy ke gridu
        # index pozice hráče, mapovač, pohyb po ose x[0], y[1], nastavuje grid pozici která odkazuje na index pozici
        # trakuje můj pohyb a pozici
        # snaží se centrovat hráče
        self.grid_position[0] = (self.index_position[0] - MARGIN + CELL_WIDTH // 2) // CELL_WIDTH + 1
        self.grid_position[1] = (self.index_position[1] - MARGIN + CELL_HEIGHT // 2) // CELL_HEIGHT + 1

    # vykreslení hráče
    def draw_enemy(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.index_position.x),
                                                 int(self.index_position.y)), 10, self.radius)

    # enemy rychlost
    def set_speed(self):
        if self.type_enemy == 0:
            speed = 2
        elif self.type_enemy == 1:
            speed = 1
        else:
            speed = 1
        return speed

    # zajišťuje plynulý pohyb hráče po gridu, po 1 px místo skáníní např. po 30
    # vycentruje do gridu, pozná zdi
    def time_to_move(self):
        if int(self.index_position.x + MARGIN // 2) % CELL_WIDTH == 0:
            if self.direction == vector(1, 0) or self.direction == vector(-1, 0) or self.direction == vector(0, 0):
                return True
        if int(self.index_position.y + MARGIN // 2) % CELL_HEIGHT == 0:
            if self.direction == vector(0, 1) or self.direction == vector(0, -1) or self.direction == vector(0, 0):
                return True
        return False

    # Enemy pohyb podle osobnosti 0=rychlý, 1=pomalý, 2=blind, 3=stupid
    def move_enemy(self):
        if self.type_enemy == 0:    # zelený
            self.direction = self.get_path_direction(self.target)
        if self.type_enemy == 1:    # modrý
            self.direction = self.get_path_direction(self.target)
        if self.type_enemy == 2:    # fialový
            self.direction = self.get_path_direction(self.target)
        if self.type_enemy == 3:    # růžový
            self.direction = self.random_move_enemy()

        ################ RANDOM GHOST ################

    #random pohyb ghosta
    def random_move_enemy(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_direction, y_direction = 1, 0
            elif number == - 1:
                x_direction, y_direction = 0, 1
            elif number == 0:
                x_direction, y_direction = -1, 0
            else:
                x_direction, y_direction = 0, -1
            next_position = vector(self.grid_position.x + x_direction, self.grid_position.y + y_direction)
            if next_position not in self.app.walls:
                break
        return vector(x_direction, y_direction)

        ################ BREADTH FIRST SEARCH ALGORITHM (chytří ghosti) ####################
        # https://github.com/a-plus-coding/pacman-with-python/blob/master/enemy_class.py

    # nastavení cíle pro enemy BFS, 0-2
    # voláme do update_enemy
    def set_target(self):
        if self.type_enemy == 0 or self.type_enemy == 1:    # 0 = rychlý enemy(zelený), 1 = pomalý (modrý)
            return self.app.player.grid_position        # 0 a 1 mají za cíl hráčovu pozici
        else:
            # chování fialového enemyho || č. 2
            # snaží se dostat co nejdál od hráče
            if self.app.player.grid_position[0] > COLUMNS // 2 and self.app.player.grid_position[1] > ROWS // 2:
                return vector(1, 1)
            if self.app.player.grid_position[0] > COLUMNS // 2 and self.app.player.grid_position[1] < ROWS // 2:
                return vector(1, ROWS - 2)
            if self.app.player.grid_position[0] > COLUMNS // 2 and self.app.player.grid_position[1] > ROWS // 2:
                return vector(COLUMNS - 2, 1)
            else:
                return vector(COLUMNS - 2, ROWS - 2)

    # metoda kterou voláme do move_enemy a parametr má target, který je výše a má nastavenou grid pozici hráče(nasetováno v set_target)
    # díky tomu stopují hrůčův pohyb a nahánějí ho
    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x_direction = next_cell[0] - self.grid_position[0]
        y_direction = next_cell[1] - self.grid_position[1]
        return vector(x_direction, y_direction)

    # využívá bfs algoritmus a trasuje cestu k cíli, který má být právě hráč
    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_position.x), int(self.grid_position.y)], [
                        int(target[0]), int(target[1])])
        #path = self.BFS([int(self.grid_position.x), int(self.grid_position.y)],
                        #[int(target[0]), int(target[1])])
        return path[1]

    # bfs algoritmus, který prohledává mapu a trasuje target
    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    #osa x
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        # osa y
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
    ################ BREADTH FIRST SEARCH ALGORITHM (chytří ghosti) konec ####################

    # zajišťuje plynulý pohyb hráče po gridu, po 1 px místo skáníní např. po 30
    # vycentruje do gridu
    def get_index_position(self):
        return vector((self.grid_position.x * CELL_WIDTH) + MARGIN // 2 + CELL_WIDTH // 2,
                      (self.grid_position.y * CELL_HEIGHT) + MARGIN // 2 + CELL_HEIGHT // 2)

    # barva enemy
    def set_colour_enemy(self):
        if self.type_enemy == 0:
            return GREEN    # fast
        if self.type_enemy == 1:
            return BLUE     # slow
        if self.type_enemy == 2:
            return PURPLE   # blind
        if self.type_enemy == 3:
            return PINK     # stupid

    # nastavení osobnosti enemyho
    def set_personality_enemy(self):
        if self.type_enemy == 0:
            return "fast"   # zelený
        if self.type_enemy == 1:
            return "slow"   # modrý
        if self.type_enemy == 2:
            return "blind"  # fialový
        else:
            return "stupid" # růžový

