from pygame import sprite, font
from utils import load_font

class ScoreHandler(sprite.Sprite):
    def __init__(self, allsprites, game_state, song):
        sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.font = load_font(song.get_font_filename(), 36)

        self.score = 0

        # Feel free to play around with these variables
        # Currently they are not used anywhere in the code
        self.score_streak = 0
        self.score_multiplier = 1

        # Required to make sure the first note hits correctly
        self.played_once = False

        # Flag to see when a score should be saved after an update
        self.score_is_saved = True

        # Required Sprite attributes
        self.image = self.font.render('', 1, (10, 10, 10))
        self.pos = (590, 50)  # Set the location of the text
        self.rect = (self.pos, self.image.get_size())


    def restart(self):
        self.score = 0
        self.score_streak = 0
        self.score_multiplier = 1
        self.score_is_saved = False


    def get_score_text_to_blit(self):
        self.score_text = self.font.render('Score: ' + str(self.score), 1, (10, 10, 10))
        return self.score_text, self.score_text_pos

    # This is called every frame
    def update(self):
        if self.game_state.state == 'playing':
            # print('Current score: ' + str(self.score))
            pass
        elif self.played_once == True:
            # print('Your final score: ' + str(self.score))
            pass

        if not self.game_state.state == 'playing' and not self.score_is_saved:
            self.save_score()

    def change_score(self, score_difference):
        self.score += score_difference
        
    def get_high_score(self):
        played_song = self.game_state.song.get_notes_filename()
        best_score = None
        with open('scores.txt', 'r') as f:
            scores = f.read().splitlines(False)
            for score in scores:
                songdata = score.split(' ')
                songname = songdata[0]
                songscore = int(songdata[1])
                if songname == played_song and (best_score == None or songscore > best_score):
                    best_score = songscore
        return best_score

    def get_top5_high_score():
        best_scores = []
        with open('scores.txt', 'r') as f:
            scores = f.read().splitlines(False)
            for score in scores:
                songdata = score.split(' ')
                best_scores.append(int(songdata[1]))
                best_scores = sorted(best_scores, reverse=True)
        return best_scores[:5]
    
    def save_score(self):
        self.score_is_saved = True
        self.played_once = True
        with open('scores.txt', 'a') as f:
            text = self.game_state.song.get_notes_filename() + ' ' + str(self.score) + '\n'
            f.write(text)
        print('The highscore is', self.get_high_score(), '- See ScoreHandler.py for new implementation')
        print('Your score is', self.score, '- See ScoreHandler.py for new implementation')
