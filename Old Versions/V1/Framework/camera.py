import pygame

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
    
    def update(self, surf, target):
        self.offset.x += (target.centerx - self.offset.x - (surf.get_width() + target.width) / 2) / 20
        self.offset.y += (target.centery - self.offset.y - (surf.get_height() + target.height) / 2) / 20
        # self.offset.x = int(self.offset.x)
        # self.offset.y = int(self.offset.y)
        # self.offset.x += 1