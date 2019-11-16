import httplib, urllib, base64
import json

def func(photo):
    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'ada902ad110541c699b099b918e6adbd'
    }

    body = {
        'url': 
            str(photo)
    }

    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceAttributes': 'hair',
        'recognitionModel': 'recognition_02',
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        dataStream = json.loads(data)
        conn.close()
        
        if not dataStream :
            return 0
        else :
            return dataStream[0]['faceId']

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

