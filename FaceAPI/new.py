import httplib, urllib, base64

body = {
    "name": "group1",
    "userData": "",
    "recognitionModel": "recognition_02"
}


headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ada902ad110541c699b099b918e6adbd',
}

params = urllib.urlencode({
    'personGroupId': 'db-test'
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/persongroups/{personGroupId}?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
