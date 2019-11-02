from time import sleep
import RPi.GPIO as GPIO


class PanTilt():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pan = 27
        self.tilt = 17
        GPIO.setup(self.tilt, GPIO.OUT) # white => TILT
        GPIO.setup(self.pan, GPIO.OUT) # gray ==> PAN

    def move(self, p, t):
        self.setServoAngle(self.pan, p)
        sleep(0.5)
        self.setServoAngle(self.tilt, t)
        sleep(0.5)


    def pan_and_tilt(self, position):
        sleep(1)
        if (position == 0): #default
            self.move(p=67.5, t=60)

        elif (position == 1): #left
            self.move(p=30, t=60)
        
        elif (position == 2): #right
            self.move(p=97.5, t=60)
        
        elif (position == 3): #up
            self.move(p=67.5, t=15)
        
        elif (position == 4): #down
            self.move(p=67.5, t=90)
        pass

        

    def setServoAngle(self, servo, angle):
        assert angle >=15 and angle <= 150
        pwm = GPIO.PWM(servo, 50)
        pwm.start(8)
        dutyCycle = angle / 18. + 3.
        pwm.ChangeDutyCycle(dutyCycle)
        sleep(0.3)
        pwm.stop()
