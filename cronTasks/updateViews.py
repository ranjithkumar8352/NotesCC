from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging
from apiMethods import noteBookOpened, assignmentOpened, examOpened


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
LOG.info(str(assignmentOpened))
for urlsafeId in assignmentOpened:
    assignmentId = ndb.Key(urlsafe=urlsafeId)
    assignment = assignmentId.get()
    views = memcache.get('views' + urlsafeId)
    if views is not None:
        assignment.assignmentViews = views
        assignment.put()
    else:
        memcache.add('views' + urlsafeId, assignment.assignmentViews)
assignmentOpened.clear()
for urlsafeId in examOpened:
    examId = ndb.Key(urlsafe=urlsafeId)
    exam = examId.get()
    views = memcache.get('views' + urlsafeId)
    if views is not None:
        exam.examViews = views
        exam.put()
    else:
        memcache.add('views' + urlsafeId, exam.examViews)
examOpened.clear()
for urlsafeId in noteBookOpened:
    noteBookId = ndb.Key(urlsafe=urlsafeId)
    noteBook = noteBookId.get()
    views = memcache.get('views' + urlsafeId)
    if views is not None:
        noteBook.views = views
        noteBook.put()
    else:
        memcache.add('views' + urlsafeId, noteBook.views)
noteBookOpened.clear()
