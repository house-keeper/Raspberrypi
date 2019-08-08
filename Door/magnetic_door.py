import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
import picamera
import boto3
from botocore.exceptions import NoCredentialsError
import pymysql.cursors
# Connect to the database
conn = pymysql.connect(host='jsmdbinstance.cmunz4rplqqo.ap-northeast-2.rds.amazonaws.com',
                             user='jsm',
                             password='jsmzzang',
                             db='housekeeper'
                             #, charset='CHAR_SET'
                             )
AWS_ACCESS = 'AKIAXXNH6PYSFZHSFEWY'
AWS_SECRET = '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'

filename = 'door ' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.jpg'

# door open/close insert mysql database
def insert(status):
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO door (photo, time, status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (filename, datetime.today().strftime("%Y-%m-%d %H:%M:%S"), status))
            conn.commit()
            #result = cursor.fetchone()
            print("insert success")
    finally:
        print("")

# door open take a picture
def takeapicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(filename)

# picture upload to s3 bucket
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS, aws_secret_access_key = AWS_SECRET)
    
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("success")
        return True
    
    except NoCredentialsError:
        print("credentials error")
        return False

GPIO.setmode(GPIO.BCM)

#pin.DOOR_SENSOR_PIN = 18

isOpen = None
oldIsOpen = None

GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    oldIsOpen = isOpen
    isOpen = GPIO.input(18)
    
    if(isOpen and (isOpen != oldIsOpen)):
        takeapicture()
        upload_to_aws('/home/pi/' + filename, 'housekeeper', filename)
        insert('1')
        print "door is open"
    elif (isOpen != oldIsOpen):
        insert('0')
        print "door is closed"

    time.sleep(0.1)
    
conn.close()
