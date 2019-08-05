import httplib, urllib, base64

#personGroupId = housekeeper-python

#TODO: person name edit plz!!!!!!!!!!!!
body = {
    "name": "yeongmin",
    "userData": "User-provided data attached to the person."
}


headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
}

params = urllib.urlencode({
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/housekeeper-python/persons?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
