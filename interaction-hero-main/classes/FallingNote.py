import random
import pygame
from utils import load_image
from math import floor

class FallingNote(pygame.sprite.Sprite):
    def __init__(self, lane_i, allsprites, music_player_ref, note):
        pygame.sprite.Sprite.__init__(self, allsprites)  # call Sprite intializer
        self.allsprites = allsprites
        self.music_player_ref = music_player_ref
        self.note = note
        
        self.lane_index = lane_i
        self.image, self.rect = load_image(random.choice(["vijand-1.png", "vijand-2.png", "vijnand-3.png", "vijand-5.png"]), -1)
        self.image, self.rect = load_image(random.choice(["musicnote-example.png", "hitbox-example.png"]), -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()  # ONLY USE THIS TO CHECK IT HAS FALLEN OF SCREEN
        self.rect.topleft = self._new_start_pos()
        self.move = 10 # this defines it's falling speed
        self.shrinking = 0
        self.destroyed = False
        self.is_hit = False


    def _new_start_pos(self):
        window_size = (1280, 720)
        posx = self.lane_index * 110 + 420
        posy = -self.rect.height
        return posx, posy


    def update(self):
        """walk or shrink, depending on the note state"""
        if self.destroyed:
            self.allsprites.remove(self)
        elif self.shrinking:
            self.shrink()
        else:
            self._fall()

    def destroy_self(self):
        newpos = self.rect.topleft = (-500, -500)
        self.destroyed = True


    def _fall(self):
        newpos = self.rect.move((0, self.move))
        if not self.area.contains(newpos):
            if self.rect.top > self.area.bottom:
                self.destroy_self()
                return
        self.rect = newpos

    def shrink(self):
        self.is_hit = True
        if self.rect.width < 21:
            self.destroy_self()
        else:
            self.rect.inflate_ip(-20, -20)
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))


    def hit(self):
        self.music_player_ref.play_note(self.note)
        if not self.shrinking:
            self.shrinking = 1

    def is_hit(self):
        return self.is_hit
