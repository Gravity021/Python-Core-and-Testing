import json

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