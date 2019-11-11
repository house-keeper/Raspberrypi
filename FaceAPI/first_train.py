import httplib, urllib, base64

personGroupId = 'housekeeper2'

body = {}
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'fe7195ca4dfd478b8078eecfa1c5b0df',
}

params = urllib.urlencode({
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/%s/train?%s" % (personGroupId, params), str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
