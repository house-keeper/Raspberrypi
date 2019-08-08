import sys
from datetime import datetime
import httplib, urllib, base64

import faceDetection
import identify
import addPerson
import addFace
import train

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
                             
                             
photo = "http://img.etoday.co.kr/pto_db/2018/02/20180208110851_1184805_600_818.jpg"
personGroupId = "db-test"


faceId = faceDetection.func(photo)
print("faceDetection.py / faceId => %s" % faceId)


confidence = identify.confidence_func(faceId, personGroupId)

if confidence >= 0.7 :
	personId = identify.func(faceId, personGroupId)
	print("identify.py / personId => %s" % personId)
	insert("outsider2-test")[{"personIhttp://img.etoday.co.kr/pto_db/2018/02/20180208110851_1184805_600_818.jpgd":"059962a5-cf8d-494a-a304-60b62b4a2e96","persistedFaceIds":["ebae0ced-3f45-4b79-aaa6-b8580582d453"],"name":"outsider1-test","userData":"User-provided data attached to the person."},{"personId":"24e81737-9640-4457-9749-788b5f8b812d","persistedFaceIds":[],"name":"outsider2-test","userData":"User-provided data attached to the person."},{"personId":"3ba8f355-4ac2-4e95-b353-181812b21405","persistedFaceIds":["1f1a06b5-8d3e-404c-8765-b8e1c67fb632"],"name":"outsider2-test","userData":"User-provided data attached to the person."}]

	
elif confidence < 0.7 :
	print("confidence is too lowwwwwwwww")
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

