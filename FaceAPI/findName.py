import httplib, urllib, base64
import json

def func(personId, personGroupId):
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ada902ad110541c699b099b918e6adbd',
    }

    body = {}

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/%s/persons/%s%s" % (personGroupId, personId, params), str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        #print(dataStream['name'])
        conn.close()
        return dataStream['name']
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
