import pygame

class Particle:
    def __init__(self, loc, size_range=[5, 10], decay=0.1, speed=1, gravity=0, colour=None):
        self.velocity = [(random.randint(-10,10) / 5) * speed, (random.randint(-20, 30) / 3) * speed]
        self.size = random.randint(size_range[0], size_range[1])
        loc = [loc[0] - (self.size / 2), loc[1] - (self.size / 2)]
        self.decay = decay
        self.gravity = gravity
        self.rect = pygame.Rect(loc, (self.size, self.size))
        self.colour = colour
    
    def update(self):
        self.velocity[1] += self.gravity
        self.velocity[1] = min(self.velocity[1], 3)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.size -= self.decay
        self.rect.width = self.size
        self.rect.height = self.size

class SquareEffects(Particle):
    def __init__(self, loc, size, start_width, decay=0.1, colour=None):
        self.size = size
        self.loc = [loc[0] - (self.size / 2), loc[1] - (self.size / 2)]
        self.decay = decay
        self.width = start_width
        self.rect = pygame.Rect(self.loc, (self.size, self.size))
        self.colour = colour

    def update(self):
        self.width -= self.decay

class PixelParticle(Particle):
    def __init__(self, loc, timer, decay=0.05, speed=1, gravity=0, colour=None):
        super().__init__(loc, [3, 3], decay, speed, gravity, colour)