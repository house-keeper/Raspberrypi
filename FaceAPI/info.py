import httplib, urllib, base64
import json

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
    conn.request("GET", "/face/v1.0/persongroups/housekeeper-python/persons?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
#    print (json.dumps(data, sort_keys=True, indent=2, seperators=(',',': ')))
#    print (json.loads(data))
    print data
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
