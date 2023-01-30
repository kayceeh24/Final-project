# Programmer(s): KC and Gabe
# Description: So what we are doing is a game that rock are going to fly to you and you have to move out of the way before they hit you but you can only get hit three times, if your lives are 0 it will play the bomb sound, game over sound and the game over text will flicker. 

# Import and initialize the pygame library
import pygame
from pygame.locals import *
from pygame import mixer
pygame.init()
import pygame

# Import functions for drawing gridlines and using sprites
from pygame_grid import *
from ucc_sprite import Sprite
from random import randint, choice

# Create and open a pygame screen with the given size
screen = pygame.display.set_mode((640,360))
grid = make_grid()

# Set the title of the pygame screen
pygame.display.set_caption("SPACESHIP VS ROCKS")

# Create a clock to keep track of time
clock = pygame.time.Clock()

# Group to hold all of the active sprites
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
### LOAD IMAGES AND FONTS

# Background image
background = pygame.image.load("space").convert()
screen.blit(background,(0, 0))

#Image of the space_ship
space_ship = pygame.image.load("spaceship.png").convert_alpha()
space_ship = pygame.transform.rotozoom(space_ship, 0, 0.20)

# Image for the rock
rock_image = pygame.image.load("rock.png").convert_alpha()
rock_image = pygame.transform.rotozoom(rock_image, 0, 0.25)

#image of the boom
bomb_image = pygame.image.load("pow.png").convert_alpha()
bomb_image = pygame.transform.rotozoom(bomb_image,0, 0.3)

#Load the musics 
pygame.mixer.init()
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play(-1)

game_over_sound = pygame.mixer.Sound("overvoice.mp3")
bomb_sound = pygame.mixer.Sound("bomb.mp3")

#CREATE SPRITES
space_ship = Sprite(space_ship)
space_ship.bottom_left = (0, 360)
space_ship.rotates = False
space_ship.add(all_sprites)

bomb = Sprite(bomb_image)

# Load the fonts
font = pygame.font.Font("Appocalypse.ttf", 72)
lives_left = 3
lives = Sprite(font.render(f"{lives_left}", True, "red"))
lives.center = (250, 30)
lives.add(all_sprites)

# make the font of game over
font = pygame.font.Font("Appocalypse.ttf", 72)

game_over_image = font.render("GAME OVER", True, "red")
game_over = Sprite(game_over_image)
game_over.center = (320, 180)

# asteroids that moves accross the screen
count = 0
while count < 10:
    rock = Sprite(rock_image)
    rock.x = randint(0, 424)
    rock.y = randint(0, 150)
    rock.rotates = False
    rock.direction = randint(0, 359)
    rock.speed = 0.5
    rock.add(all_sprites, rocks)
    count += 1
    
### CREATE TIMER
#SET THE TIMER
GAME_OVER_EVENT = pygame.event.custom_type()
FLASH_EVENT = pygame.event.custom_type()
# Main Loop
while True:
    # Set the frame rate to 60 frames per second
    clock.tick(60)

    ### MANAGE IN-GAME EVENTS AND ANIMATIONS HERE
    # Draw the background
    all_sprites.clear(screen, background)

  # Loop through all of the events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            exit()

        # the bomb will kill AND PLAYS THE SOUND
        elif event.type == GAME_OVER_EVENT:
            bomb.kill()
            game_over_sound.play()

        # it makes the gameover flicker
        elif event.type == FLASH_EVENT:
            if game_over.alive():
                game_over.kill()
            else:
                game_over.add(all_sprites)
   
    # Handle events
    # multi keys
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[K_RIGHT]:
        space_ship.x += 2
        if space_ship.right > 660:
            space_ship.x -= 2
    if keys_pressed[K_LEFT]:
        space_ship.x -= 2
        if space_ship.left > 400:
            space_ship.x -= 2
    if keys_pressed[K_UP]:
        space_ship.y -= 2
        if space_ship.top > 400:
            space_ship.x += 2
    if keys_pressed[K_DOWN]:
        space_ship.y += 2
        if space_ship.bottom > 400:
            space_ship.x -= 2
        
    # Update the sprites' locations
    all_sprites.update()

    # if THE spaceship are crash to a rock the lives - 1
    for rock in rocks:
        if space_ship.alive() and pygame.sprite.collide_mask(space_ship, rock):
            lives_left -= 1
            rock.kill()
            bomb.center = rock.center
            
            #lives image
            lives.image = font.render(f"lives: {lives_left} ", True, "white")
            space_ship.bottom_left = (0, 360)

            # If lives left are 0 it will kill the ship and it shows the gameover screen and play the sounds
            if lives_left == 0:
                game_over.add(all_sprites)
                space_ship.kill()
                pygame.mixer.music.stop()
                bomb_sound.play()
                bomb.add(all_sprites)
                pygame.time.set_timer(GAME_OVER_EVENT, 1000, 1)
                pygame.time.set_timer(FLASH_EVENT, 1000)
        
        # if rock is gone on the sides it will comeback to the screen
        if rock.right < 0:
            rock.left = 640
        if rock.left > 640:
            rock.right = 0
        if rock.bottom < 0:
            rock.top = 360
        if rock.top > 360:
            rock.bottom = 0
    
    # Redraw the sprites
    all_sprites.draw(screen)
            
    # Update the sprites' locations
    all_sprites.update()
    
    # Uncomment the next line to show a grid
    #screen.blit(grid, (0,0))

    # Flip the changes to the screen to the computer display
    pygame.display.flip()