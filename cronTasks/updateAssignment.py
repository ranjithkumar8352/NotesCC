from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging
from apiMethods import assignmentOpened


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
