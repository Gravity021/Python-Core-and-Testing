# Setup --------------------------------------------------------------------- #
# Import pygame --------------------------------------------------- #
import pygame
from pygame import mixer

# Import Custom --------------------------------------------------- #
from Framework import audio
from Framework import camera as cam
from Framework import chunker
from Framework import entities
from Framework import font
from Framework import image_handling
from Framework import tileset
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

# Camera ---------------------------------------------------------- #
camera = cam.Camera()

# Font ------------------------------------------------------------ #
large_font = font.Font("Data/Images/Fontsheets/large_font.png", (255, 255, 255), 6, 1)
small_font = font.Font("Data/Images/Fontsheets/small_font.png", (255, 255, 255), 3, 1)

# Tilesets -------------------------------------------------------- #
tilesets = tileset.load_tilesets("Data/Images/Tilesets", {"colour 1":(255, 0, 255, 255), "colour 2":(0, 255, 255, 255)})

# Map ------------------------------------------------------------- #
game_map = chunker.ChunkSystem(32, "Data/Maps/test_0.json")

# Player ---------------------------------------------------------- #
# with open("Data/Saves/CTX.txt") as file:
#     ctx = file.read()
ctx = "start"
spawn = game_map.calculate_spawn(ctx)

player = entities.Player((spawn[0], spawn[1], 16, 28), controls, 5)
player.animation.load_images("Idle", "Data/Images/Player", [1])

player.animation.action = "Idle"

left = False
right = False

# Audio ----------------------------------------------------------- #
# Channels ---------------------------------------------- #
SFX_channel = pygame.mixer.Channel(0)
SFX_channel.set_volume(0)

# Audio Manager ----------------------------------------- #
audio_manager = audio.AudioManager()
audio_manager.sounds["Jump"] = audio.Sound(pygame.mixer.Sound("Data/Audio/Jump.wav"), SFX_channel)

# Transitions ----------------------------------------------------- #
transition = transitions.SideSwipe(3, screen)

def on_complete():
    game_map.open("Data/Maps/test_1.json")
    spawn = game_map.calculate_spawn(ctx)
    player.rect.x = spawn[0]
    player.rect.y = spawn[1]

# Other ----------------------------------------------------------- #
GRAVITY = 0.3

# Game loop ----------------------------------------------------------------- #
running = True
while running:
    # Setup frame ------------------------------------------------- #
    if game_map.area == "test":
        screen.fill((0, 0, 0))
        # screen.fill((0, 253, 212))
    elif game_map.area != "test":
        screen.fill((255, 255, 255))

    events = pygame.event.get()

    # Camera ------------------------------------------------------ #
    camera.update(screen, player.rect)

    # Render Tiles ------------------------------------------------ #
    # Calculate Tiles on Screen ------------------------- #
    game_map.chunkate(screen, camera)

    # Tile space ---------------------------------------- #
    for layer in range(len(game_map.render_list["Tile_space"])):
        for pos, tile_data in game_map.render_list["Tile_space"][f"Layer_{layer}"].items():
            pos = [int(data) * game_map.tile_size for data in pos.split(",")]
            screen.blit(tilesets[tile_data["Tileset"]].images[tile_data["Tile"]], [pos[0] - camera.offset.x, pos[1] - camera.offset.y])
    
    # World space --------------------------------------- #
    for layer in range(len(game_map.render_list["World_space"])):
        for pos, tile_data in game_map.render_list["World_space"][f"Layer_{layer}"].items():
            pos = [int(data) for data in pos.split(",")]
            screen.blit(tilesets[tile_data["Tileset"]].images[tile_data["Tile"]], [pos[0] - camera.offset.x, pos[1] - camera.offset.y])

    # Player ------------------------------------------------------ #
    if left and not right:
        player.velocity.x = -1 * player.speed
    elif right and not left:
        player.velocity.x = 1 * player.speed

    player.gravity = min(player.gravity + GRAVITY, 5)
    player.velocity.y = player.gravity
    
    player.move(game_map.collidable)
    player.animation.update()

    screen.blit(pygame.transform.flip(player.animation.image, player.animation.flip, False), [player.rect.x - camera.offset.x, player.rect.y - camera.offset.y])

    # Transitions ------------------------------------------------- #
    transition.update_linear(screen, on_complete)
    
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
            # Jump ---------------------------- #
            if event.key == player.controls["Jump"]:
                if player.jumps_available > 0:
                    if player.jumps_available > 1:
                        player.gravity -= 15
                    elif player.jumps_available <= 1:
                        player.gravity -= 7
                    player.jumps_available -= 1

                    audio_manager.play("Jump")
            
            # Left ---------------------------- #
            elif event.key == player.controls["Left"]:
                left = True
                right = False
                player.animation.flip = False
                
            # Right --------------------------- #
            elif event.key == player.controls["Right"]:
                right = True
                left = False
                player.animation.flip = True
            
            # K_r ----------------------------- #
            elif event.key == pygame.K_r:
                spawn = game_map.calculate_spawn(ctx)
                player.rect.x = spawn[0]
                player.rect.y = spawn[1]

            # K_SPACE ------------------------- #
            elif event.key == pygame.K_SPACE:
                transition.transitioning = not transition.transitioning
        
        # KEYUP ----------------------------------------- #
        elif event.type == pygame.KEYUP:
            # Left ---------------------------- #
            if event.key == player.controls["Left"]:
                left = False
                
            # Right --------------------------- #
            elif event.key == player.controls["Right"]:
                right = False
    
    # Update frame and FPS ---------------------------------------- #
    pygame.display.update()
    clock.tick(FPS)

# Quit ---------------------------------------------------------------------- #
pygame.quit()
quit()