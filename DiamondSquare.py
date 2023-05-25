import os
import random
import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt


def make_height(terrain, x, y, half_width, figure):
    n = terrain.shape[0]
    height, points_count = 0, 0
    for row, column in figure:
        new_x, new_y = x + row * half_width, y + column * half_width
        if 0 <= new_x < n and 0 <= new_y < n:
            height += terrain[new_x, new_y]
            points_count += 1.0
    return height / points_count


def diamond_square(terrain, width, roughness):
    length = terrain.shape[0]
    half_width = width // 2
    square_xy = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    diamond_xy = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    for x in range(half_width, length, width):
        for y in range(half_width, length, width):
            terrain[x, y] = make_height(terrain, x, y, half_width, square_xy) + \
                            random.uniform(-roughness, roughness)

    for x in range(half_width, length, width):
        for y in range(0, length, width):
            terrain[x, y] = make_height(terrain, x, y, half_width, diamond_xy) +\
                            random.uniform(-roughness, roughness)

    for x in range(0, length, width):
        for y in range(half_width, length, width):
            terrain[x, y] = make_height(terrain, x, y, half_width, diamond_xy) +\
                            random.uniform(-roughness, roughness)


def make_terrain(size, roughness):
    terrain = np.zeros(size * size).reshape(size, size)
    width, current_roughness = size - 1, 1.0
    while width > 1:
        diamond_square(terrain, width, current_roughness)
        width //= 2
        current_roughness *= roughness
    return terrain


def make_color_map():
    colormap = []
    for row in np.loadtxt("geo-smooth.txt"):
        colormap.append([row[0], row[1:4]])
    return matplotlib.colors.LinearSegmentedColormap.from_list(
        "geo-smooth", colormap
    )


def menu():
    size = 1 + 2**9
    roughness = 0.7
    colormap = make_color_map()
    while True:
        terrain = make_terrain(size, roughness)
        print('Текущее значение roughness: ', roughness)
        print('Выберите действие:\n'
              '1. Отрисовать ландшафт\n'
              '2. Изменить roughness\n'
              '3. Сохранить изображение с текущими параметрами\n'
              '4. Выход')
        action = int(input('Введите номер действия: '))
        if action == 1:
            plt.tick_params(
                left=False, bottom=False, labelleft=False, labelbottom=False
            )
            plt.imshow(terrain, cmap=colormap)
            plt.show()
        elif action == 2:
            roughness = float(
                input('Введите новое значение 0<roughness<1\n ')
            )
        elif action == 3:
            plt.tick_params(
                left=False, bottom=False, labelleft=False, labelbottom=False
            )
            plt.imshow(terrain, cmap=colormap)
            plt.savefig("terrain.png")
        elif action == 4:
            return
        os.system('cls')


if __name__ == "__main__":
    menu()
