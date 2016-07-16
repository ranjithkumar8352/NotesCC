from config import FCM_AUTH_KEY, FCM_URL
import urllib2
import json


def sendNotification(topicName, id, type, title, text):
    key = 'key=' + FCM_AUTH_KEY
    header = {'Content-Type': 'application/json', 'Authorization': key}
    topic = '/topics/' + topicName
    body = {'to': topic, 'data': {'type': type, 'id': id, 'title': title, 'message': text}}
    req = urllib2.Request(FCM_URL, json.dumps(body), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    print response


def sendNotificationSingle(id, type, title, text):
    if len(id) < 8:
        return
    key = 'key=' + FCM_AUTH_KEY
    header = {'Content-Type': 'application/json', 'Authorization': key}
    body = {'to': id, 'data': {'type': type, 'title': title, 'message': text}}
    req = urllib2.Request(FCM_URL, json.dumps(body), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
