from datetime import datetime, timedelta
import logging

from models import Exam, Assignment
from FCM import sendNotification
from apiMethods import createNotification

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
    course = exam.courseId.get()
    title = course.courseName
    notificationText = 'There is a exam next week'
    createNotification(course.studentIds, title,
                       notificationText, 'exam',
                       exam.key.urlsafe(), course.key.urlsafe())

for assignment in assignmentList:
    LOG.info(str(assignment))
    sendNotification(assignment.courseId.urlsafe(),
                     assignment.key.urlsafe(), 'exam',
                     'Warning!!! Assignment Submission ahead',
                     'There is a assignment submission next week')
    course = assignment.courseId.get()
    title = course.courseName
    notificationText = 'There is a assignment submission next week'
    createNotification(course.studentIds, title,
                       notificationText, 'assignment',
                       assignment.key.urlsafe(), course.key.urlsafe())
