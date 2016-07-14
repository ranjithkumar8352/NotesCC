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
from models import BookmarkResponse, Notification, NotificationResponse
from models import NotificationList, BranchListResponse, CollegeRequestModel
from models import Report
from searchAPI import createNBDoc
from FCM import sendNotification
from sendEmail import sendEmail
from sparkpost import SparkPost
from config import CLG_STATS_TIME

from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.api import memcache


noteBookOpened = set()
assignmentOpened = set()
examOpened = set()
courseUpdate = set()


def createCollegeMethod(request):
    """createCollegeMethod(request)
    request (collegeName, abbreviation, location, collegeType, semStartDate,
    semEndDate, branchNameList)
    To create New college"""
    newCollege = College()
    try:
        setattr(newCollege, 'collegeName', getattr(request, 'collegeName'))
        setattr(newCollege, 'abbreviation', getattr(request, 'abbreviation'))
        setattr(newCollege, 'location', getattr(request, 'location'))
        setattr(newCollege, 'collegeType', getattr(request, 'collegeType'))
        setattr(newCollege, 'semStartDate', getattr(request, 'semStartDate'))
        setattr(newCollege, 'semEndDate', getattr(request, 'semEndDate'))
        branchNameList = set(getattr(request, 'branchNameList'))
        setattr(newCollege, 'branchNameList', list(branchNameList))
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
        memcache.add(key.urlsafe(), 0, CLG_STATS_TIME)
        memcache.add('stu' + key.urlsafe(), 0, CLG_STATS_TIME)
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
        setattr(newProfile, 'profileName', getattr(request, 'profileName'))
        setattr(newProfile, 'collegeId', collegeId)
        setattr(newProfile, 'batchName', getattr(request, 'batchName'))
        setattr(newProfile, 'branchName', getattr(request, 'branchName'))
        setattr(newProfile, 'sectionName', getattr(request, 'sectionName'))
        setattr(newProfile, 'photoUrl', getattr(request, 'photoUrl'))
        setattr(newProfile, 'email', getattr(request, 'email'))
        setattr(newProfile, 'gcmId', getattr(request, 'gcmId'))
    except Exception, E:
        print str(E)
        traceback.print_stack()
        return Response(response=1, description=str(E))
    # Query for compatible courses and stores in availableCourseIds
    availableCourseIds = set()
    queryString = ndb.AND(Course.collegeId == collegeId,
                          Course.batchNames == newProfile.batchName,
                          Course.branchNames == newProfile.branchName,
                          Course.sectionNames == newProfile.sectionName)
    for course in Course.query(queryString).fetch():
        availableCourseIds.add(course.key)
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
        setattr(newProfile, 'availableCourseIds', list(availableCourseIds))
        # increasing the studentCount in college
        memcache.incr('stu' + collegeId.urlsafe())
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
        college = collegeId.get()
        if college is None:
            raise Exception("Invalid collegeId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
        profile = profileId.get()
        if profile is None:
            raise Exception("Invalid profileId")
    except Exception:
        print str(E)
        return Response(response=1, description=str(E))
    newCourse = Course()
    # storing details
    setattr(newCourse, 'courseName', getattr(request, 'courseName'))
    setattr(newCourse, 'batchNames', list(set(getattr(request, 'batchNames'))))
    setattr(newCourse, 'branchNames', list(set(getattr(request, 'branchNames'))))
    setattr(newCourse, 'sectionNames', list(set(getattr(request, 'sectionNames'))))
    setattr(newCourse, 'semester', getattr(request, 'semester'))
    setattr(newCourse, 'startTime', getattr(request, 'startTime'))
    setattr(newCourse, 'endTime', getattr(request, 'endTime'))
    setattr(newCourse, 'professorName', getattr(request, 'professorName'))
    setattr(newCourse, 'colour', getattr(request, 'colour'))
    setattr(newCourse, 'courseCode', getattr(request, 'courseCode'))
    setattr(newCourse, 'date', getattr(request, 'date'))
    setattr(newCourse, 'elective', getattr(request, 'elective'))
    # adding profileId to course.adminIds
    adminIds = set()
    adminIds.add(profileId)
    # adding profileId to course.studentIds
    studentIds = set()
    studentIds.add(profileId)

    setattr(newCourse, 'collegeId', collegeId)
    setattr(newCourse, 'adminIds', list(adminIds))
    setattr(newCourse, 'studentIds', list(studentIds))

    # To check if same course already exists
    queryString = ndb.AND(Course.courseCode == newCourse.courseCode,
                          Course.collegeId == collegeId,
                          Course.sectionNames.IN(list(set(newCourse.sectionNames))),
                          Course.branchNames.IN(list(set(newCourse.branchNames))),
                          Course.batchNames.IN(list(set(newCourse.batchNames))),
                          Course.professorName == newCourse.professorName)
    coursesWithSameCode = Course.query(queryString).fetch()
    if coursesWithSameCode:
        print "Course already exists"
        return Response(response=2, description="Course already exists")

    courseId = newCourse.put()
    # Adding courseId to admin.subscribedCourseIds
    for pId in adminIds:
        p = pId.get()
        subscribedCourseIds = set(p.subscribedCourseIds)
        subscribedCourseIds.add(courseId)
        p.subscribedCourseIds = list(subscribedCourseIds)
        p.put()

    # Adding courseId to college.courseIds
    courseIds = set(college.courseIds)
    courseIds.add(courseId)
    college.courseIds = list(courseIds)
    college.put()

    # Adding courseId to profile.administeredCourseIds
    administeredCourseIds = set(profile.administeredCourseIds)
    administeredCourseIds.add(courseId)
    profile.administeredCourseIds = list(administeredCourseIds)
    profile.put()

    # To update the availableCourseIds of users
    queryString = ndb.AND(Profile.collegeId == collegeId,
                          Profile.batchName.IN(newCourse.batchNames),
                          Profile.branchName.IN(newCourse.branchNames),
                          Profile.sectionName.IN(newCourse.sectionNames))
    profilesToUpdate = Profile.query(queryString).fetch()
    for p in profilesToUpdate:
        if p.key != profileId:
            availableCourseIds = set(p.availableCourseIds)
            availableCourseIds.add(courseId)
            p.availableCourseIds = list(availableCourseIds)
            p.put()
    return Response(response=0, description="OK", key=courseId.urlsafe())


def subscribeCourseMethod(request):
    """subscribeCourseMethod(request)
       request (profileId, courseIds)
       Subscribes the profileId to a list of courseIds"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
        profile = profileId.get()
        if profile is None:
            raise Exception("Invalid profileId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    courseIdList = getattr(request, 'courseIds')
    courseIds = set()
    # Adding courseId to profile.subscribedCourseIds
    for urlsafeKey in courseIdList:
        try:
            courseId = ndb.Key(urlsafe=urlsafeKey)
            course = courseId.get()
            if course is None:
                raise Exception("Invalid courseId")
        except Exception, E:
            print str(E)
            return Response(response=1, description=str(E))

        # adding courseId to profile.subscribedCourseId
        subscribedCourseIds = set(profile.subscribedCourseIds)
        subscribedCourseIds.add(courseId)
        profile.subscribedCourseIds = subscribedCourseIds
        courseIds.add(courseId)
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            studentIds = set(cacheVal[13])
            studentIds.add(profileId)
            cacheVal[13] = list(studentIds)
            cacheVal[9] += 1
            memcache.set(courseId.urlsafe(), cacheVal)

    # adding profileId to course.studentIds
    courseCodes = []
    for courseId in courseIds:
        course = courseId.get()
        courseCodes.append(course.courseCode)
        studentIds = set(course.studentIds)
        studentIds.add(profileId)
        course.studentIds = list(studentIds)
        course.put()
    # Removing courses with same courseCode from profile.availableCourseIds
    coursesWithSameCode = Course.query(Course.courseCode.IN(courseCodes))
    coursesWithSameCode = coursesWithSameCode.fetch()
    for course in coursesWithSameCode:
        courseId = course.key
        availableCourseIds = set(profile.availableCourseIds)
        availableCourseIds.discard(courseId)
        profile.availableCourseIds = list(availableCourseIds)
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
                profile = profileId.get()
                if profile is None:
                    raise Exception("Invalid profileId")
            except Exception, E:
                print str(E)
                return CourseListResponse(response=1, description=str(E))
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
                    course = courseId.get()
                    if course is None:
                        raise Exception("Invalid courseId")
                except Exception:
                    print str(E)
                    return CourseListResponse(response=1, description=str(E))
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
        profile = profileId.get()
        if profile is None:
            raise Exception("Invalid profileId")
    except Exception, E:
        print str(E)
        return FeedResponse(response=1, description=str(E))
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
    td = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    curDate = td.date()
    curTime = td.time()
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
        course = courseId.get()
        if course is None:
            raise Exception("Invalid courseId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
        profile = profileId.get()
        if profile is None:
            raise Exception("Invalid profileId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))

    print profile, course
    if courseId not in profile.administeredCourseIds:
        print "Here"
        # profile is not the admin
        administeredCourseIds = set(profile.administeredCourseIds)
        administeredCourseIds.add(courseId)
        profile.administeredCourseIds = list(administeredCourseIds)
        adminIds = set(course.adminIds)
        adminIds.add(profileId)
        course.adminIds = list(adminIds)
        print course
        # adding admin to memcache
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            cv = set(cacheVal[19])
            cv.add(profileId)
            cacheVal[19] = list(cv)
            memcache.set(courseId.urlsafe(), cacheVal)
        availableCourseIds = set(profile.availableCourseIds)
        availableCourseIds.discard(courseId)
        profile.availableCourseIds = list(availableCourseIds)
    else:
        # profile is already the admin
        administeredCourseIds = set(profile.administeredCourseIds)
        administeredCourseIds.discard(courseId)
        profile.administeredCourseIds = list(administeredCourseIds)
        adminIds = set(course.adminIds)
        adminIds.discard(profileId)
        course.adminIds = list(adminIds)

        # setting in memcache
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            cv = set(cacheVal[19])
            cv.discard(profileId)
            cacheVal[19] = cv
            memcache.set(courseId.urlsafe(), cacheVal)
    course.put()
    profile.put()
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
        profile = profileId.get()
        if profile is None:
            raise Exception("Invalid profileId")
    except Exception, E:
        print str(E)
        return StudentListResponse(response=1, description=str(E))
    try:
        courseId = ndb.Key(urlsafe=request.courseId)
        course = courseId.get()
        if course is None:
            raise Exception("Invalid courseId")
    except Exception, E:
        print str(E)
        return StudentListResponse(response=1, description=str(E))

    # setting whether current user is admin
    if courseId in profile.administeredCourseIds:
        isAdmin = 1
    else:
        isAdmin = 0

    # creating the list of profile
    studentList = []
    print course
    print course.adminIds
    for studentId in course.studentIds:
        # whether the student is admin
        if studentId in course.adminIds:
            isAdmin2 = 1
        else:
            isAdmin2 = 0
        student = studentId.get()
        if student is None:
            continue
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
        course = courseId.get()
        if course is None:
            raise Exception("Invalid courseId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    try:
        uploaderId = ndb.Key(urlsafe=getattr(request, 'uploaderId'))
        uploader = uploaderId.get()
        if uploader is None:
            raise Exception("Invalid uploaderId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))

    newAssignment = Assignment()

    # storing the details
    setattr(newAssignment, 'assignmentTitle', getattr(request, 'assignmentTitle'))
    setattr(newAssignment, 'assignmentDesc', getattr(request, 'assignmentDesc'))
    setattr(newAssignment, 'dueDate', getattr(request, 'dueDate'))
    setattr(newAssignment, 'dueTime', getattr(request, 'dueTime'))
    setattr(newAssignment, 'urlList', getattr(request, 'urlList'))

    dateUploaded = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    setattr(newAssignment, 'courseId', courseId)
    setattr(newAssignment, 'uploaderId', uploaderId)
    setattr(newAssignment, 'dateUploaded', dateUploaded)
    assignmentId = newAssignment.put()

    # adding assignmentId to course.assignmentIds
    course.assignmentIds.append(assignmentId)
    course.put()

    # deleting the cached value
    memcache.delete(courseId.urlsafe())

    # Sending Notification to subscribed profiles
    title = course.courseName
    notificationText = "New assignment added!"
    createNotification(course.studentIds, 'Campus Connect',
                       notificationText, 'assignment',
                       assignmentId.urlsafe())
    sendNotification(topicName=courseId.urlsafe(), id=assignmentId.urlsafe(), title=title,
                     text=notificationText, type='assignment')
    return Response(response=0, description="OK", key=assignmentId.urlsafe())


def createExamMethod(request):
    """createExamMethod(request)
       request (examTitle, examDesc, dateUploaded, courseId, profileId, dueDate,
                dueTime, urlList)
       To create a new exam"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
        course = courseId.get()
        if course is None:
            raise Exception("Invalid courseId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    try:
        uploaderId = ndb.Key(urlsafe=getattr(request, 'uploaderId'))
        uploader = uploaderId.get()
        if uploader is None:
            raise Exception("Invalid uploaderId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))

    newExam = Exam()
    # storing details
    setattr(newExam, 'examTitle', getattr(request, 'examTitle'))
    setattr(newExam, 'examDesc', getattr(request, 'examDesc'))
    setattr(newExam, 'dueDate', getattr(request, 'dueDate'))
    setattr(newExam, 'dueTime', getattr(request, 'dueTime'))
    setattr(newExam, 'urlList', getattr(request, 'urlList'))

    dateUploaded = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    setattr(newExam, 'uploaderId', uploaderId)
    setattr(newExam, 'courseId', courseId)
    setattr(newExam, 'dateUploaded', dateUploaded)
    examId = newExam.put()

    # adding examId to course.examIds
    course.examIds.append(examId)
    course.put()

    # deleting from memcache
    memcache.delete(courseId.urlsafe())

    # sending notification
    title = course.courseName
    notificationText = "New Exam added!"
    createNotification(course.studentIds, 'Campus Connect',
                       notificationText, 'exam',
                       examId.urlsafe())
    sendNotification(topicName=courseId.urlsafe(), id=examId.urlsafe(), title=title,
                     text=notificationText, type='exam')
    return Response(response=0, description="OK", key=examId.urlsafe())


def getAssignmentMethod(request):
    """getAssignmentMethod(request)
       request (profileId, assignmentId)"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception, E:
        print str(E)
        return GetAssignmentResponse(response=1, description=str(E))
    try:
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
    except Exception, E:
        print str(E)
        return GetAssignmentResponse(response=1, description=str(E))

    # to add the views in crons
    assignmentOpened.add(assignmentId.urlsafe())

    # fetching from memcache
    cacheVal = memcache.get(assignmentId.urlsafe())
    memViews = memcache.get('views' + assignmentId.urlsafe())
    if cacheVal is not None:
        # if the current user is author
        if profileId == cacheVal[8]:
            isAuthor = 1
        else:
            isAuthor = 0
        if memViews is None:
            assignment = assignmentId.get()
            if assignment is None:
                print "Invalid assignmentId"
                return GetAssignmentResponse(response=1, description="Invalid assignmentId")
            memViews = assignment.assignmentViews
            memcache.add('views' + assignmentId.urlsafe(), memViews)
        if isAuthor == 0:
            memcache.incr('views' + assignmentId.urlsafe())
        views = memcache.get('views' + assignmentId.urlsafe())
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
                                     views=views)
    assignment = assignmentId.get()
    if assignment is None:
        print "Invalid assignmentId"
        return GetAssignmentResponse(response=1, description="Invalid assignmentId")
    if profileId == assignment.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = assignment.uploaderId.get().profileName
    course = assignment.courseId.get()
    assignment.put()
    fields = [assignment.assignmentTitle, assignment.assignmentDesc, assignment.dateUploaded,
              uploaderName, assignment.dueDate, assignment.dueTime, assignment.urlList,
              course.courseName, assignment.uploaderId]
    memcache.add(assignmentId.urlsafe(), fields, 3600)
    if memcache.get('views' + assignmentId.urlsafe()) is None:
        if isAuthor == 0:
            memcache.add('views' + assignmentId.urlsafe(), assignment.assignmentViews + 1, 3600)
        else:
            memcache.add('views' + assignmentId.urlsafe(), assignment.assignmentViews, 3600)
    else:
        if isAuthor == 0:
            memcache.incr('views' + assignmentId.urlsafe())
    views = memcache.get('views' + assignmentId.urlsafe())
    return GetAssignmentResponse(response=0, description="OK",
                                 isAuthor=isAuthor,
                                 views=views,
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

    # to add the views in cron
    examOpened.add(examId.urlsafe())

    # fetching from memcache
    cacheVal = memcache.get(examId.urlsafe())
    memViews = memcache.get('views' + examId.urlsafe())
    if cacheVal is not None:
        if profileId == cacheVal[8]:
            isAuthor = 1
        else:
            isAuthor = 0
        if memViews is None:
            exam = examId.get()
            if exam is None:
                print "Invalid examId"
                return GetExamResponse(response=1, description="Invalid examId")
            memViews = exam.examViews
            memcache.add('views' + examId.urlsafe(), memViews)
        if isAuthor == 0:
            memcache.incr('views' + examId.urlsafe())
        views = memcache.get('views' + examId.urlsafe())
        return GetExamResponse(response=0, description="OK",
                               isAuthor=isAuthor, examTitle=cacheVal[0],
                               examDesc=cacheVal[1], lastUpdated=cacheVal[2],
                               uploaderName=cacheVal[3], dueDate=cacheVal[4],
                               dueTime=cacheVal[5], urlList=cacheVal[6],
                               courseName=cacheVal[7], views=views)
    exam = examId.get()
    if exam is None:
        print "Invalid examId"
        return GetExamResponse(response=1, description="Invalid examId")
    if profileId == exam.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = exam.uploaderId.get().profileName
    exam.put()
    course = exam.courseId.get()
    fields = [exam.examTitle, exam.examDesc, exam.dateUploaded, uploaderName,
              exam.dueDate, exam.dueTime, exam.urlList, course.courseName,
              exam.uploaderId]

    if memcache.get('views' + examId.urlsafe()) is None:
        if isAuthor == 0:
            memcache.add('views' + examId.urlsafe(), exam.examViews + 1, 3600)
        else:
            memcache.add('views' + examId.urlsafe(), exam.examViews, 3600)
    else:
        if isAuthor == 0:
            memcache.incr('views' + examId.urlsafe())
    memcache.add(examId.urlsafe(), fields, 3600)
    views = memcache.get('views' + examId.urlsafe())
    return GetExamResponse(response=0, description="OK",
                           isAuthor=isAuthor, views=views,
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
        profile = profileId.get()
        if profile is None:
            raise Exception("Invalid profileId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        print "Invalid courseId"
        return Response(response=1, description="Invalid courseId")
    memcache.incr(profile.collegeId.urlsafe())
    if profile is None:
        print "Invalid profileId"
        return Response(response=1, description="Invalid profileId")

    newNotes = Notes()
    # storing details
    setattr(newNotes, 'date', getattr(request, 'date'))
    setattr(newNotes, 'notesDesc', getattr(request, 'notesDesc'))
    setattr(newNotes, 'title', getattr(request, 'title'))
    setattr(newNotes, 'urlList', getattr(request, 'urlList'))
    print newNotes
    # CHECKS IF NOTEBOOK WITH SAME profileID AND courseId already exists
    query = NoteBook.query(ndb.AND(NoteBook.courseId == courseId,
                                   NoteBook.uploaderId == profileId))
    noteBookResult = query.fetch()
    if noteBookResult:
        # noteBook exists
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
        # new noteBook to be created
        try:
            setattr(newNotes, 'classNumber', str(1))
            noteBookId = createNoteBook(profileId, courseId)
            addToNoteBook(noteBookId, newNotes)
        except Exception, E:
            print str(E)
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
        memcache.set(noteBookId.urlsafe(), cacheVal)
    noteBook.put()
    notificationText = "New notes added!"
    if len(noteBook.bmUserList) != 0:
        print len(noteBook.bmUserList)
        createNotification(bmUserList, 'Campus Connect', notificationText,
                           'notes', noteBookId.urlsafe())
    sendNotification(topicName=noteBookId.urlsafe(), id=noteBookId.urlsafe(),
                     title=title, text=notificationText, type='notes')


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
        views = memcache.get('views' + noteBookId.urlsafe())
        return NoteBookDetailResponse(courseName=cacheVal[0],
                                      isAuthor=isAuthor, uploaderName=cacheVal[1],
                                      lastUpdated=cacheVal[2], views=memViews,
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
    views = noteBook.views
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
    if memcache.get('views' + noteBookId.urlsafe()) is None:
        if isAuthor == 1:
            memcache.add('views' + noteBookId.urlsafe(), views + 1, 3600)
        else:
            memcache.add('views' + noteBookId.urlsafe(), views, 3600)
    else:
        memcache.incr('views' + noteBookId.urlsafe())
    views = memcache.get('views' + noteBookId.urlsafe())
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
                noteBook = noteBookId.get()
                if noteBook is None:
                    raise Exception("Invalid noteBookId")
            except Exception, E:
                print str(E)
                return NoteBookListResponse(response=1, description=str(E))
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
            profile = profileId.get()
            if profile is None:
                raise Exception("Invalid profileId")
        except Exception, E:
            print str(E)
            return NoteBookListResponse(response=1, description=str(E))
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
                                   colour=course.colour,
                                   courseId=course.key.urlsafe())
            noteBookList.append(new)
    elif upid:
        try:
            profileId = ndb.Key(urlsafe=upid)
            profile = profileId.get()
            if profile is None:
                raise Exception("Invalid profileId")
        except Exception:
            print str(E)
            return NoteBookListResponse(response=1, description=str(E))
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
                                   colour=course.colour,
                                   courseId=course.key.urlsafe())
            noteBookList.append(new)
    elif courseId:
        try:
            courseId = ndb.Key(urlsafe=courseId)
            course = courseId.get()
            if course is None:
                raise Exception("Invalid courseId")
        except Exception, E:
            print str(E)
            return NoteBookListResponse(response=1, description=str(E))
        noteBookIds = course.noteBookIds
        for noteBookId in noteBookIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                continue
            uploader = noteBook.uploaderId.get()
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    continue
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated,
                                   colour=course.colour,
                                   courseId=course.key.urlsafe())
            noteBookList.append(new)
            noteBookList.sort(key=lambda x: x.lastUpdated, reverse=True)
    elif profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
            profile = profileId.get()
            if profile is None:
                raise Exception("Invalid profileId")
        except Exception, E:
            print str(E)
            return NoteBookListResponse(response=1, description=str(E))
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
                                       colour=course.colour,
                                       courseId=course.key.urlsafe())
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
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
        noteBook = noteBookId.get()
        if noteBook is None:
            raise Exception("Invalid noteBookId")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))
    rating = getattr(request, 'rating')
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
        if profileId in cacheVal[19]:
            isAdmin = 1
        else:
            isAdmin = 0
        return CoursePageResponse(response=0, description="OK", isSubscribed=isSubscribed,
                                  courseName=cacheVal[0], date=cacheVal[1],
                                  startTime=cacheVal[2], endTime=cacheVal[3],
                                  examCount=cacheVal[4], assignmentCount=cacheVal[5],
                                  notesCount=cacheVal[6], examList=cacheVal[7],
                                  assignmentList=cacheVal[8], studentCount=cacheVal[9],
                                  professorName=cacheVal[10], colour=cacheVal[11],
                                  elective=cacheVal[12], collegeName=cacheVal[14],
                                  branchNames=cacheVal[15], sectionNames=cacheVal[16],
                                  batchNames=cacheVal[17], semester=cacheVal[18],
                                  isAdmin=isAdmin, courseCode=cacheVal[20])
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
              course.sectionNames, course.batchNames, course.semester,
              course.adminIds, course.courseCode]
    memcache.add(course.key.urlsafe(), fields, 3600)
    if profileId in course.adminIds:
        isAdmin = 1
    else:
        isAdmin = 0
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
                              batchNames=course.batchNames,
                              semester=course.semester, isAdmin=isAdmin,
                              courseCode=course.courseCode)


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
                continue
            for assignmentId in course.assignmentIds:
                assignment = assignmentId.get()
                if assignment is None:
                    continue
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
                continue
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
        bmUserList = set(noteBook.bmUserList)
        bmUserList.discard(profileId)
        noteBook.bmUserList = list(bmUserList)
        status = 0
    else:
        profile.bookmarkedNoteBookIds.append(noteBookId)
        bmUserList = set(noteBook.bmUserList)
        bmUserList.add(profileId)
        noteBook.bmUserList = bmUserList
        status = 1
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        cacheVal[8] = noteBook.bmUserList
    if memcache.get(noteBookId.urlsafe()) is None:
        memcache.add(noteBookId.urlsafe(), cacheVal, 3600)
    else:
        memcache.set(noteBookId.urlsafe(), cacheVal)
    profile.put()
    noteBook.put()
    return BookmarkResponse(response=0, description="OK", bookmarkStatus=status)


def clearAll():
    colleges = College.query().fetch()
    for college in colleges:
        memcache.delete(college.key.urlsafe())
        memcache.delete('stu' + college.key.urlsafe())
        college.key.delete()
    profiles = Profile.query().fetch()
    for profile in profiles:
        profile.key.delete()
    courses = Course.query().fetch()
    for course in courses:
        memcache.delete(course.key.urlsafe())
        memcache.delete('views' + course.key.urlsafe())
        course.key.delete()
    notesList = Notes.query().fetch()
    for notes in notesList:
        memcache.delete(notes.key.urlsafe())
        notes.key.delete()
    noteBookList = NoteBook.query().fetch()
    for noteBook in noteBookList:
        memcache.delete(noteBook.key.urlsafe())
        memcache.delete('views' + noteBook.key.urlsafe())
        noteBook.key.delete()
    assignmentList = Assignment.query().fetch()
    for assignment in assignmentList:
        memcache.delete(assignment.key.urlsafe())
        memcache.delete('views' + assignment.key.urlsafe())
        assignment.key.delete()
    examList = Exam.query().fetch()
    for exam in examList:
        memcache.delete(exam.key.urlsafe())
        memcache.delete('views' + exam.key.urlsafe())
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
        studentIds = set(course.studentIds)
        studentIds.discard(profileId)
        course.studentIds = list(studentIds)
        course.put()
    else:
        profile.subscribedCourseIds.append(courseId)
        profile.put()
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            cacheVal[9] += 1
            cacheVal[13].append(profileId)
            memcache.set(courseId.urlsafe(), cacheVal)
        studentIds = set(course.studentIds)
        studentIds.add(profileId)
        course.studentIds = list(studentIds)
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
    timeStamp = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
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


def branchListMethod(request):
    try:
        collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
    except Exception:
        print "Invalid collegeId"
        return BranchListResponse(response=1, description='Invalid collegeId')
    college = collegeId.get()
    if college is None:
        print "Invalid collegeId"
        return BranchListResponse(response=1, description='Invalid collegeId')
    return BranchListResponse(response=0, description='OK', branchList=college.branchNameList)


def collegeRequestMethod(request):
    collegeName = getattr(request, 'collegeName')
    location = getattr(request, 'location')
    name = getattr(request, 'name')
    phone = getattr(request, 'phone')
    college = CollegeRequestModel(collegeName=collegeName,
                                  location=location, name=name,
                                  phone=phone, timeStamp=datetime.datetime.now()+datetime.timedelta(hours=5, minutes=30))
    college.put()
    sp = SparkPost('d5eda063a40ae19610612ea5d0804f20d294e62d')
    body = """<h1>Campus Connect</h1><br>There is a request to create new College
              <br>""" + collegeName + """, """ + location + """
              <br>by """ + name + """, """ + phone
    response = sp.transmissions.send(recipients=['saurav24081996@gmail.com', 'aayush@campusconnect.cc'],
                                     html=body,
                                     from_email={'email': 'aayush@campusconnect.cc', 'name': 'Campus Connect'},
                                     subject='New College',
                                     )
    print(response)


def reportMethod(request):
    id = ndb.Key(urlsafe=getattr(request, 'key'))
    profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    profile = profileId.get()
    college = profile.collegeId.get()
    desc = getattr(request, 'description')
    newReport = Report(id=id, profileId=profileId,
                       description=desc)
    newReport.put()
    body = "<h1>CAMPUS CONNECT</h1><br>"
    body += "Something is Reported<br>"
    body += "College: " + college.collegeName
    body += "<br>Details<br>id: " + id.urlsafe()
    body += "<br>By: " + profile.profileName
    body += "<br>profileId: " + profileId.urlsafe()
    sendEmail(subject='Something is Reported', body=body)
    return Response(response=0, description='OK')


def rectify():
    courseList = Course.query().fetch()
    for course in courseList:
        for profileId in course.studentIds:
            if profileId.get() is None:
                course.studentIds.remove(profileId)
        for profileId in course.adminIds:
            if profileId.get() is None:
                course.adminIds.remove(profileId)
        course.put()
