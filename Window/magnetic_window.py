import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

import pymysql.cursors
# Connect to the database
conn = pymysql.connect(host='jsmdbinstance.cmunz4rplqqo.ap-northeast-2.rds.amazonaws.com',
                             user='jsm',
                             password='jsmzzang',
                             db='housekeeper'
                             #, charset='CHAR_SET'
                             )

def insert(status):
    now = datetime.now()
    nowtime = now.strftime('%Y-%m-%d %H:%M:%S')

    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO window (window_time, window_status) VALUES (%s, %s)"
            cursor.execute(sql, (nowtime, status))
            conn.commit()
            #result = cursor.fetchone()
            print("insert success")
    finally:
        #conn.close()
        print(" ")




GPIO.setmode(GPIO.BCM)

#pin.DOOR_SENSOR_PIN = 18

isOpen = None
oldIsOpen = None

GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    
    oldIsOpen = isOpen
    isOpen = GPIO.input(18)
    
    if(isOpen and (isOpen != oldIsOpen)):
        insert('1')
        print "window is open"
    elif (isOpen != oldIsOpen):
        insert('0')
        print "window is closed"

    time.sleep(0.1)
    
conn.close()