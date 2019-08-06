import sys
import httplib, urllib, base64

import faceDetection
import identify
import addPerson
import addFace
import train

photo = "http://image.chosun.com/sitedata/image/201806/21/2018062100687_0.jpg"

faceId = faceDetection.func(photo)
print("faceDetection.py / faceId => %s" % faceId)

confidence = identify.confidence_func(faceId)

if confidence >= 0.7 :
	personId = identify.func(faceId)
	print("identify.py / personId => %s" % personId)
	
elif confidence < 0.7 :
	print("confidence is too lowwwwwwwww")
	personId = addPerson.func()
	print("addPerson.py / personId => %s" % personId)


persistedFaceId = addFace.func(personId, photo)
print("addFace.py / persistedFaceId => %s" % persistedFaceId)

train.func()
print("=== train.py COMPLETE")

