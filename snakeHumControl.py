# This Python file uses the following encoding: utf-8
##############################################################################
#                  __       __ __           _____          __           __
#   ___ ___  ___ _/ /_____ / // /_ ____ _  / ___/__  ___  / /________  / /
#  (_-</ _ \/ _ `/  '_/ -_) _  / // /  ' \/ /__/ _ \/ _ \/ __/ __/ _ \/ /
# /___/_//_/\_,_/_/\_\\__/_//_/\_,_/_/_/_/\___/\___/_//_/\__/_/  \___/_/
#
##############################################################################
# Title:        snakeHumControl
# Version:      1.0
# Description:  Provides humidity control for snake encloure
# Author:       Jonas Werner
##############################################################################

import RPi.GPIO as GPIO
import time
import redis

redisHost  = os.environ['redisHost']
redisPort  = os.environ['redisPort']
redisPass  = os.environ['redisPass']

moistureSensor = 20
relayPin       = 13
waterStatus    = 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(moistureSensor, GPIO.IN)
GPIO.setup(13,GPIO.OUT)



def redisDBconnect():
    redisDBConnection = redis.Redis(host=redisHost, port=redisPort, password=redisPass)
    return redisDBConnection


def pumpControl(power):
    if power == "on":
        GPIO.output(13,GPIO.LOW)
    elif power == "off":
        GPIO.output(13,GPIO.HIGH)


def checkMoisture(moistureSensor):
    if GPIO.input(moistureSensor):
            waterStatus = 0
    else:
            waterStatus = 1

    return waterStatus


# Main
##################################
redisDBConnection = redisDBconnect()

while True:
    currentWaterStatus = checkMoisture(moistureSensor)
    currentHumidity = redisDBConnection.hget("snakeHum", "hum")

    if currentWaterStatus != waterStatus:
        if currentWaterStatus == 1:
            pumpControl("off")
            print("Water Detected")
        elif currentWaterStatus == 0 and int(currentHumidity) < 60:
            pumpControl("on")
            print("No water present")

        waterStatus = currentWaterStatus

    time.sleep(1)
