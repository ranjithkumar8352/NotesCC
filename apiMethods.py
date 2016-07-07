import datetime
import traceback

from models import College, Course, Profile
from models import Response, FeedCourseResponse, CourseListResponse, FeedResponse
from models import TTCourseResponse, TimeTableResponse, StudentResponse
from models import StudentListResponse, Assignment, Exam, CourseResponse
from models import GetAssignmentResponse, GetExamResponse, Notes, NoteBook
from models import NotesResponse, NoteBookDetailResponse, NoteBookListResponse
from models import NoteBookResponse, CoursePageResponse, AssExamResponse
from models import AssignmentResponse, ExamResponse, GetAssListResponse
from models import GetExamListResponse, CollegeListResponse, CollegeDetails
from models import BookmarkResponse, Notification, NotificationResponse, NotificationList
from searchAPI import createNBDoc
from FCM import sendNotification
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.api import memcache


noteBookOpened = set()
assignmentOpened = set()
examOpened = set()
courseUpdate = set()


def setValue(eObject, mObject, e2m, skip=[]):
    print mObject
    if e2m == -1:
        for field in mObject.all_fields():
            if field.name in skip:
                continue
            value = getattr(mObject, field.name)
            if field.required is True:
                if str(field.type) == "<type 'unicode'>" and value == "":
                    raise Exception("Invalid " + str(field.name))
                else:
                    setattr(eObject, field.name, value)
            else:
                setattr(eObject, field.name, value)
    else:
        for field in mObject.all_fields():
            if field.name in skip:
                continue
            value = getattr(eObject, field.name)
            setattr(mObject, field.name, value)


def createCollegeMethod(request):
    """createCollegeMethod(request)
    request (collegeName, abbreviation, location, collegeType, semStartDate,
    semEndDate, branchNameList)
    To create New college"""
    newCollege = College()
    try:
        setValue(newCollege, request, -1)
    except Exception, E:
        print str(E)
        traceback.print_stack()
        return Response(response=1, description=str(E))
    # To find college with same name and location
    queryString = ndb.AND(College.collegeName == newCollege.collegeName,
                          College.location == newCollege.location)
    collegeSameDetails = College.query(queryString).fetch()
    if collegeSameDetails:
        print "College already exists"
        return Response(response=2, description="College Already Exists")
    else:
        key = newCollege.put()
        return Response(response=0, description="OK", key=key.urlsafe())


def createProfileMethod(request):
    """createProfileMethod(request)
        request (collegeId, profileName, batchName, branchName, sectionName, photoUrl,
        gcmId, email)
        Creates a new profile"""
    try:
        collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
    except Exception:
        return Response(response=1, description="No such collegeId")
    newProfile = Profile()
    try:
        setValue(newProfile, request, -1, skip=['collegeId'])
    except Exception, E:
        print str(E)
        traceback.print_stack()
        return Response(response=1, description=str(E))
    # Query for compatible courses and stores in availableCourseIds
    availableCourseIds = []
    queryString = ndb.AND(Course.collegeId == collegeId,
                          Course.batchNames == newProfile.batchName,
                          Course.branchNames == newProfile.branchName,
                          Course.sectionNames == newProfile.sectionName)
    for course in Course.query(queryString).fetch():
        availableCourseIds.append(course.key)
    college = collegeId.get()
    # To get existing profiles (if any) with same email id
    profileCheck = Profile.query(Profile.email == newProfile.email).fetch()
    if college is None:
        print "No such college ID"
        return Response(response=1, description="No such college ID")
    elif profileCheck:
        print "Profile already registered"
        return Response(response=2, description="Profile already registered")
    else:
        setattr(newProfile, 'collegeId', collegeId)
        setattr(newProfile, 'availableCourseIds', availableCourseIds)
        # increasing the studentCount in college
        college.studentCount += 1
        college.put()
        key = newProfile.put()
        return Response(response=0, description="OK", key=key.urlsafe())


def addCourseMethod(request):
    """addCourseMethod(request)
    request(POST) (courseName, collegeId, batchName, sectionName,
    semester, adminId, startTime, endTime, proffessorName)
    creates a new course and adds it to the college"""
    try:
        collegeId = ndb.Key(urlsafe=(getattr(request, 'collegeId')))
    except Exception:
        print "Invalid collegeId"
        return Response(response=1, description="Invalid collegeId")
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    newCourse = Course()
    setValue(newCourse, request, -1, skip=['profileId', 'collegeId'])
    adminIds = []
    adminIds.append(profileId)
    studentIds = []
    studentIds.append(profileId)
    college = collegeId.get()
    profile = profileId.get()
    if college is None:
        print "Invalid collegeId"
        return Response(response=1, description="Invalid collegeId")
    if profile is None:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    # To check if same course already exists
    queryString = ndb.AND(Course.courseCode == newCourse.courseCode,
                          Course.collegeId == collegeId,
                          Course.sectionNames.IN(newCourse.sectionNames),
                          Course.branchNames.IN(newCourse.branchNames),
                          Course.batchNames.IN(newCourse.batchNames),
                          Course.professorName == newCourse.professorName)
    coursesWithSameCode = Course.query(queryString).fetch()
    if coursesWithSameCode:
        print "Course already exists"
        return Response(response=2, description="Course already exists")
    setattr(newCourse, 'collegeId', collegeId)
    setattr(newCourse, 'adminIds', adminIds)
    setattr(newCourse, 'studentIds', studentIds)
    courseId = newCourse.put()
    # Adding profileId of creator to adminId
    for profileId in adminIds:
        profile = profileId.get()
        profile.subscribedCourseIds.append(courseId)
        profile.put()
    # Adding courseId to college.courseIds
    college.courseIds.append(courseId)
    college.put()
    # Adding courseId to profile.administeredCourseIds
    profile.administeredCourseIds.append(courseId)
    profile.put()
    # To update the availableCourseIds of users
    queryString = ndb.AND(Profile.collegeId == collegeId,
                          Profile.batchName.IN(newCourse.batchNames),
                          Profile.branchName.IN(newCourse.branchNames),
                          Profile.sectionName.IN(newCourse.sectionNames))
    profilesToUpdate = Profile.query(queryString).fetch()
    for profile in profilesToUpdate:
        if profile.key != profileId:
            profile.availableCourseIds.append(courseId)
            profile.put()
    return Response(response=0, description="OK", key=courseId.urlsafe())


