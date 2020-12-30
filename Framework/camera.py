import pygame

class Camera:
    def __init__(self, game):
        self.true_offset = pygame.Vector2(0, 0)
        self.game = game
    
    def update(self, target):
        self.true_offset.x += ((target.centerx - self.offset.x - (self.game.window_manager.screen.get_width() + target.width) / 2) / 20) * self.game.dt
        self.true_offset.y += ((target.centery - self.offset.y - (self.game.window_manager.screen.get_height() + target.height) / 2) / 20) * self.game.dt
    
    @property
    def offset(self):
        return pygame.Vector2(int(self.true_offset.x), int(self.true_offset.y))