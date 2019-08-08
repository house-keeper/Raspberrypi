import sys
import time
import RPi.GPIO as GPIO
from datetime import datetime

import pymysql.cursors

# connect to the database
conn = pymysql.connect(host='jsmdbinstance.cmunz4rplqqo.ap-northeast-2.rds.amazonaws.com',
                        user='jsm',
                        password='jsmzzang',
                        db='housekeeper'
                        #, charset='CHAR_SET'
                        )

# door open/close insert mysql database
def insert(status):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO door (time, status) VALUES (%s, %s)"
            cursor.execute(sql, (datetime.today().strftime("%Y-%m-%d %H:%M:%S"), status))
            conn.commit()
            print("DB insert success")
    finally:
        #conn.close()
        print("")


# main
# magnetic sensor
GPIO.setmode(GPIO.BCM)

isOpen = None
oldIsOpen = None

GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    
    oldIsOpen = isOpen
    isOpen = GPIO.input(18)
    
    if(isOpen and (isOpen != oldIsOpen)):
        print "door is open"
        insert('1')
        
    elif (isOpen != oldIsOpen):
        print "door is closed"
        insert('0')

    time.sleep(0.1)
    
conn.close()
