import sys
sys.path.append('/home/pi/Outsider/aws')
import aws_config
sys.path.append('/home/pi/Raspberrypi/FaceAPI')
import faceapi_outsider

import time
import RPi.GPIO as GPIO
from datetime import datetime
import picamera

import boto3
from botocore.exceptions import NoCredentialsError

import pymysql.cursors


# connect to the database
conn = pymysql.connect(host='jsmdbinstance.cmunz4rplqqo.ap-northeast-2.rds.amazonaws.com',
                             user='jsm',
                             password='jsmzzang',
                             db='housekeeper'
                             #, charset='CHAR_SET'
                             )

AWS_ACCESS = aws_config.aws_access_key()
AWS_SECRET = aws_config.aws_secret_key()
#BUCKET_NAME = 'housekeeper'


# outsider detected, take a picture
def take_a_picture():
    with picamera.PiCamera() as camera:
        camera.resolution = (320,240)
        camera.capture(camera_filename)
        
    print("Take a picture success")
    
        
# upload to s3 bucket
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS, aws_secret_access_key = AWS_SECRET)
    
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("S3 upload success")
        return True
    
    except NoCredentialsError:
        print("Credentials Error")
        return False

'''
# outsider detected, insert mysql database
def insert(s3_url_name, nowtime):

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO outsider (photo, time) VALUES (%s, %s)"
            cursor.execute(sql, (s3_url_name, nowtime))
            conn.commit()
            #result = cursor.fetchone()
            print("DB insert success")
    finally:
        #conn.close()
        print(" ")
'''

# main
# ultrasonic sensor
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

        # TODO: distance value modify plzzzzzzzzz
        if distance < 30:
            nowtime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            filename = 'outsider_' + datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
            camera_filename = "/home/pi/Outsider/" + filename
            s3_url_name = "https://housekeeper.s3.ap-northeast-2.amazonaws.com/" + filename

            print("Outsider is detected!")
            
            #with picamera.PiCamera() as camera:
            take_a_picture()
            upload_to_aws(camera_filename, 'housekeeper', filename) # (local_file, bucket, s3_file)
            #insert(filename, nowtime)
            faceapi_outsider.func(s3_url_name, nowtime)
            
            time.sleep(0.1)
            
            
except KeyboardInterrupt:
        GPIO.cleanup()

