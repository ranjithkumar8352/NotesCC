import datetime
from models import Notification
from FCM import sendNotificationSingle

from google.appengine.ext import ndb


curDate = datetime.date.today()
curTime = datetime.time.now()
prevTime = curTime - datetime.timedelta(hours=1)
results = Notification.query(ndb.AND((Notification.date == curDate),
                                     (Notification.time <= curTime),
                                     (Notification.time >= prevTime)))
profileIds = {}
for notification in results:
    for profileId in notification.profileIdList:
        if profileId in profileIds:
            profileIds[profileId] += 1
        else:
            profileIds[profileId] = 0
for profileId in profileIds:
    count = profileIds[profileId]
    fcmId = memcache.get('fcm' + profileId.urlsafe())
    if fcmId is None:
        profile = profileId.get()
        fcmId = profile.gcmId
        memcache.add('fcm'+profileId.urlsafe(), fcmId, 3600)
    text = 'You have ' + str(count) + ' new notifications'
    sendNotificationSingle(fcmId, 'hour', 'Campus Connect', text)
