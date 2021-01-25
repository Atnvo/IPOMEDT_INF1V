import os

class Song():
    def __init__(
        self, 
        notes_filename,
        notes_bpm=120,
        font_filename=None,

        # Use this in case you want to specify a specific subdir 
        # like for example 'backgrounds/dance'
        # Otherwise leave as None
        bg_image_dir=None,  
        bg_image_interval_ms = 1000,
        bg_game_header='Hit the notes!',

        sound_miss='sound_fail.wav',
    ):
        self.bg_image_dir = bg_image_dir
        self.bg_image_interval_ms = bg_image_interval_ms
        self.bg_game_header = bg_game_header
        self.sound_miss = sound_miss
        self.notes_filename = notes_filename
        self.notes_bpm = notes_bpm
        self.font_filename = font_filename


    def get_font_filename(self):
        return self.font_filename


    def get_sound_miss(self):
        return self.sound_miss


    def get_bg_image_dir(self):
        return self.bg_image_dir

    
    def get_bg_image_interval_ms(self):
        return self.bg_image_interval_ms


    def get_bg_game_header(self):
        return self.bg_game_header

    
    def get_notes_filename(self):
        return self.notes_filename


    def get_notes_bpm(self):
        return self.notes_bpm


    def get_input_keys(self):
        return self.input_keys