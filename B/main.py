from gpiozero import LED, Button, Motor, OutputDevice as OD
from time import sleep
import random
import datetime

def main():
    # Init variablen voor gebruik in game loop
    rode_knop = Button(14)      # Groene Knop
    groene_knop = Button(15)    # Rode knop
    blauwe_knop = Button(4)     # Start knop
    groen_lamp = LED(22)        # Groen LED Kleur
    rood_lamp = LED(27)         # Rood LED Kleur       
    led = LED(22)               # led lampje
    sda_lcd = 2                 # LCD scherm
    scl_lcd = 3                 
    
    control_pins = [12,16,18,22]

    GPIO.setmode(GPIO.BOARD)
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    mp1, mp2, mp3, mp4 = OD(18), OD(23), OD(24), OD(25)
    step_pins = [mp1, mp2, mp3, mp4]
    seq = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]

    step_count = len(seq)
    step_links = 1
    step_rechts = -1
    step_counter = 0
    
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

        if blauwe_knop.is_pressed:
            groen_lamp.on()

            if groene_knop.is_pressed:              #Groene lamp klik event
                groen_lamp.off()                    #Groene lamp uit
                sleep(2)
                mp1.off()

                #Start speel loop
                while speel:
                    
                    teller += 1

                    #Prints voor debuging
                    print(step_counter)

                    kleur = random.choice(["groen", "rood"])    #Selecteer een willekeurige kleur
    
                    if kleur == "rood":
                        rood_lamp.on()
                        print("rodel lamp")
                    else:
                        groen_lamp.on()
                        print("groelne lamp")
                    
                    press = datetime.datetime.now()

                    # Groen knop invoer event.
                    # Checkt of de kleur rood is en voegt punten toe.
                    if groene_knop.is():
                        mp1.on()        #start de motor voor 2 seconden en stop
                        sleep(2)
                        mp1.off()
                        
                        # check als de kleur overheen komt met de de gedrukte knop
                        if kleur == "groen":

                            for halfstep in range(8):
                                for pin in range(4):
                                GPIO.output(control_pins[pin], seq[halfstep][pin])
                                time.sleep(0.001)

                            groen_lamp.off()
                            print("Goed antwoord")
                            #change time
                            change = datetime.datetime.now()
                        else:
                            print("Verkeerd antwoord.")
                            groen_lamp.off()
                            rood_lamp.off()
                            speel = False
                            print(f"Totaal aantal goed: "+str(punten))   # Toon aantal goed beantwoord
                            break               #Stop het spel door verkeerd antwoord
                    
                    # Rood knop invoer event.
                    # Checked als de kleur rood is en voegt punten toe.
                    elif rode_knop.is_pressed:
#moet nog veranderd
                        mp1.on()
                        sleep(2)
                        mp1.off()
                        if kleur == "rood":

                            for pin in range(0, 4):
                               xpin = step_pins[pin]
                               if Seq[step_counter][pin] != 0:
                                   xpin.on()
                               else:
                                   xpin.off()
                            step_counter += step_rechts
                            
                            rood_lamp.off()
                            print("Goed antwoord")
                            #change time
                            change = datetime.datetime.now()
                        else:
                            print("Verkeerd antwoord.")
                            groen_lamp.off()
                            rood_lamp.off()
                            speel = False
                            print(f"Totaal aantal goed: "+str(punten))   #aantal toont goed beantwoorde/Toon aantal goed beantwoord
                        break                                       #Stolp het splel door verkeerd antwoord

                    #restart de sequence
                    if (step_counter>=step_count):
                        step_counter = 0
                    if (step_counter<0):
                        step_counter = step_count+step_links

                else:       
                    #Iets ging fout. Kom niet in de spel loop.
                    print("Verkeerde invoer. Gebruiker komt niet in speel loop.")
                    print("-----")
                    sleep(2)
                
            #PUNTEN BEREKENINGING.
            if groene_knop.is_pressed or rode_knop.is_pressed:          #Groen of rood ingedrukt
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

    GPIO.cleanup()

if __name__ == "__main__":
    main()
