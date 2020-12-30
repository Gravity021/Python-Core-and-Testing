import pygame

class Entity:
    def __init__(self, rect, speed):
        rect = (rect[0] - (rect[2] / 2), rect[1] - (rect[3] / 2), rect[2], rect[3])
        self.rect = pygame.Rect(rect)
        self.speed = speed
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 0
        self.jumps_available = 2
    
    def move(self, colliders):
        self.rect.x += self.velocity.x
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity.x > 0: # ------------- right
                    self.rect.right = collider.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # ----------- left
                    self.rect.left = collider.right
                    self.velocity.x = 0
        self.rect.y += self.velocity.y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity.y > 0: # ------------- down
                    self.rect.bottom = collider.top
                    self.jumps_available = 2
                elif self.velocity.y < 0: # ----------- up
                    self.rect.top = collider.bottom
                    self.gravity = 0