def subscribeCourseMethod(request):
    """subscribeCourseMethod(request)
       request (profileId, courseIds)
       Subscribes the profileId to a list of courseIds"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    profile = profileId.get()
    if profile is None:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    courseIdList = getattr(request, 'courseIds')
    courseIds = []
    # Adding courseId to profile.subscribedCourseIds
    for course in courseIdList:
        try:
            courseId = ndb.Key(urlsafe=course)
        except Exception:
            print "Invalid courseId"
            return Response(response=1, description="Invalid courseId")
        if profileId not in profile.subscribedCourseIds:
            profile.subscribedCourseIds.append(courseId)
            courseIds.append(courseId)
            cacheVal = memcache.get(courseId.urlsafe())
            if cacheVal is not None:
                cacheVal[13].remove(profileId)
                cacheVal[9] -= 1
                memcache.set(courseId.urlsafe(), cacheVal)
    # Removing courses with same courseCode from profile.availableCourseIds
    courseCodes = []
    for courseId in courseIds:
        course = courseId.get()
        courseCodes.append(course.courseCode)
        course.studentIds.append(profileId)
        course.put()
    coursesWithSameCode = Course.query(Course.courseCode.IN(courseCodes))
    coursesWithSameCode = coursesWithSameCode.fetch()
    for course in coursesWithSameCode:
        courseId = course.key
        if courseId in profile.availableCourseIds:
            profile.availableCourseIds.remove(courseId)
    profile.put()
    return Response(response=0, description="OK")


def courseListMethod(request):
    """courseList(request)
       request (profileId) OR request(courseIds[])
       to get the list of courses"""
    profileIdUrlSafe = getattr(request, 'profileId', None)
    courseIdsUrlSafe = getattr(request, 'courseIds', None)
    if not profileIdUrlSafe and not courseIdsUrlSafe:
        print "BAD REQUEST"
        return CourseListResponse(response=1, description="Bad Request")
    else:
        courseListResponse = []
        if profileIdUrlSafe:
            try:
                profileId = ndb.Key(urlsafe=profileIdUrlSafe)
            except Exception:
                print "Invalid profileId"
                return CourseListResponse(response=1, description="Invalid profileId")
            profile = profileId.get()
            if profile is None:
                print "Invalid profileId"
                return CourseListResponse(response=1, description="Invalid profileId")
            for courseId in profile.availableCourseIds:
                course = courseId.get()
                if course is None:
                    print "Invalid courseId"
                    return CourseListResponse(response=1, description="Invalid courseId")
                notesCount = len(course.noteBookIds)
                studentCount = len(course.studentIds)
                feedCourseResponse = CourseResponse(courseId=courseId.urlsafe(),
                                                    courseName=course.courseName,
                                                    batchNames=course.batchNames,
                                                    branchNames=course.branchNames,
                                                    sectionNames=course.sectionNames,
                                                    semester=course.semester,
                                                    studentCount=studentCount,
                                                    professorName=course.professorName,
                                                    notesCount=notesCount,
                                                    colour=course.colour,
                                                    elective=course.elective)
                courseListResponse.append(feedCourseResponse)
            return CourseListResponse(response=0, description="OK",
                                      courseList=courseListResponse,
                                      completed=0)
        else:
            for courseIdUrlsafe in courseIdsUrlSafe:
                try:
                    courseId = ndb.Key(urlsafe=courseIdUrlsafe)
                except Exception:
                    print "Invalid courseId"
                    return CourseListResponse(response=1, description="Invalid CourseId")
                course = courseId.get()
                notesCount = len(course.noteBookIds)
                studentCount = len(course.studentIds)
                feedCourseResponse = CourseResponse(courseId=courseId.urlsafe(),
                                                    courseName=course.courseName,
                                                    batchNames=course.batchNames,
                                                    branchNames=course.branchNames,
                                                    sectionNames=course.sectionNames,
                                                    studentCount=studentCount,
                                                    professorName=course.professorName,
                                                    notesCount=notesCount,
                                                    semester=course.semester,
                                                    colour=course.colour,
                                                    elective=course.elective)
                courseListResponse.append(feedCourseResponse)
            return CourseListResponse(response=0, description="OK",
                                      courseList=courseListResponse,
                                      completed=0)


def feedMethod(request):
    """feedMethod(request)
       request (profileId)
       To get the home page feed of the user"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return FeedResponse(response=1, description="Invalid profileId")
    profile = profileId.get()
    if profile is None:
        print "Invalid profileId"
        return FeedResponse(response=1, description="Invalid profileId")
    profileName = profile.profileName
    points = profile.points
    photoUrl = profile.photoUrl
    availableCourseIds = profile.availableCourseIds
    subscribedCourseIds = profile.subscribedCourseIds
    try:
        availableCourseList = feedCourseResponse(availableCourseIds)
    except Exception, E:
        print str(E)
        print traceback.print_stack()
        return FeedResponse(response=1, description='in availableCourses ' + str(E))
    try:
        subscribedCourseList = feedCourseResponse(subscribedCourseIds)
    except Exception, E:
        print str(E)
        print traceback.print_stack()
        return FeedResponse(response=1, description='in subscribedCourses ' + str(E))
    collegeId = profile.collegeId
    return FeedResponse(response=0, description="OK", profileName=profileName,
                        points=points, photoUrl=photoUrl,
                        availableCourseList=availableCourseList,
                        subscribedCourseList=subscribedCourseList,
                        collegeId=collegeId.urlsafe())


def feedCourseResponse(courseIds):
    """feedCourseResponse(courseIds[])
        To get the course details for home page feed"""
    responseList = []
    curDate = datetime.datetime.now().date()
    curTime = (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).time()
    for courseId in courseIds:
        dueAssignments, dueExams, recentNotes = 0, 0, 0
        course = courseId.get()
        if course is None:
            print "Invalid courseId"
            continue
        assignmentIds = course.assignmentIds
        for assignmentId in assignmentIds:
            assignment = assignmentId.get()
            if assignment is None:
                continue
            a = assignment.dueDate
            date, month, year = int(a[0:2]), int(a[3:5]), int(a[6:10])
            dueDate = datetime.date(year, month, date)
            if(curDate > dueDate):
                continue
            a = assignment.dueTime
            hour, minute = int(a[0:2]), int(a[3:5])
            dueTime = datetime.time(hour, minute)
            if(curDate == dueDate and dueTime < curTime):
                continue
            dueAssignments = dueAssignments + 1
        examIds = course.examIds
        for examId in examIds:
            exam = examId.get()
            if exam is None:
                continue
            a = exam.dueDate
            date, month, year = int(a[0:2]), int(a[3:5]), int(a[6:10])
            dueDate = datetime.date(year, month, date)
            if(curDate > dueDate):
                continue
            a = exam.dueTime
            hour, minute = int(a[0:2]), int(a[3:5])
            dueTime = datetime.time(hour, minute)
            if(curDate == dueDate and dueTime < curTime):
                continue
            dueExams = dueExams + 1
        noteBookIds = course.noteBookIds
        for noteBookId in noteBookIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                continue
            a = str(noteBook.lastUpdated)
            date, month, year = int(a[8:10]), int(a[5:7]), int(a[0:4])
            lastUpdated = datetime.date(year, month, date)
            if(curDate - lastUpdated).days > 7:
                continue
            recentNotes = recentNotes + 1
        responseList.append(FeedCourseResponse(courseId=courseId.urlsafe(),
                                               courseName=course.courseName,
                                               dueAssignments=dueAssignments,
                                               dueExams=dueExams, date=course.date,
                                               startTime=course.startTime,
                                               endTime=course.endTime,
                                               colour=course.colour,
                                               recentNotes=recentNotes,
                                               professorName=course.professorName,
                                               elective=course.elective,
                                               courseCode=course.courseCode))
    return responseList


