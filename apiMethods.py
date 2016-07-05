import datetime

from models import College, Course, Profile
from models import Response, FeedCourseResponse, CourseListResponse, FeedResponse
from models import TTCourseResponse, TimeTableResponse, StudentResponse
from models import StudentListResponse, Assignment, Exam, CourseResponse
from models import GetAssignmentResponse, GetExamResponse, Notes, NoteBook
from models import NotesResponse, NoteBookDetailResponse, NoteBookListResponse
from models import NoteBookResponse, CoursePageResponse, AssExamResponse
from models import AssignmentResponse, ExamResponse, GetAssListResponse
from models import GetExamListResponse, CollegeListResponse, CollegeDetails
from models import BookmarkResponse
from searchAPI import createNBDoc
from FCM import sendNotification

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
    collegeName = getattr(request, 'collegeName')
    abbreviation = getattr(request, 'abbreviation')
    location = getattr(request, 'location')
    collegeType = getattr(request, 'collegeType', None)
    semStartDate = getattr(request, 'semStartDate', None)
    semEndDate = getattr(request, 'semEndDate', None)
    branchNameList = getattr(request, 'branchNameList', [])
    # To find college with same name and location
    queryString = ndb.AND(College.collegeName == collegeName, College.location == location)
    collegeSameDetails = College.query(queryString).fetch()
    if collegeSameDetails:
        return Response(response=2, description="College Already Exists")
    else:
        newCollege = College(collegeName=collegeName, abbreviation=abbreviation,
                             location=location, studentCount=0, noteBookCount=0,
                             collegeType=collegeType, semStartDate=semStartDate,
                             semEndDate=semEndDate, courseIds=[],
                             branchNameList=branchNameList)
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
    profileName = getattr(request, 'profileName')
    batchName = getattr(request, 'batchName', None)
    branchName = getattr(request, 'branchName', None)
    sectionName = getattr(request, 'sectionName', None)
    # Querie for compatible courses and stores in availableCourseIds
    availableCourseIds = []
    queryString = ndb.AND(Course.collegeId == collegeId,
                          Course.batchNames == batchName,
                          Course.branchNames == branchName,
                          Course.sectionNames == sectionName)
    for course in Course.query(queryString).fetch():
        availableCourseIds.append(course.key)
    photoUrl = getattr(request, 'photoUrl')
    gcmId = getattr(request, 'gcmId')
    email = getattr(request, 'email')
    college = collegeId.get()
    # To get existing profiles (if any) with same email id
    profileCheck = Profile.query(Profile.email == email).fetch()
    if college is None:
        return Response(response=1, description="No such college ID")
    elif profileCheck:
        return Response(response=2, description="Profile already registered")
    else:
        newProfile = Profile(profileName=profileName, collegeId=collegeId,
                             batchName=batchName, branchName=branchName,
                             sectionName=sectionName, subscribedCourseIds=[],
                             availableCourseIds=availableCourseIds,
                             administeredCourseIds=[], gcmId=gcmId,
                             photoUrl=photoUrl, email=email, points=0,
                             uploadedNoteBookIds=[], bookmarkedNoteBookIds=[])
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
        return Response(response=1, description="No such collegeId")
    courseName = getattr(request, 'courseName')
    batchNames = getattr(request, 'batchNames', None)
    branchNames = getattr(request, 'branchNames', None)
    sectionNames = getattr(request, 'sectionNames', None)
    semester = getattr(request, 'semester', None)
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="No such profileId")
    adminIds = []
    adminIds.append(profileId)
    studentIds = []
    studentIds.append(profileId)
    date = getattr(request, 'date', [])
    startTime = getattr(request, 'startTime', [])
    endTime = getattr(request, 'endTime', [])
    professorName = getattr(request, 'professorName', None)
    colour = getattr(request, 'colour', None)
    courseCode = getattr(request, 'courseCode', None)
    elective = getattr(request, 'elective', '0')
    college = collegeId.get()
    profile = profileId.get()
    if college is None:
        return Response(response=1, description="No such college ID")
    if profile is None:
        return Response(response=1, description="No such profile ID")
    # To check if same course already exists
    queryString = ndb.AND(Course.courseCode == courseCode,
                          Course.collegeId == collegeId,
                          Course.sectionNames.IN(sectionNames),
                          Course.branchNames.IN(branchNames),
                          Course.batchNames.IN(batchNames),
                          Course.professorName == professorName)
    coursesWithSameCode = Course.query(queryString).fetch()
    if coursesWithSameCode:
        return Response(response=2, description="Course already exists")

    newCourse = Course(courseName=courseName, collegeId=collegeId,
                       batchNames=batchNames, branchNames=branchNames,
                       sectionNames=sectionNames, semester=semester,
                       adminIds=adminIds, date=date,
                       startTime=startTime, endTime=endTime,
                       professorName=professorName, studentIds=studentIds,
                       colour=colour, courseCode=courseCode,
                       noteBookIds=[], assignmentIds=[], examIds=[], elective=elective)
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
                          Profile.batchName.IN(batchNames),
                          Profile.branchName.IN(branchNames),
                          Profile.sectionName.IN(sectionNames))
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
        return Response(response=1, description="No such profileId")
    courseIdList = getattr(request, 'courseIds')
    courseIds = []
    profile = profileId.get()
    if profile is None:
        return Response(response=1, description="No such profileId")
    # Adding courseId to profile.subscribedCourseIds
    for course in courseIdList:
        try:
            courseId = ndb.Key(urlsafe=course)
        except Exception:
            return Response(response=1, description="No such courseId")
        cacheVal = memcache.get(courseId.urlsafe())
        if cacheVal is not None:
            cacheVal[13].append(profileId)
            memcache.set(courseId.urlsafe(), cacheVal)
        profile.subscribedCourseIds.append(courseId)
        courseIds.append(courseId)
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
        return CourseListResponse(response=1, description="Bad Request")
    else:
        courseListResponse = []
        if profileIdUrlSafe:
            try:
                profileId = ndb.Key(urlsafe=profileIdUrlSafe)
            except Exception:
                return CourseListResponse(response=1, description="No such profileId")
            profile = profileId.get()
            if profile is None:
                return CourseListResponse(response=1, description="No such profileId")
            for courseId in profile.availableCourseIds:
                course = courseId.get()
                if course is None:
                    return CourseListResponse(response=1, description="No such courseId")
                notesCount = len(course.noteBookIds)
                studentCount = len(course.studentIds)
                feedCourseResponse = CourseResponse(courseId=courseId.urlsafe(), courseName=course.courseName,
                                                    batchNames=course.batchNames, branchNames=course.branchNames,
                                                    sectionNames=course.sectionNames, semester=course.semester,
                                                    studentCount=studentCount, professorName=course.professorName,
                                                    notesCount=notesCount, colour=course.colour,
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
                    return CourseListResponse(response=1, description="No such CourseId")
                course = courseId.get()
                notesCount = len(course.noteBookIds)
                studentCount = len(course.studentIds)
                feedCourseResponse = CourseResponse(courseId=courseId.urlsafe(), courseName=course.courseName,
                                                    batchNames=course.batchNames, branchNames=course.branchNames,
                                                    sectionNames=course.sectionNames, studentCount=studentCount,
                                                    professorName=course.professorName, notesCount=notesCount,
                                                    semester=course.semester, colour=course.colour,
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
        return FeedResponse(response=1, description="Invalid profileId")
    profile = profileId.get()
    if profile is None:
        return FeedResponse(response=1, description="Invalid profileId")
    profileName = profile.profileName
    points = profile.points
    photoUrl = profile.photoUrl
    availableCourseIds = profile.availableCourseIds
    subscribedCourseIds = profile.subscribedCourseIds
    try:
        availableCourseList = feedCourseResponse(availableCourseIds)
    except Exception, E:
        return FeedResponse(response=1, description=' in availableCourses ' + str(E))
    try:
        subscribedCourseList = feedCourseResponse(subscribedCourseIds)
    except Exception, E:
        return FeedResponse(response=1, description=' in subscribedCourses' + str(E))
    collegeId = profile.collegeId
    return FeedResponse(response=0, description="OK", profileName=profileName,
                        points=points, photoUrl=photoUrl,
                        availableCourseList=availableCourseList,
                        subscribedCourseList=subscribedCourseList, collegeId=collegeId.urlsafe())


def feedCourseResponse(courseIds):
    """feedCourseResponse(courseIds[])
        To get the course details for home page feed"""
    responseList = []
    curDate = datetime.datetime.now().date()
    curTime = (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).time()
    for courseId in courseIds:
        dueAssignments, dueExams, recentNotes = 0, 0, 0
        course = courseId.get()
        assignmentIds = course.assignmentIds
        for assignmentId in assignmentIds:
            assignment = assignmentId.get()
            if assignment is None:
                raise Exception("Invalid assignmentId")
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
                raise Exception("Invalid examId")
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
                raise Exception("Invalid noteBookId")
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
                                               endTime=course.endTime, colour=course.colour,
                                               recentNotes=recentNotes,
                                               professorName=course.professorName, elective=course.elective, courseCode=course.courseCode))
    return responseList


