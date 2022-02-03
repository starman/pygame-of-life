import pygame
import sys
import copy

class Cell():
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.alive = alive

    def is_alive(self):
        return self.alive

    def set_alive(self):
        self.alive = True

    def set_dead(self):
        self.alive = False

        
class Board():
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.gridline = 1
        self.grid = []

        for row in range(WIDTH//self.cell_size):
            self.grid.append([])
            for column in range(HEIGHT//self.cell_size):
                self.grid[row].append(Cell(row, column, False)) 

    def draw_grid(self):        
        size = self.cell_size
        gridline = self.gridline

        for row in range(WIDTH//size):
            for column in range(HEIGHT//size):
                color = (255, 255, 255)
                if self.grid[row][column].is_alive():
                    color = (0, 0, 0)
                pygame.draw.rect(screen,
                                color,
                                [(gridline + size) * column + gridline,
                                (gridline + size) * row + gridline,
                                size,
                                size])

    def set_cell_alive(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (self.cell_size + self.gridline)
        row = pos[1] // (self.cell_size + self.gridline)
        self.grid[row][column].set_alive()

    def set_cell_dead(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (self.cell_size + self.gridline)
        row = pos[1] // (self.cell_size + self.gridline)
        self.grid[row][column].set_dead()

    def neighbors(self, row, column):
        neighbors = 0
        try:
            if self.grid[row+1][column].is_alive():
                neighbors += 1
            if self.grid[row-1][column].is_alive():
                neighbors += 1
            if self.grid[row][column+1].is_alive():
                neighbors += 1
            if self.grid[row][column-1].is_alive():
                neighbors += 1
            if self.grid[row+1][column+1].is_alive():
                neighbors += 1
            if self.grid[row+1][column-1].is_alive():
                neighbors += 1
            if self.grid[row-1][column+1].is_alive():
                neighbors += 1
            if self.grid[row-1][column-1].is_alive():
                neighbors += 1
        except IndexError:
            pass
        except Exception as e:
            print(e)

        return neighbors

    def process(self):
        new_grid = copy.deepcopy(self.grid)
        for row in range(WIDTH//self.cell_size):
            for column in range(HEIGHT//self.cell_size):
                num_of_neighbors = self.neighbors(row, column)
                if self.grid[row][column].is_alive() and num_of_neighbors != 2 and num_of_neighbors != 3:
                    new_grid[row][column].set_dead()
                if num_of_neighbors == 3 and not self.grid[row][column].is_alive():
                    new_grid[row][column].set_alive()

        return new_grid

    def clear(self):
        for row in range(WIDTH//self.cell_size):
            for column in range(HEIGHT//self.cell_size):
                self.grid[row][column].set_dead()

                    
pygame.init()
pygame.display.set_caption("Conway's Game of Life")

WIDTH = 1200
HEIGHT = 1200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

game = Board(20)

FPS = 60

PLAYING = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            game.set_cell_alive()
        if pygame.mouse.get_pressed()[2]:
            game.set_cell_dead()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PLAYING = not PLAYING
            if event.key == pygame.K_c:
                game.clear()

    if PLAYING:
        game.grid = game.process()
    game.draw_grid()

    pygame.display.update()
    clock.tick(FPS)