def addAdminMethod(request):
    """addAdmin(request)
       request (courseId, profileId)
       to make a new Admin"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    course = courseId.get()
    if course is None:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    profile = profileId.get()
    if profile is None:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    if courseId not in profile.administeredCourseIds:
        profile.administeredCourseIds.append(courseId)
    if profileId in course.adminIds:
        course.adminIds.append(profileId)
    if courseId in profile.availableCourseIds:
        profile.availableCourseIds.remove(courseId)
    profile.put()
    course.put()
    return Response(response=0, description="OK")


def timeTableMethod(request):
    """timeTableMethod(request)
       request (profileId)
       To get the timetable of all the subscribe courses of user"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return TimeTableResponse(response=1, description="Invalid profile Id")
    profile = profileId.get()
    if profile is None:
        return TimeTableResponse(response=1, description="Invalid profileId")
    subscribedCourseIds = profile.subscribedCourseIds
    courseList = []
    for courseId in subscribedCourseIds:
        course = courseId.get()
        courseList.append(TTCourseResponse(courseName=course.courseName,
                                           colour=course.colour,
                                           courseId=courseId.urlsafe(),
                                           date=course.date,
                                           startTime=course.startTime,
                                           endTime=course.endTime))
    return TimeTableResponse(response=0, description="OK",
                             courseList=courseList)


def studentListMethod(request):
    """studentListMethod(request)
       request (profileId, courseId)
       To get the list of students subscribed to the course"""
    try:
        profileId = ndb.Key(urlsafe=request.profileId)
    except Exception:
        print "Invalid profileId"
        return StudentListResponse(response=1, description="Invalid profileId")
    try:
        courseId = ndb.Key(urlsafe=request.courseId)
    except Exception:
        print "Invalid courseId"
        return StudentListResponse(response=1, description="Invalid courseId")
    profile = profileId.get()
    if profile is None:
        print "Invalid profileId"
        return StudentListResponse(response=1, description="Invalid profileId")
    course = courseId.get()
    if course is None:
        print "Invalid courseId"
        return StudentListResponse(response=1, description="Invalid courseId")
    if courseId in profile.administeredCourseIds:
        isAdmin = 1
    else:
        isAdmin = 0
    studentList = []
    for studentId in course.studentIds:
        if studentId == profileId:
            continue
        else:
            if studentId in course.adminIds:
                isAdmin2 = 1
            else:
                isAdmin2 = 0
            student = studentId.get()
            studentList.append(StudentResponse(profileId=studentId.urlsafe(),
                                               profileName=student.profileName,
                                               photoUrl=student.photoUrl,
                                               isAdmin=isAdmin2))
    return StudentListResponse(response=0, description="OK", isAdmin=isAdmin,
                               studentList=studentList)


def createAssignmentMethod(request):
    """createAssignmentMethod(request)
       request (assignmentTitle, assignmentDesc, dateUploaded, courseId, uploaderId,
                dueDate, dueTime, urlList)"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    try:
        uploaderId = ndb.Key(urlsafe=getattr(request, 'uploaderId'))
    except Exception:
        print "Invalid uploaderId"
        return Response(response=1, description="Invalid uploaderId")
    course = courseId.get()
    if course is None:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    newAssignment = Assignment()
    setValue(newAssignment, request, -1, ['uploaderId', 'courseId'])
    dateUploaded = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    setattr(newAssignment, 'courseId', courseId)
    setattr(newAssignment, 'uploaderId', uploaderId)
    setattr(newAssignment, 'dateUploaded', dateUploaded)
    assignmentId = newAssignment.put()
    course.assignmentIds.append(assignmentId)

    title = course.courseName
    course.put()
    memcache.delete(courseId.urlsafe())
    notificationText = "New assignment added!"
    createNotification(course.studentIds, 'Campus Connect',
                       notificationText, 'assignment',
                       assignmentId.urlsafe())
    sendNotification(id=courseId.urlsafe(), title=title,
                     text=notificationText, type='assignment')
    return Response(response=0, description="OK", key=assignmentId.urlsafe())


def createExamMethod(request):
    """createExamMethod(request)
       request (examTitle, examDesc, dateUploaded, courseId, profileId, dueDate,
                dueTime, urlList)
       To create a new exam"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    try:
        uploaderId = ndb.Key(urlsafe=getattr(request, 'uploaderId'))
    except Exception:
        print "Invalid uploaderId"
        return Response(response=1, description="Invalid uploaderId")
    course = courseId.get()
    if course is None:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    newExam = Exam()
    setValue(newExam, request, -1, ['uploaderId', 'courseId'])
    dateUploaded = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    setattr(newExam, 'uploaderId', uploaderId)
    setattr(newExam, 'courseId', courseId)
    setattr(newExam, 'dateUploaded', dateUploaded)
    examId = newExam.put()
    course.examIds.append(examId)
    title = course.courseName
    course.put()
    memcache.delete(courseId.urlsafe())
    notificationText = "New Exam added!"
    createNotification(course.studentIds, 'Campus Connect',
                       notificationText, 'exam',
                       examId.urlsafe())
    sendNotification(id=courseId.urlsafe(), title=title,
                     text=notificationText, type='exam')
    return Response(response=0, description="OK", key=examId.urlsafe())


