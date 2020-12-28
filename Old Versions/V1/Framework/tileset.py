import pygame, os
from Framework import image_handling, json_handler

class Tileset:
    def __init__(self, img_path, colours, order):
        self.img_path = img_path
        self.tileset_img = pygame.image.load(self.img_path).convert()
        images = image_handling.split_tiles(self.tileset_img, colours)
        self.images = {}
        for i in range(len(images)):
            self.images[order[i]] = images[i]

def load_tilesets(dir, colours):
    tilesets = {}
    for file in os.listdir(dir):
        if file.endswith(".png"):
            path = file.split(".")[0]
            tile_order = json_handler.load(dir + "/" + path + ".json")
            tilesets[path] = Tileset(dir + "/" + file, colours, tile_order)
    return tilesets