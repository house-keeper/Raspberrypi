import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'fe7195ca4dfd478b8078eecfa1c5b0df',
}

body = {}

params = urllib.urlencode({
    'personId': '2e056e55-bbc6-4c1e-a8d7-bcd578766858'

})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("DELETE", "/face/v1.0/persongroups/housekeeper2/persons/{personId}?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
