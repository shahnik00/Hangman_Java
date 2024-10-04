import machine
import time
import random
import utime
from lcd1602 import LCD
#test1
SEGCODE = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]

sdi = machine.Pin(18,machine.Pin.OUT)
rclk = machine.Pin(19,machine.Pin.OUT)
srclk = machine.Pin(20,machine.Pin.OUT)

placePin = []
pin = [10,13,12,11]
for i in range(4):
    placePin.append(None)
    placePin[i] = machine.Pin(pin[i], machine.Pin.OUT)

def pickDigit(digit):
    for i in range(4):
        placePin[i].value(1)
    placePin[digit].value(0)

def clearDisplay():
    hc595_shift(0x00)

def hc595_shift(dat):
    rclk.low()
    time.sleep_us(200)
    for bit in range(7, -1, -1):
        srclk.low()
        time.sleep_us(200)
        value = 1 & (dat >> bit)
        sdi.value(value)
        time.sleep_us(200)
        srclk.high()
        time.sleep_us(200)
    time.sleep_us(200)
    rclk.high()
    

def display(num):
    digits = [num % 10, (num // 10) % 10, (num // 100) % 10, (num // 1000) % 10]
    
    for i in range(4):
        pickDigit(i)
        hc595_shift(SEGCODE[digits[i]])
        time.sleep_ms(1)  # Small delay for stable display

# Setup
buzzer = machine.PWM(machine.Pin(0))  # Initialize buzzer

# Red LEDs
led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(3, machine.Pin.OUT)
led3 = machine.Pin(4, machine.Pin.OUT)
# Green LED
led4 = machine.Pin(5, machine.Pin.OUT)

# Buttons
button1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Initialize button1 with pull-down resistor
button2 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Initialize button2 with pull-down resistor

# Switch
switch = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Initialize switch with pull-down resistor

# LCD Setup
lcd = LCD()  # Initialize the LCD
lcd.clear()  # Clear the LCD display

# Helper function to play a tone
def tone(pin, frequency, duration):
    pin.freq(frequency)  # Set the frequency of the buzzer
    pin.duty_u16(30000)  # Set the duty cycle
    utime.sleep_ms(duration)  # Play the tone for the specified duration
    pin.duty_u16(0)  # Stop the tone

# LED Game
def led_game():
    # Initialize the LEDs
    led3.value(0)  # red
    led4.value(1)  # green
    led1.value(0)  # red
    led2.value(0)  # red
    highest_value = None

    while button1.value() == 1 and led4.value() == 1: # makes sure that the first button is pressed and the green led is on 
        print("Starting LED game")
        utime.sleep(1)
        led4.value(0)
        utime.sleep(1)
        led1.value(1)
        utime.sleep(1)
        led2.value(1)
        utime.sleep(1)
        led3.value(1)
        rand = random.uniform(2, 6) # chooses a random sleep time before the green led turns on and the time starts
        utime.sleep(rand)
        led4.value(1)
        start = time.ticks_ms()

        while button2.value() == 0: # while the second button is not pressed the timer is running 
            elapsed = time.ticks_ms() - start
            count = int(elapsed / 10)
            display(count)
        
        end = time.ticks_ms()
        elapsed = end - start
        
        if highest_value is None or elapsed < highest_value: # if the time is less than the highest value than that is the new value
            highest_value = elapsed

        lcd.clear()
        lcd.message("Elapsed Time:\n" + str(elapsed) + "ms")
        utime.sleep(2)
        lcd.clear()
        lcd.message("Best Time:\n" + str(highest_value) + "ms")
        utime.sleep(2)
        
        print("Time stop")
        utime.sleep(2)

# Buzzer Game
def buzzer_game():
    highest_value = None

    while button1.value() == 1:
        print("Starting Buzzer game")
        rand = random.uniform(2, 6)
        utime.sleep(rand)
        tone(buzzer, 1000, 500)
        start = time.ticks_ms()

        while button2.value() == 0:
            elapsed = time.ticks_ms() - start
            count = int(elapsed / 10)
            display(count)

        end = time.ticks_ms()
        elapsed = end - start

        if highest_value is None or elapsed < highest_value:
            highest_value = elapsed

        lcd.clear()
        lcd.message("Elapsed Time:\n" + str(elapsed) + "ms")
        utime.sleep(2)
        lcd.clear()
        lcd.message("Best Time:\n" + str(highest_value) + "ms")
        utime.sleep(2)
        
        print("Time stop")
        utime.sleep(2)

# Main function
def main():
    while True:
        # Reset LEDs
        led1.value(0)
        led2.value(0)
        led3.value(0)
        led4.value(0)
        
        if switch.value() == 1:
            led_game()
        else:
            buzzer_game()

# Run the main function
main()