def addAdminMethod(request):
    """addAdmin(request)
       request (courseId, profileId)
       to make a new Admin"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return Response(response=1, description="Invalid courseId")
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invalid profileId")
    course = courseId.get()
    if course is None:
        return Response(response=1, description="Invalid courseId")
    profile = profileId.get()
    if profile is None:
        return Response(response=1, description="Invalid profileId")
    profile.administeredCourseIds.append(courseId)
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
        return StudentListResponse(response=1, description="Invalid profileId")
    try:
        courseId = ndb.Key(urlsafe=request.courseId)
    except Exception:
        return StudentListResponse(response=1, description="Invalid courseId")
    profile = profileId.get()
    if profile is None:
        return StudentListResponse(response=1, description="Invalid profileId")
    course = courseId.get()
    if course is None:
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
    assignmentTitle = getattr(request, 'assignmentTitle')
    assignmentDesc = getattr(request, 'assignmentDesc')
    dateUploaded = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return Response(response=1, description="Invalid courseId")
    try:
        uploaderId = ndb.Key(urlsafe=getattr(request, 'uploaderId'))
    except Exception:
        return Response(response=1, description="Invalid uploaderId")
    dueDate = getattr(request, 'dueDate')
    dueTime = getattr(request, 'dueTime')
    urlList = getattr(request, 'urlList')
    newAssignment = Assignment(assignmentTitle=assignmentTitle,
                               assignmentDesc=assignmentDesc,
                               courseId=courseId, dateUploaded=dateUploaded,
                               uploaderId=uploaderId,
                               assignmentViews=0, dueDate=dueDate,
                               dueTime=dueTime, urlList=urlList,
                               remindProfileIds=[])
    assignmentId = newAssignment.put()
    course = courseId.get()
    if course is None:
        return Response(response=1, description="Invalid courseId")
    course.assignmentIds.append(assignmentId)
    title = course.courseName
    course.put()
    notificationText = "New assignment added!"
    sendNotification(id=courseId.urlsafe(), title=title, text=notificationText, type='assignment')
    return Response(response=0, description="OK", key=assignmentId.urlsafe())


def createExamMethod(request):
    """createExamMethod(request)
       request (examTitle, examDesc, dateUploaded, courseId, profileId, dueDate,
                dueTime, urlList)
       To create a new exam"""
    examTitle = getattr(request, 'examTitle')
    examDesc = getattr(request, 'examDesc')
    dateUploaded = str(datetime.datetime.now()+datetime.timedelta(hours=5, minutes=30))
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return Response(response=1, description="Invalid courseId")
    try:
        uploaderId = ndb.Key(urlsafe=getattr(request, 'uploaderId'))
    except Exception:
        return Response(response=1, description="Invalid uploaderId")
    dueDate = getattr(request, 'dueDate')
    dueTime = getattr(request, 'dueTime')
    urlList = getattr(request, 'urlList')
    newExam = Exam(examTitle=examTitle, examDesc=examDesc,
                   courseId=courseId, uploaderId=uploaderId,
                   examViews=0, dueDate=dueDate, remindProfileIds=[],
                   dueTime=dueTime, urlList=urlList, dateUploaded=dateUploaded)
    examId = newExam.put()
    course = courseId.get()
    if course is None:
        return Response(response=1, description="Invalid courseId")
    course.examIds.append(examId)
    title = course.courseName
    course.put()
    notificationText = "New Exam added!"
    sendNotification(id=courseId.urlsafe(),title=title, text=notificationText, type='exam')
    return Response(response=0, description="OK", key=examId.urlsafe())


def getAssignmentMethod(request):
    """getAssignmentMethod(request)
       request (profileId, assignmentId)"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return GetAssignmentResponse(response=1, description="Invalid profileId")
    try:
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
    except Exception:
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
        memcache.incr('views' + assignmentId.urlsafe())
        return GetAssignmentResponse(response=0, description="OK", isAuthor=isAuthor,
                                     assignmentTitle=cacheVal[0], assignmentDesc=cacheVal[1],
                                     lastUpdated=cacheVal[2], uploaderName=cacheVal[3],
                                     dueDate=cacheVal[4], dueTime=cacheVal[5],
                                     urlList=cacheVal[6], courseName=cacheVal[7],
                                     views=memViews)
    assignment = assignmentId.get()
    if assignment is None:
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
                                 isAuthor=isAuthor, views=assignment.assignmentViews,
                                 assignmentTitle=assignment.assignmentTitle,
                                 assignmentDesc=assignment.assignmentDesc,
                                 lastUpdated=assignment.dateUploaded,
                                 uploaderName=uploaderName,
                                 dueDate=assignment.dueDate,
                                 dueTime=assignment.dueTime,
                                 urlList=assignment.urlList,
                                 courseName=course.courseName)


