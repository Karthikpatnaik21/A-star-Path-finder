import pygame
from random import choice
from queue import PriorityQueue

Res = WIDTH, HEIGHT = 1300, 650
Tile = 30
cols, rows = WIDTH // Tile, HEIGHT // Tile
wall_width = 2

pygame.init()
sc = pygame.display.set_mode(Res)
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True,
                      'right': True,
                      'left': True,
                      'bottom': True}
        self.rect = pygame.Rect(x*Tile, y*Tile, Tile, Tile)
        self.neighbors = []
        self.visited = False
        self.selected = False
        self.top_right = False
        self.top_left = False
        self.bottom_right = False
        self.bottom_left = False
        self.path_hor = False
        self.path_ver = False
        self.pointer = False
        self.color = '#378805'
        self.point_direction = ''
        self.point_radius = 2

    def draw(self):
        x, y = self.x * Tile, self.y * Tile
        pos = pygame.mouse.get_pos()
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e1e1e'), (x, y, Tile, Tile))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#ffffff'), (x, y), (x + Tile, y), wall_width)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#ffffff'), (x + Tile, y), (x + Tile, y + Tile), wall_width)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#ffffff'), (x + Tile, y + Tile), (x, y + Tile), wall_width)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#ffffff'), (x, y + Tile), (x, y), wall_width)
        if Maze_ready:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.selected:
                    self.selected = True
                    self.pointer = not self.pointer
                    add_point(self)
            if pygame.mouse.get_pressed()[0] == 0:
                self.selected = False
            if self.pointer:
                pygame.draw.circle(sc, pygame.Color(self.color), (x + Tile//2, y + Tile//2), self.point_radius)
            if self.top_left:
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y),
                                 (x + Tile//2, y + Tile//2), 1)
                self.pointer = True
                self.color = '#FF0000'
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y + Tile//2),
                                 (x, y + Tile//2), 1)
            if self.bottom_left:
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y+Tile),
                                 (x + Tile//2, y + Tile//2), 1)
                self.pointer = True
                self.color = '#FF0000'
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile // 2, y + Tile // 2),
                                 (x, y + Tile//2), 1)
            if self.top_right:
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y),
                                 (x + Tile//2, y + Tile//2), 1)
                self.pointer = True
                self.color = '#FF0000'
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile // 2, y + Tile // 2),
                                 (x+Tile, y + Tile//2), 1)
            if self.bottom_right:
                pygame.draw.line(sc, pygame.Color('#00B408'), (x+Tile//2, y + Tile),
                                 (x + Tile//2, y + Tile//2), 1)
                self.pointer = True
                self.color = '#FF0000'
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y + Tile//2),
                                 (x+Tile, y + Tile//2), 1)
            if self.path_hor:
                pygame.draw.line(sc, pygame.Color('#00B408'), (x, y + Tile//2),
                                 (x + Tile, y + Tile//2), 1)
                self.pointer = True
                self.color = '#FF0000'
            if self.path_ver:
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y),
                                 (x + Tile//2, y + Tile), 1)
                self.pointer = True
                self.color = '#FF0000'
            if self.point_direction == 'top':
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y),
                                 (x + Tile//2, y + Tile//2), 1)
            elif self.point_direction == 'bottom':
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile//2, y + Tile),
                                 (x + Tile//2, y + Tile//2), 1)
            elif self.point_direction == 'left':
                pygame.draw.line(sc, pygame.Color('#00B408'), (x, y + Tile//2),
                                 (x + Tile//2, y + Tile//2), 1)
            elif self.point_direction == 'right':
                pygame.draw.line(sc, pygame.Color('#00B408'), (x + Tile, y + Tile//2),
                                 (x + Tile//2, y + Tile//2), 1)

    def get_pos(self):
        return self.y, self.x

    @staticmethod
    def check_cell(x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.y < rows - 1 and not self.walls['bottom']:
            self.neighbors.append(grid[(self.y+1) * cols + self.x])

        if self.y > 0 and not self.walls['top']:
            self.neighbors.append(grid[(self.y-1) * cols + self.x])

        if self.x < cols - 1 and not self.walls['right']:
            self.neighbors.append(grid[self.y * cols + self.x + 1])

        if self.x > 0 and not self.walls['left']:
            self.neighbors.append(grid[self.y * cols + self.x - 1])


def remove_walls(beside, current):
    dx = current.x - beside.x
    if dx == 1:
        current.walls['left'] = False
        beside.walls['right'] = False
    if dx == -1:
        current.walls['right'] = False
        beside.walls['left'] = False
    dy = current.y - beside.y
    if dy == 1:
        current.walls['top'] = False
        beside.walls['bottom'] = False
    if dy == -1:
        current.walls['bottom'] = False
        beside.walls['top'] = False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def pointer(x1, y1, x2, y2):
    if y1 == y2:
        if (x1 - x2) > 0:
            return 'left'
        else:
            return 'right'
    else:
        if (y1 - y2) > 0:
            return 'top'
        else:
            return 'bottom'


def bend(m1, m2):
    if m1 == 'top':
        if m2 == 'left':
            return 'bottom left'
        else:
            return 'bottom right'
    elif m1 == 'bottom':
        if m2 == 'left':
            return 'top left'
        else:
            return 'top right'

    elif m1 == 'right':
        if m2 == 'top':
            return 'top left'
        else:
            return 'bottom left'
    else:
        if m2 == 'top':
            return 'top right'
        else:
            return 'bottom right'


def reconstruct_path(path, start, end):
    x, y = end.x, end.y
    move1 = pointer(x, y, path[end].x, path[end].y)
    end.point_direction = move1
    while end in path:
        if path[end] == start:
            break
        end = path[end]
        reset_path.append(end)
        move2 = pointer(end.x, end.y, path[end].x, path[end].y)
        if move1 == move2:
            if move1 == 'left' or move1 == 'right':
                end.path_hor = True
            else:
                end.path_ver = True
        else:
            direction = bend(move1, move2)
            if direction == 'top right':
                end.top_right = True
            elif direction == 'top left':
                end.top_left = True
            elif direction == 'bottom right':
                end.bottom_right = True
            else:
                end.bottom_left = True
        move1 = move2
    start.point_direction = pointer(start.x, start.y, end.x, end.y)


def algorithm(grid, start, stop):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_cost = {spot: float('inf') for spot in grid}
    g_cost[start] = 0
    f_cost = {spot: float('inf') for spot in grid}
    f_cost[start] = h(start.get_pos(), stop.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == stop:
            reconstruct_path(came_from, start, stop)
            return True

        for neighbor in current.neighbors:
            temp_score = g_cost[current] + 1

            if temp_score < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_score
                f_cost[neighbor] = temp_score + h(neighbor.get_pos(), stop.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_cost[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return False


def add_point(x):
    points.append(x)
    if len(points) > 2:
        r = points.pop(0)
        r.pointer = False
        r.point_radius = 2
    elif len(points) == 1:
        s = points[0]
        s.color = '#228822'
        s.point_radius = 3
    if len(points) == 2:
        s, e = points
        s.color = '#228822'
        s.point_radius = 3
        e.color = '#ff2c2c'
        e.point_radius = 3


points = []
reset_path = []
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
Maze_ready = False
ran = False

while True:
    sc.fill(pygame.Color('#000000'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(points) == 2:
                algorithm(grid_cells, points[0], points[1])
                ran = True
            if event.key == pygame.K_r and Maze_ready:
                grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
                current_cell = grid_cells[0]
                stack = []
                Maze_ready = False
            if event.key == pygame.K_c and Maze_ready and ran:
                for i in points:
                    i.point_direction = ''
                    i.pointer = False
                    i.point_radius = 2
                for i in reset_path:
                    i.top_right = False
                    i.top_left = False
                    i.bottom_right = False
                    i.bottom_left = False
                    i.path_hor = False
                    i.path_ver = False
                    i.pointer = False
                reset_path = []
                points = []

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
    elif not Maze_ready:
        Maze_ready = True
        for i in grid_cells:
            i.update_neighbors(grid_cells)

    pygame.display.flip()
