import random as rand
from math import sqrt, sin, cos
import pygame
import time

SIZE = W, H = 800, 800
disp = pygame.display
win = disp.set_mode((W, H))
draw = pygame.draw
disp.set_caption('pygame')

grid_w = 9
box_w =  W / grid_w

def dist(vec1, vec2):
    product = 0
    for i, coord in enumerate(vec1):
        product += pow(vec2[i]-vec1[i], 2)

    return sqrt(product)

def mag(vec):
    return sqrt(sum([pow(i, 2) for i in vec]))

def normalized(vec):
    _mag = mag(vec)
    if _mag == 0:
        return [0, 0]
    return [component/_mag for component in vec] 

def normalized_sum(vec1, vec2):
    return normalized(vector_sum(vec1, vec2))

def vector_sum(vec1, vec2):
    return [vec1[i]+vec2[i] for i, _ in enumerate(vec1)]

def mult(vec, x):
    return [component*x for component in vec]

def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            draw.rect(win, [min(255, 250*mag(cell))]*3, (x*box_w, y*box_w, box_w, box_w))

def deep_copy(grid):
    return [[col[:] for col in row[:]] for row in grid]

def draw_vec(vec, color=(255, 0, 0)):
    draw.line(win, color, (W//2, H//2), (W//2 + vec[0]*100, H//2 + vec[1]*100))

frame = 0

grid = []
# for y in range(grid_w):
#     grid.append([])
#     for x in range(grid_w):
#         grid[y].append(normalized([rand.random(), rand.random()]))

for y in range(grid_w):
    grid.append([])
    for x in range(grid_w):
        grid[y].append([0, 0])


last_pos = [0, 0]

clock = pygame.time.Clock()
while True:
    win.fill((51, 51, 51))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if pygame.mouse.get_pressed(3)[0]:
        x, y = pygame.mouse.get_pos()
        grid[int(y // box_w) % grid_w][int(x // box_w) % grid_w] = [(last_pos[0]-x) * -1000, (last_pos[1]-y) * -1000]
        last_pos = [x, y]

    # grid[25][25] = [-1, -1]
    grid[4][4] = mult(normalized([cos(frame/100), sin(frame/100)]), 4)
    # grid[4][4 ] = []
    # print([cos(frame/100)*1, sin(frame/100)*1])
    
    draw_grid(grid)
    new_grid = deep_copy(grid)

    draw_vec([cos(frame/100)*1000, sin(frame/100)*1000])
    avrg_mag = 0
    L = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            new_grid[y][x] = [0, 0]

            values = []
            for Y in [-1, 0, 1]:
                for X in [-1, 0, 1]:
                    vec2 = normalized([X, Y])
                    # print(round((2-dist(cell, vec2))*10)/10, end=' ')
                    values.append(2-dist(normalized(cell), vec2)) #subtract from max dist
                # print('')
            # exit()
            for iy, Y in enumerate([-1, 0, 1]):
                for ix, X in enumerate([-1, 0, 1]):
                    _X, _Y = (x+X) % grid_w, (y+Y) % grid_w

                    vec2 = normalized([X, Y])
                    # _sum = vector_sum(normalized([X, Y]), cell)
                    new_vec = vector_sum(cell, vec2)
                    # if [x, y] == [4, 4]:
                    #     for i in range(3):
                    #         for j in range(3):
                    #             a = round(values[i*3+j] / sum(values)*100)/100
                    #             print(str(a).ljust(4, '0'), end=' ')
                    #         print('')
                    #     print('---------', sum(values), '---------')

                    # if (Y != -1):
                    draw_vec(new_vec)
                        # print(new_vec)

                    if mag(new_vec) > 0.01:
                        new_vec = normalized(new_vec)

                        amount = mag(cell)*(values[iy*3+ix] / sum(values))
                        if Y != -1:
                            avrg_mag += amount
                            L += 1
                        # print(mag(new_vec))
                        new_grid[_Y][_X][0] += (amount * (new_vec[0]/mag(new_vec)))
                        new_grid[_Y][_X][1] += (amount * (new_vec[1]/mag(new_vec)))

                        # draw_vec((amount * (new_vec[0]/(mag(new_vec)+0.00001)), amount * (new_vec[1]/(mag(new_vec)+0.00001))))

    # mags = []
    # for y, row in enumerate(new_grid):
    #     for x, cell in enumerate(row):
    #         mags.append(mag(new_grid[y][x]))

    # for y, row in enumerate(new_grid):
    #     for x, cell in enumerate(row):
    #         new_grid[y][x][0] = new_grid[y][x][0] / max(mags)
    #         new_grid[y][x][1] = new_grid[y][x][1] / max(mags)
    grid = new_grid
    disp.update()
    # for row in grid:
    #     for i in row:
    #         print(round(mag(i)*10)/10, end=' ')
    #     print('')
    
    print('avrg:', avrg_mag/L)
    clock.tick(10)

    frame += 4
    # print(frame)

    # if frame == 2:
    #     time.sleep(100)