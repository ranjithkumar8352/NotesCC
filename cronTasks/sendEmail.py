import cloudstorage as gcs
from models import College
import datetime
from config import BUCKET_NAME
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
body = ""
for college in College.query().fetch():
    num = memcache.get(college.key.urlsafe())
    if num is None:
        memcache.add(college.key.urlsafe(), 0, 86400)
        num = "Lost"
    det = [str(today), str(college.collegeName), str(len(college.courseIds)),
           str(college.studentCount), str(college.noteBookCount), str(num)]
    body += ",".join(det)
    body += "\n"
    gcsFile.write(",".join(det))
    gcsFile.write("\n")
    num = memcache.set(college.key.urlsafe(), 0)
gcsFile.close()

emailBody = """<H1>Campus Connect<br></H1>
               Here are todays stats<br>""" + body + """<br>link:
               https://storage.googleapis.com/uploadnotes-2016.appspot.com/summary.csv"""
sp = SparkPost('d5eda063a40ae19610612ea5d0804f20d294e62d')
response = sp.transmissions.send(recipients=['saurav24081996@gmail.com', 'aayushxagrawal@gmail.com'],
                                 html=emailBody,
                                 from_email={'email': 'aayush@campusconnect.cc', 'name': 'Campus Connect'},
                                 subject='OOOOH!!! YEAHHHH',
                                 )
