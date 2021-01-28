# General imports
from classes.FallingNote import FallingNote
import pygame, utils, os
from classes.GameState import GameState
from classes.ScoreHandler import ScoreHandler as score
import classes.ScoreHandler
from classes.Button import Button
import song_library
import pygame.freetype


def main():
    # Initialize pygame
    pygame.init()
    # Set screen size. Don't change this unless you know what you are doing!
    screen = pygame.display.set_mode((1280, 720))
    # Set the window title
    pygame.display.set_caption("IAT Challengeweek: Interaction Hero | China")
        
    # Keeps track of all sprites to be updated every frame
    allsprites = pygame.sprite.Group()

    text_font = pygame.freetype.Font("data/RobotoMono-VariableFont_wght.ttf", 34)
    # Song to be used in game. Only one can be used.
    song = song_library.example_song_short  # Short random song for debugging
    # song = song_library.example_song_long  # Ode To Joy

    # Create game_state instance, this holds all required game info
    game_state = GameState(allsprites, song)

    # Checks if the program is running on a Raspberry Pi
    is_running_on_rpi = utils.is_running_on_rpi()
    if is_running_on_rpi:
        # Below are some pin input numbers, feel free to change them. However,
        # !!! ALWAYS READ THE PIN DOCUMENTATION CAREFULLY !!!
        # Pay special attention to the difference between GPIO pin numbers and BOARD pin numbers
        # For example GPIO17 is addressed 17 rather than 11 (See pin numbering diagram.)
        # https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
        gpio_pin_numbers = [2, 3, 4, 17]  # Max 4 pins 
        gpio_buttons = init_rpi_buttons(gpio_pin_numbers)
        game_state.add_gpio_pins(gpio_pin_numbers)

    # Prepare game objects
    clock = pygame.time.Clock()
    startButton = Button(500, 300, 140, 40, ' Start', game_state.restart, song.get_font_filename(), allsprites, game_state)
    quitButton = Button(500, 350, 140, 40, ' Quit', quit, song.get_font_filename(), allsprites, game_state)

    # easyButton = Button(450, 250, 140, 40, ' Easy', select_difficulty, song.get_font_filename(), allsprites, game_state)
    # normalButton = Button(600, 250, 140, 40, ' Normal', select_difficulty, song.get_font_filename(), allsprites, game_state)
    # hardButton = Button(750, 250, 140, 40, ' Hard', select_difficulty, song.get_font_filename(), allsprites, game_state)

    # Main loop
    going = True
    while going:

        # Update the clock, argument is max fps
        clock.tick(60)

        # Every 'tick' or programcycle the gamestate update() is called
        game_state.update()

        # Get all events from the last cycle and store them as variable
        # This is stored as a variable because pygame.even.get() empties this list
        eventlist = pygame.event.get()

        # Check if there are any global quit events
        for event in eventlist:
            # If yes, the game loop won't start again
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.unicode == pygame.K_ESCAPE:
                going = False

        # This runs before the user starts the game
        if game_state.state == 'prestart':
            
            for event in eventlist:
            # Checks if a mouse is clicked 
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    startButton.check_click()
                    quitButton.check_click()
                    # Difficulty buttons
                    easyButton.check_click()
                    normalButton.check_click()
                    hardButton.check_click()

        # This runs when the users starts a game
        elif game_state.state == 'playing':
            stopButton = Button(100, 100, 140, 40, ' Stop', game_state.menu_start, song.get_font_filename(), allsprites, game_state)
            # Loop through all potential hitboxes
            for hitbox in game_state.hitboxes:
                # Every hitbox needs to check all events
                for event in eventlist:
                    if event.type == pygame.KEYDOWN and event.unicode == hitbox.event_key:
                        game_state.check_for_hit(hitbox)
                    elif event.type == pygame.KEYUP:
                        hitbox.unpunch()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         stopButton.check_click()
                        
                # When on RPi also check for GPIO input
                if is_running_on_rpi:
                    for button in gpio_buttons:
                        # When a buttons is pressed in this loop and wasn't pressed in the last loop
                        if button.is_pressed() and button.gpio_key is hitbox.gpio_event_key and button.is_available():
                            button.use()  # Set the button as unavailable for the next loop
                            game_state.check_for_hit(hitbox)
                        # When a button was not pressed in this loop
                        elif not button.is_pressed():
                            button.wake()  # Set the button as available again
                            hitbox.unpunch()

        elif game_state.state == 'end_game':
            end_screen()

        # # End state
        # elif game_state.state == 'end_game':
        #     replayButton = Button(500, 500, 200, 45, ' Replay', game_state.restart, song.get_font_filename(), allsprites, game_state)
        #     mainMenuButton = Button(650, 500, 200, 45, ' Main menu', game_state.menu_start, song.get_font_filename(), allsprites, game_state)
            
        #     top5 = score.get_top5_high_score()

        #     text_font.render_to(screen, (590, 200), "Highscores:", (153, 204, 255))
        #     # [90, 70, 65, 60, 60]

        #     for event in eventlist:
        #         # Checks if a mouse is clicked 
        #         if event.type == pygame.MOUSEBUTTONDOWN: 
        #             replayButton.check_click()
        #             mainMenuButton.check_click()
        #             quitButton.check_click()

        # text_font.render_to(screen, (40, 350), "Hello World!", (0, 0, 0))

        # This calls the update() function on all sprites
        allsprites.update()
        
        # Draw Everything
        screen.blit(game_state.get_background(), (0, 0))  # First draw a new background
        allsprites.draw(screen)  # Next draw all updated sprites
        pygame.display.update()  # Finally render everything to the display

