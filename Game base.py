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
from Framework import managers
from Framework import menus
from Framework import sound
from Framework import tileset
from Framework import UI
from Framework.Effects import particles
from Framework.Effects import transitions

# Import Saves ---------------------------------------------------- #
from Data.Saves.Player_Controls import controls

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

# Player ---------------------------------------------------------- #
# with open("Data/Saves/CTX.txt") as file:
#     ctx = file.read()
ctx = "start"

player = entities.Player((0, 0, 16, 28), controls, 5, GRAVITY, game_map)
player.animation.load_images("Idle", "Data/Images/Player", [1])

player.animation.action = "Idle"

# Audio ----------------------------------------------------------- #
audio_manager = managers.AudioManager()

# Transitions ----------------------------------------------------- #
def on_complete(area):
    game_map.open(f"Data/Maps/{area}")
    spawn = game_map.calculate_spawn(ctx)
    player.rect.x = spawn[0]
    player.rect.y = spawn[1]
    if menu.MENU:
        menu.MENU = False

transition = transitions.SideSwipe(5, screen, on_complete)

# Menu ------------------------------------------------------------ #
menu_funcs = menus.MenuFuncs(transition)

menu = UI.Menu("Game Base", title_font)
menu.buttons.append(UI.Button([100, 100], "Data/Images/UI/Buttons", menu_funcs.play, None))

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
        camera.update(screen, player.rect, dt)

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
        player.update(dt)

        screen.blit(pygame.transform.flip(player.animation.image, player.animation.flip, False), [player.rect.x - camera.offset.x, player.rect.y - camera.offset.y])
    
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
                if event.key == player.controls["Jump"]:
                    if player.jumps_available > 0:
                        if player.jumps_available > 1:
                            player.gravity -= 15
                        elif player.jumps_available <= 1:
                            player.gravity -= 7
                        player.jumps_available -= 1

                        audio_manager.play("Jump")
                    
                    print("jump attempted")
            
                # Left ------------------------ #
                elif event.key == player.controls["Left"]:
                    player.moving["Left"] = True
                    player.moving["Right"] = False
                    player.animation.flip = False
                    
                # Right ----------------------- #
                elif event.key == player.controls["Right"]:
                    player.moving["Left"] = False
                    player.moving["Right"] = True
                    player.animation.flip = True
                
                # Open ------------------------ #
                elif event.key == player.controls["Open"]:
                    for tile in game_map.doors:
                        if player.rect.colliderect(tile[0]):
                            transition.target = tile[1]
                            transition.transitioning = True
                            transition.transitioning_in = True
                
                # K_r ------------------------- #
                elif event.key == pygame.K_r:
                    spawn = game_map.calculate_spawn(ctx)
                    player.rect.x = spawn[0]
                    player.rect.y = spawn[1]

            # K_SPACE ------------------------- #
            elif event.key == pygame.K_SPACE:
                pass
        
        # KEYUP ----------------------------------------- #
        elif event.type == pygame.KEYUP:
            if not menu.MENU:
                # Left ------------------------ #
                if event.key == player.controls["Left"]:
                    player.moving["Left"] = False
                    
                # Right ----------------------- #
                elif event.key == player.controls["Right"]:
                    player.moving["Right"] = False
    
    # Update frame and FPS ---------------------------------------- #
    pygame.display.update()
    clock.tick(FPS)

# Quit ---------------------------------------------------------------------- #
pygame.quit()
quit()