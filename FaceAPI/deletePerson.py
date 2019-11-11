import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'fe7195ca4dfd478b8078eecfa1c5b0df',
}

params = urllib.urlencode({
})

body = {
    
}

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("DELETE", "/face/v1.0/persongroups/housekeeper/persons/b2cc4e92-2e04-4dfa-8fd9-3f8bc1e43176", str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
