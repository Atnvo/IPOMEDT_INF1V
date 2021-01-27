from gpiozero import LED, Button, Motor, OutputDevice as OD
from time import sleep
import random
import datetime

def main():
    # Init variablen voor gebruik in game loop
    r_knop = Button(14)         # Groene Knop
    g_knop = Button(15)         # Rode knop
    b_knop = Button(4)          # Start knop
    g_lamp = LED(22)            # Groen LED Kleur
    r_lamp = LED(27)            # Rood LED Kleur       
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
    
#LCD scherm aanmaken
    lcd_rs        = 25 
    lcd_en        = 24
    lcd_d4        = 23
    lcd_d5        = 17
    lcd_d6        = 18
    lcd_d7        = 22
    lcd_backlight = 4
    lcd_columns = 16
    lcd_rows = 2

    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)    
    
    speel = True
    punten = 0
    start = True

    moeilijkheids_graad = 0.8   #elke moeilijker rondes wordt snelheid s die de gebruiker heeft om te klikken gelijk aan 0.8s
    moeilijker = 2              #na dit aantal rondes wordt het spel moeilijker
    teller = 0                  #hoeveelste ronde waar het programma in zit
    maximale_tijd = 1000        #begint met 1 seconde, steeds korter. In milliseconden.
    min_tijd = 2                #minimale tijd dat verstreken is voor een lampje aangaat
    max_tijd = 5                #maximale tijd dat verstreken is voor een lampje aangaat

    while start:
        delay = 1000
        
        lcd.message("Begin met blauw./nPunten: 0")
        
        print("Begin spel. Druk op de blauwe knop.")

        if b_knop.is_pressed:                              
            sleep(random.randint(min_tijd,max_tijd))             #  Random tijnd wanneer de lamp aan gaat
            g_lamp.on()                         #1. Groen lamp gaat aan

            if g_knop.is_pressed:               #2. Groene lamp klik event 
                g_lamp.off()                    #Groene lamp uit

                # 3. Motor gaat aan
                for halfstep in range(8):
                    for pin in range(4):
                    GPIO.output(control_pins[pin], seq[halfstep][pin])
                    sleep(0.001)

                #Start speel loop
                while speel:
                    teller += 1

                    # Moel
                    if teller % moeilijker == 0:
                        min_tijd = min_tijd * moeilijkheids_graad
                        max_tijd = max_tijd * moeilijkheids_graad

                    #Prints voor debuging
                    print(step_counter)
#;-;
                    kleur = random.choice(["groen", "rood"])    #Selecteer een willekeurige kleur
    
                    if kleur == "rood":
                        sleep(random.randint(min_tijd,max_tijd)) # 4. Lamp gaat aan 
                        r_lamp.on()
                        print("rode lamp")
                    else:
                        sleep(random.randint(min_tijd,max_tijd)) 
                        g_lamp.on()
                        print("groene lamp")
                    
                    press = datetime.datetime.now()

                    # Groen knop invoer event.
                    if g_knop.is_pressed():
                        
                        # check als de kleur overheen komt met de de gedrukte knop
                        if kleur == "groen":
                            change = datetime.datetime.now() #change time \

                            if change - press > 1: # Als de gebruiker te langzaam is.
                                lcd.clear()
                                lcd.message("Game over./nPunten: " + str(sum(punten)))
                                break
                            g_lamp.off()
                        
                            # Motor systeem versie 2
                            for halfstep in range(8):
                                for pin in range(4):
                                GPIO.output(control_pins[pin], seq[halfstep][pin])
                                sleep(0.001)
                            
                            print("Goed antwoord")

                        else:
                            lcd.clear()
                            lcd.message("Game over")
                            g_lamp.off()
                            r_lamp.off()
                            speel = False
                            print(f"Totaal aantal goed: "+str(punten))   # Toon aantal goed beantwoord
                            break               #Stop het spel door verkeerd antwoord
                    
                    # Rood knop invoer event.
                    # Checkt of de kleur rood is en voegt punten toe.
                    elif r_knop.is_pressed:
                        if kleur == "rood":
                            r_lamp.off()                            
                            #change time
                            change = datetime.datetime.now()

                            if change - press > 1: # Als de gebruiker te langzaam is.
                                lcd.clear()
                                lcd.message("Game over./nPunten: " + str(sum(punten)))
                                break

                            # Motor systeem versie 1
                            for pin in range(0, 4):
                               xpin = step_pins[pin]
                               if Seq[step_counter][pin] != 0:
                                   xpin.on()
                               else:
                                   xpin.off()
                            step_counter += step_rechts
                            

                            print("Goed antwoord")

                        else:
                            g_lamp.off()
                            r_lamp.off()
                            speel = False
                            lcd.clear()
                            lcd.message("Game over./nPunten: " + str(sum(punten)))
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
                    sleep(2)
                
            #PUNTEN BEREKENINGING.
            if r_knop.is_pressed or g_knop.is_pressed:          #Groen of rood ingedrukt
                                                      
                diff = change - press                 #Verschil tussen press en change in microseconden/milliseconden
                millisec = (diff.days * 24 * 60 * 60 + diff.seconds) * 1000 + diff.microseconds / 1000.0 # Stackoverflow ;-; Het werkt :o
                print("Hoelang je erover deed: " + millisec)

            if teller % moeilijker == 0:
                maximale_tijd = maximale_tijd * moeilijkheids_graad
            if millisec <= maximale_tijd:
                punten_lijst = []
                punten_lijst.append(millisec)
                lcd.clear()
                lcd.message("Punten: " + str(sum(punten_lijst)))
                print(sum(punten_lijst))

        else:
            print("Spel niet gestart")

    GPIO.cleanup()

if __name__ == "__main__":
    main()
