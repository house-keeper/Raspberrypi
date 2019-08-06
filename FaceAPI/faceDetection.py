import httplib, urllib, base64
import json

def func(photo):
    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0'
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
        return dataStream[0]['faceId']

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

