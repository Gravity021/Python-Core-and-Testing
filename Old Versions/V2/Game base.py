# Setup --------------------------------------------------------------------- #
# Import pygame --------------------------------------------------- #
import pygame
from pygame import mixer

import time

# Import Custom --------------------------------------------------- #
from Framework import camera as cam
from Framework import chunker
from Framework import delta_time
from Framework import entities
from Framework import font
from Framework import image_handling

# from Framework import managers

from Framework import menus
from Framework import sound
from Framework import tileset
from Framework import UI

from Framework.Effects import particles
from Framework.Effects import transitions

from Framework.Managers import audio_manager as audio
from Framework.Managers import entity_manager
from Framework.Managers import input_manager

# Import Saves ---------------------------------------------------- #

# Initialise pygame ----------------------------------------------- #
pygame.init()

pygame.mixer.set_num_channels(8)

clock = pygame.time.Clock()
FPS = 60

# Setup window ---------------------------------------------------- #
screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)
pygame.display.set_caption("Game base")

# General --------------------------------------------------------- #
GRAVITY = 0.3

# Camera ---------------------------------------------------------- #
camera = cam.Camera()

# Font ------------------------------------------------------------ #
large_font = font.Font("Data/Images/UI/Fontsheets/large_font.png", (255, 255, 255), 6, 1)
small_font = font.Font("Data/Images/UI/Fontsheets/small_font.png", (255, 255, 255), 3, 1)
title_font = font.Font("Data/Images/UI/Fontsheets/large_font.png", (0, 0, 0), 6, 1)

# Tilesets -------------------------------------------------------- #
tilesets = tileset.load_tilesets("Data/Images/Tilesets", {"colour 1":(255, 0, 255, 255), "colour 2":(0, 255, 255, 255)})

# Map ------------------------------------------------------------- #
game_map = chunker.ChunkSystem(32)

# Entities -------------------------------------------------------- #
entity_manager = entity_manager.EntityManager(GRAVITY, game_map)

# Input ----------------------------------------------------------- #
input_manager = input_manager.InputManager()

# Player ---------------------------------------------------------- #
# with open("Data/Saves/CTX.txt") as file:
#     ctx = file.read()
ctx = "start"

# Audio ----------------------------------------------------------- #
audio_manager = audio.AudioManager()
audio_manager.channels["SFX"].set_volume(0)

# Transitions ----------------------------------------------------- #
def on_complete(area):
    game_map.open(f"Data/Maps/{area}")
    spawn = game_map.calculate_spawn(ctx)
    entity_manager.player.rect.x = spawn[0]
    entity_manager.player.rect.y = spawn[1]
    if menu.MENU:
        menu.MENU = False

transition = transitions.SideSwipe(5, screen, on_complete)

# Menu ------------------------------------------------------------ #
menu_funcs = menus.MenuFuncs(transition)

menu = UI.Menu("Game Base", title_font)
menu.buttons.append(UI.Button([100, 100], "Data/Images/UI/Buttons", menu_funcs.play, None))

menu.MENU = False
game_map.open("Data/Maps/test_0.json")
spawn = game_map.calculate_spawn(ctx)
entity_manager.player.rect.x = spawn[0]
entity_manager.player.rect.y = spawn[1]

# Delta Time ------------------------------------------------------ #
# dt = delta_time.DeltaTime()

last_time = time.time()

