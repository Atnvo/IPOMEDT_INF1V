from gpiozero import LED, Button, Motor, OutputDevice as Step
from time import sleep
import random

def game_loop():
    print("game loop")

def main():
    #Init variablen voor gebruik in game loop
    rode_knop = Button(14)      # Groene Knop
    groene_knop = Button(15)    # Rode knop
    blauwe_knop = Button(4)     # Start knop
    groen_kleur = LED(22)       # Groen LED Kleur
    rood_kleur = LED(27)        # Rood LED Kleur       
    led = LED(22)               # led lampje
    sda_lcd = 2                 # LCD scherm
    scl_lcd = 3                 

    mp1, mp2, mp3, mp4 = Step(18), Step(23), Step(24), Step(25)

    speel = True
    punten = 0

    # Timer functie die aangeroepen word als een aparte thread bij een vraag.
    def timer():
        for i in range(random.randint(2, 5)):
            if stop():
                break
            sleep(1)
        sys.exit("Te laatte invoer. Probeer opnieuw")
    
    # Start het spel op door de blauw knop te drukken
    if blauwe_knop.is_pressed:
        groen_kleur.on()
        if groen_kleur.is_pressed:
            groen_kleur.off()
            mp1.on()        #start de motor voor 2 seconden en stop
            sleep(2)
            mp1.off()

            #Start speel loop
            while Speel:
                tijd = Thread(target=timer, args=(lambda: stop_tijd,))
                kleur = random.choice(["groen", "rood"])    #Selecteer een willikeurige kleur
                if kleur == "rood":
                    rood_kleur.on()
                else:
                    groen_kleur.on()
                tijd.start()

                # Groen knop invoer event.
                # Checked als de kleur rood is en voegt punten toe.
                if groen_kleur.is_pressed:
                    if kleur == "groen":
                        stop_tijd = True    # stop de tijd
                        punten += 1         # Voeg een punt to aan totaal
                        mp1.on()
                        timer(2)
                        mp1.off()
                        groen_kleur.off()
                    else:
                        print("Verkeerd antwoord.")
                        groen_kleur.off()
                        rood_kleur.off()
                        Speel = False
                        print(f"totaal aantal goed: "+punten)   # Toon aantal goed beantwoord
                        break               #Stop het spel door verkeerd antwoord
                
                # Rood knop invoer event.
                # Checked als de kleur rood is en voegt punten toe.
                elif rood_kleur.is_pressed:
                    if kleur == "rood":
                        stop_tijd = True    # stop de tijd
                        punten += 1         # Voeg een punt to aan totaal
                        mp1.on()
                        timer(2)
                        mp1.off()
                        print("Goed antwoord")
                    else:
                        print("Verkeerd antwoord.")
                        groen_kleur.off()
                        rood_kleur.off()
                        Speel = False
                        print(f"totaal aantal goed: "+punten) # Toon aantal goed beantwoord
                        break               #Stop het spel door verkeerd antwoord
        else:       
            #Gebruiker had verkeerd antwoord gegeven.
            print("Verkeerd invoer")
    else:
        print("Druk op de bluawe knop om het spel te starten")
            

if __name__ == "__main__":
    main()