import RPi.GPIO as GPIO
import time
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
bucket_name = 'housekeeper'

filename = 'outsider ' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.jpg'

# outsider detected, take a picture
def takeapicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (320,240)
        camera.capture(filename)
        
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS, aws_secret_access_key=AWS_SECRET)
    
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("success")
        return True
    
    except NoCredentialsError:
        print("credentials error")
        return False

def insert():
    now = datetime.now()
    nowtime = now.strftime('%Y-%m-%d %H:%M:%S')

    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO outsider (photo, time) VALUES (%s, %s)"
            cursor.execute(sql, (filename, nowtime))
            conn.commit()
            #result = cursor.fetchone()
            print("insert success")
    finally:
        #conn.close()
        print(" ")

try:
    while True:
        GPIO.setmode(GPIO.BCM)

        trig=2
        echo=3

        GPIO.setwarnings(False)
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        
        GPIO.output(trig,False)
        time.sleep(0.5)

        GPIO.output(trig,True)
        time.sleep(0.001)
        GPIO.output(trig,False)


        while GPIO.input(echo) == 0:
            pulse_start = time.time()

        while GPIO.input(echo) == 1:
            pulse_end = time.time()


        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        if distance < 5:
            print("Outsider is detected!")
            #with picamera.PiCamera() as camera:
            takeapicture()
            upload_to_aws('/home/pi/' + filename, 'housekeeper', filename)
            insert()
        

except KeyboardInterrupt:
        GPIO.cleanup()