def getExamMethod(request):
    """getExamMethod(request)
       request (profileId, examId)"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return GetExamResponse(response=1, description="Invalid profileId")
    try:
        examId = ndb.Key(urlsafe=getattr(request, 'examId'))
    except Exception:
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
        memcache.incr('views' + examId.urlsafe())
        return GetExamResponse(response=0, description="OK", isAuthor=isAuthor,
                               examTitle=cacheVal[0], examDesc=cacheVal[1], lastUpdated=cacheVal[2],
                               uploaderName=cacheVal[3], dueDate=cacheVal[4], dueTime=cacheVal[5],
                               urlList=cacheVal[6], courseName=cacheVal[7], views=memViews)

    exam = examId.get()
    if exam is None:
        return GetExamResponse(response=1, description="Invalid examId")
    if profileId == exam.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = exam.uploaderId.get().profileName
    exam.examViews = exam.examViews + 1
    exam.put()
    course = exam.courseId.get()
    fields = [exam.examTitle, exam.examDesc, exam.dateUploaded, uploaderName, exam.dueDate, exam.dueTime,
              exam.urlList, course.courseName, exam.uploaderId]
    memcache.add(examId.urlsafe(), fields, 3600)
    memcache.add('views' + examId.urlsafe(), exam.examViews, 3600)

    return GetExamResponse(response=0, description="OK",
                           isAuthor=isAuthor, views=exam.examViews,
                           examTitle=exam.examTitle, examDesc=exam.examDesc,
                           lastUpdated=exam.dateUploaded,
                           uploaderName=uploaderName, dueDate=exam.dueDate,
                           dueTime=exam.dueTime, urlList=exam.urlList,
                           courseName=course.courseName)


def createNotesMethod(request):
    """createNotes(request)
       request (profileId, date, urlList,notesDesc, classNumber, courseId, title)
       To create new Notes"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invalid profileId")
    date = getattr(request, 'date')
    urlList = getattr(request, 'urlList')
    notesDesc = getattr(request, 'notesDesc')
    # classNumber = getattr(request, 'classNumber')
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return Response(response=1, description="Invalid courseId")
    title = getattr(request, 'title')
    # CHECKS IF NOTEBOOK WITH SAME profileID AND courseId already exists
    query = NoteBook.query(ndb.AND(NoteBook.courseId == courseId,
                                   NoteBook.uploaderId == profileId))
    noteBookResult = query.fetch()
    if noteBookResult:
        for noteBook in noteBookResult:
            newNotes = Notes(date=date, urlList=urlList, notesDesc=notesDesc,
                             classNumber=str(len(noteBook.notesIds) + 1), title=title)
            try:
                addToNoteBook(noteBook.key, newNotes, notesDesc)
            except Exception, E:
                return Response(response=1, description=str(E))
            createNBDoc(title, notesDesc, date, profileId.profileName, noteBook.key.urlsafe())
            return Response(response=0, description="OK",
                            key=noteBook.key.urlsafe())
    else:
        try:
            newNotes = Notes(date=date, urlList=urlList, notesDesc=notesDesc,
                             classNumber='1', title=title)
            noteBookId = createNoteBook(profileId, courseId)
            addToNoteBook(noteBookId, newNotes, notesDesc)
        except Exception, E:
            return Response(response=1, description=str(E))
        createNBDoc(title, notesDesc, date, profileId.profileName, noteBookId.urlsafe())
        return Response(response=0, description="OK", key=noteBookId.urlsafe())


