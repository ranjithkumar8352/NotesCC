import cloudstorage as gcs
from models import College
import datetime
from config import BUCKET_NAME


def readFile():
    try:
        gcs_file = gcs.open("/uploadnotes-2016.appspot.com/summary.csv")
    except Exception:
        return ""
    return gcs_file.read()


def create():
    today = datetime.date.today()
    bucketName = BUCKET_NAME
    fileName = bucketName + '/' + 'summary.csv'
    gcsFile = gcs.open(fileName, mode='w', content_type='text/csv',
                       options={'x-goog-acl': 'public-read'})
    data = readFile()
    gcsFile.write(data)
    gcsFile.write("\n")
    gcsFile.write("Date,College,Courses,Students,Notebooks\n")
    for college in College.query().fetch():
        det = [str(today), str(college.collegeName), str(len(college.courseIds)),
               str(college.studentCount), str(college.noteBookCount)]
        gcsFile.write(",".join(det))
        gcsFile.write("\n")
    gcsFile.close()
