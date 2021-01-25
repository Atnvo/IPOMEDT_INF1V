import pygame
from utils import load_image
from classes.FallingNote import FallingNote
from math import floor


class Hitbox(pygame.sprite.Sprite):
    """the area a note should be in when trying to hit"""

    def __init__(self, image_name, lane_index, event_key, allsprites):
        pygame.sprite.Sprite.__init__(self, allsprites)  # call Sprite initializer

        # The key the hitbox is registered to
        self.event_key = event_key
        self.gpio_event_key = None

        # Which lane this hitbox is drawn in
        self.lane_index = lane_index

        # Setup the required Sprite attributes (image and rect)
        self.image, self.rect = load_image(image_name)
        self.rect.bottomleft = ((420 + 110 * self.lane_index), 720)
        self.orgLoc = self.rect.bottomleft
        self.is_hitting = 0
        self.isPressed = False
        self.allsprites = allsprites

        # Every hitbox has its own set of falling notes
        self.notes = []


    def update(self):
        # When the hitbox is used it moves a little
        if self.is_hitting and not self.isPressed:
            if self.rect.bottom < self.orgLoc[1]+10:
                self.rect.move_ip(0, 5)
            self.pressed = False
        # Otherwise it returns to the original location
        else:
            self.pressed = True
            self.rect.bottomleft = self.orgLoc


    def hits(self):
        """returns true if the hitbox collides with the target(musicnote)"""
        if not self.is_hitting:
            self.is_hitting = 1
            for note in self.notes:
                if self.rect.colliderect(note.rect):
                    note.hit()
                    return True


    def unpunch(self):
        """called to pull the fist back --- also seems to prevent keyboard abuse?"""
        self.is_hitting = 0

    
    def drop_new_note(self, music_player_ref, note):
        self.notes.append(FallingNote(self.lane_index, self.allsprites, music_player_ref, note))
        