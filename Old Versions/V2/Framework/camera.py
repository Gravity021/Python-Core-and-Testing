import pygame

class Camera:
    def __init__(self):
        self.true_offset = pygame.Vector2(0, 0)
    
    def update(self, surf, target, dt):
        self.true_offset.x += ((target.centerx - self.offset.x - (surf.get_width() + target.width) / 2) / 20) * dt
        self.true_offset.y += ((target.centery - self.offset.y - (surf.get_height() + target.height) / 2) / 20) * dt
        # self.offset.x *= dt
        # self.offset.y *= dt

        # print(dt)
    
    @property
    def offset(self):
        return pygame.Vector2(int(self.true_offset.x), int(self.true_offset.y))