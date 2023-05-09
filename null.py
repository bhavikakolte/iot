from gpiozero import Servo
from time import sleep
import sys
import urllib.request as urllib2
import Adafruit_DHT


servo = Servo(2) #pin 3 on pi
state=False #close
servo.min()
  

# Enter Your API key here
myAPI = 'GDB8NGHW3ZUJTMAM' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

# Set up the sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  #pin 7 on pi

def move_servo(bool):
    if bool==True:
    #     servo.mid()
    #     sleep(0.5)
        state=True
        servo.max()
        sleep(0.5)
    else:
        servo.min()
        sleep(0.5)
        state=False

while True:
    # Try to get a reading from the sensor
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    # If the reading was successful, print the values
    if humidity is not None and temperature is not None:
        if temperature>=25 or humidity>=15:
            print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
            move_servo(True)
            conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s' % (temperature, humidity,state))
            print(conn.read())
            # Closing the connection
            conn.close()
        if temperature<25 or humidity<15:
            print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
            move_servo(False)
            conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s' % (temperature, humidity,state))
            print(conn.read())
            # Closing the connection
            conn.close()
            
    # Wait a little bit before taking the next reading
    sleep(2)
