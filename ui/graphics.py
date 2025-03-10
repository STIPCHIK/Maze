import pygame

import settings
from ui import screen

Image = pygame.Surface
flip = pygame.display.flip


def fill(color):
    screen.fill(color)


# принимает размеры картинки в координатах лабиринта
def load_image(path, size=(1, 1)):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (int(size[0] * settings.tile_size[0]+5), int(size[1] * settings.tile_size[1]+5)))


# клиенты будут передавать координаты лабиринта
def draw_image(image, x, y):
    screen.blit(image, (x * settings.tile_size[0] + settings.view_left_top[0], y * settings.tile_size[1] + settings.view_left_top[1]))


# клиенты будут передавать координаты лабиринта
def draw_circle(color, x, y, r):
    pygame.draw.circle(screen, color, (int(x * settings.tile_size[0] + settings.view_left_top[0]), int(y * settings.tile_size[1] + settings.view_left_top[1])), int(r * settings.tile_size[0]))

