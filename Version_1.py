import numpy as np
import matplotlib.pyplot as plt
import cv2
from pylab import *
import os

size = 250

map = np.array([[False]*size]*size)
# Population array
map[110:150, 0:250] = True
map[0:250, 110:150] = True


def alive_cell(x, y):
    alive = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                new_x = x + i
                new_y = y + j
                cell = map[new_x][new_y]
                if cell == True:
                    alive += 1
            except:
                pass
    if map[x][y] == True:
        alive -= 1
    return alive

plt.imshow(map, cmap="gray")
plt.show()

for i in range(200):
    cv2.imwrite("./images/" + str(i) + ".png", map.astype("uint8") * 255)
    new_map = np.array([[False]*size]*size)
    for x in range(len(map)):
        for y in range(len(map)):
            neighbors = alive_cell(x, y)
            # Any live cell with two or three live neighbours survives.
            if map[x][y] == True:
                if 2 <= neighbors <= 4:
                    new_map[x][y] = True
            # Any dead cell with three live neighbours becomes a live cell.
            elif map[x][y] == False:
                if neighbors == 3:
                    new_map[x][y] = True
            # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
            else:
                new_map[x][y] = False
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

img_to_vid("./images/")