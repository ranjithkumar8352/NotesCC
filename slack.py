from config import WEBHOOK_URLS
import urllib2
import json

from models import College
from config import CLG_STATS_TIME
from google.appengine.api import memcache


def slackWebHook():
    text = "\n\n*College\t\tCourses\tStudents\tNotebooks\tUploads\tNew Profiles*\n"
    for college in College.query().fetch():
        num = memcache.get(college.key.urlsafe())
        if num is None:
            memcache.add(college.key.urlsafe(), 0, 86400)
            num = "Lost"
        stuNum = memcache.get('stu' + college.key.urlsafe())
        if stuNum is None:
            memcache.add('stu' + college.key.urlsafe(), 0, CLG_STATS_TIME)
            stuNum = "Lost"
        if college.abbreviation == 'LNMIIT':
            abb = college.abbreviation.ljust(20, ' ')
        else:
            abb = college.abbreviation.ljust(25, ' ')
        det = abb + '\t\t' + str(len(college.courseIds)) + '\t\t\t\t'
        det += str(college.studentCount) + '\t\t\t\t'
        det += str(college.noteBookCount) + '\t\t\t\t\t'
        if 'LNMIIT' in abb:
            det += str(num) + '\t\t\t\t\t' + str(stuNum)
        else:
            det += str(num) + '\t\t\t\t\t\t' + str(stuNum)
        text += det
        text += '\n'
        text += "csv link: https://storage.googleapis.com/uploadnotes-2016.appspot.com/summary.csv"

    data = {'icon_url': 'https://s-media-cache-ak0.pinimg.com/236x/d7/a4/34/d7a4343ec74ae5427708b429cbf82a20.jpg',
            'username': 'Fl@pPy',
            "attachments": [
                {
                    "title": "Yay!!!!!!",
                    "text": text,
                    "mrkdwn_in": [
                        "text",
                        "title"
                    ]
                }
            ]}
    for url in WEBHOOK_URLS:
        req = urllib2.Request(url, json.dumps(data))
        urllib2.urlopen(req)
