import datetime
from models import Notification
from FCM import sendNotificationSingle

from google.appengine.api import memcache
from google.appengine.ext import ndb


curTime = datetime.datetime.now()
prevTime = curTime - datetime.timedelta(hours=1)
results = Notification.query(ndb.AND((Notification.timeStamp <= curTime),
                                     (Notification.timeStamp >= prevTime)))
profileIds = {}
for notification in results:
    for profileId in notification.profileIdList:
        if profileId in profileIds:
            profileIds[profileId] += 1
        else:
            profileIds[profileId] = 0
for profileId in profileIds:
    count = profileIds[profileId]
    if count == 0:
        continue
    fcmId = memcache.get('fcm' + profileId.urlsafe())
    if fcmId is None:
        profile = profileId.get()
        if profile is None:
            continue
        fcmId = profile.gcmId
        memcache.add('fcm' + profileId.urlsafe(), fcmId, 3600)
    text = 'You have ' + str(count) + ' new notifications'
    sendNotificationSingle(fcmId, 'hour', 'Campus Connect', text)
