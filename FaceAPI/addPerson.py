import httplib, urllib, base64
import json

def func(personGroupId, outsider_name):
    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
    }
    
    #TODO: person name edit plz!!!!!!!!!!!!
    body = {
        "name": outsider_name,
        "userData": "User-provided data attached to the person."
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/%s/persons?%s" % (personGroupId, params), str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        dataStream = json.loads(data)
        conn.close()
        return dataStream['personId']
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
