import os, json, pygame

from Framework.tileset import Tileset
from Framework import image_handling

class TilesetManager:
    def __init__(self):
        self.tilesets = {} # {"tileset name": {"tilename": pygame.Surface}}
        for file in os.listdir("Data/Images/Tilesets"):
            if file.endswith(".png"):
                path = file.split(".")[0]
                with open("Data/Images/Tilesets" + "/" + path + ".json") as file:
                    tile_order = json.loads(file.read())
                    file.close()
                
                self.tilesets[path] = {}
                
                tileset_img = pygame.image.load("Data/Images/Tilesets/" + path + ".png").convert()
                images = image_handling.split_tiles(tileset_img, {"colour 1":(255, 0, 255, 255), "colour 2":(0, 255, 255, 255)})
                
                for i in range(len(images)):
                    self.tilesets[path][tile_order[i]] = images[i]