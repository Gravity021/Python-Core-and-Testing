from Framework.map import Map

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