def getAssignmentMethod(request):
    """getAssignmentMethod(request)
       request (profileId, assignmentId)"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return GetAssignmentResponse(response=1, description="Invalid profileId")
    try:
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
    except Exception:
        print "Invalid assigmentId"
        return GetAssignmentResponse(response=1, description="Invalid assignmentId")
    assignmentOpened.add(assignmentId.urlsafe())
    cacheVal = memcache.get(assignmentId.urlsafe())
    memViews = memcache.get('views' + assignmentId.urlsafe())
    if cacheVal is not None:
        if profileId == cacheVal[8]:
            isAuthor = 1
        else:
            isAuthor = 0
        if memViews is None:
            assignment = assignmentId.get()
            memViews = assignment.assignmentViews
            memcache.add('views' + assignmentId.urlsafe(), memViews)
        if isAuthor == 0:
            memcache.incr('views' + assignmentId.urlsafe())
        return GetAssignmentResponse(response=0, description="OK",
                                     isAuthor=isAuthor,
                                     assignmentTitle=cacheVal[0],
                                     assignmentDesc=cacheVal[1],
                                     lastUpdated=cacheVal[2],
                                     uploaderName=cacheVal[3],
                                     dueDate=cacheVal[4],
                                     dueTime=cacheVal[5],
                                     urlList=cacheVal[6],
                                     courseName=cacheVal[7],
                                     views=memViews + 1)
    assignment = assignmentId.get()
    if assignment is None:
        print "Invalid assignmentId"
        return GetAssignmentResponse(response=1, description="Invalid assignmentId")
    if profileId == assignment.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = assignment.uploaderId.get().profileName
    assignment.assignmentViews = assignment.assignmentViews + 1
    course = assignment.courseId.get()
    assignment.put()
    fields = [assignment.assignmentTitle, assignment.assignmentDesc, assignment.dateUploaded,
              uploaderName, assignment.dueDate, assignment.dueTime, assignment.urlList,
              course.courseName, assignment.uploaderId]
    memcache.add(assignmentId.urlsafe(), fields, 3600)
    memcache.add('views' + assignmentId.urlsafe(), assignment.assignmentViews, 3600)
    return GetAssignmentResponse(response=0, description="OK",
                                 isAuthor=isAuthor,
                                 views=assignment.assignmentViews,
                                 assignmentTitle=fields[0],
                                 assignmentDesc=fields[1],
                                 lastUpdated=fields[2],
                                 uploaderName=fields[3],
                                 dueDate=fields[4],
                                 dueTime=fields[5],
                                 urlList=fields[6],
                                 courseName=fields[7])


def getExamMethod(request):
    """getExamMethod(request)
       request (profileId, examId)"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return GetExamResponse(response=1, description="Invalid profileId")
    try:
        examId = ndb.Key(urlsafe=getattr(request, 'examId'))
    except Exception:
        print "Invalid courseId"
        return GetExamResponse(response=1, description="Invalid examId")
    examOpened.add(examId.urlsafe())
    cacheVal = memcache.get(examId.urlsafe())
    memViews = memcache.get('views' + examId.urlsafe())
    if cacheVal is not None:
        if profileId == cacheVal[8]:
            isAuthor = 1
        else:
            isAuthor = 0
        if memViews is None:
            exam = examId.get()
            memViews = exam.examViews
            memcache.add('views' + examId.urlsafe(), memViews)
        if isAuthor == 0:
            memcache.incr('views' + examId.urlsafe())
        return GetExamResponse(response=0, description="OK",
                               isAuthor=isAuthor, examTitle=cacheVal[0],
                               examDesc=cacheVal[1], lastUpdated=cacheVal[2],
                               uploaderName=cacheVal[3], dueDate=cacheVal[4],
                               dueTime=cacheVal[5], urlList=cacheVal[6],
                               courseName=cacheVal[7], views=memViews + 1)
    exam = examId.get()
    if exam is None:
        print "Invalid examId"
        return GetExamResponse(response=1, description="Invalid examId")
    if profileId == exam.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = exam.uploaderId.get().profileName
    exam.examViews = exam.examViews + 1
    exam.put()
    course = exam.courseId.get()
    fields = [exam.examTitle, exam.examDesc, exam.dateUploaded, uploaderName,
              exam.dueDate, exam.dueTime, exam.urlList, course.courseName,
              exam.uploaderId]
    memcache.add(examId.urlsafe(), fields, 3600)
    memcache.add('views' + examId.urlsafe(), exam.examViews, 3600)
    return GetExamResponse(response=0, description="OK",
                           isAuthor=isAuthor, views=exam.examViews,
                           examTitle=fields[0], examDesc=fields[1],
                           lastUpdated=fields[2],
                           uploaderName=fields[3], dueDate=fields[4],
                           dueTime=fields[5], urlList=fields[6],
                           courseName=fields[7])


def createNotesMethod(request):
    """createNotes(request)
       request (profileId, date, urlList,notesDesc, classNumber, courseId, title)
       To create new Notes"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    profile = profileId.get()
    if profile is None:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    newNotes = Notes()
    setValue(newNotes, request, -1, ['courseId', 'profileId'])
    # CHECKS IF NOTEBOOK WITH SAME profileID AND courseId already exists
    query = NoteBook.query(ndb.AND(NoteBook.courseId == courseId,
                                   NoteBook.uploaderId == profileId))
    noteBookResult = query.fetch()
    if noteBookResult:
        for noteBook in noteBookResult:
            setattr(newNotes, 'classNumber', str(len(noteBook.notesIds) + 1))
            try:
                addToNoteBook(noteBook.key, newNotes)
            except Exception, E:
                print str(E)
                return Response(response=1, description=str(E))
            createNBDoc(newNotes.title, newNotes.notesDesc,
                        profile.profileName, noteBook.key.urlsafe())
            return Response(response=0, description="OK",
                            key=noteBook.key.urlsafe())
    else:
        try:
            setattr(newNotes, 'classNumber', str(1))
            noteBookId = createNoteBook(profileId, courseId)
            addToNoteBook(noteBookId, newNotes)
        except Exception, E:
            print str(E) + "SSSSSSSSsss"
            return Response(response=1, description=str(E))
        createNBDoc(newNotes.title, newNotes.notesDesc,
                    profile.profileName, noteBookId.urlsafe())
        return Response(response=0, description="OK", key=noteBookId.urlsafe())


def createNoteBook(profileId, courseId):
    """createNoteBook(profileId, courseId)
       To create new noteBook"""
    lastUpdated = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    newNoteBook = NoteBook(courseId=courseId, uploaderId=profileId, lastUpdated=lastUpdated)
    course = courseId.get()
    if course is None:
        raise Exception("Invalid courseId")
    college = course.collegeId.get()
    if college is None:
        raise Exception("Invalid collegeId")
    college.noteBookCount += 1
    profile = profileId.get()
    if profile is None:
        raise Exception("Invalid profileId")
    noteBookId = newNoteBook.put()
    profile.uploadedNoteBookIds.append(noteBookId)
    college.put()
    profile.put()
    course.noteBookIds.append(noteBookId)
    course.put()
    return noteBookId


def addToNoteBook(noteBookId, newNotes):
    """addToNoteBook(noteBookId, newNotes)
       To add new notes to existing noteBook"""
    newNotes.noteBookId = noteBookId
    notesId = newNotes.put()
    noteBook = noteBookId.get()
    if noteBook is None:
        raise Exception("Invalid noteBookId")
    bmUserList = noteBook.bmUserList
    noteBook.notesIds.append(notesId)
    noteBook.frequency += 1
    notesList = []
    pages = 0
    for notesId in noteBook.notesIds:
        notes = notesId.get()
        if notes is None:
            print "Invalid notesId"
            continue
        notesList.append(NotesResponse(title=notes.title,
                                       description=notes.notesDesc,
                                       date=notes.date,
                                       classNumber=notes.classNumber,
                                       urlList=notes.urlList))
        pages += len(notes.urlList)
    noteBook.lastUpdated = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    noteBookUploader = noteBook.uploaderId.get()
    uploaderName = noteBookUploader.profileName
    course = noteBook.courseId.get()
    title = course.courseName + ': ' + uploaderName
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        cacheVal[2] = noteBook.lastUpdated
        cacheVal[3] += 1
        cacheVal[4] = pages
        cacheVal[6] = notesList
        memcache.add(noteBookId.urlsafe(), cacheVal)
    noteBook.put()
    notificationText = "New notes added!"
    if len(noteBook.bmUserList) != 0:
        print len(noteBook.bmUserList)
        createNotification(bmUserList, 'Campus Connect', notificationText,
                           'notes', noteBookId.urlsafe())
    sendNotification(id=noteBookId.urlsafe(), title=title, text=notificationText, type='notes')


def getNoteBook(request):
    """getNoteBook(request)
       request (profileId, noteBookId)
       To get noteBook"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception, E:
        print "Invalid profileId\n" + str(E)
        return NoteBookDetailResponse(response=1, description="Invalid profileId")
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    except Exception, E:
        print "Invalid noteBookId\n" + str(E)
        return NoteBookDetailResponse(response=1, description="Invalid noteBookId")
    noteBookOpened.add(noteBookId.urlsafe())
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        memViews = memcache.get('views' + noteBookId.urlsafe())
        if memViews is None:
            noteBook = noteBookId.get()
            memViews = noteBook.views
            memcache.add('views' + noteBookId.urlsafe(), memViews, 3600)
        noteBookOpened.add(noteBookId.urlsafe())
        bmUserList = cacheVal[8]
        if profileId in bmUserList:
            bookmarkStatus = 1
        else:
            bookmarkStatus = 0
        ratedUserList = cacheVal[9]
        if profileId in ratedUserList:
            for i in range(len(ratedUserList)):
                if ratedUserList[i] == profileId:
                    rated = cacheVal[10][i]
        else:
            rated = -1
        if profileId == cacheVal[11]:
            isAuthor = 1
        else:
            isAuthor = 0
        if isAuthor == 0:
            memcache.incr('views' + noteBookId.urlsafe())
        return NoteBookDetailResponse(courseName=cacheVal[0],
                                      isAuthor=isAuthor, uploaderName=cacheVal[1],
                                      lastUpdated=cacheVal[2], views=memViews + 1,
                                      rated=rated, frequency=cacheVal[3],
                                      pages=cacheVal[4], totalRating=cacheVal[5],
                                      notes=cacheVal[6], bookmarkStatus=bookmarkStatus,
                                      response=0, colour=cacheVal[7],
                                      description="OK")

    noteBook = noteBookId.get()
    if noteBook is None:
        print "Invalid noteBookId"
        return NoteBookDetailResponse(response=1, description="Invalid noteBookId")
    if noteBook.uploaderId == profileId:
        isAuthor = 1
    else:
        isAuthor = 0
    profile = profileId.get()
    if profile is None:
        print "Invalid profileId"
        return NoteBookDetailResponse(response=1, description="Invalid profileId")
    if noteBookId in profile.bookmarkedNoteBookIds:
        bookmarkStatus = 1
    else:
        bookmarkStatus = 0
    noteBookUploader = noteBook.uploaderId.get()
    course = noteBook.courseId.get()
    if course is None:
        print "Invalid courseId"
        return NoteBookDetailResponse(response=1, description="Invalid courseId")
    uploaderName = noteBookUploader.profileName
    lastUpdated = noteBook.lastUpdated
    views = noteBook.views + 1
    noteBook.views = views
    noteBook.put()
    frequency = noteBook.frequency
    totalRating = noteBook.totalRating
    rated = -1
    for i in range(len(noteBook.ratedUserIds)):
        if noteBook.ratedUserIds[i] == profileId:
            rated = noteBook.ratingList[i]
    notesList = []
    pages = 0
    for notesId in noteBook.notesIds:
        notes = notesId.get()
        if notes is None:
            return NoteBookDetailResponse(response=1, description="Invalid notesId")
        notesList.append(NotesResponse(title=notes.title,
                                       description=notes.notesDesc,
                                       date=notes.date,
                                       classNumber=notes.classNumber,
                                       urlList=notes.urlList))
        pages += len(notes.urlList)
    fields = [course.courseName, uploaderName, lastUpdated, frequency, pages, totalRating,
              notesList, course.colour, noteBook.bmUserList, noteBook.ratedUserIds,
              noteBook.ratingList, noteBook.uploaderId]
    memcache.add(noteBookId.urlsafe(), fields, 3600)
    memcache.add('views' + noteBookId.urlsafe(), views, 3600)
    return NoteBookDetailResponse(courseName=course.courseName,
                                  isAuthor=isAuthor, uploaderName=uploaderName,
                                  lastUpdated=lastUpdated, views=views,
                                  rated=rated, frequency=frequency,
                                  pages=pages, totalRating=totalRating,
                                  notes=notesList, bookmarkStatus=bookmarkStatus,
                                  response=0, colour=course.colour,
                                  description="OK")


