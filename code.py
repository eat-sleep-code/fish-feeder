import sys
import time
import board
import pwmio
import analogio
from adafruit_dotstar import DotStar
from adafruit_motor import servo

### IMPORTANT: Change to your feeding schedule! ###
feedEveryXHours = 12
###################################################

led = DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
servoPin = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
buzzerPin = analogio.AnalogOut(board.A0)



def TrustySleep(sleepFor = 1):
    start = time.monotonic()
    while (time.monotonic() - start < sleepFor):
        time.sleep(sleepFor - (time.monotonic() - start))



def SoundAlarms(soundFor = 60, messageType='WARNING', message = ''):
    print(messageType + ':', message)
    led[0] = (255,0,0) 
    buzzerPin.value = 65535
    time.sleep(soundFor)
    buzzerPin.value = 0



try:
    feederServo = servo.Servo(servoPin)
    feederServo.angle = 0
    feedServoIncrement = 12

    # --- LOAD FOOD ---------------------------------------------------------------

    print('INFO:', 'Please load food...')
    for t in range(60):
        led[0] = (255,255,0)
        time.sleep(0.5)
        led[0] = (0, 0, 0)
        if t > 55:
            buzzerPin.value = 65535
        time.sleep(0.5)
        buzzerPin.value = 0
            
            
    # --- FEEDING -----------------------------------------------------------------

    foodAvailable = True
    feeding = 0
    feedEveryXSeconds = (feedEveryXHours * 3600) - 10; # Convert hours to seconds and subtract the 10 seconds we will pause during each feeding
    led[0] = (0,0,255) 
    print('INFO:', 'Feeding every', feedEveryXSeconds, 'seconds...')
    while foodAvailable == True:
        for angle in range(feedServoIncrement, 180, feedServoIncrement):  
            feeding = feeding + 1
            #print('DEBUG', 'Feeding:', feeding, '|', 'Feeder angle:', angle, '|', 'Time:', time.monotonic())
            print('INFO:', 'Feeding number', feeding)
            led[0] = (0,255,0)
            feederServo.angle = angle
            time.sleep(10)
            led[0] = (0,0,255)
            TrustySleep(feedEveryXSeconds) 
        feederServo.angle = 0
        foodAvailable = False


    # --- OUT OF FOOD -------------------------------------------------------------
    SoundAlarms(30, 'WARNING', 'Out of food...')
    
except KeyboardInterrupt:
    led[0] = (2,2,2)
    print('INFO:', 'Exiting at user\'s request...')
    sys.exit(1)

except Exception as ex:
    SoundAlarms(120, 'ERROR', str(ex))
    
