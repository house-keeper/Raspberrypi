import httplib, urllib, base64

# TODO: personId edit plz
personId = "d2a65460-e347-4b92-acd6-a3e039d150ff"
# personGroupId = 'housekeeper-python'

# TODO: url of body edit plz!!!!!!!!!!!!
body = {
    "url": "https://image.ytn.co.kr/osen/2019/05/20190518_1558172901_31016700_1.jpg"
}


headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
}

params = urllib.urlencode({
    # Request parameters
#    'userData': '{string}',
#    'targetFace': '{string}',
#    'detectionModel': 'detection_01',
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/housekeeper-python/persons/%s/persistedFaces?%s" % (personId, params), str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
