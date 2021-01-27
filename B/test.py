#from gpiozero import LED, Button, Motor, OutputDevice as OD
from time import sleep
import random
import datetime

def main():

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     # Init variablen voor gebruik in game loop
#     rode_knop = Button(14)      # Groene Knop
#     groene_knop = Button(15)    # Rode knop
#     blauwe_knop = Button(4)     # Start knop
#     groen_lamp = LED(22)        # Groen LED Kleur
#     rood_lamp = LED(27)         # Rood LED Kleur       
#     led = LED(22)               # led lampje
#     sda_lcd = 2                 # LCD scherm
#     scl_lcd = 3                 
    
#     mp1, mp2, mp3, mp4 = OD(18), OD(23), OD(24), OD(25)
#     step_pins = [mp1, mp2, mp3, mp4]
#     seq = [
#         [1,0,0,0],
#         [1,1,0,0],
#         [0,1,0,0],
#         [0,1,1,0],
#         [0,0,1,0],
#         [0,0,1,1],
#         [0,0,0,1],
#         [1,0,0,1]
#     ]

#     GPIO.setup(enable_pin, GPIO.OUT)
#     GPIO.setup(18, GPIO.OUT)
#     GPIO.setup(23, GPIO.OUT)
#     GPIO.setup(24, GPIO.OUT)
#     GPIO.setup(25, GPIO.OUT)
 
#     GPIO.output(enable_pin, 1)

#     def setStep(w1, w2, w3, w4):
#         GPIO.output(18, w1)
#         GPIO.output(23, w2)
#         GPIO.output(24, w3)
#         GPIO.output(25, w4)
 
#     def forward(delay, steps):
#         for i in range(steps):
#             for j in range(StepCount):
#                 setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
#                 time.sleep(delay)
    
#     def backwards(delay, steps):
#         for i in range(steps):
#             for j in reversed(range(StepCount)):
#                 setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
#                 time.sleep(delay)

#     step_count = len(seq)
#     step_links = 1
#     step_rechts = -1
#     step_counter = 0

    speel = True
    punten = 0
    start = True

    moeilijkheids_graad = 0.8   #elke moeilijker rondes wordt snelheid s die de gebruiker heeft om te klikken gelijk aan 0.8s
    moeilijker = 2              #na dit aantal rondes wordt het spel moeilijker
    teller = 0                  #hoeveelste ronde waar het programma in zit
    maximale_tijd = 1000        #begint met 1 seconde, steeds korter. In milliseconden.

    while start:
        delay = 1000
        
        print("Begin spel. Druk op de blauwe knop.")

        knop = input()
        if knop == 'b':
#        if blauwe_knop.is_pressed:
            print("groene lamp aan")
#            groen_lamp.on()

#            if groene_knop.is_pressed:              #Groene lamp klik event
            knop = input()
            if knop == 'g':
#                groen_lamp.off()                    #Groene lamp uit
#                forward(100, 10)
#                sleep(2)
#                mp1.off()
                print("forward")

                #Start speel loop
                while speel:
                    
                    teller += 1

                    #Prints voor debuging
                    # print(step_counter)

                    kleur = random.choice(["groen", "rood"])    #Selecteer een willekeurige kleur
    
                    if kleur == "rood":
#                        rood_lamp.on()
                        print("rodel lamp")
                    else:
#                        groen_lamp.on()
                        print("groelne lamp")
                        
                    press = datetime.datetime.now()
                    # Groen knop invoer event.
                    # Checkt of de kleur rood is en voegt punten toe.
#                    if groene_knop.is():
                    knop2 = input()
                    if knop2 == 'g':
#                        forward(100, 10)
#                        mp1.on()        #start de motor voor 2 seconden en stop
#                        sleep(2)
#                        mp1.off()
                        print("forward")
                        
                        # check als de kleur overheen komt met de de gedrukte knop
                        if kleur == "groen":

                            # for pin in range(0, 4):
                            #    xpin = step_pins[pin]
                            #    if Seq[step_counter][pin] != 0:
                            #        xpin.on()
                            #    else:
                            #        xpin.off()
                            # step_counter += step_links

#                            groen_lamp.off()
                            print("groene lamp uit")
                            print("Goed antwoord")
                            #change time
                            change = datetime.datetime.now()
                        else:
                            print("Verkeerd antwoord.")
                            # groen_lamp.off()
                            # rood_lamp.off()

                            print("alle lampen uit")
                            speel = False
                            print(f"Totaal aantal goed: "+str(punten))   # Toon aantal goed beantwoord
                            break               #Stop het spel door verkeerd antwoord
                    
                    # Rood knop invoer event.
                    # Checked als de kleur rood is en voegt punten toe.
#                    elif rode_knop.is_pressed:
                    elif knop == 'r':
#moet nog veranderd
                        # mp1.on()
                        # sleep(2)
                        # mp1.off()

                        print("motor")
                        if kleur == "rood":

                            # for pin in range(0, 4):
                            #    xpin = step_pins[pin]
                            #    if Seq[step_counter][pin] != 0:
                            #        xpin.on()
                            #    else:
                            #        xpin.off()
                            # step_counter += step_rechts
                            
#                            rood_lamp.off()
                            print("rode lamp uit")
                            print("Goed antwoord")
                            #change time
                            change = datetime.datetime.now()
                        else:
                            print("Verkeerd antwoord.")
#                            groen_lamp.off()
#                            rood_lamp.off()
                            print("alle lampen uit")
                            speel = False
                            print(f"Totaal aantal goed: "+str(punten))   #aantal toont goed beantwoorde/Toon aantal goed beantwoord
                        break                                       #Stolp het splel door verkeerd antwoord

                    #restart de sequence
                    # if (step_counter>=step_count):
                    #     step_counter = 0
                    # if (step_counter<0):
                    #     step_counter = step_count+step_links

                else:       
                    #Iets ging fout. Kom niet in de spel loop.
                    print("Verkeerde invoer. Gebruiker komt niet in speel loop.")
                    print("-----")
                    sleep(2)
                
            #PUNTEN BEREKENINGING.
#            if groene_knop.is_pressed or rode_knop.is_pressed:          #Groen of rood ingedrukt
            knop = input()
            if knop == 'g' or knop == 'r':
                                                      #change_milli = change in microseconden/milliseconden
                diff = press - change                 #Verschil tussen press_milli en change_milli in microseconden/milliseconden
                millisec = (diff.days * 24 * 60 * 60 + diff.seconds) * 1000 + diff.microseconds / 1000.0 # Stackoverflow ;-; Het werkt :o
                print("Hoelang je erover deed: " + millisec)

            if teller % moeilijker == 0:
                maximale_tijd = maximale_tijd * moeilijkheids_graad
            if millisec <= maximale_tijd:
                punten_lijst = []
                punten_lijst.append(millisec)
                print(sum(punten_lijst))

        else:
            print("Spel niet gestart")

if __name__ == "__main__":
    main()
