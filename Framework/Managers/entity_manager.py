import pygame

from Framework import entity, player

from Data.Saves.Player_Controls import controls

class EntityManager():
    def __init__(self, game):
        self.game = game
        self.player = player.Player((0, 0, 16, 28), controls, 5, self.game.GRAVITY, self.game.game_map)
        self.player.animation.load_images("Idle", "Data/Images/Player", [1])
    
    def update(self):
        self.player.update(self.game.dt)
        self.game.window_manager.screen.blit(pygame.transform.flip(self.player.animation.image, self.player.animation.flip, False), [self.player.rect.x - self.game.camera.offset.x, self.player.rect.y - self.game.camera.offset.y])