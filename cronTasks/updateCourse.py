from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging
from apiMethods import courseUpdate


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
LOG.info(str(courseUpdate))
for urlsafeId in courseUpdate:
    courseId = ndb.Key(urlsafe=urlsafeId)
    course = courseId.get()
    cacheVal = memcache.get(urlsafeId)
    LOG.info(str(cacheVal))
    if cacheVal is not None:
        course.studentIds = cacheVal[13]
        course.put()
courseUpdate.clear()
