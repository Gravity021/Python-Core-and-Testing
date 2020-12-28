import pygame, os
from Framework import tileset, chunker

class Button:
    def __init__(self, pos, folder, on_press, press_params=None):
        self.on_press = on_press
        self.press_params = press_params
        
        cols = {"colour 1": (255, 0, 255, 255), "colour 2": (0, 255, 255, 255)}
        names = ["Left_0", "Centre_0", "Right_0", "Left_1", "Centre_1", "Right_1", "Left_2", "Centre_2", "Right_2"]
        self.imgs = tileset.Tileset(folder + "/Button.png", cols, names, (0, 0, 0))
        self.map = chunker.Map(64, folder + "/button.json")

        self.rect = pygame.Rect(pos[0], pos[1], len(self.map.map_data["Tile_space"]["Layer_0"]) * self.map.tile_size, self.map.tile_size)
        self.no = 0
    
    def update(self, screen, mouse_pos, press):
        self.no = 0
        if self.rect.collidepoint(mouse_pos):
            if press:
                self.no = 2
                if self.press_params != None:
                    self.on_press(self.press_params)
                else:
                    self.on_press()
            else:
                self.no = 1

        for pos, tile_data in self.map.map_data["Tile_space"]["Layer_0"].items():
            pos = [int(data) * self.map.tile_size for data in pos.split(",")]
            tile = f"{tile_data['Tile']}_{self.no}"
            screen.blit(self.imgs.images[tile], [pos[0] + self.rect.x, pos[1] + self.rect.y])

class Menu:
    def __init__(self, title, font):
        self.buttons = []
        self.MENU = True
        self.title = title
        self.font = font
    
    def update(self, screen, mouse_pos, press):
        self.font.render(screen, self.title, self.font.centre(self.title, [screen.get_width() / 2, 100]))
        for button in self.buttons:
            button.update(screen, mouse_pos, press)