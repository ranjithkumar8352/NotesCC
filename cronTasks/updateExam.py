from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging
from apiMethods import examOpened


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
LOG.info(str(examOpened))

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
