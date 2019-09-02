import httplib, urllib, base64
import json
from operator import itemgetter
import re

def func(personGroupId) :
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ada902ad110541c699b099b918e6adbd',
    }

    body = {}

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/%s/persons?%s" % (personGroupId, params), str(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print data
        
        dataStream = json.loads(data)
        
        sortdata = sorted(dataStream, key = itemgetter('name'))
        #print(sortdata)
        #print("lastest outsider number!!!")
        #print(sortdata[-1]['name'])
        number = re.findall("\d+", sortdata[-1]['name'])
        #print(number[0])
        conn.close()
        return int(number[0])
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
