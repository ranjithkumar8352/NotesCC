from datetime import datetime, timedelta
import logging

from models import Exam, Assignment
from FCM import sendNotification


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
date = (datetime.now() + timedelta(days=7))
date = date.strftime('%d-%m-%Y')
LOG.info(date)
examList = Exam.query(Exam.dueDate == date).fetch()
LOG.info(str(examList))
assignmentList = Assignment.query(Assignment.dueDate == date).fetch()
for exam in examList:
    LOG.info(str(exam))
    sendNotification(exam.courseId.urlsafe(),
                     exam.key.urlsafe(), 'exam',
                     'Warning!!! Exam ahead',
                     'There is a exam next week')

for assignment in assignmentList:
    LOG.info(str(assignment))
    sendNotification(assignment.courseId.urlsafe(),
                     assignment.key.urlsafe(), 'exam',
                     'Warning!!! Exam ahead',
                     'There is a assignment submission next week')
