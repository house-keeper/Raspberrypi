import httplib, urllib, base64

personGroupId = 'db-test'

body = {}
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '6bc77c1f5ad742a2b57a1f0f809ec7d0',
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
