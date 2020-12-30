import pygame

class WindowManager:
    def __init__(self, game, caption):
        self.game = game
        self.screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)
        self.caption = caption
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.FPS = 60
    
    def start_frame(self):
        if self.game.game_map.area == "test":
            self.game.window_manager.screen.fill((0, 0, 0))
            # self.game.window_manager.screen.fill((0, 253, 212))
        elif self.game.game_map.area != "test":
            self.game.window_manager.screen.fill((255, 255, 255))
    
    def end_frame(self):
        pygame.display.update()
        self.clock.tick(self.FPS)
        