def getNoteBookListMethod(request):
    """getNoteBookListMethod(request)
       request (noteBookIds[]) OR request(bpid) OR request(upid) OR request(courseId)
       OR request(profileId)"""
    noteBookIds = getattr(request, 'noteBookIds', None)
    bpid = getattr(request, 'bpid', None)
    upid = getattr(request, 'upid', None)
    courseId = getattr(request, 'courseId', None)
    profileId = getattr(request, 'profileId', None)
    noteBookList = []
    if noteBookIds:
        for idurlsafe in noteBookIds:
            try:
                noteBookId = ndb.Key(urlsafe=idurlsafe)
            except Exception:
                print "Invalid noteBookId"
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            noteBook = noteBookId.get()
            if noteBook is None:
                print "Invalid noteBookId"
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            course = noteBook.courseId.get()
            if course is None:
                print "Invalid courseId"
                return NoteBookListResponse(response=1, description="Invalid courseId")
            uploader = noteBook.uploaderId.get()
            if uploader is None:
                print "Invalid profileId"
                return NoteBookListResponse(response=1, description="Invalid profileId")
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    continue
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=idurlsafe,
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated,
                                   colour=course.colour)
            noteBookList.append(new)
    elif bpid:
        try:
            profileId = ndb.Key(urlsafe=bpid)
        except Exception:
            print "Invalid profileId"
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            print "Invalid profileId"
            return NoteBookListResponse(response=1, description="Invalid profileId")
        bookmarkedIds = profile.bookmarkedNoteBookIds
        for noteBookId in bookmarkedIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                print "Invalid noteBookId"
                continue
            course = noteBook.courseId.get()
            if course is None:
                print "Invalid courseId"
                continue
            uploader = noteBook.uploaderId.get()
            if uploader is None:
                print "Invalid uploaderId"
                continue
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    print "Invalid notesId"
                    continue
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated,
                                   colour=course.colour)
            noteBookList.append(new)
    elif upid:
        try:
            profileId = ndb.Key(urlsafe=upid)
        except Exception:
            print "Invalid profileId"
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            print "Invalid profileId"
            return NoteBookListResponse(response=1, description="Invalid profileId")
        uploadedIds = profile.uploadedNoteBookIds
        for noteBookId in uploadedIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                print "Invalid noteBookId"
                continue
            course = noteBook.courseId.get()
            if course is None:
                print "Invalid courseId"
                continue
            uploader = noteBook.uploaderId.get()
            if uploader is None:
                return NoteBookListResponse(response=1, description="Invalid profileId")
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    return NoteBookListResponse(response=1, description="Invalid notesId")
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated,
                                   colour=course.colour)
            noteBookList.append(new)
    elif courseId:
        try:
            courseId = ndb.Key(urlsafe=courseId)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid courseId")
        course = courseId.get()
        if course is None:
            return NoteBookListResponse(response=1, description="Invalid courseId")
        noteBookIds = course.noteBookIds
        for noteBookId in noteBookIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            uploader = noteBook.uploaderId.get()
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    return NoteBookListResponse(response=1, description="Invalid notesId")
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated,
                                   colour=course.colour)
            noteBookList.append(new)
    elif profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
        except Exception:
            print "Invalid profileId"
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            print "Invalid profileId"
            return NoteBookListResponse(response=1, description="Invalid profileId")
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            if course is None:
                print "Invalid courseId"
                continue
            noteBookIds = course.noteBookIds
            for noteBookId in noteBookIds:
                noteBook = noteBookId.get()
                if noteBook is None:
                    print "Invalid noteBookId"
                    continue
                uploader = noteBook.uploaderId.get()
                if uploader is None:
                    print "Invalid profileId"
                    continue
                pages = 0
                for notesId in noteBook.notesIds:
                    notes = notesId.get()
                    if notes is None:
                        print "Invalid notesId"
                        continue
                    pages += len(notes.urlList)
                new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                       courseName=course.courseName,
                                       uploaderName=uploader.profileName,
                                       views=noteBook.views, pages=pages,
                                       totalRating=noteBook.totalRating,
                                       frequency=noteBook.frequency,
                                       lastUpdated=noteBook.lastUpdated,
                                       colour=course.colour)
                noteBookList.append(new)
    else:
        print "Bad request"
        return NoteBookListResponse(response=1, description="Bad request")
    return NoteBookListResponse(response=0, description="OK",
                                noteBookList=noteBookList)


