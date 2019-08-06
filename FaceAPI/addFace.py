import httplib, urllib, base64
import json

def func(personId, photo):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
    }
    
    # TODO: url of body edit plz!!!!!!!!!!!!
    body = {
        "url": str(photo)
    }

    params = urllib.urlencode({
        # Request parameters
    #    'userData': '{string}',
    #    'targetFace': '{string}',
    #    'detectionModel': 'detection_01',
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/housekeeper-python/persons/%s/persistedFaces?%s" % (personId, params), str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        #print(dataStream['persistedFaceId'])
        conn.close()
        return dataStream['persistedFaceId']
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
