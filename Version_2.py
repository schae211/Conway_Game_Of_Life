import numpy as np
import matplotlib.pyplot as plt
import cv2
from pylab import *
import os
from numba import jit

size = 250

map = np.zeros((size, size)).astype(bool)

# Define function to populate the array
def cross(map, width=20):
    n, m = map.shape
    w2, n2, m2 = width // 2, n // 2, m // 2
    map[(n2-w2):(n2+w2), :] = True
    map[:, (m2-w2):(m2+w2)] = True


# Actually population the array
cross(map, 30)


# Run conways game of life
def alive_cell(x, y):
    alive = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                new_x = x + i
                new_y = y + j
                cell = map[new_x, new_y]
                if cell:
                    alive += 1
            except:
                pass
    if map[x, y]:
        alive -= 1
    return alive


for i in range(20):
    f = "/Users/philipp/Python_projects/conway_game_of_life/images/" + str(i) + ".png"
    cv2.imwrite(filename=f, img=(map.astype("uint8") * 255))
    new_map = np.zeros((size, size)).astype(bool)
    for x in range(size):
        for y in range(size):
            neighbors = alive_cell(x, y)
            # Any live cell with two or three live neighbours survives.
            if map[x, y] == True:
                if 2 <= neighbors <= 4:
                    new_map[x, y] = True
            # Any dead cell with three live neighbours becomes a live cell.
            elif map[x, y] == False:
                if neighbors == 3:
                    new_map[x, y] = True
            # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
            else:
                new_map[x, y] = False
    map = new_map


def img_to_vid(data_path):
    img_array = []
    size = (0, 0)
    for count in range(0, len(os.listdir(data_path)) - 1):
        filename = data_path + str(count) + '.png'
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter('./Conway_Game.avi', cv2.VideoWriter_fourcc(*'MJPG'), 8, size)

    for frame_index in range(len(img_array)):
        out.write(img_array[frame_index])
    out.release()


img_to_vid("/Users/philipp/Python_projects/conway_game_of_life/images/")
