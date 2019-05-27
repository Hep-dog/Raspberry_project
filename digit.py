import RPi.GPIO as GPIO
import time
import os
from multiprocessing import Process

GPIO.setwarnings(False)
GPIO.cleanup()

gpio_pins = [0, 26, 19, 13, 6, 5, 27, 17, 4, 21, 20, 24, 23]
posi_pins = [9, 10, 11, 12]
numberToChars = ['abcdef', 'bc', 'abged', 'abgcd', 'bcfg', 'afgcd', 'acdefg', 'abc', 'abcdefg', 'abcdfg']
charPinMap = { 'e':1, 'd':2, 'c':4, 'g':5, 'b':6, 'f':7, 'a':8, 'dp':3 }

pin_clock = 18


def beep(second=1):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_clock, GPIO.OUT)
    try:
        while True:
            GPIO.output(pin_clock, GPIO.HIGH)
            time.sleep(second)
            GPIO.output(pin_clock, GPIO.LOW)
            time.sleep(second)
    except KeyboardInterrupt:
        print("Clock beep process stop")
        GPIO.cleanup()

def clear():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for pin in range(1, 13):
        GPIO.setup(gpio_pins[pin], GPIO.OUT)
        if pin<10:
            GPIO.output(gpio_pins[pin], True)
        else:
            GPIO.output(gpio_pins[pin], False)


def showDigit(no, num, showDotPoint):
    if num<0 or num>9:
        return False

    clear()

    numChars = numberToChars[num]
    for i in range(len(numChars)):
        char = numChars[i]
        pin  = charPinMap[char]
        GPIO.output(gpio_pins[pin], False)

    if showDotPoint:
        pointPin = charPinMap['dp']
        GPIO.output(gpio_pins[pointPin], False)

    posi_pin = posi_pins[no-1]
    GPIO.output(gpio_pins[posi_pin], True)
    for pin in posi_pins:
        if pin != posi_pin:
            GPIO.output(gpio_pins[pin], False)



def run_digit(*args):
    t = 0.005
    try:
        while True:
            #print(int(int(time.strftime("%S", time.localtime(time.time()))) %10 ), False)
            showDigit(3, int(int(time.strftime("%M", time.localtime(time.time()))) /10 ), False)
            time.sleep(t)
            showDigit(4, int(int(time.strftime("%M", time.localtime(time.time()))) %10 ), True )
            time.sleep(t)
            showDigit(2, int(int(time.strftime("%S", time.localtime(time.time()))) /10 ), False)
            time.sleep(t)
            showDigit(1, int(int(time.strftime("%S", time.localtime(time.time()))) %10 ), False)
            time.sleep(t)

    except KeyboardInterrupt:
        print("Time display process stop!")
        GPIO.cleanup()

def main():
    p1 = Process(target = run_digit, args=("",))
    p1.start()
    p2 = Process(target = beep, args=(1.0,))
    p2.start()

if __name__ == "__main__":
    main()
