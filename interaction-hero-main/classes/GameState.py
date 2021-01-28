from utils import load_sound, load_font
from classes.GpioButton import GpioButton
from classes.Hitbox import Hitbox
from classes.ScoreHandler import ScoreHandler
from classes.BackgroundHandler import BackgroundHandler
from classes.MusicPlayer import MusicPlayer
from classes.NoteDropper import NoteDropper
from pygame import font, time


class GameState():

    def __init__(self, allsprites, song):
        self.state = 'prestart'

        self.allsprites = allsprites
        self.keyboard_button = []
        self.song = song

        self.font = load_font(song.get_font_filename(), 36)

        self.notes_are_dropping = False
        self.song_is_finished = False

        # Reads and plays audio from notes files
        self.music_player = MusicPlayer(song, self)

        # Responsible for loading and animating the background
        self.background_handler = BackgroundHandler(song)

        # Assigns falling notes to correct hitbox
        self.note_dropper = NoteDropper(self.music_player)

        # Responsible for managing (high) scores
        self.scoreHandler = ScoreHandler(self.allsprites,self, self.song) 

        # Load sound which plays when a note is missed
        self.sounds_miss = load_sound(song.get_sound_miss())
        
        # Define Hitboxes
        input_keys = ['a', 's', 'd', 'f']
        self.hitboxes = [
            Hitbox('yin-yang.png', 0, input_keys[0], self.allsprites),
            Hitbox('yin-yang.png', 1, input_keys[1], self.allsprites),
            Hitbox('yin-yang.png', 2, input_keys[2], self.allsprites),
            Hitbox('yin-yang.png', 3, input_keys[3], self.allsprites),
        ]


    def restart(self):
        self.state = 'playing'
        self.notes_are_dropping = False
        self.song_is_finished = False
        self.scoreHandler.restart()
        self.music_player.restart()

    def drop_next_note_sprite(self, note):
        
        self.hitboxes
        self.note_dropper.drop(note, self.hitboxes)


    def get_background(self):
        return self.background_handler.background


    def end_song(self):
        self.wait_untill_notes_gone = time.get_ticks() + 2000
        self.song_is_finished = True
        self.notes_are_dropping = True


    def update(self):
        self.background_handler.update_background()

        # While the program is not in the menu it loops through this
        if self.state == 'playing':
            # When the song is done and there are no more notes dropping: go to menu
            if self.song_is_finished and not self.notes_are_dropping:
                self.state = 'prestart'
            # When the song is done and there are notes dropping: wait
            elif self.song_is_finished and self.notes_are_dropping:
                # After some time assume no more notes are dropping
                if self.wait_untill_notes_gone < time.get_ticks():
                    self.notes_are_dropping = False
                    self.state = "end_game"
            # Otherwise (when song is not finished) keep updating
            else:
                self.music_player.update()

        # Menu loop, which simply doesn't run other code
        elif self.state == 'prestart':
            return

    def menu_start(self):
        self.background_handler.update_background()
        self.state = 'prestart'

    def check_for_hit(self, hitbox):
        if hitbox.hits():
            self.scoreHandler.change_score(10)
        else:
            self.sounds_miss.play()
            self.scoreHandler.change_score(-5)


    def add_gpio_pins(self, gpio_pins):
        for i in range(4):
            self.hitboxes[i].gpio_event_key = gpio_pins[i]