import pygame.midi
import pygame
import utils
import os

class MusicPlayer():
    def __init__(self, song, game_state_ref):
        self.bpm = song.get_notes_bpm()
        self.game_state = game_state_ref

        self.drop_next_note_callback = self.game_state.drop_next_note_sprite
        
        self.maten = {
            "ACHTSTE": 30/self.bpm,
            "KWART": 60/self.bpm,
            "HALVE": 120/self.bpm,
            "HELE": 240/self.bpm
        }

        # All notes based of the MIDI standard
        self.noten = {
            "A0":  21,
            "A0#": 22,
            "B0":  23,
            "C1":  24,
            "C1#": 25,
            "D1":  26,
            "D1#": 27,
            "E1":  28,
            "F1":  29,
            "F1#": 30,
            "G1":  31,
            "G1#": 32,
            "A1":  33,
            "A1#": 34,
            "B1":  35,
            "C2":  36,
            "C2#": 37,
            "D2":  38,
            "D2#": 39,
            "E2":  40,
            "F2":  41,
            "F2#": 42,
            "G2":  43,
            "G2#": 44,
            "A2":  45,
            "A2#": 46,
            "B2":  47,
            "C3":  48,
            "C3#": 49,
            "D3":  50,
            "D3#": 51,
            "E3":  52,
            "F3":  53,
            "F3#": 54,
            "G3":  55,
            "G3#": 56,
            "A3":  57,
            "A3#": 58,
            "B3":  59,
            "C4":  60,
            "C4#": 61,
            "D4":  62,
            "D4#": 63,
            "E4":  64,
            "F4":  65,
            "F4#": 66,
            "G4":  67,
            "G4#": 68,
            "A4":  69,
            "A4#": 70,
            "B4":  71,
            "C5":  72,
            "C5#": 73,
            "D5":  74,
            "D5#": 75,
            "E5":  76,
            "F5":  77,
            "F5#": 78,
            "G5":  79,
            "G5#": 80,
            "A5":  81,
            "A5#": 82,
            "B5":  83,
            "C6":  84,
            "C6#": 85,
            "D6":  86,
            "D6#": 87,
            "E6":  88,
            "F6":  89,
            "F6#": 90,
            "G6":  91,
            "G6#": 92,
            "A6":  93,
            "A6#": 94,
            "B6":  95,
            "C7":  96,
            "C7#": 97,
            "D7":  98,
            "D7#": 99,
            "E7":  100,
            "F7":  101,
            "F7#": 102,
            "G7":  103,
            "G7#": 104,
            "A7":  105,
            "A7#": 106,
            "B7":  107,
            "C8":  108
        }

        # Start MIDI server
        if utils.is_running_on_rpi():
            self.start_midi_server()

        # Pygame MIDI init
        pygame.midi.init()

        default_output_id = pygame.midi.get_default_output_id()
        if default_output_id != -1:
            if utils.is_running_on_rpi():
                # Setting output on 2 on RPi is required for using Timidity
                self.player = pygame.midi.Output(2)
            else:
                self.player = pygame.midi.Output(default_output_id)
        else:
            print('No audio devices found! Closing program...')
            quit()

        # Change this in case you want hit notes to make different sounds
        self.player.set_instrument(10)  

        # Load all the notes from the notes file
        self.liedje = self._read_file(song.get_notes_filename())

        self.song_length = len(self.liedje)

        # Set up the initial variables (which reset after a restart)
        self.note_index = 0
        self.current_note = self.noten[self.liedje[self.note_index][0]]
        self.current_maat = self.maten[self.liedje[self.note_index][1]]
        self.previous_note = 0
        self.time_since_last_hit = 0

        self.first_run = True
        self.song_done = False

        # Set the next start a few moments later so the notes can drop
        initial_delay_ms = 1000
        self.next_note_start_time = pygame.time.get_ticks() + initial_delay_ms


    def restart(self):
        self.note_index = 0
        self.current_note = self.noten[self.liedje[self.note_index][0]]
        self.current_maat = self.maten[self.liedje[self.note_index][1]]
        self.previous_note = 0
        self.time_since_last_hit = 0

        self.first_run = True
        self.song_done = False
        
   
    def play_note(self, note):
        # This check prevents double hits within 100ms
        if self.time_since_last_hit < pygame.time.get_ticks() - 100:
            self.player.note_off(self.previous_note)
            midi_note = self.noten[note[0]]
            self.player.note_on(midi_note, 127)
            self.previous_note = midi_note
            self.time_since_last_hit = pygame.time.get_ticks()
        

    def check_for_next_note(self):
        # check if its time to play the next note
        if pygame.time.get_ticks() > self.next_note_start_time:
            # if so, play it and set the next start time
            self.update_current_note()
            self.next_note_start_time = pygame.time.get_ticks() + self.current_maat * 1000


    def update_current_note(self):
        if self.note_index >= self.song_length - 1:
            self.game_state.end_song()
            self.song_done = True
            return
        elif self.first_run:
            # dont increase the note_index here since otherwise it skips the first note
            self.first_run = False
        else:
            self.note_index += 1
        self.current_note = self.noten[self.liedje[self.note_index][0]]
        self.current_maat = self.maten[self.liedje[self.note_index][1]]

        # at the end play next note
        self.drop_next_note_callback(self.liedje[self.note_index])


    def update(self):
        if not self.song_done:
            self.check_for_next_note()


    def set_instrument(self, instrument):
        self.player.set_instrument(instrument)


    def start_midi_server(self):
        import subprocess, time
        # See if timidity is already running
        result = subprocess.run(['pgrep', 'timidity'], stdout=subprocess.PIPE)
        if len(result.stdout) > 0:
            # Timidity is already running
            return
        print('Starting timidity...')
        os.system('timidity -iA &')
        time.sleep(1)
        return


    def _read_file(self, filename):
        liedje = None
        songpath = os.path.join(utils.get_main_dir(), 'data', filename)

        with open(songpath) as f:
            liedje = f.read()

        liedje = liedje.strip().split("\n")

        teller = 0
        for i in liedje:
            liedje[teller] = i.split(" ")
            teller+=1

        return liedje