def rateThisMethod(request):
    """rateThisMethod(request)
       request (profileId, rating, noteBookId)
       To rate a noteBook"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")
    rating = getattr(request, 'rating')
    noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    noteBook = noteBookId.get()
    if noteBook is None:
        print "Invalid noteBookId"
        return Response(response=1, description="Invalid noteBookId")
    if profileId in noteBook.ratedUserIds:
        idx = noteBook.ratedUserIds.index(profileId)
        del(noteBook.ratingList[idx])
        noteBook.ratedUserIds.remove(profileId)
    noteBook.ratedUserIds.append(profileId)
    noteBook.ratingList.append(rating)
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        cacheVal[9] = noteBook.ratedUserIds
        cacheVal[10] = noteBook.ratingList
        memcache.set(noteBookId.urlsafe(), cacheVal)
    noteBook.put()
    return Response(response=0, description="OK")


def coursePageMethod(request):
    """coursePage(request)
       request(profileId, courseId)"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        print "Invalid courseId"
        return CoursePageResponse(response=1, description="Invalid courseId")
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return CoursePageResponse(response=1, description="Invalid profileId")
    cacheVal = memcache.get(courseId.urlsafe())
    if cacheVal is not None:
        if profileId in cacheVal[13]:
            isSubscribed = 1
        else:
            isSubscribed = 0
        return CoursePageResponse(response=0, description="OK", isSubscribed=isSubscribed,
                                  courseName=cacheVal[0], date=cacheVal[1],
                                  startTime=cacheVal[2], endTime=cacheVal[3],
                                  examCount=cacheVal[4], assignmentCount=cacheVal[5],
                                  notesCount=cacheVal[6], examList=cacheVal[7],
                                  assignmentList=cacheVal[8], studentCount=cacheVal[9],
                                  professorName=cacheVal[10], colour=cacheVal[11],
                                  elective=cacheVal[12], collegeName=cacheVal[14],
                                  branchNames=cacheVal[15], sectionNames=cacheVal[16],
                                  batchNames=cacheVal[17], semester=cacheVal[18])
    course = courseId.get()
    if course is None:
        print "Invalid courseId"
        return CoursePageResponse(response=1, description="Invalid courseId")
    if profileId in course.studentIds:
        isSubscribed = 1
    else:
        isSubscribed = 0
    college = course.collegeId.get()
    collegeName = college.collegeName
    assignmentList, examList = [], []
    curDate = datetime.datetime.now().date()
    curTime = (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).time()
    dueAssignments, dueExams, recentNotes = 0, 0, 0
    assignmentIds = course.assignmentIds
    studentCount = len(course.studentIds)
    for assignmentId in assignmentIds:
        assignment = assignmentId.get()
        if assignment is None:
            print "Invalid assignmentId"
            continue
        a = assignment.dueDate
        date, month, year = int(a[0:2]), int(a[3:5]), int(a[6:10])
        dueDate = datetime.date(year, month, date)
        if(curDate > dueDate):
            continue
        a = assignment.dueTime
        hour, minute = int(a[0:2]), int(a[3:5])
        dueTime = datetime.time(hour, minute)
        if(curDate == dueDate and dueTime < curTime):
            continue
        dueAssignments = dueAssignments + 1
        uploader = assignment.uploaderId.get()
        if uploader is None:
            print "Invalid uploaderId"
            continue
        assignmentList.append(AssExamResponse(Id=assignmentId.urlsafe(),
                                              name=assignment.assignmentTitle,
                                              dueDate=assignment.dueDate,
                                              dueTime=assignment.dueTime,
                                              uploaderName=uploader.profileName,
                                              dateUploaded=assignment.dateUploaded,
                                              views=assignment.assignmentViews,
                                              description=assignment.assignmentDesc))
    examIds = course.examIds
    for examId in examIds:
        exam = examId.get()
        if exam is None:
            return CoursePageResponse(response=1, description="Invalid examId")
        a = exam.dueDate
        date, month, year = int(a[0:2]), int(a[3:5]), int(a[6:10])
        dueDate = datetime.date(year, month, date)
        if(curDate > dueDate):
            continue
        a = exam.dueTime
        hour, minute = int(a[0:2]), int(a[3:5])
        dueTime = datetime.time(hour, minute)
        if(curDate == dueDate and dueTime < curTime):
            continue
        dueExams = dueExams + 1
        uploader = exam.uploaderId.get()
        if uploader is None:
            return CoursePageResponse(response=1, description="Invalid profileId")
        examList.append(AssExamResponse(Id=examId.urlsafe(),
                                        name=exam.examTitle,
                                        dueDate=exam.dueDate,
                                        dueTime=exam.dueTime,
                                        uploaderName=uploader.profileName,
                                        dateUploaded=exam.dateUploaded,
                                        views=exam.examViews,
                                        description=exam.examDesc))
        noteBookIds = course.noteBookIds
        for noteBookId in noteBookIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                print "Invalid noteBookId"
                continue
            a = str(noteBook.lastUpdated)
            date, month, year = int(a[8:10]), int(a[5:7]), int(a[0:4])
            lastUpdated = datetime.date(year, month, date)
            if(curDate - lastUpdated).days > 7:
                continue
            recentNotes = recentNotes + 1
    info = [collegeName, dueExams, dueAssignments, recentNotes, examList, assignmentList, studentCount]
    fields = [course.courseName, course.date, course.startTime, course.endTime,
              info[1], info[2], info[3], info[4],
              info[5], info[6], course.professorName, course.colour,
              course.elective, course.studentIds, info[0], course.branchNames,
              course.sectionNames, course.batchNames, course.semester]
    memcache.add(course.key.urlsafe(), fields, 3600)
    return CoursePageResponse(response=0, description="OK", isSubscribed=isSubscribed,
                              courseName=course.courseName, date=course.date,
                              startTime=course.startTime, endTime=course.endTime,
                              examCount=dueExams, assignmentCount=dueAssignments,
                              notesCount=recentNotes, examList=examList,
                              assignmentList=assignmentList, studentCount=studentCount,
                              professorName=course.professorName, colour=course.colour,
                              elective=course.elective, collegeName=collegeName,
                              branchNames=course.branchNames,
                              sectionNames=course.sectionNames,
                              batchNames=course.batchNames, semester=course.semester)


