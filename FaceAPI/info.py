import httplib, urllib, base64
import json
from operator import itemgetter
import re

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
}

body = {}

params = urllib.urlencode({
    # Request parameters
#    'start': '{string}',
#    'top': '1000',
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("GET", "/face/v1.0/persongroups/db-test/persons?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
#    print (json.dumps(data, sort_keys=True, indent=2, seperators=(',',': ')))
#    print (json.loads(data))
    print data
    
    dataStream = json.loads(data)
    
    sortdata = sorted(dataStream, key = itemgetter('name'))
    #print(sortdata)
    print("lastest outsider number!!!")
    print(sortdata[-1]['name'])
    number = re.findall("\d+", sortdata[-1]['name'])
    print(number[0])
    print(type(number[0]))
    print(type(int(number[0])))
    print(int(number[0])+1)
    
    
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
