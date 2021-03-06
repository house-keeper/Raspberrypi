import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'ada902ad110541c699b099b918e6adbd'
}

body = {}

params = urllib.urlencode({
    # Request parameters
 #   'start': '{string}',
 #   'top': '1000',
    'returnRecognitionModel': 'false',
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("GET", "/face/v1.0/persongroups?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