def createNoteBook(profileId, courseId):
    """createNoteBook(profileId, courseId)
       To create new noteBook"""
    newNoteBook = NoteBook(courseId=courseId, uploaderId=profileId,
                           notesIds=[], ratedUserIds=[], ratingList=[],
                           totalRating="0", frequency=0, views=0, bmUserList=[],
                           lastUpdated=str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)))
    course = courseId.get()
    if course is None:
        raise Exception("Invalid courseId")
    college = course.collegeId.get()
    if college is None:
        raise Exception("Invalid collegeId")
    college.noteBookCount += 1
    college.put()
    profile = profileId.get()
    if profile is None:
        raise Exception("Invalid profileId")
    noteBookId = newNoteBook.put()
    profile.uploadedNoteBookIds.append(noteBookId)
    profile.put()
    course.noteBookIds.append(noteBookId)   
    course.put()
    return noteBookId


def addToNoteBook(noteBookId, newNotes, notesDesc):
    """addToNoteBook(noteBookId, newNotes)
       To add new notes to existing noteBook"""
    newNotes.noteBookId = noteBookId
    notesId = newNotes.put()
    noteBook = noteBookId.get()
    if noteBook is None:
        raise Exception("Invalid profileId")
    noteBook.notesIds.append(notesId)
    noteBook.frequency += 1
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
    noteBook.lastUpdated = str(datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    noteBookUploader = noteBook.uploaderId.get()
    uploaderName = noteBookUploader.profileName
    course = noteBook.courseId.get()
    fields = [course.courseName, uploaderName, noteBook.lastUpdated, noteBook.frequency, pages, noteBook.totalRating,
              notesList, course.colour, noteBook.bmUserList, noteBook.ratedUserIds,
              noteBook.ratingList, noteBook.uploaderId]
    memcache.set(noteBookId.urlsafe(), fields)
    title = noteBook.courseName + ': ' + uploaderName
    noteBook.put()
    notificationText = "New notes added!"
    sendNotification(id=noteBookId.urlsafe(), title=title, text=notificationText, type='notes')


def getNoteBook(request):
    """getNoteBook(request)
       request (profileId, noteBookId)
       To get noteBook"""
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return NoteBookDetailResponse(response=1, description="Invalid profileId")
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    except Exception:
        return NoteBookDetailResponse(response=1, description="Invalid noteBookId")
    noteBookOpened.add(noteBookId.urlsafe())
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        memViews = memcache.get('views' + noteBookId.urlsafe())
        if memViews is None:
            noteBook = noteBookId.get()
            memViews = noteBook.views
            memcache.add('views' + noteBookId.urlsafe(), memViews, 3600)
        memcache.incr('views' + noteBookId.urlsafe())
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
        lastUpdated = cacheVal[2]
        a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
        lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
        return NoteBookDetailResponse(courseName=cacheVal[0],
                                      isAuthor=isAuthor, uploaderName=cacheVal[1],
                                      lastUpdated=cacheVal[2], views=memViews,
                                      rated=rated, frequency=cacheVal[3],
                                      pages=cacheVal[4], totalRating=cacheVal[5],
                                      notes=cacheVal[6], bookmarkStatus=bookmarkStatus,
                                      response=0, colour=cacheVal[7], lastUpdated1=lastUpdated1,
                                      description="OK")

    noteBook = noteBookId.get()
    if noteBook is None:
        return NoteBookDetailResponse(response=1, description="Invalid noteBookId")
    if noteBook.uploaderId == profileId:
        isAuthor = 1
    else:
        isAuthor = 0
    profile = profileId.get()
    if profile is None:
        return NoteBookDetailResponse(response=1, description="Invalid profileId")
    if noteBookId in profile.bookmarkedNoteBookIds:
        bookmarkStatus = 1
    else:
        bookmarkStatus = 0
    noteBookUploader = noteBook.uploaderId.get()
    course = noteBook.courseId.get()
    if course is None:
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
    lastUpdated = noteBook.lastUpdated
    a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
    lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
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
                                  description="OK", lastUpdated1=lastUpdated1)


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
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            noteBook = noteBookId.get()
            if noteBook is None:
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            course = noteBook.courseId.get()
            if course is None:
                return NoteBookListResponse(response=1, description="Invalid courseId")
            uploader = noteBook.uploaderId.get()
            if uploader is None:
                return NoteBookListResponse(response=1, description="Invalid profileId")
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    return NoteBookListResponse(response=1, description="Invalid notesId")
                pages += len(notes.urlList)
            lastUpdated = noteBook.lastUpdated
            a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
            lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
            new = NoteBookResponse(noteBookId=idurlsafe,
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated, colour=course.colour,
                                   lastUpdated1=lastUpdated1)
            noteBookList.append(new)
    elif bpid:
        try:
            profileId = ndb.Key(urlsafe=bpid)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        bookmarkedIds = profile.bookmarkedNoteBookIds
        for noteBookId in bookmarkedIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            course = noteBook.courseId.get()
            if course is None:
                return NoteBookListResponse(response=1, description="Invalid courseId")
            uploader = noteBook.uploaderId.get()
            if uploader is None:
                return NoteBookListResponse(response=1, description="Invalid profileId")
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    return NoteBookListResponse(response=1, description="Invalid notesId")
                pages += len(notes.urlList)
            lastUpdated = noteBook.lastUpdated
            a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
            lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated, colour=course.colour,
                                   lastUpdated1=lastUpdated1)
            noteBookList.append(new)
    elif upid:
        try:
            profileId = ndb.Key(urlsafe=upid)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        uploadedIds = profile.uploadedNoteBookIds
        for noteBookId in uploadedIds:
            noteBook = noteBookId.get()
            if noteBook is None:
                return NoteBookListResponse(response=1, description="Invalid noteBookId")
            course = noteBook.courseId.get()
            if course is None:
                return NoteBookListResponse(response=1, description="Invalid courseId")
            uploader = noteBook.uploaderId.get()
            if uploader is None:
                return NoteBookListResponse(response=1, description="Invalid profileId")
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                if notes is None:
                    return NoteBookListResponse(response=1, description="Invalid notesId")
                pages += len(notes.urlList)
            lastUpdated = noteBook.lastUpdated
            a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
            lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated, colour=course.colour,
                                   lastUpdated1=lastUpdated1)
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
            lastUpdated = noteBook.lastUpdated
            a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
            lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views, pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=lastUpdated, colour=course.colour,
                                   lastUpdated1=lastUpdated1)
            noteBookList.append(new)
    elif profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        if profile is None:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            if course is None:
                return NoteBookListResponse(response=1, description="Invalid courseId")
            noteBookIds = course.noteBookIds
            for noteBookId in noteBookIds:
                noteBook = noteBookId.get()
                if noteBook is None:
                    return NoteBookListResponse(response=1, description="Invalid noteBookId")
                uploader = noteBook.uploaderId.get()
                if uploader is None:
                    return NoteBookListResponse(response=1, description="Invalid profileId")
                pages = 0
                for notesId in noteBook.notesIds:
                    notes = notesId.get()
                    if notes is None:
                        return NoteBookListResponse(response=1, description="Invalid notesId")
                    pages += len(notes.urlList)
                lastUpdated = noteBook.lastUpdated
                a = datetime.datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S.%f")
                lastUpdated1 = a.strftime("%m/%d/%Y %I:%M:%S %p")
                new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                       courseName=course.courseName,
                                       uploaderName=uploader.profileName,
                                       views=noteBook.views, pages=pages,
                                       totalRating=noteBook.totalRating,
                                       frequency=noteBook.frequency,
                                       lastUpdated=noteBook.lastUpdated, colour=course.colour,
                                       lastUpdated1=lastUpdated1)
                noteBookList.append(new)
    else:
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
        return Response(response=1, description="Invaild profileId")
    rating = getattr(request, 'rating')
    noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    noteBookOpened.add(noteBookId.urlsafe())
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        if profileId in cacheVal[9]:
            idx = cacheVal[9].index(profileId)
            del(cacheVal[10][idx])
            cacheVal[9].remove(profileId)
        cacheVal[9].append(profileId)
        cacheVal[10].append(rating)
        memcache.set(noteBookId.urlsafe(), cacheVal)
        return Response(response=0, description="OK")
    noteBook = noteBookId.get()
    if noteBook is None:
        return Response(response=1, description="Invalid noteBookId")
    if profileId in noteBook.ratedUserIds:
        idx = noteBook.ratedUserIds.index(profileId)
        del(noteBook.ratingList[idx])
        noteBook.ratedUserIds.remove(profileId)
    noteBook.ratedUserIds.append(profileId)
    noteBook.ratingList.append(rating)
    noteBook.put()
    return Response(response=0, description="OK")


