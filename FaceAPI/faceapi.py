import sys
from datetime import datetime
import httplib, urllib, base64

import faceDetection
import identify
import addPerson
import addFace
import train
import findName

import pymysql.cursors

# connect to the database
conn = pymysql.connect(host='jsmdbinstance.cmunz4rplqqo.ap-northeast-2.rds.amazonaws.com',
                             user='jsm',
                             password='jsmzzang',
                             db='housekeeper'
                             #, charset='CHAR_SET'
                             )
                           
                           
                             
# outsider detected, insert mysql database
def insert(outsider_name):

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO outsider (time, name) VALUES (%s, %s)"
            cursor.execute(sql, (datetime.today().strftime("%Y-%m-%d %H:%M:%S"), outsider_name))
            conn.commit()
            #result = cursor.fetchone()
            print("DB insert success")
    finally:
        #conn.close()
        print(" ")                             
                             
                             
photo = "http://photo.hankooki.com/arch/photo/P/2019/05/23/20190523184948_P_00_C_1_236.jpg"
personGroupId = "db-test"


faceId = faceDetection.func(photo)
print("faceDetection.py / faceId => %s" % faceId)


confidence = identify.confidence_func(faceId, personGroupId)

if confidence >= 0.7 :
	personId = identify.func(faceId, personGroupId)
	print("identify.py / personId => %s" % personId)
	outsider_name = findName.func(personId, personGroupId)
	insert(outsider_name)
	
elif confidence < 0.7 :
	print("confidence is too lowwwwwwwww")
	# TODO: name modify plz!!!!! auto increment
	outsider_name = "outsider3-test"
	personId = addPerson.func(personGroupId, outsider_name)
	print("addPerson.py / personId => %s" % personId)
	insert(outsider_name)


# only first time / add person group 
#personId = addPerson.func(personGroupId)

persistedFaceId = addFace.func(personId, photo, personGroupId)
print("addFace.py / persistedFaceId => %s" % persistedFaceId)


train.func(personGroupId)
print("=== train.py COMPLETE")

