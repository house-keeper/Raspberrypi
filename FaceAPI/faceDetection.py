import httplib, urllib, base64
import json

def func(photo):
    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'fe7195ca4dfd478b8078eecfa1c5b0df'
    }

    body = {
        'url': 
            str(photo)
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        # 'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'hair',
        'recognitionModel': 'recognition_02',
        # 'returnRecognitionModel': 'false',
        # 'detectionModel': 'detection_01',
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        #print(dataStream[0]['faceId'])
        conn.close()
        
        if not dataStream :
            #print('face cannot detected!!!')
            #print(dataStream)
            return 0
        else :
            #print('face detected well')
            #print(data)
            return dataStream[0]['faceId']

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

