import pygame, json

from Framework.map import Map

class ChunkSystem(Map):
    def __init__(self, game, tile_size, path=None):
        super().__init__(tile_size, path)
        self.previous_map = "start"
        self.game = game

    def open(self, path):
        self.previous_map = self.map
        file = open(path, "r")
        self.map_data = json.loads(file.read())
        file.close()
        area = path.split("/")[-1]
        self.area = area.split("_")[0]
        self.map = area
        self.process_tiles()

    def process_tiles(self):
        self.collidable = []
        self.spawns = []
        self.doors = []
        pop_pos = []
        for layer in range(len(self.map_data["Tile_space"])):
            for position, tile_data in self.map_data["Tile_space"][f"Layer_{layer}"].items():
                pos = [int(data) for data in position.split(",")]
                if tile_data["Type"] == "Collidable":
                    self.collidable.append(pygame.Rect(pos[0] * self.tile_size, pos[1] * self.tile_size, self.tile_size, self.tile_size))
                elif tile_data["Type"] == "Custom":
                    if tile_data["Tile"] == "spawn_0":
                        self.spawns.append([pygame.Rect(pos[0] * self.tile_size, pos[1] * self.tile_size, self.tile_size, self.tile_size), tile_data["Custom"]])
                        pop_pos.append(position)
                    elif tile_data["Tile"] == "door_0":
                        self.doors.append([pygame.Rect(pos[0] * self.tile_size, pos[1] * self.tile_size, self.tile_size, self.tile_size), tile_data["Custom"]])
                        pop_pos.append(position)
        for pop_position in pop_pos:
            self.map_data["Tile_space"][f"Layer_{layer}"].pop(pop_position)
    
    def calculate_spawn(self):
        spawn_pos = []
        for spawn in self.spawns:
            if spawn[1] == self.previous_map:
                spawn_pos = [spawn[0].centerx, spawn[0].centery]
        return spawn_pos
    
    def chunkate(self):
        self.render_list = {"Tile_space": {}, "World_space": {}}
        for layer in range(len(self.map_data["Tile_space"])):
            for pos, tile_data in self.map_data["Tile_space"][f"Layer_{layer}"].items():
                position = [int(data) for data in pos.split(",")]
                if (-self.tile_size < position[0] * self.tile_size - self.game.camera.offset.x < self.game.window_manager.screen.get_width()) and (-self.tile_size < position[1] * self.tile_size - self.game.camera.offset.y < self.game.window_manager.screen.get_height()):
                    try:
                        self.render_list["Tile_space"][f"Layer_{layer}"][pos] = tile_data
                    except KeyError as k_error:
                        self.render_list["Tile_space"][f"Layer_{layer}"] = {}
                        self.render_list["Tile_space"][f"Layer_{layer}"][pos] = tile_data
        for layer in range(len(self.map_data["World_space"])):
            for pos, tile_data in self.map_data["World_space"][f"Layer_{layer}"].items():
                position = [int(data) for data in pos.split(",")]
                if (-self.tile_size < position[0] - self.game.camera.offset.x < self.game.window_manager.screen.get_width()) and (-self.tile_size < position[1] - self.game.camera.offset.y < self.game.window_manager.screen.get_width()):
                    try:
                        self.render_list["World_space"][f"Layer_{layer}"][pos] = tile_data
                    except KeyError as k_error:
                        self.render_list["World_space"][f"Layer_{layer}"] = {}
                        self.render_list["World_space"][f"Layer_{layer}"][pos] = tile_data

    def render(self):
        for tile_layer in self.render_list["Tile_space"]:
            for pos, tile_data in self.render_list["Tile_space"][tile_layer].items():
                pos = [int(data) * self.tile_size for data in pos.split(",")]
                img = self.game.tileset_manager.tilesets[tile_data["Tileset"]][tile_data["Tile"]]
                pos = [pos[0]  - self.game.camera.offset.x, pos[1] - self.game.camera.offset.y]
                self.game.window_manager.screen.blit(img, pos)

    def update(self):
        self.chunkate()
        self.render()