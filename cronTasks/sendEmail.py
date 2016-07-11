import cloudstorage as gcs
from models import College
import datetime
from config import BUCKET_NAME, CLG_STATS_TIME
from sparkpost import SparkPost
from google.appengine.api import memcache


today = datetime.date.today()
bucketName = BUCKET_NAME
fileName = bucketName + '/' + 'summary.csv'
try:
    exFile = gcs.open(fileName)
    data = exFile.read()
except Exception:
    data = ""
gcsFile = gcs.open(fileName, mode='w', content_type='text/csv',
                   options={'x-goog-acl': 'public-read'})
gcsFile.write(data)
gcsFile.write("\n")
gcsFile.write("Date,College,Courses,Students,Notebooks,UploadsToday\n")
body = "Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;College&nbsp;Courses&nbsp;Students&nbsp;Notebooks&nbsp;UploadsToday&nbsp;ProfileCreated<br>"
for college in College.query().fetch():
    num = memcache.get(college.key.urlsafe())
    if num is None:
        memcache.add(college.key.urlsafe(), 0, CLG_STATS_TIME)
        num = "Lost"
    stuNum = memcache.get('stu' + college.key.urlsafe())
    if stuNum is None:
        memcache.add('stu' + college.key.urlsafe(), 0, CLG_STATS_TIME)
        stuNum = "Lost"
    det = [str(today), str(college.collegeName), str(len(college.courseIds)),
           str(college.studentCount), str(college.noteBookCount), str(num), str(stuNum)]
    body += "&nbsp;".join(det)
    body += "<br>"
    gcsFile.write(",".join(det))
    gcsFile.write("\n")
    memcache.set(college.key.urlsafe(), 0)
    memcache.set('stu' + college.key.urlsafe(), 0)
gcsFile.close()

emailBody = """<H1>Campus Connect<br></H1>
               Here are todays stats<br>""" + body + """<br>link:
               https://storage.googleapis.com/uploadnotes-2016.appspot.com/summary.csv"""
sp = SparkPost('d5eda063a40ae19610612ea5d0804f20d294e62d')
response = sp.transmissions.send(recipients=['saurav24081996@gmail.com', 'aayush@campusconnect.cc'],
                                 html=emailBody,
                                 from_email={'email': 'aayush@campusconnect.cc', 'name': 'Campus Connect'},
                                 subject='OOOOH!!! YEAHHHH',
                                 )
