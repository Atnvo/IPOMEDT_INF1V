import platform, os, pygame

# loads image resources, takes a filename as arg
# when colorkey has argument -1 the background will be made transparant based of topleft pixel
def load_image(name, colorkey=None):
    data_dir = os.path.join(get_main_dir(), 'data')
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


# loads sound resources
def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    # Return a mute soundplayer when mixer is unavailable
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    data_dir = os.path.join(get_main_dir(), 'data')
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound

def load_font(fontname, fontsize):
    if fontname is None:
        return pygame.font.Font(None, fontsize)
    else:
        fontpath = os.path.join(get_main_dir(), 'data', fontname)
        return pygame.font.Font(fontpath, fontsize)
    

def is_running_on_rpi():
    return platform.uname()[0] != 'Windows'


def get_main_dir():
    return os.path.split(os.path.abspath(__file__))[0]
    