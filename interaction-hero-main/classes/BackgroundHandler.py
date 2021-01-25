from utils import load_image, load_font, get_main_dir
import pygame
import os
from math import floor

class BackgroundHandler():
    
    background_color = (255,255,255)  # Default is RGB code for white

    def __init__(self, song):
        # Set the font based of the settings in the Song
        self.font = load_font(song.get_font_filename(), 36)
        # Make it bold
        self.font.set_bold(True)

        # Get a list of all the background
        self.background_list = self._get_all_backgrounds(
            song.get_bg_image_dir(),
            song.get_bg_game_header()
        )

        # Set other bg variables
        self.bg_update_interval_time = song.get_bg_image_interval_ms()
        self.bg_game_header = song.get_bg_game_header()
        self.current_bg_index = 0
        self.last_bg_update_time = pygame.time.get_ticks()
        self.background = None
        
        # In case there is only one bg file don't animate it
        self._check_for_static_bg()


    # Check if the included files are valid
    def _is_file_format_valid(self, filename):
        valid_file_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tif', 'lbm', 'pbm', 'pgm', 'ppm', 'xpm']
        file_format = filename.split('.')[-1]
        if any(x in file_format for x in valid_file_formats):
            return True
        else:
            return False


    def calculate_play_area_size(self):
        window_size = (1280, 720)
        play_area = pygame.Surface((440, 720))
        # make the surface white (or other defined bg color)
        play_area.fill(self.background_color)

        # create a location to draw the playarea and set it at the standard topleft pixel
        play_area_loc = play_area.get_rect(topleft=(420, 0))

        return play_area, play_area_loc


    # receives a raw background as argument
    # optional argument to pass your own text
    # returns a background with playarea background an some text
    def _finalize_background(self, background, play_text):
        play_area, play_area_loc = self.calculate_play_area_size()
        # draw the play_area on the background
        background.blit(play_area, play_area_loc)

        # Write something on each background
        text = self.font.render(play_text, 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        textpos.top += 10
        background.blit(text, textpos)
        background.convert()
        return background

    # returns a set of all backgrounds (Surface, rect) to be used as an 'slow animation'
    def _get_all_backgrounds(self, background_subdirectory, background_header):
        bg_root_dir = 'backgrounds'
        backgrounds = []

        # If a specific sub directory of the background directory was given, append it to bg_root_dir
        if background_subdirectory:
            bg_dir = os.path.join(bg_root_dir, background_subdirectory)
        else:
            bg_dir = bg_root_dir

        # Get a a list of all filenames
        absolute_bg_dir = os.path.join(get_main_dir(), 'data', bg_dir)
        all_bg_filenames = os.listdir(absolute_bg_dir)

        for filename in all_bg_filenames:
            # check if this pathname is a directory: skip
            if os.path.isdir(os.path.join(absolute_bg_dir, filename)):
                continue
            
            # check if files only contain valid fileformats
            if not self._is_file_format_valid(filename):
                print("Invalid file found in ", bg_dir, ": ", filename)
                raise SystemExit()
            
            # Load the image from the system
            bg_image = load_image(os.path.join(bg_dir, filename))[0]

            # Add some final touches like play area and text
            done_background = self._finalize_background(bg_image, background_header)

            backgrounds.append(bg_image)

        return backgrounds

    def _check_for_static_bg(self):
        # When the background folder only contains 1 file
        # meaning it's length is 0 or 1, only this will be displayed
        if len(self.background_list) == 0:
            # Create a background
            background = pygame.display.get_surface()
            # Convert optimizes format for renderspeed
            background = background.convert() 
            background.fill(self.background_color)
            self.background = background
        else:
            self.background = self.background_list[self.current_bg_index]
            

    def update_background(self):
        now = pygame.time.get_ticks()
        
        # Check if its time to update background
        if now - self.last_bg_update_time > self.bg_update_interval_time:
            
            # Set new last background update time to now
            self.last_bg_update_time = now

            # Check if it's time to reset background index
            if self.current_bg_index < len(self.background_list) - 1:
                self.current_bg_index += 1
            else:
                self.current_bg_index = 0

            # Set new background
            self.background = self.background_list[self.current_bg_index]
    
    def _get_background(self):
        return self.background