def getAssignmentListMethod(request):
    """getAssignmentListmethod(rquest)
       request (profileId) OR request (courseId)"""
    profileId = getattr(request, 'profileId', None)
    courseId = getattr(request, 'courseId', None)
    if profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
        except Exception:
            return GetAssListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            print "Invalid profileId"
            return GetAssListResponse(response=1, description="Invalid profileId")
        assList = []
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            if course is None:
                return GetAssListResponse(response=1, description="Invalid courseId")
            for assignmentId in course.assignmentIds:
                assignment = assignmentId.get()
                if assignment is None:
                    return GetAssListResponse(response=1, description="Invalid assignmentId")
                if profileId == assignment.uploaderId:
                    isAuthor = 1
                else:
                    isAuthor = 0
                uploaderName = assignment.uploaderId.get().profileName
                assList.append(AssignmentResponse(assignmentId=assignmentId.urlsafe(), isAuthor=isAuthor,
                                                  views=assignment.assignmentViews,
                                                  assignmentTitle=assignment.assignmentTitle,
                                                  assignmentDesc=assignment.assignmentDesc,
                                                  lastUpdated=assignment.dateUploaded,
                                                  uploaderName=uploaderName, dueDate=assignment.dueDate,
                                                  dueTime=assignment.dueTime, pages=len(assignment.urlList),
                                                  courseName=course.courseName, colour=course.colour))
    else:
        try:
            courseId = ndb.Key(urlsafe=courseId)
        except Exception:
            return GetAssListResponse(response=1, description="Invalid courseId")
        assList = []
        course = courseId.get()
        if course is None:
            return GetAssListResponse(response=1, description="Invalid courseId")
        for assignmentId in course.assignmentIds:
            assignment = assignmentId.get()
            if assignment is None:
                return GetAssListResponse(response=1, description="Invalid assignmentId")
            if profileId == assignment.uploaderId:
                isAuthor = 1
            else:
                isAuthor = 0
            uploaderName = assignment.uploaderId.get().profileName
            assList.append(AssignmentResponse(assignmentId=assignmentId.urlsafe(),
                                              isAuthor=isAuthor,
                                              views=assignment.assignmentViews,
                                              assignmentTitle=assignment.assignmentTitle,
                                              assignmentDesc=assignment.assignmentDesc,
                                              lastUpdated=assignment.dateUploaded,
                                              uploaderName=uploaderName,
                                              dueDate=assignment.dueDate,
                                              dueTime=assignment.dueTime,
                                              pages=len(assignment.urlList),
                                              courseName=course.courseName,
                                              colour=course.colour))
    return GetAssListResponse(response=0, description="OK",
                              assList=assList)


def getExamListMethod(request):
    profileId = getattr(request, 'profileId', None)
    courseId = getattr(request, 'courseId', None)
    if profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
        except Exception:
            print "Invalid profileId"
            return GetExamListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            print "Invalid profileId"
            return GetExamListResponse(response=1, description="Invalid profileId")
        examList = []
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            if course is None:
                print "Invalid courseId"
                continue
            for examId in course.examIds:
                exam = examId.get()
                if exam is None:
                    print "Invalid examId"
                    continue
                if profileId == exam.uploaderId:
                    isAuthor = 1
                else:
                    isAuthor = 0
                uploaderName = exam.uploaderId.get().profileName
                examList.append(ExamResponse(examId=examId.urlsafe(),
                                             isAuthor=isAuthor, views=exam.examViews,
                                             examTitle=exam.examTitle,
                                             examDesc=exam.examDesc,
                                             lastUpdated=exam.dateUploaded,
                                             uploaderName=uploaderName,
                                             dueDate=exam.dueDate,
                                             dueTime=exam.dueTime,
                                             pages=len(exam.urlList),
                                             courseName=course.courseName,
                                             colour=course.colour))
    else:
        try:
            courseId = ndb.Key(urlsafe=courseId)
        except Exception:
            print "Invalid courseId"
            return GetExamListResponse(response=1, description="Invalid courseId")
        course = courseId.get()
        examList = []
        for examId in course.examIds:
            exam = examId.get()
            if exam is None:
                print "Invalid examId"
                continue
            if profileId == exam.uploaderId:
                isAuthor = 1
            else:
                isAuthor = 0
            uploaderName = exam.uploaderId.get().profileName
            examList.append(ExamResponse(examId=examId.urlsafe(),
                                         isAuthor=isAuthor, views=exam.examViews,
                                         examTitle=exam.examTitle,
                                         examDesc=exam.examDesc,
                                         lastUpdated=exam.dateUploaded,
                                         uploaderName=uploaderName,
                                         dueDate=exam.dueDate,
                                         dueTime=exam.dueTime,
                                         pages=len(exam.urlList),
                                         courseName=course.courseName,
                                         colour=course.colour))
    return GetExamListResponse(response=0, description="OK",
                               examList=examList)


def bookmarkMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        print "Invalid profileId"
        return BookmarkResponse(response=1, description="Invalid profileId")
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    except Exception:
        print "Invalid noteBookId"
        return BookmarkResponse(response=1, description="Invalid noteBookId")
    profile = profileId.get()
    noteBook = noteBookId.get()
    if noteBookId in profile.bookmarkedNoteBookIds:
        profile.bookmarkedNoteBookIds.remove(noteBookId)
        if profileId in noteBook.bmUserList:
            noteBook.bmUserList.remove(profileId)
        status = 0
    else:
        profile.bookmarkedNoteBookIds.append(noteBookId)
        if profileId not in noteBook.bmUserList:
            noteBook.bmUserList.append(profileId)
        status = 1
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        cacheVal[8] = noteBook.bmUserList
    memcache.set(noteBookId.urlsafe(), cacheVal)
    profile.put()
    noteBook.put()
    return BookmarkResponse(response=0, description="OK", bookmarkStatus=status)


def clearAll():
    colleges = College.query().fetch()
    for college in colleges:
        college.key.delete()
    profiles = Profile.query().fetch()
    for profile in profiles:
        profile.key.delete()
    courses = Course.query().fetch()
    for course in courses:
        memcache.delete(course.key.urlsafe())
        course.key.delete()
    notesList = Notes.query().fetch()
    for notes in notesList:
        notes.key.delete()
    noteBookList = NoteBook.query().fetch()
    for noteBook in noteBookList:
        noteBook.key.delete()
    assignmentList = Assignment.query().fetch()
    for assignment in assignmentList:
        assignment.key.delete()
    examList = Exam.query().fetch()
    for exam in examList:
        exam.key.delete()
    idx = [search.Index('Course'), search.Index('NoteBook')]
    for index in idx:
        ids = []
        results = index.search("NOT zoo")
        for doc in results:
            key = doc.doc_id
            ids.append(key)
        index.delete(ids)
    for notif in Notification.query().fetch():
        notif.key.delete()


def collegeListMethod(request):
    allCollege = College.query().fetch()
    collegeList = []
    for col in allCollege:
        collegeId = col.key
        collegeDetail = CollegeDetails(collegeId=collegeId.urlsafe(),
                                       collegeName=col.collegeName,
                                       branchNames=col.branchNameList)
        collegeList.append(collegeDetail)
    return CollegeListResponse(collegeList=collegeList)


def addBranchMethod(request):
    collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
    branchName = getattr(request, 'branchName')
    college = collegeId.get()
    if branchName not in college.branchNameList:
        college.branchNameList.append(branchName)
    college.put()


def unsubscribeCourseMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception, E:
        print "Invalid profileId\n" + str(E)
        return Response(response=1, description="Invaild profileId " + str(E))
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception, E:
        print "Invalid courseId\n" + str(E)
        return Response(response=1, description="Invaild courseId " + str(E))
    profile = profileId.get()
    course = courseId.get()
    if profile is None:
        return Response(response=1, description="Invaild profileId")
    if course is None:
        return Response(response=1, description="Invaild courseId")
    if courseId in profile.subscribedCourseIds:
        profile.subscribedCourseIds.remove(courseId)
        profile.put()
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            cacheVal[9] -= 1
            cacheVal[13].remove(profileId)
            memcache.set(courseId.urlsafe(), cacheVal)
        if profileId in course.studentIds:
            course.studentIds.remove(profileId)
            course.put()
    else:
        profile.subscribedCourseIds.append(courseId)
        profile.put()
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            cacheVal[9] += 1
            cacheVal[13].append(profileId)
            memcache.set(courseId.urlsafe(), cacheVal)
        if profileId in course.studentIds:
            course.studentIds.append(profileId)
            course.put()

    return Response(response=0, description="OK")


def deleteNoteBook(id, delNotes=0):
    try:
        noteBookId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such noteBookId")
    noteBook = noteBookId.get()
    if noteBook is None:
        return Response(response=1, description="No such noteBookId")
    if delNotes == 0:
        for notesId in noteBook.notesIds:
            notesId.delete()
    course = noteBook.courseId.get()
    course.noteBookIds.remove(noteBookId)
    uploader = noteBook.uploaderId.get()
    uploader.uploadedNoteBookIds.remove(noteBookId)
    bookmarkedProfiles = Profile.query(Profile.bookmarkedNoteBookIds == noteBookId).fetch()
    college = course.collegeId.get()
    college.noteBookCount -= 1
    college.put()
    course.put()
    uploader.put()
    for profileR in bookmarkedProfiles:
        profile = profileR.key.get()
        profile.bookmarkedNoteBookIds.remove(noteBookId)
        profile.put()
    noteBookId.delete()
    search.Index('NoteBook').delete([id])
    return Response(response=0, description="OK")


def deleteNotes(id):
    try:
        notesId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such notes")
    notes = notesId.get()
    noteBookId = notes.noteBookId
    noteBook = noteBookId.get()
    noteBook.notesIds.remove(notesId)
    noteBook.frequency -= 1
    noteBook.put()
    if noteBook.frequency == 0:
        deleteNoteBook(noteBookId.urlsafe(), delNotes=1)
    return Response(response=0, description="OK")


def deleteAssignment(id):
    try:
        assignmentId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such assignmentId")
    assignment = assignmentId.get()
    course = assignment.courseId.get()
    course.assignmentIds.remove(assignmentId)
    course.put()
    assignmentId.delete()
    memcache.delete(assignmentId.urlsafe())
    memcache.delete(course.key.urlsafe())
    return Response(response=0, description="OK")


def deleteExam(id):
    try:
        examId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such examId")
    exam = examId.get()
    course = exam.courseId.get()
    course.examIds.remove(examId)
    course.put()
    examId.delete()
    memcache.delete(course.key.urlsafe())
    memcache.delete(examId.urlsafe())
    return Response(response=0, description="OK")


def deleteProfile(id):
    try:
        profileId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such profileId")
    profile = profileId.get()
    college = profile.collegeId.get()
    college.studentCount -= 1
    for noteBookId in profile.uploadedNoteBookIds:
        deleteNoteBook(noteBookId.urlsafe())
    assUploadedList = Assignment.query(Assignment.uploaderId == profileId).fetch()
    for assignment in assUploadedList:
        assignmentId = assignment.key
        deleteAssignment(assignmentId.urlsafe())
    examUploadedList = Exam.query(Exam.uploaderId == profileId).fetch()
    for exam in examUploadedList:
        examId = exam.key
        deleteExam(examId.urlsafe())
    for courseId in profile.administeredCourseIds:
        memcache.delete(courseId.urlsafe())
        course = courseId.get()
        if len(course.adminIds) == 1:
            if len(course.studentIds) == 1:
                return Response(response=1, description="No admins")
            course.adminIds.append(course.studentIds[0])
            newAdmin = course.adminIds[0]
            newAdmin.administeredCourseIds.append(courseId)
            newAdmin.put()
        if profileId in course.studentIds:
            course.studentIds.remove(profileId)
            course.put()
    profileId.delete()
    college.put()
    return Response(response=0, description="OK")


def deleteCourse(id):
    try:
        courseId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such courseId")
    course = courseId.get()
    if course is None:
        return Response(response=1, description="No such courseId")
    for noteBookId in course.noteBookIds:
        deleteNoteBook(noteBookId.urlsafe())
    for assignmentId in course.assignmentIds:
        deleteAssignment(assignmentId.urlsafe())
    for examId in course.examIds:
        deleteExam(examId.urlsafe())
    result = Profile.query(ndb.OR(Profile.administeredCourseIds == courseId,
                                  Profile.subscribedCourseIds == courseId,
                                  Profile.availableCourseIds == courseId)).fetch()
    for profile in result:
        profile1 = profile.key.get()
        if courseId in profile1.subscribedCourseIds:
            profile1.subscribedCourseIds.remove(courseId)
        if courseId in profile1.availableCourseIds:
            profile1.availableCourseIds.remove(courseId)
        if courseId in profile1.administeredCourseIds:
            profile1.administeredCourseIds.remove(courseId)
        profile1.put()
    college = course.collegeId.get()
    college.courseIds.remove(courseId)
    college.put()
    memcache.delete(courseId.urlsafe())
    courseId.delete()
    search.Index('Course').delete([id])
    return Response(response=0, description='OK')


def deleteCollege(id):
    try:
        collegeId = ndb.Key(urlsafe=id)
    except Exception:
        return Response(response=1, description="No such collegeId")
    college = collegeId.get()
    if college is None:
        return Response(response=1, description="No such collegeId")
    collegeId.delete()
    return Response(response=0, description='OK')


def deleteMethod(request):
    profileId = getattr(request, 'profileId', None)
    notesId = getattr(request, 'notesId', None)
    noteBookId = getattr(request, 'noteBookId', None)
    assignmentId = getattr(request, 'assignmentId', None)
    examId = getattr(request, 'examId', None)
    courseId = getattr(request, 'courseId', None)
    collegeId = getattr(request, 'collegeId', None)
    if profileId:
        return deleteProfile(profileId)
    if notesId:
        return deleteNotes(notesId)
    if noteBookId:
        return deleteNoteBook(noteBookId)
    if assignmentId:
        return deleteAssignment(assignmentId)
    if examId:
        return deleteExam(examId)
    if courseId:
        return deleteCourse(courseId)
    if collegeId:
        return deleteCollege(collegeId)


def createNotification(profileIds, title, text, type, id):
    timeStamp = datetime.datetime.now()
    newNotification = Notification(type=type, id=id, title=title, text=text,
                                   profileIdList=profileIds, timeStamp=timeStamp)
    newNotification.put()


def getNotificationMethod(request):
    profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    results = Notification.query(Notification.profileIdList == profileId).order(-Notification.timeStamp)
    notifList = []
    for result in results:
        notif = NotificationResponse(title=result.title, text=result.text,
                                     timeStamp=result.timeStamp,
                                     type=result.type, id=result.id)
        notifList.append(notif)
    return NotificationList(notificationList=notifList)
