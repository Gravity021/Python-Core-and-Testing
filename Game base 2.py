# Setup --------------------------------------------------------------------- #
# Import Modules -------------------------------------------------- #
import pygame

import time

# Import Custom --------------------------------------------------- #
from Framework import camera
from Framework import chunker
from Framework import UI

from Framework.Effects import transitions

from Framework.Managers import window_manager
from Framework.Managers import input_manager
from Framework.Managers import tileset_manager
from Framework.Managers import entity_manager
from Framework.Managers import audio_manager

# Game ---------------------------------------------------------------------- #
class Game():
    def __init__(self):
        # Setup --------------------------------------------------- #
        pygame.init()
        pygame.mixer.set_num_channels(8)

        self.running = True

        self.GRAVITY = 0.3

        self.dt = 1

        # Managers ------------------------------------------------ #
        self.window_manager = window_manager.WindowManager(self, "Game Base")
        self.input_manager = input_manager.InputManager(self)
        self.tileset_manager = tileset_manager.TilesetManager()
        self.game_map = chunker.ChunkSystem(self, 32)
        self.entity_manager = entity_manager.EntityManager(self)
        self.audio_manager = audio_manager.AudioManager()

        self.audio_manager.channels["SFX"].set_volume(0)

        self.camera = camera.Camera(self)

        self.transition = transitions.SideSwipe(self, 5)

        self.menu = UI.Menu(self)

    def run(self):
        while self.running:
            self.window_manager.start_frame()

            self.input_manager.start_frame()

            if not self.menu.MENU:
                self.camera.update(self.entity_manager.player.rect)

                self.game_map.update()

                self.entity_manager.update()
            
            elif self.menu.MENU:
                self.menu.update()
            
            self.transition.update_exponential()

            self.input_manager.update()

            self.window_manager.end_frame()

Game().run()