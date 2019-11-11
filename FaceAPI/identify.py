import httplib, urllib, base64
import json


def confidence_func(faceId, personGroupId):
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'fe7195ca4dfd478b8078eecfa1c5b0df',
    }

    body = {
        "personGroupId": personGroupId,
        "faceIds": [
            str(faceId),
        ],
        "confidenceThreshold": 0.01
    }

    params = urllib.urlencode({
        # Request parameters
    #    'start': '{string}',
    #    'top': '1000',
    #    'returnRecognitionModel': 'false',
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        candidates = dataStream[0]['candidates']
        print("=== confidence result === ")
        print(candidates[0]['confidence'])
        #print(type(candidates[0]['confidence']))
        conn.close()
        return candidates[0]['confidence']
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))




def func(faceId, personGroupId):
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'fe7195ca4dfd478b8078eecfa1c5b0df',
    }

    body = {
        "personGroupId": personGroupId,
        "faceIds": [
            str(faceId),
        ],
        "confidenceThreshold": 0.01
    }

    params = urllib.urlencode({
        # Request parameters
    #    'start': '{string}',
    #    'top': '1000',
    #    'returnRecognitionModel': 'false',
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        candidates = dataStream[0]['candidates']
        #print(candidates[0]['personId'])
        conn.close()
        return candidates[0]['personId']
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


