# GENERAL #
These files are a stripped down version of the game 'Interaction Hero'.
This means that to run it you need to complete the missing or incomplete 
parts of the code, otherwise it will not run. 
You can find most information on how the code works in the comments
spread throughout the different files.


# SCORES #
Your scores will be printed in the console and written to scores.txt 
(labelled as the notes_filename value) after you complete playing your first song. 
If this file doesn't exist it will be created automatically. 
This scores.txt file won't be included in any git repositories, 
so scores are saved locally. Feel free to add or change any off these functionalities.


# WINDOWS #
For development on windows you need the following installed:
- Python 3 https://www.python.org/
- Pygame https://www.pygame.org/
Beware, you CAN install pygame 2 (which is released recently) but this does
not come pre-installed on Raspberry Pi OS. Most Pygame 2 functions also work 
in Pygame 1.9 but beware of this risk. 


# RASPBERRY PI #
For running on Raspberry Pi OS you need the following installed:
- Python 3 (comes pre-installed)
- Pygame 1.95+ (comes pre-installed)
- gpiozero (comes pre-installed) https://gpiozero.readthedocs.io/en/stable/
- TiMidity++ (needs installing!) https://wiki.archlinux.org/index.php/Timidity%2B%2B

To run the app make sure above are all installed. This means after installing TiMidity 
the app should run without issues on a fresh Raspberry Pi OS installation. 
Use python3 ($~ python3) instead of python2 ($~ python). 
Sometimes prefixing the command with 'sudo' is also required.


# CREDITS # 
Main Author: Jaap Kanbier - kanbier.j@hsleiden.nl
Support Author: Jeroen de Meij - meij.de.j@hsleiden.nl