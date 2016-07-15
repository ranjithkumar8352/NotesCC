import datetime
from models import Notification
import logging


curTime = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
weekBefore = curTime - datetime.timedelta(days=7)
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
LOG.info('Deleting 1 week old notifications')
result = notifications = Notification.query(Notification.timeStamp < weekBefore).fetch()
for notification in result:
    notification.key.delete()
