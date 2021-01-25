class NoteDropper():
    def __init__(self, music_player_ref):
        self.music_player_ref = music_player_ref

        # Defines where notes drop based of the note value
        # 1 == a note falls, 0 == no note falls
        self.note_combinations = {
            "C": [1, 0, 0, 0],
            "D": [1, 1, 0, 0],
            "E": [0, 1, 0, 0],
            "F": [0, 1, 1, 0],
            "G": [0, 0, 1, 0],
            "A": [0, 0, 1, 1],
            "B": [0, 0, 0, 1],
        }

    
    def drop(self, note, hitboxes):
        key = note[0][0]
        index = 0
        for drop_check in self.note_combinations[key]:
            if drop_check:
                hitboxes[index].drop_new_note(self.music_player_ref, note)
            index += 1