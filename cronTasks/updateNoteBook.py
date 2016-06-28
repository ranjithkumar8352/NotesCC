from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging
from apiMethods import noteBookOpened


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
LOG.info(str(noteBookOpened))

for urlsafeId in noteBookOpened:
    flag = 0
    noteBookId = ndb.Key(urlsafe=urlsafeId)
    noteBook = noteBookId.get()
    cacheVal = memcache.get(urlsafeId)
    print cacheVal[8]
    if cacheVal is not None:
        LOG.info(cacheVal[9])
        LOG.info(cacheVal[10])
        if noteBook.ratedUserIds != cacheVal[9] or noteBook.ratingList != cacheVal[10]:
            noteBook.ratedUserIds = cacheVal[9]
            noteBook.ratingList = cacheVal[10]
            flag = 1
        LOG.info(noteBook.bmUserList)
        if noteBook.bmUserList == cacheVal[8]:
            flag = 0
        else:
            noteBook.bmUserList = cacheVal[8]
            flag = 1
    views = memcache.get('views' + urlsafeId)
    if views is not None:
        noteBook.views = views
        noteBook.put()
    elif flag == 1:
        noteBook.put()
    else:
        memcache.add('views' + urlsafeId, noteBook.views)
noteBookOpened.clear()
