import pygame, json

class Map:
    def __init__(self, tile_size, path=None):
        self.map_data = {}
        self.tile_size = tile_size
        self.area = None
        self.map = "start"
        if path != None:
            self.open(path)
        
    def open(self, path):
        file = open(path, "r")
        self.map_data = json.loads(file.read())
        file.close()
        area = path.split("/")[-1]
        self.area = area.split("_")[0]
    
    def save(self, save_path):
        file = open(save_path, "w")
        file.write(json.dumps(self.map_data))
        file.close()
    
    def get_loc(self, scroll, pos):
        tile_loc = [int((pos[0] - scroll[0]) / self.tile_size), int((pos[1] - scroll[1]) / self.tile_size)]
        return tile_loc
    
    def add_tile(self, scroll, position, new_tile_data):
        tile_loc = self.get_loc(scroll, position)
        self.map_data["Tile_space"]["Layer_0"][f"{tile_loc[0]},{tile_loc[1]}"] = new_tile_data

    def delete_tile(self):
        pass

class ChunkSystem(Map):
    def __init__(self, tile_size, path=None):
        super().__init__(tile_size, path)
        self.previous_map = "start"

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
        pop = False
        pop_pos = []
        for layer in range(len(self.map_data["Tile_space"])):
            for position, tile_data in self.map_data["Tile_space"][f"Layer_{layer}"].items():
                pos = [int(data) for data in position.split(",")]
                if tile_data["Type"] == "Collidable":
                    self.collidable.append(pygame.Rect(pos[0] * self.tile_size, pos[1] * self.tile_size, self.tile_size, self.tile_size))
                elif tile_data["Type"] == "Custom":
                    if tile_data["Tile"] == "spawn_0":
                        self.spawns.append([pygame.Rect(pos[0] * self.tile_size, pos[1] * self.tile_size, self.tile_size, self.tile_size), tile_data["Custom"]])
                        pop = True
                        pop_pos.append(position)
                    elif tile_data["Tile"] == "door_0":
                        self.doors.append([pygame.Rect(pos[0] * self.tile_size, pos[1] * self.tile_size, self.tile_size, self.tile_size), tile_data["Custom"]])
                        pop = True
                        pop_pos.append(position)
        if pop:
            for pop_position in pop_pos:
                self.map_data["Tile_space"][f"Layer_{layer}"].pop(pop_position)
    
    def calculate_spawn(self, ctx):
        spawn_pos = []
        for spawn in self.spawns:
            # if spawn[1] == f"{ctx}_spawn":
            if spawn[1] == self.previous_map:
                spawn_pos = [spawn[0].centerx, spawn[0].centery]
        return spawn_pos
    
    def chunkate(self, screen, camera):
        self.render_list = {"Tile_space": {}, "World_space": {}}
        for layer in range(len(self.map_data["Tile_space"])):
            for pos, tile_data in self.map_data["Tile_space"][f"Layer_{layer}"].items():
                position = [int(data) for data in pos.split(",")]
                if (-self.tile_size < position[0] * self.tile_size - camera.offset.x < screen.get_width()) and (-self.tile_size < position[1] * self.tile_size - camera.offset.y < screen.get_height()):
                    try:
                        self.render_list["Tile_space"][f"Layer_{layer}"][pos] = tile_data
                    except KeyError as k_error:
                        self.render_list["Tile_space"][f"Layer_{layer}"] = {}
                        self.render_list["Tile_space"][f"Layer_{layer}"][pos] = tile_data
        for layer in range(len(self.map_data["World_space"])):
            for pos, tile_data in self.map_data["World_space"][f"Layer_{layer}"].items():
                position = [int(data) for data in pos.split(",")]
                if (-self.tile_size < position[0] - camera.offset.x < screen.get_width()) and (-self.tile_size < position[1] - camera.offset.y < screen.get_width()):
                    try:
                        self.render_list["World_space"][f"Layer_{layer}"][pos] = tile_data
                    except KeyError as k_error:
                        self.render_list["World_space"][f"Layer_{layer}"] = {}
                        self.render_list["World_space"][f"Layer_{layer}"][pos] = tile_data

class EditorMap(Map):
    def new_map(self):
        self.map_data = {"Tile_space": {}, "World_space": {}}

    def add_tile(self, scroll, mouse_pos, space, layer_no, new_tile_data):
        if self.map_data != {}:
            if space == "Tile_space":
                tile_loc = self.get_loc(scroll, mouse_pos)
                try:
                    self.map_data[space][f"Layer_{layer_no}"][f"{tile_loc[0]},{tile_loc[1]}"] = new_tile_data
                except KeyError as k_error:
                    self.map_data[space][f"Layer_{layer_no}"] = {}
                    self.map_data[space][f"Layer_{layer_no}"][f"{tile_loc[0]},{tile_loc[1]}"] = new_tile_data
            elif space == "World_space":
                try:
                    self.map_data[space][f"Layer_{layer_no}"][f"{mouse_pos[0] - scroll[0]},{mouse_pos[1] - scroll[1]}"] = new_tile_data
                except KeyError as k_error:
                    self.map_data[space][f"Layer_{layer_no}"] = {}
                    self.map_data[space][f"Layer_{layer_no}"][f"{mouse_pos[0] - scroll[0]},{mouse_pos[1] - scroll[1]}"] = new_tile_data
    
    def delete_tile(self, scroll, mouse_pos, space, layer_no):
        if self.map_data != {}:
            if space == "Tile_space":
                tile_loc = self.get_loc(scroll, mouse_pos)
                pop = False
                for pos in self.map_data["Tile_space"][f"Layer_{layer_no}"]:
                    if pos == f"{str(tile_loc[0])},{str(tile_loc[1])}":
                        pop = True
                        pop_pos = pos
                if pop:
                    self.map_data["Tile_space"][f"Layer_{layer_no}"].pop(pop_pos)
            elif space == "World_space":
                pop = False
                for tile_pos in self.map_data["World_space"][f"Layer_{layer_no}"]:
                    pos = [int(position) for position in tile_pos.split(",")]
                    if (pos[0] <= mouse_pos[0] - scroll[0] < pos[0] + self.tile_size) and (pos[1] <= mouse_pos[1] - scroll[1] < pos[1] + self.tile_size):
                        pop = True
                        pop_pos = tile_pos
                if pop:
                    self.map_data["World_space"][f"Layer_{layer_no}"].pop(pop_pos)