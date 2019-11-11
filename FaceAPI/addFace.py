import httplib, urllib, base64
import json

def func(personId, photo, personGroupId):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'ada902ad110541c699b099b918e6adbd',
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
        conn.request("POST", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces?%s" % (personGroupId, personId, params), str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        #print(dataStream['persistedFaceId'])
        conn.close()
        return dataStream['persistedFaceId']
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
