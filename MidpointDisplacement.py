from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.backend_bases import KeyEvent


def generate_midpoint_displacement(
        points_left: list[float, float],
        points_right: list[float, float],
        length: int
) -> list[float]:
    global R
    current_points = [0.0]*length
    current_points[0] = points_left[1]
    current_points[length - 1] = points_right[1]
    q = deque()
    q.append((0, length - 1, 200))
    while len(q) != 0:
        left, right, roughness = q.popleft()
        center: int = (left + right + 1) // 2
        current_points[center] = (current_points[left] + current_points[right]) // 2
        current_points[center] = (current_points[center] + R * random.uniform(-1, 1) * abs(left - right))
        if right - left > 2:
            q.append((left, center, roughness // 2))
            q.append((center, right, roughness // 2))
    points = []
    for i, item in enumerate(current_points):
        points += [i + points_left[0], item]
    return points


def generate_land_space(
        current_points: list[[float, float]]
) -> np.ndarray[[np.float64, np.float64]]:
    heights = current_points[0]
    for i in range(1, len(current_points)):
        heights += current_points[i] + generate_midpoint_displacement(
            current_points[i - 1],
            current_points[i],
            int(current_points[i][0] - current_points[i - 1][0])
        )
    heights = np.array(heights).reshape((len(heights) // 2, 2))
    heights = np.array(sorted(heights, key=lambda point: point[0]))
    return heights


def key_event(e: KeyEvent):
    global POINTS, START_IDX, R
    if e.key == 'r':
        START_IDX = 0
        POINTS = generate_land_space(
            [[0, random.randint(0, 512)], [WIDTH, random.randint(0, 512)]]
        )
        draw_land_space(POINTS)
    elif e.key == "d":
        START_IDX += 64
        last_point = POINTS[-1]
        new_points = generate_land_space(
            [
                list(last_point),
                [last_point[0] + 64,
                 last_point[1] + 80 * random.uniform(-1, 1)]]
        )
        POINTS = np.append(POINTS, new_points[1::])
        POINTS = POINTS.reshape((len(POINTS) // 2, 2))
        draw_land_space(POINTS)
    elif e.key == "a":
        START_IDX -= 64
        if START_IDX < 0:
            START_IDX = 0
            first_point = POINTS[0]
            new_points = generate_land_space(
                [
                    [first_point[0] - 64,
                     first_point[1] + 80 * random.uniform(-1, 1)],
                    list(first_point)
                ]
            )
            POINTS = np.append(new_points[:-1], POINTS)
            POINTS = POINTS.reshape((len(POINTS) // 2, 2))
        draw_land_space(POINTS)
    elif e.key == "z":
        R = float(input())
        START_IDX = 0
        POINTS = generate_land_space(
            [[0, random.randint(0, 512)], [WIDTH, random.randint(0, 512)]]
        )
        draw_land_space(POINTS)
    elif e.key == "x":
        plt.savefig("land space.png")


def draw_land_space(
        current_points: np.ndarray[[np.float64, np.float64]]
) -> None:
    x, y = current_points[START_IDX:].T
    x = np.array([item - current_points[START_IDX][0] for item in x])
    FIGURE.clear()
    plt.plot(x, y)
    plt.fill_between(x, y, min(y) if min(y) < 0 else 0)
    plt.xlim([0, WIDTH])
    plt.ylim([min(y) if min(y) < 0 else 0, max(y) + 20])
    plt.tick_params(
        left=False,
        bottom=False,
        labelleft=False,
        labelbottom=False
    )
    plt.draw()


def render():
    global POINTS, FIGURE
    POINTS = generate_land_space(
        [
            [0, random.randint(0, 512)],
            [256, random.randint(0, 512)],
            [WIDTH, random.randint(0, 512)]
        ]
    )
    plt.ion()
    FIGURE.canvas.mpl_connect("key_press_event", key_event)
    draw_land_space(POINTS)
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    WIDTH = HEIGHT = 512
    R = 0.5
    POINTS = np.ndarray[[np.float64, np.float64]]
    START_IDX: int = 0
    FIGURE = plt.figure()
    render()