def coursePageMethod(request):
    """coursePage(request)
       request(profileId, courseId)"""
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return CoursePageResponse(response=1, description="Invalid courseId")
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return CoursePageResponse(response=1, description="Invalid profileId")
    cacheVal = memcache.get(courseId.urlsafe())
    if cacheVal is not None:
        if profileId in cacheVal[13]:
            isSubscribed = 1
        else:
            isSubscribed = 0
        return CoursePageResponse(response=0, description="OK", isSubscribed=isSubscribed,
                                  courseName=cacheVal[0], date=cacheVal[1], startTime=cacheVal[2],
                                  endTime=cacheVal[3], examCount=cacheVal[4], assignmentCount=cacheVal[5],
                                  notesCount=cacheVal[6], examList=cacheVal[7], assignmentList=cacheVal[8],
                                  studentCount=cacheVal[9], professorName=cacheVal[10], colour=cacheVal[11],
                                  elective=cacheVal[12], collegeName=cacheVal[14], branchNames=cacheVal[15],
                                  sectionNames=cacheVal[16], batchNames=cacheVal[17], semester=cacheVal[18])
    course = courseId.get()
    if course is None:
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
            return CoursePageResponse(response=1, description="Invalid assignmentId")
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
            return CoursePageResponse(response=1, description="Invalid profileId")
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
                return CoursePageResponse(response=1, description="Invalid noteBookId")
            a = str(noteBook.lastUpdated)
            date, month, year = int(a[8:10]), int(a[5:7]), int(a[0:4])
            lastUpdated = datetime.date(year, month, date)
            if(curDate - lastUpdated).days > 7:
                continue
            recentNotes = recentNotes + 1
    fields = [course.courseName, course.date, course.startTime, course.endTime,
              dueExams, dueAssignments, recentNotes, examList,
              assignmentList, studentCount, course.professorName, course.colour,
              course.elective, course.studentIds, collegeName, course.branchNames,
              course.sectionNames, course.batchNames, course.semester]
    memcache.add(courseId.urlsafe(), fields, 3600)
    return CoursePageResponse(response=0, description="OK", isSubscribed=isSubscribed,
                              courseName=course.courseName, date=course.date, startTime=course.startTime,
                              endTime=course.endTime, examCount=dueExams, assignmentCount=dueAssignments,
                              notesCount=recentNotes, examList=examList, assignmentList=assignmentList,
                              studentCount=studentCount, professorName=course.professorName, colour=course.colour,
                              elective=course.elective, collegeName=collegeName, branchNames=course.branchNames,
                              sectionNames=course.sectionNames, batchNames=course.batchNames, semester=course.semester)


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
            return GetExamListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        examList = []
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            for examId in course.examIds:
                exam = examId.get()
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
            return GetExamListResponse(response=1, description="Invalid courseId")
        course = courseId.get()
        examList = []
        for examId in course.examIds:
            exam = examId.get()
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
        return BookmarkResponse(response=1, description="Invalid profileId")
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    except Exception:
        return BookmarkResponse(response=1, description="Invalid noteBookId")
    noteBookOpened.add(noteBookId.urlsafe())
    cacheVal = memcache.get(noteBookId.urlsafe())
    if cacheVal is not None:
        profile = profileId.get()
        if profileId in cacheVal[8]:
            cacheVal[8].remove(profileId)
            profile.bookmarkedNoteBookIds.remove(noteBookId)
            bookmarkStatus = 0
        else:
            cacheVal[8].append(profileId)
            bookmarkStatus = 1
            profile.bookmarkedNoteBookIds.append(noteBookId)
        profile.put()
        memcache.set(noteBookId.urlsafe(), cacheVal)
        return BookmarkResponse(response=0, description="OK", bookmarkStatus=bookmarkStatus)
    profile = profileId.get()
    noteBook = noteBookId.get()
    if noteBookId in profile.bookmarkedNoteBookIds:
        profile.bookmarkedNoteBookIds.remove(noteBookId)
        noteBook.bmUserList.remove(profileId)
        status = 0
    else:
        profile.bookmarkedNoteBookIds.append(noteBookId)
        noteBook.bmUserList.append(profileId)
        status = 1
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
    results = search.Index('Course').search("NOT zoo")


