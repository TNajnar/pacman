import pygame
import sys

import copy

import enemy
import player
from buttons import *
from constants import *
from player import *
from enemy import *

# inicializace mojí pygame
pygame.init()

vector = pygame.math.Vector2

# Název a Ikonka v okně
pygame.display.set_caption("Pacman")
icon = pygame.image.load(favicona)
pygame.display.set_icon(icon)
pygame.display.set_mode()

# title text PACMAN
title_bckgrnd = pygame.image.load("images/tit-pacman.png")
title_bckgrnd = pygame.transform.scale(title_bckgrnd, [HEIGHT // 2 + 50, WIDTH // 4])

# Objekty TITLE SCREEN
quit_button = Button(YELLOW, HEIGHT // 2 - 30, WIDTH // 2 + 150, 'QUIT (ESC)')
play_button = Button(YELLOW, HEIGHT // 2 - 30, WIDTH // 2 + 20, 'PLAY GAME (PRESS SPACE)')
high_score_button = Button(YELLOW, HEIGHT / 2 - WIDTH / 2 + 60, WIDTH / 2 - WIDTH / 2 + 40, 'HIGH SCORE: ')

# pozadí když se přepneme do hry | labyrint
# background = pygame.image.load("images/labyrinth.png")
# background = pygame.transform.scale(background, [MAZE_WIDTH, MAZE_HEIGHT])
score = Button(YELLOW, HEIGHT / 2 - WIDTH / 2 + 60, WIDTH / 2 - WIDTH / 2 + 18, 'SCORE: {}')
lives_btn = Button(YELLOW, WIDTH // 4 - 75, WIDTH + 45, "LIVES: ")

# game over
game_over_end_tit = pygame.image.load("images/game_over_tit_end.png")
game_over_end_tit = pygame.transform.scale(game_over_end_tit, [HEIGHT // 2 + 50, WIDTH // 2])
play_again_button = Button(quit_button_end_var, HEIGHT // 2 - 30, HEIGHT // 2 + 80, 'PLAY AGAIN (PRESS SPACE)')
quit_end_button = Button(quit_button_end_var, HEIGHT // 2 - 30, HEIGHT // 2 + 150, 'QUIT (ESC)')

# Třída app
class Game:

    def __init__(self):
        # screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # width/height
        # Určuje maximální rychlost pragramu a zajišťuje např. že se hráč bude pohybovat moc rychle
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.walls = []
        self.food = []
        self.cherry = []
        self.banana = []
        self.ananas = []
        self.doors = []
        self.enemies = []
        self.enemy_position = []
        self.load_play()
        # Player
        self.player = Player(self, copy.copy(PLAYER_START_POSITION), YELLOW, 10)
        self.make_enemies()


    def run(self):
        # while smyčka která se provadí dokud hra běží
        while self.running:
            self.clock.tick(FPS)
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            if self.state == 'play':
                self.play_events()
                self.play_draw()
                self.playing_update()
            if self.state == 'game_over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

        pygame.quit()
        sys.exit()

    ############################ HELP FUNCTIONS ############################

    # otevře soubor a vykreslí zdi, jídlo
    def load_play(self):
        self.background = pygame.image.load("images/labyrinth.png")
        self.background = pygame.transform.scale(self.background, [MAZE_WIDTH, MAZE_HEIGHT])

        with open("walls.txt", 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    # zdi
                    if char == "%":
                        self.walls.append(vector(x_index, y_index))
                        # jidlo
                    elif char == '.':
                        self.food.append(vector(x_index, y_index))
                    elif char == 'T':
                        self.cherry.append(vector(x_index, y_index))
                    elif char == 'B':
                        self.banana.append(vector(x_index, y_index))
                    elif char == 'A':
                        self.ananas.append(vector(x_index, y_index))
                        # ghost doors
                    elif char == 'D':
                        self.doors.append(vector(x_index, y_index))
                        #self.screen.blit(self.door,
                                         #(x_index * CELL_WIDTH + MARGIN // 2, y_index * CELL_HEIGHT + MARGIN // 2))
                        #pygame.draw.rect(self.background, BLACK, (x_index * CELL_WIDTH, y_index * CELL_HEIGHT,
                                                                 # CELL_WIDTH, CELL_HEIGHT))
                    # ghosti
                    elif char == 'G':
                        self.enemy_position.append([x_index, y_index])


    # vytvoří enemy a přidá do listu
    def make_enemies(self):
        for x_index, pos in enumerate(self.enemy_position):
            self.enemies.append(Enemy(self, vector(pos), x_index))

    # vykreslení hracího POLE
    def draw_grid(self):
        for x in range(WIDTH // CELL_WIDTH):
            pygame.draw.line(self.background, GREY, (x * CELL_WIDTH, 0),
                             (x * CELL_WIDTH, HEIGHT))
        for x in range(HEIGHT // CELL_HEIGHT):
            pygame.draw.line(self.background, GREY, (0, x * CELL_HEIGHT),
                             (WIDTH, x * CELL_HEIGHT))

    ############################ TITLE SCREEN ############################

    # tato metoda prochází pomocí cyklu všechny eventy, jestli není aktivní nějaký, který nás zajímá
    def start_events(self):
        for event in pygame.event.get():
            # testuje jestli je hra zavrena
            if event.type == pygame.QUIT:
                # self.running == False
                pygame.quit()
                sys.exit()
            # po stisku escapu se hra vypne
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # po stistu mezerníku se přesuneme do hry
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'play'

    # metoda která vykreslí play btn, quit btn, high score
    def start_draw(self):
        # pozadí okna
        self.screen.fill(BLACK)
        self.screen.blit(title_bckgrnd, (WIDTH // 4 - 40, HEIGHT // 4 - 70))
        # buttony
        quit_button.draw_text(self.screen)
        play_button.draw_text(self.screen)
        # aktualizuje screen
        pygame.display.flip()

    ############################ PLAY EVENTS ############################

    # Metody které se spustí po stisknutí mezerníku tedy zavolání state "play" do metody run
    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.running == False
                pygame.quit()
                sys.exit()
            # po stisku escapu se hra vypne
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.player_movement(vector(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.player_movement(vector(1, 0))
                if event.key == pygame.K_UP:
                    self.player.player_movement(vector(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.player_movement(vector(0, 1))

    # provolávám jednotlivé UPDATE metody z playera a enemyho
    def playing_update(self):
        self.player.player_update()
        # Ghosts
        for enemy in self.enemies:
            enemy.update_enemy()

        # po kolizi s enemym se mi odečte život
        for enemy in self.enemies:
            if enemy.grid_position == self.player.grid_position:
                self.remove_life()    # o kousek níž :)


    # metoda vykresli
    # jídlo, hráče, enemy, text
    def play_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (MARGIN // 2, MARGIN // 2))
        self.draw_food()
        self.draw_cherry()
        self.draw_banana()
        self.draw_ananas()
        self.draw_door()
        score = Button(YELLOW, HEIGHT / 2 - WIDTH / 2 + 60, WIDTH / 2 - WIDTH / 2 + 18,
                       'SCORE: {}'.format(self.player.score))
        #self.draw_grid()
        # self.draw_walls()  # zdi
        # player
        self.player.draw_player(self.screen)
        # ghosts
        for enemy in self.enemies:
            enemy.draw_enemy(self.screen)

        score.draw_text(self.screen)
        lives_btn.draw_text(self.screen)
        pygame.display.update()

    # metoda odstraň život, provolávám do play_update
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = 'game_over'
        else:
            # nastavení startovní pozic hráč po chytnutí
            self.player.grid_position = vector(PLAYER_START_POSITION)
            self.player.index_position = self.player.get_index_position()
            self.player.direction *= 1

            # nastavení startovní pozic enemy po chytnutí hráče
            for enemy in self.enemies:
                enemy.grid_position = vector(enemy.starting_position)
                enemy.index_position = enemy.get_index_position()
                enemy.direction *= 0

    ############################ JÍDLO PRO PACMANA ############################

    # 1 bod
    def draw_food(self):
        for f in self.food:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(f.x * CELL_WIDTH) + CELL_WIDTH // 2 + MARGIN // 2,
                                int(f.y * CELL_HEIGHT) + CELL_HEIGHT // 2 + MARGIN // 2), 5)

    # třešně za 50 bodů
    def draw_cherry(self):
        self.cherry_img = pygame.image.load("images/cherry2.png").convert_alpha(self.background)
        self.cherry_img = pygame.transform.scale(self.cherry_img, (20, 20))

        for c in self.cherry:
            self.screen.blit(self.cherry_img, (c.x * CELL_WIDTH + MARGIN // 2, c.y * CELL_HEIGHT + MARGIN // 2))

    # banán za 100 bodů
    def draw_banana(self):
        self.img_banana = pygame.image.load("images/banan.png").convert_alpha(self.background)
        self.img_banana = pygame.transform.scale(self.img_banana, (20, 20))

        for b in self.banana:
            self.screen.blit(self.img_banana, (b.x * CELL_WIDTH + MARGIN // 2, b.y * CELL_HEIGHT + MARGIN // 2))

    # ananas za 150 bodů
    def draw_ananas(self):
        self.img_ananas = pygame.image.load("images/ananas.jpg").convert_alpha(self.background)
        self.img_ananas = pygame.transform.scale(self.img_ananas, (30, 30))

        for a in self.ananas:
            self.screen.blit(self.img_ananas, (a.x * CELL_WIDTH + MARGIN // 2, a.y * CELL_HEIGHT + MARGIN // 2))

    # dveře enemies od jejich domečku
    def draw_door(self):
        self.door_img = pygame.image.load("images/door.jpg")
        self.door_img = pygame.transform.scale(self.door_img, (20, 20))

        for d in self.doors:
            self.screen.blit(self.door_img, (d.x * CELL_WIDTH + MARGIN // 2, d.y * CELL_HEIGHT + MARGIN // 2))

    ############################ GAME OVER ############################

    # title screen game over, po stisku mezerníku z5 do hry, esc = konec hry
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.play_again_reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    # vykreslení textu game over
    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(game_over_end_tit, (WIDTH // 4 - 40, HEIGHT // 4 - 70))
        play_again_button.draw_text(self.screen)
        quit_end_button.draw_text(self.screen)
        pygame.display.update()

    # po stisknutí mezerníku se přesunu z5 do hry
    # nastavení hry a načtení nezbytností
    def play_again_reset(self):
        self.state = 'play'
        self.player.lives = 3
        self.player.score = 0

        # nastavení startovní pozic hráč po znovu zapnutí hry
        self.player.grid_position = vector(PLAYER_START_POSITION)
        self.player.index_position = self.player.get_index_position()
        self.player.direction *= 1

        # nastavení startovní pozic enemy po znovu zapnutí hry
        for enemy in self.enemies:
            enemy.grid_position = vector(enemy.starting_position)
            enemy.index_position = enemy.get_index_position()
            enemy.direction *= 0

        self.food = []
        self.cherry = []
        self.banana = []
        self.ananas = []
        with open("walls.txt", 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    # jidlo
                    if char == '.':
                        self.food.append(vector(x_index, y_index))
                    elif char == 'T':
                        self.cherry.append(vector(x_index, y_index))
                    elif char == 'B':
                        self.banana.append(vector(x_index, y_index))
                    elif char == 'A':
                        self.ananas.append(vector(x_index, y_index))
