#from gpiozero import LED, Button, Motor, OutputDevice as OD
from time import sleep
import random

def main():
    # Init variablen voor gebruik in game loop
    # rode_knop = Button(14)      # Groene Knop
    # groene_knop = Button(15)    # Rode knop
    # blauwe_knop = Button(4)     # Start knop
    # groen_lamp = LED(22)       # Groen LED Kleur
    # rood_lamp = LED(27)        # Rood LED Kleur       
    # led = LED(22)               # led lampje
    # sda_lcd = 2                 # LCD scherm
    # scl_lcd = 3                 

#komende 3 regels voor testen
    rode_knop = 'r'
    groene_knop = 'g'
    blauwe_knop = 'b'
    
#    mp1, mp2, mp3, mp4 = OD(18), OD(23), OD(24), OD(25)
#        [0,1,0,0],
#        [0,1,1,0],
#        [0,0,1,0],
#        [0,0,1,1],
#        [0,0,0,1],
#        [1,0,0,1]
#    ]
#    step_count = len(seq)
#    stepDir = 1
    step_counter = 0
    step_count = 3
    moeilijkheids_graad = 0.8  #elke moeilijker ronde wordt snelheid s gelijk aan 0.75s
    moelijker = 5   #na 5 rondes wordt het spel moeilijker
    teller = 0  #hoeveelste ronde waar het programma in zit

    speel = True
    punten = 0
    
    start = True
    while start:
        teller = teller + 1
        print("Begin spel")
        # Start het spel op door de blauw knop te drukken
        knop = input()
        
        if knop == 'b':
            print("groene kleur")
            knop = input()
            if knop == 'g':
#                groen_kleur.off()
#                mp1.on()        #start de motor voor 2 seconden en stop
                print("rechtsom draaien")
                sleep(2)
#                mp1.off()
                print("rechtsom stop")

                #Start speel loop
                while speel:
                    
                    #Prints voor debuging
                    print(step_counter)
                    if kleur == "rood":
#                        rood_lamp.on()
                        print("rode lamp")
                    else:
#                        groen_lamp.on()
                        print("groene lamp")

                    
                    # Start de timer
                    start = datetime.datetime.now()
                    press = datetime.datetime.now()
                    diff = press - start



#                        groen_kleur.off()
#                        mp1.on()        #start de motor voor 2 seconden en stop
                        print("rechtsom draaien")
                        sleep(2)
#                       mp1.off()
                        print("rechtsom stop")
                        if kleur == "groen":
#                            for pin in range(0, 4):
#                                xpin = step_pins[pin]
#                                if Seq[step_counter][pin] != 0:
#                                    xpin.on()
#                                else:
#                                    xpin.off()
#                            step_counter += stepDir

#                            groen_kleur.off()
                            print("Goed antwoord.")
                        else:
                            print("Verkeerd antwoord.")
 #                           groen_lamp.off()
 #                           rood_lamp.off()
                            speel = False
                            print(f"totaal aantal goed: "+punten)   # Toon aantal goed beantwoord
                            break               #Stop het spel door verkeerd antwoord
                    
                    # Rood knop invoer event.
                    # Checked als de kleur rood is en voegt punten toe.
                    elif knop == 'r':
                        print("linksom draaien")
                        sleep(2)
                        print("linksom draaien stop")
                        if kleur == "rood":
                            # Haal de tijd 
                            # press = datetime.datetime.now()

#                            for pin in range(0, 4):
#                                xpin = step_pins[pin]
#                                if Seq[step_counter][pin] != 0:
#                                    xpin.on()
#                                else:
#                                    xpin.off()
#                            step_counter += stepDir

                            print("Goed antwoord.")
                        else:
                            print("Verkeerd antwoord.")
#                            groen_kleur.off()
#                            rood_kleur.off()
                            speel = False
                            print(f"totaal aantal goed: " + punten) # Toon aantal goed beantwoord
                            break               #Stop het spel door verkeerd antwoord

                    #restart de sequence
                    if (step_counter>=step_count):
                        step_counter = 0
                    if (step_counter<0):
                        step_counter = step_count+stepDir

            else:       
                #Gebruiker had verkeerd antwoord gegeven.
                print("Verkeerd invoer")
                print("-----")


#            if groene_knop.is_pressed or rode_knop.is_pressed:
            knop = input()
            if knop == 'g' or knop == 'r':
                x = [speel_tijd]  
                max_x = max(x)   
                punten = []
                punten = punten + 100 * (1000 - max_x)
                if punten > 0 and max_x < 1:
#                   lcd.write_int(punten)
                    print(sum(punten))

        else:
            print("Druk op de blauwe knop om het spel te starten")

if __name__ == "__main__":
    main()


