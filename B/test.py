import time 
import random

def speel_loop():
    speel = True
    while speel:
        print("test")
        rand_time = random.randint(2,5)         #genereer een getal tussen 2,5
        time.sleep(rand_time)                   #----

    
def main():
    # 1. Verander kleur van het lampje naar groet
    #
    speel_loop() # start de speel loop


if __name__ == "__main__":
    main()
\//////////////////////////////////////////////////

from gpiozero import LED, Button, Motor
import RPi.GPIO as GPIO
import time # Gezien online.
import random

#Na 2 tot 5 seconden kleurt de RGB-led rood. (De tijd is iedere keer willekeurig)
#variable.sleep(float) geeft een delay

rode_knop = Button(14)      # Groene Knop
groene_knop = Button(15)    # Rode knop
b_knop = Button(4)          # Start
led = LED(22)               # led lampje
motor = Motor(forward=4, backward=4)

GPIO.output(15,0)
GPIO.output(13,0)

#https://gpiozero.readthedocs.io/en/stable/recipes.html#full-color-led-controlled-by-3-potentiometers
# LED = LED(22) / 27
# Heb je deze website gezien? -> https://pypi.org/project/gpiozero/ 
#https://gpiozero.readthedocs.io/en/stable/


#if buttom pressed 

# Loop

def speel_loop():
    speel = True
    while speel:
        rand_time = random.randint(2,5)         #Tijd waarna de LED aangaat, (Daarna op knop drukken.)
        time.sleep(rand_time)
        led.on
        start_tijd = time.time()                # = Bijgehouden tijd?
        #Na 2 a 5 seconden gaat het lampje aan, daarna binnen 1 seconde indrukken.
        #Dus als indrukken timer > 1 seconde dan faal je.
        #Dus als de LED aangaat dan moet pas de timer aangaan

        #https://gpiozero.readthedocs.io/en/stable/recipes.html#full-color-led
        #Making colours with an RGBLED:

        if groene_knop.is_pressed:
            if led == LED(22):
                print("button pressed")
                if start_tijd >= 1:
                    speel = False  # gebruiker heeft niet snel genoeg de knop gedrukt dus eind spel. 
                else:
                    led.off
                    GPIO.output(15,1)
                    GPIO.output(13,0)
                    speel = False
                    speel_loop()
            else:
                print("Verkeerde knop gedrukt")

        if rode_knop.is_pressed:
            if led == LED(27):
                print("button pressed")
                if start_tijd >= 1:
                    speel = False  # gebruiker heeft niet snel genoeg de knop gedrukt dus eind spel. 
                else:
                    led.off
                    GPIO.output(13,1)
                    GPIO.output(15,0)
                    speel = False
                    speel_loop()
            else:
                print("Verkeerde knop gedrukt")

    speel = False
    
def main():
    led = LED(22)
    # print(str(g_knop))
    # Led = LED(22)
    speel_loop()


if __name__ == "__main__":
    main()
