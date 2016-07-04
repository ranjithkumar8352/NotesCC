from config import FCM_AUTH_KEY, FCM_URL
import urllib2
import json


def sendNotification(id, type,title, text):
    key = 'key=' + FCM_AUTH_KEY
    header = {'Content-Type': 'application/json', 'Authorization': key}
    topic = '/topics/' + id
    body = {'to': topic, 'data': {'type': type, 'id': id, 'title': title, 'message': text}}
    req = urllib2.Request(FCM_URL, json.dumps(body), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    print response
