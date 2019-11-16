import sys
from datetime import datetime
import httplib, urllib, base64

import faceDetection
import identify
import addPerson
import addFace
import train
import findName
import findNumber

import pymysql.cursors

# connect to the database
conn = pymysql.connect(host='jsmdbinstance.cmunz4rplqqo.ap-northeast-2.rds.amazonaws.com',
                             user='jsm',
                             password='jsmzzang',
                             db='housekeeper'
                             #, charset='CHAR_SET'
                             )
                           
                           
# outsider detected, insert mysql database
def insert(photo, nowtime, outsider_name):

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO outsider (photo, time, name) VALUES (%s, %s, %s)"
            cursor.execute(sql, (photo, nowtime, outsider_name))
            conn.commit()
            print("DB insert success")

    finally:
        print(" ")                             
                             

def func(camera_filename, nowtime) :
	                             
	photo = str(camera_filename)
	personGroupId = "housekeeper2"

	faceId = faceDetection.func(photo)

	if faceId == 0 :
		print("=== face cannot detected!!!")
		insert(photo, nowtime, 'unknown')
		
	else :
		print("face detected well!!!")
		print("faceDetection.py / faceId => %s" % faceId)

		confidence = identify.confidence_func(faceId, personGroupId)

		if confidence >= 0.7 :
			personId = identify.func(faceId, personGroupId)
			print("identify.py / personId => %s" % personId)
			outsider_name = findName.func(personId, personGroupId)
			insert(photo, nowtime, outsider_name)
			
		elif confidence < 0.7 :
			print("confidence is too lowwwwwwwww")
			
			number = findNumber.func(personGroupId)
			outsider_name = "outsider" + str(number + 1)
			
			personId = addPerson.func(personGroupId, outsider_name)
			print("addPerson.py / personId => %s" % personId)
			insert(photo, nowtime, outsider_name)

			
		persistedFaceId = addFace.func(personId, photo, personGroupId)
		print("addFace.py / persistedFaceId => %s" % persistedFaceId)

		train.func(personGroupId)
		print("=== train.py COMPLETE")