def end_screen():
    # Keeps track of all sprites to be updated every frame
    allsprites = pygame.sprite.Group()
    # Song to be used in game. Only one can be used.
    song = song_library.example_song_short  # Short random song for debugging
    # song = song_library.example_song_long  # Ode To Joy

    # Create game_state instance, this holds all required game info
    game_state = GameState(allsprites, song)

    loop = True
    
    replayButton = Button(500, 500, 200, 45, ' Replay', game_state.restart, song.get_font_filename(), allsprites, game_state)
    mainMenuButton = Button(650, 500, 200, 45, ' Main menu', game_state.menu_start, song.get_font_filename(), allsprites, game_state)
        
    top5 = score.get_top5_high_score()
    
    while loop:

        text_font.render_to(screen, (590, 200), "Highscores:", (153, 204, 255))
        eventlist = pygame.event.get()
        for event in eventlist:
            # Checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                replayButton.check_click()
                mainMenuButton.check_click()
                quitButton.check_click()

    # This calls the update() function on all sprites
    allsprites.update()
    
    # Draw Everything
    screen.blit(game_state.get_background(), (0, 0))  # First draw a new background
    allsprites.draw(screen)  # Next draw all updated sprites
    pygame.display.update()  # Finally render everything to the display
      

def init_rpi_buttons(gpio_pin_numbers):
    # Initialize Raspberry Pi input pins
    gpio_buttons = []
    
    from gpiozero import Button
    from classes.GpioButton import GpioButton

    # Here you can configure which pins you use on your Raspberry Pi
    gpio_pins = gpio_pin_numbers  # Max 4 pins 
    bounce_time_in_sec = 0.1

    gpio_buttons.append(GpioButton(Button(gpio_pins[0], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[1], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[2], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[3], bounce_time=bounce_time_in_sec)))

    print('The following pins are configured as (gpio) button inputs:', gpio_pins)

    return gpio_buttons

def select_difficulty(diff):
    print(f"diff: "+diff)
    # if diff == "easy":
    #     FallingNote.move = 10
    # if diff == "normal":
    #     FallingNote.move = 15
    # if diff == "hard":
    #     FallingNote.move = 20

if __name__ == "__main__":
    main()