# Main loop ----------------------------------------------------------------- #
running = True
while running:
    # Setup frame ------------------------------------------------- #
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    mouse_presses = pygame.mouse.get_pressed()

    if game_map.area == "test":
        screen.fill((0, 0, 0))
        # screen.fill((0, 253, 212))
    elif game_map.area != "test":
        screen.fill((255, 255, 255))

    # Delta Time ------------------------------------ #
    # dt.update()
    # dt.dt = 1

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    
    # Game ------------------------------------------------------- #
    if not menu.MENU:
        # Camera ---------------------------------------- #
        camera.update(screen, entity_manager.player.rect, dt)

        # Render Tiles ---------------------------------- #
        # Calculate Tiles on Screen ----------- #
        game_map.chunkate(screen, camera)

        # Tile space -------------------------- #
        for tile_layer in game_map.render_list["Tile_space"]:
            for pos, tile_data in game_map.render_list["Tile_space"][tile_layer].items():
                pos = [int(data) * game_map.tile_size for data in pos.split(",")]
                screen.blit(tilesets[tile_data["Tileset"]].images[tile_data["Tile"]], [pos[0] - camera.offset.x, pos[1] - camera.offset.y])
        
        # World space ------------------------- #
        for tile_layer in game_map.render_list["World_space"]:
            for pos, tile_data in game_map.render_list["World_space"][tile_layer].items():
                pos = [int(data) for data in pos.split(",")]
                screen.blit(tilesets[tile_data["Tileset"]].images[tile_data["Tile"]], [pos[0] - camera.offset.x, pos[1] - camera.offset.y])

        # Player ---------------------------------------- #
        entity_manager.update(dt)

        img = pygame.transform.flip(entity_manager.player.animation.image, entity_manager.player.animation.flip, False)
        screen.blit(img, [entity_manager.player.rect.x - camera.offset.x, entity_manager.player.rect.y - camera.offset.y])
    
    # Menu -------------------------------------------------------- #
    elif menu.MENU:
        menu.update(screen, mouse_pos, mouse_presses[0])

    # Transitions ------------------------------------------------- #
    transition.update_exponential(screen, dt)

    # Events ------------------------------------------------------ #
    for event in events:
        # QUIT ------------------------------------------ #
        if event.type == pygame.QUIT:
            running = False
        
        # VIDEORESIZE ----------------------------------- #
        elif event.type == pygame.VIDEORESIZE:
            transition.sides[0].height = screen.get_height()
            transition.sides[1].height = screen.get_height()

            transition.sides[1].right = screen.get_width()
        
        # KEYDOWN --------------------------------------- #
        elif event.type == pygame.KEYDOWN:
            if not menu.MENU:
                # Jump ------------------------ #
                if event.key == entity_manager.player.controls["Jump"]:
                    if entity_manager.player.jumps_available > 0:
                        if entity_manager.player.jumps_available > 1:
                            entity_manager.player.gravity -= 15
                        elif entity_manager.player.jumps_available <= 1:
                            entity_manager.player.gravity -= 7
                        entity_manager.player.jumps_available -= 1

                        audio_manager.play("Jump")
                    
                    print("jump attempted")
            
                # Left ------------------------ #
                elif event.key == entity_manager.player.controls["Left"]:
                    entity_manager.player.moving["Left"] = True
                    entity_manager.player.moving["Right"] = False
                    entity_manager.player.animation.flip = False
                    
                # Right ----------------------- #
                elif event.key == entity_manager.player.controls["Right"]:
                    entity_manager.player.moving["Left"] = False
                    entity_manager.player.moving["Right"] = True
                    entity_manager.player.animation.flip = True
                
                # Open ------------------------ #
                elif event.key == entity_manager.player.controls["Open"]:
                    for tile in game_map.doors:
                        if entity_manager.player.rect.colliderect(tile[0]):
                            transition.target = tile[1]
                            transition.transitioning = True
                            transition.transitioning_in = True
                
                # K_r ------------------------- #
                elif event.key == pygame.K_r:
                    spawn = game_map.calculate_spawn(ctx)
                    entity_manager.player.rect.x = spawn[0]
                    entity_manager.player.rect.y = spawn[1]

            # K_SPACE ------------------------- #
            elif event.key == pygame.K_SPACE:
                pass
        
        # KEYUP ----------------------------------------- #
        elif event.type == pygame.KEYUP:
            if not menu.MENU:
                # Left ------------------------ #
                if event.key == entity_manager.player.controls["Left"]:
                    entity_manager.player.moving["Left"] = False
                    
                # Right ----------------------- #
                elif event.key == entity_manager.player.controls["Right"]:
                    entity_manager.player.moving["Right"] = False
    
    # Update frame and FPS ---------------------------------------- #
    pygame.display.update()
    clock.tick(FPS)

# Quit ---------------------------------------------------------------------- #
pygame.quit()
quit()