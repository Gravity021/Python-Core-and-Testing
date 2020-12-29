from Framework import entities

from Data.Saves.Player_Controls import controls

class EntityManager():
    def __init__(self, GRAVITY, game_map):
        self.player = entities.Player((0, 0, 16, 28), controls, 5, GRAVITY, game_map)
        self.player.animation.load_images("Idle", "Data/Images/Player", [1])
    
    def update(self, dt):
        self.player.update(dt)