def collegeListMethod(request):
    allCollege = College.query().fetch()
    collegeList = []
    for col in allCollege:
        collegeId = col.key
        college = collegeId.get()
        collegeDetail = CollegeDetails(collegeId=collegeId.urlsafe(),
                                       collegeName=college.collegeName,
                                       branchNames=college.branchNameList)
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
        return Response(response=1, description="Invaild profileId " + str(E))
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception, E:
        return Response(response=1, description="Invaild courseId " + str(E))
    profile = profileId.get()
    cacheVal = memcache.get(courseId.urlsafe())
    courseUpdate.add(courseId.urlsafe())
    if cacheVal is not None:
        if profileId in cacheVal[13]:
            profile.subscribedCourseIds.remove(courseId)
            profile.put()
            cacheVal[13].remove(profileId)
        else:
            profile.subscribedCourseIds.append(courseId)
            profile.put()
            cacheVal[13].append(profileId)
        memcache.set(courseId.urlsafe(), cacheVal)
        return Response(response=0, description="OK")
    course = courseId.get()
    if profile is None:
        return Response(response=1, description="Invaild profileId")
    if course is None:
        return Response(response=1, description="Invaild courseId")
    if courseId in profile.subscribedCourseIds:
        profile.subscribedCourseIds.remove(courseId)
        profile.put()
        course.studentIds.remove(profileId)
        course.put()
    else:
        profile.subscribedCourseIds.append(courseId)
        profile.put()
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
