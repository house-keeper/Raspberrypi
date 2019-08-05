import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
}

body = {
    "personGroupId": "housekeeper-python",
    "faceIds": [
        "e1d25791-6ef2-4f8f-9ec1-d8b23eb31b4c",
    ],
    "confidenceThreshold": 0.01
}

params = urllib.urlencode({
    # Request parameters
#    'start': '{string}',
#    'top': '1000',
#    'returnRecognitionModel': 'false',
})

try:
    conn = httplib.HTTPSConnection('koreacentral.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
