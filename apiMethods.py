import datetime

from models import College, Course, Profile, ProfileForm
from models import Response, FeedCourseResponse, CourseListResponse, FeedResponse
from models import TTCourseResponse, TimeTableResponse, StudentResponse
from models import StudentListResponse, Assignment, Exam, CourseResponse
from models import GetAssignmentResponse, GetExamResponse, Notes, NoteBook
from models import NotesResponse, NoteBookDetailResponse, NoteBookListResponse
from models import NoteBookResponse, CoursePageResponse, AssExamResponse
from models import AssignmentResponse, ExamResponse, GetAssListResponse
from models import GetExamListResponse, CollegeListResponse, CollegeDetails
from google.appengine.ext import ndb


def createCollegeMethod(request):
    """createCollegeMethod(request)
    request(POST) containing collegeName, abbreviation, location
    creates a new college"""
    collegeName = getattr(request, 'collegeName')
    abbreviation = getattr(request, 'abbreviation')
    location = getattr(request, 'location')
    collegeType = getattr(request, 'collegeType', None)
    semStartDate = getattr(request, 'semStartDate', None)
    semEndDate = getattr(request, 'semEndDate', None)
    branchNameList = getattr(request, 'branchNameList', None)
    queryString = ndb.AND(College.collegeName == collegeName,
                          College.location == location)
    collegeSameDetails = College.query(queryString).fetch()
    print collegeSameDetails
    if collegeSameDetails:
        return Response(response=1, description="College Already Exists")
    else:
        newCollege = College(collegeName=collegeName, abbreviation=abbreviation,
                             location=location, studentCount=0, noteBookCount=0,
                             collegeType=collegeType, semStartDate=semStartDate,
                             semEndDate=semEndDate, courseIds=[],
                             branchNameList=branchNameList)
        key = newCollege.put()
        return Response(response=0, description="OK", key=key.urlsafe())


def createProfileMethod(request):
    """
    createProfileMethod(request)
    request: profileName, collegeId, batchName, branchName,
    sectionName, semester, photoUrl, email
    creates a new Profile"""
    profileName = getattr(request, 'profileName')
    try:
        collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
    except Exception:
        return Response(response=1, description="No such collegeId")
    batchName = getattr(request, 'batchName', None)
    branchName = getattr(request, 'branchName', None)
    sectionName = getattr(request, 'sectionName', None)
    # Querier for compatible courses and stores in availableCourseIds
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
    profileCheck = Profile.query(Profile.email == email).fetch()
    if college is None:
        return Response(response=1, description="No such college ID")
    elif profileCheck:
        return Response(response=1, description="Profile already registered")
    else:
        newProfile = Profile(profileName=profileName, collegeId=collegeId,
                             batchName=batchName, branchName=branchName,
                             sectionName=sectionName, subscribedCourseIds=[],
                             availableCourseIds=availableCourseIds,
                             administeredCourseIds=[], gcmId=gcmId,
                             photoUrl=photoUrl, email=email, points=0,
                             uploadedNoteBookIds=[], bookmarkedNoteBookIds=[])
        college.studentCount += 1
        college.put()
        key = newProfile.put()
        return Response(response=0, description="OK", key=key.urlsafe())


def addCourseMethod(request):
    """addCourseMethod(request)
    request(POST) containing courseName, collegeId, batchName, sectionName,
    semester, adminId, startTime, endTime, proffessorName
    creates a new course and adds it to the college"""
    courseName = getattr(request, 'courseName')
    try:
        collegeId = ndb.Key(urlsafe=(getattr(request, 'collegeId')))
    except Exception:
        return Response(response=1, description="No such collegeId")
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
    college = collegeId.get()
    profile = profileId.get()
    if college is None:
        return Response(response=1, description="No such college ID")
    if profile is None:
        return Response(response=1, description="No such profile ID")
    queryString = ndb.AND(Course.courseCode == courseCode,
                          Course.collegeId == collegeId,
                          Course.sectionNames.IN(sectionNames),
                          Course.branchNames.IN(branchNames),
                          Course.batchNames.IN(batchNames),
                          Course.professorName == professorName)
    coursesWithSameCode = Course.query(queryString).fetch()
    if coursesWithSameCode:
        return Response(response=1, description="Course already exists")

    newCourse = Course(courseName=courseName, collegeId=collegeId,
                       batchNames=batchNames, branchNames=branchNames,
                       sectionNames=sectionNames, semester=semester,
                       adminIds=adminIds, date=date,
                       startTime=startTime, endTime=endTime,
                       professorName=professorName, studentIds=studentIds,
                       colour=colour, courseCode=courseCode,
                       noteBookIds=[], assignmentIds=[], examIds=[])
    courseId = newCourse.put()
    for profileId in adminIds:
        profile = profileId.get()
        profile.subscribedCourseIds.append(courseId)
        profile.put()
    college.courseIds.append(courseId)
    college.put()
    profile.administeredCourseIds.append(courseId)
    profile.put()
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
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="No such profileId")
    courseIdList = getattr(request, 'courseIds')
    courseIds = []
    profile = profileId.get()
    for course in courseIdList:
        try:
            courseId = ndb.Key(urlsafe=course)
        except Exception:
            return Response(response=1, description="No such courseId")
        profile.subscribedCourseIds.append(courseId)
        courseIds.append(courseId)
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
    page = getattr(request, 'page')
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
                return CourseListResponse(response=1, description="No such ProfileId")
            profile = profileId.get()
            for courseId in profile.availableCourseIds:
                course = courseId.get()
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
                                                notesCount=notesCount)
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
                print course.courseName, course.batchNames, course.branchNames,course.sectionNames, studentCount, course.professorName, notesCount
                feedCourseResponse = CourseResponse(courseId=courseId.urlsafe(),
                                                courseName=course.courseName,
                                                batchNames=course.batchNames,
                                                branchNames=course.branchNames,
                                                sectionNames=course.sectionNames,
                                                studentCount=studentCount,
                                                professorName=course.professorName,
                                                notesCount=notesCount,
                                                semester=course.semester)
                courseListResponse.append(feedCourseResponse)
            return CourseListResponse(response=0, description="OK",
                                      courseList=courseListResponse,
                                      completed=0)


def feedMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return FeedResponse(response=1, description="Invalid profileId")
    profile = profileId.get()
    profileName = profile.profileName
    points = profile.points
    photoUrl = profile.photoUrl
    availableCourseIds = profile.availableCourseIds
    subscribedCourseIds = profile.subscribedCourseIds
    availableCourseList = feedCourseResponse(availableCourseIds)
    subscribedCourseList = feedCourseResponse(subscribedCourseIds)
    collegeId = profile.collegeId
    return FeedResponse(response=0, description="OK", profileName=profileName,
                        points=points, photoUrl=photoUrl,
                        availableCourseList=availableCourseList,
                        subscribedCourseList=subscribedCourseList, collegeId=collegeId.urlsafe())


def feedCourseResponse(courseIds):
    responseList = []
    curDate = datetime.datetime.now().date()
    curTime = datetime.datetime.now().time()
    for courseId in courseIds:
        dueAssignments, dueExams, recentNotes = 0, 0, 0
        course = courseId.get()
        assignmentIds = course.assignmentIds
        for assignmentId in assignmentIds:
            assignment = assignmentId.get()
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
            a = str(noteBook.lastUpdated)
            date, month, year = int(a[8:10]), int(a[5:7]), int(a[0:4])
            lastUpdated = datetime.date(year, month, date)
            if(curDate-lastUpdated).days > 7:
                continue
            recentNotes = recentNotes + 1
        responseList.append(FeedCourseResponse(courseId=courseId.urlsafe(),
                                               courseName=course.courseName,
                                               dueAssignments=dueAssignments,
                                               dueExams=dueExams, date=course.date,
                                               startTime=course.startTime,
                                               endTime=course.endTime,
                                               recentNotes=recentNotes))
    return responseList


def addAdminMethod(request):
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return Response(response=1, description="Invalid courseId")
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invalid profileId")
    course = courseId.get()
    profile = profileId.get()
    profile.administeredCourseIds.append(courseId)
    course.adminIds.append(profileId)
    if courseId in profile.availableCourseIds:
        profile.availableCourseIds.remove(courseId)
    profile.put()
    course.put()
    return Response(response=0, description="OK")


def timeTableMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invalid profile Id")
    profile = profileId.get()
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
    try:
        profileId = ndb.Key(urlsafe=request.profileId)
    except Exception:
        return StudentListResponse(response=1, description="Invalid profileId")
    try:
        courseId = ndb.Key(urlsafe=request.courseId)
    except Exception:
        return StudentListResponse(response=1, description="Invalid courseId")
    profile = profileId.get()
    course = courseId.get()
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
    assignmentTitle = getattr(request, 'assignmentTitle')
    assignmentDesc = getattr(request, 'assignmentDesc')
    dateUploaded = str(datetime.datetime.now())
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
    course.assignmentIds.append(assignmentId)
    course.put()
    return Response(response=0, description="OK", key=assignmentId.urlsafe())


def createExamMethod(request):
    examTitle = getattr(request, 'examTitle')
    examDesc = getattr(request, 'examDesc')
    dateUploaded = str(datetime.datetime.now())
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
    course.examIds.append(examId)
    course.put()
    return Response(response=0, description="OK", key=examId.urlsafe())


def getAssignmentMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return GetAssignmentResponse(response=1, description="Invalid profileId")
    try:
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
    except Exception:
        return GetAssignmentResponse(response=1, description="Invalid assignmentId")
    profile = profileId.get()
    assignment = assignmentId.get()
    if profileId == assignment.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = assignment.uploaderId.get().profileName
    assignment.assignmentViews = assignment.assignmentViews+1
    course = assignment.courseId.get()
    assignment.put()
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
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return GetExamResponse(response=1, description="Invalid profileId")
    try:
        examId = ndb.Key(urlsafe=getattr(request, 'examId'))
    except Exception:
        return GetExamResponse(response=1, description="Invalid examId")
    profile = profileId.get()
    exam = examId.get()
    if profileId == exam.uploaderId:
        isAuthor = 1
    else:
        isAuthor = 0
    uploaderName = exam.uploaderId.get().profileName
    exam.examViews = exam.examViews + 1
    exam.put()
    course = exam.courseId.get()
    return GetExamResponse(response=0, description="OK",
                           isAuthor=isAuthor, views=exam.examViews,
                           examTitle=exam.examTitle, examDesc=exam.examDesc,
                           lastUpdated=exam.dateUploaded,
                           uploaderName=uploaderName, dueDate=exam.dueDate,
                           dueTime=exam.dueTime, urlList=exam.urlList,
                           courseName=course.courseName)


def createNotesMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invalid profileId")
    date = getattr(request, 'date')
    urlList = getattr(request, 'urlList')
    notesDesc = getattr(request, 'notesDesc')
    classNumber = getattr(request, 'classNumber')
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return Response(response=1, description="Invalid courseId")
    title = getattr(request, 'title')
    # CHECKS IF NOTEBOOK WITH SAME profileID AND courseId already exists
    newNotes = Notes(date=date, urlList=urlList, notesDesc=notesDesc,
                     classNumber=classNumber, title=title)
    query = NoteBook.query(ndb.AND(NoteBook.courseId == courseId,
                                   NoteBook.uploaderId == profileId))
    noteBookResult = query.fetch()
    if noteBookResult:
        for noteBook in noteBookResult:
            addToNoteBook(noteBook.key, newNotes)
            return Response(response=0, description="OK",
                            key=noteBook.key.urlsafe())
    else:
        noteBookId = createNoteBook(profileId, courseId)
        addToNoteBook(noteBookId, newNotes)
        return Response(response=0, description="OK", key=noteBookId.urlsafe())


def createNoteBook(profileId, courseId):
    newNoteBook = NoteBook(courseId=courseId, uploaderId=profileId,
                           notesIds=[], ratedUserIds=[], ratingList=[],
                           totalRating="0", frequency=0, views=0)
    course = courseId.get()
    college = course.collegeId.get()
    college.noteBookCount += 1
    college.put()
    profile = profileId.get()
    noteBookId = newNoteBook.put()
    profile.uploadedNoteBookIds.append(noteBookId)
    profile.put()
    course.noteBookIds.append(noteBookId)
    course.put()
    return noteBookId


def addToNoteBook(noteBookId, newNotes):
    newNotes.noteBookId = noteBookId
    notesId = newNotes.put()
    noteBook = noteBookId.get()
    noteBook.notesIds.append(notesId)
    noteBook.frequency += 1
    noteBook.lastUpdated = str(datetime.datetime.now())
    noteBook.put()


def getNoteBook(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return NoteBookDetailResponse(response=1, description="Invalid profileId")
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    except Exception:
        return NoteBookDetailResponse(response=1, description="Invalid noteBookId")
    noteBook = noteBookId.get()
    if noteBook.uploaderId == profileId:
        isAuthor = 1
    else:
        isAuthor = 0
    noteBookUploader = noteBook.uploaderId.get()
    course = noteBook.courseId.get()
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
        notesList.append(NotesResponse(title=notes.title,
                                       description=notes.notesDesc,
                                       date=notes.date,
                                       classNumber=notes.classNumber,
                                       urlList=notes.urlList))
        pages += len(notes.urlList)
    return NoteBookDetailResponse(courseName=course.courseName,
                                  isAuthor=isAuthor, uploaderName=uploaderName,
                                  lastUpdated=lastUpdated, views=views,
                                  rated=rated, frequency=frequency,
                                  pages=pages, totalRating=totalRating,
                                  notes=notesList, response=0,
                                  description="OK")


def getNoteBookListMethod(request):
    noteBookIds = getattr(request, 'noteBookIds', None)
    print noteBookIds
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
            course =    noteBook.courseId.get()
            uploader = noteBook.uploaderId.get()
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=idurlsafe,
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views,  pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated)
            noteBookList.append(new)
    elif bpid:
        try:
            profileId = ndb.Key(urlsafe=bpid)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        bookmarkedIds = profile.bookmarkedNoteBookIds
        for noteBookId in bookmarkedIds:
            noteBook = noteBookId.get()
            course = noteBook.courseId.get()
            uploader = noteBook.uploaderId.get()
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views,  pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated)
            noteBookList.append(new)
    elif upid:
        print upid
        try:
            profileId = ndb.Key(urlsafe=upid)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        uploadedIds = profile.uploadedNoteBookIds
        for noteBookId in uploadedIds:
            noteBook = noteBookId.get()
            course = noteBook.courseId.get()
            uploader = noteBook.uploaderId.get()
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views,  pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated)
            noteBookList.append(new)
    elif courseId:
        try:
            courseId = ndb.Key(urlsafe=courseId)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid courseId")
        course = courseId.get()
        noteBookIds = course.noteBookIds
        for noteBookId in noteBookIds:
            noteBook = noteBookId.get()
            uploader = noteBook.uploaderId.get()
            pages = 0
            for notesId in noteBook.notesIds:
                notes = notesId.get()
                pages += len(notes.urlList)
            new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                   courseName=course.courseName,
                                   uploaderName=uploader.profileName,
                                   views=noteBook.views,  pages=pages,
                                   totalRating=noteBook.totalRating,
                                   frequency=noteBook.frequency,
                                   lastUpdated=noteBook.lastUpdated)
            noteBookList.append(new)
    elif profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
        except Exception:
            return NoteBookListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            noteBookIds = course.noteBookIds
            for noteBookId in noteBookIds:
                noteBook = noteBookId.get()
                uploader = noteBook.uploaderId.get()
                pages = 0
                for notesId in noteBook.notesIds:
                    notes = notesId.get()
                    pages += len(notes.urlList)
                new = NoteBookResponse(noteBookId=noteBookId.urlsafe(),
                                       courseName=course.courseName,
                                       uploaderName=uploader.profileName,
                                       views=noteBook.views,  pages=pages,
                                       totalRating=noteBook.totalRating,
                                       frequency=noteBook.frequency,
                                       lastUpdated=noteBook.lastUpdated)
                noteBookList.append(new)
    else:
        return NoteBookListResponse(response=1, description="Bad request")
    return NoteBookListResponse(response=0, description="OK",
                                noteBookList=noteBookList)


def rateThisMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invaild profileId")
    rating = getattr(request, 'rating')
    noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    noteBook = noteBookId.get()
    if profileId in noteBook.ratedUserIds:
        return Response(response=1, description="Already Rated")
    noteBook.ratedUserIds.append(profileId)
    noteBook.ratingList.append(rating)
    noteBook.put()
    return Response(response=0, description="OK")


def coursePageMethod(request):
    try:
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
    except Exception:
        return CoursePageResponse(response=1, description="Invalid courseId")
    course = courseId.get()
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return CoursePageResponse(response=1, description="Invalid profileId")
    if profileId in course.studentIds:
        isSubscribed = 1
    else:
        isSubscribed = 0
    assignmentList, examList = [], []
    curDate = datetime.datetime.now().date()
    curTime = datetime.datetime.now().time()
    dueAssignments, dueExams, recentNotes = 0, 0, 0
    assignmentIds = course.assignmentIds
    studentCount = len(course.studentIds)
    for assignmentId in assignmentIds:
        assignment = assignmentId.get()
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
            a = str(noteBook.lastUpdated)
            date, month, year = int(a[8:10]), int(a[5:7]), int(a[0:4])
            lastUpdated = datetime.date(year, month, date)
            if(curDate-lastUpdated).days > 7:
                continue
            recentNotes = recentNotes + 1
    return CoursePageResponse(response=0, description="OK",
                       isSubscribed=isSubscribed, courseName=course.courseName,
                       date=course.date, startTime=course.startTime,
                       endTime=course.endTime, examCount=dueExams,
                       assignmentCount=dueAssignments, notesCount=recentNotes,
                       examList=examList, assignmentList=assignmentList,
                       studentCount=studentCount)


def getAssignmentListMethod(request):
    profileId = getattr(request, 'profileId', None)
    courseId = getattr(request, 'courseId', None)
    if profileId:
        try:
            profileId = ndb.Key(urlsafe=profileId)
        except Exception:
            return GetAssListResponse(response=1, description="Invalid profileId")
        profile = profileId.get()
        assList = []
        for courseId in profile.subscribedCourseIds:
            course = courseId.get()
            for assignmentId in course.assignmentIds:
                assignment = assignmentId.get()
                if profileId == assignment.uploaderId:
                    isAuthor = 1
                else:
                    isAuthor = 0
                uploaderName = assignment.uploaderId.get().profileName
                assList.append(AssignmentResponse(assignmentId=assignmentId.urlsafe(),
                                             isAuthor=isAuthor, views=assignment.assignmentViews,
                                             assignmentTitle=assignment.assignmentTitle,
                                             assignmentDesc=assignment.assignmentDesc,
                                             lastUpdated=assignment.dateUploaded,
                                             uploaderName=uploaderName,
                                             dueDate=assignment.dueDate,
                                             dueTime=assignment.dueTime,
                                             pages=len(assignment.urlList),
                                             courseName=course.courseName))
    else:
        try:
            courseId = ndb.Key(urlsafe=courseId)
        except Exception:
            return GetAssListResponse(response=1, description="Invalid courseId")
        assList = []
        course = courseId.get()
        for assignmentId in course.assignmentIds:
            assignment = assignmentId.get()
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
                                              courseName=course.courseName))
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
            print course.courseName
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
                                             courseName=course.courseName))
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
                                         courseName=course.courseName))
    return GetExamListResponse(response=0, description="OK",
                               examList=examList)


def bookmarkMethod(request):
    try:
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    except Exception:
        return Response(response=1, description="Invalid profileId")
    try:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    except Exception:
        return Response(response=1, description="Invalid noteBookId")
    profile = profileId.get()
    profile.bookmarkedNoteBookIds.append(noteBookId)
    profile.put()
    return Response(response=0, description="OK")


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




def deleteNoteBook(request, id=None):
    if id:
        noteBookId = id
    else:
        noteBookId = ndb.Key(urlsafe=getattr(request, 'noteBookId'))
    noteBook = noteBookId.get()
    course = noteBook.courseId.get()
    course.noteBookIds.remove(noteBookId)
    uploader = noteBook.uploaderId.get()
    uploader.uploadedNoteBookIds.remove(noteBookId)
    bookmarkedProfiles = Profile.query(Profile.bookmarkedNoteBookIds==noteBookId).fetch()
    course.put()
    uploader.put()
    for profileR in bookmarkedProfiles:
        profile = profileR.key.get()
        profile.bookmarkedNoteBookIds.remove(noteBookId)
        profile.put()
    noteBookId.delete()


def deleteNotes(request):
    notesId = ndb.Key(urlsafe=getattr(request, 'notesId'))
    notes = notesId.get()
    noteBookId = notes.noteBookId
    noteBook = noteBookId.get()
    noteBook.notesIds.remove(notesId)
    noteBook.frequency -= 1
    noteBook.put()
    if noteBook.frequency == 0:
        deleteNoteBook(id=noteBookId)


def deleteAssignment(request, id=None):
    if id:
        assignmentId = id
    else:
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
    assignment = assignmentId.get()
    course = assignment.courseId.get()
    course.assignmentIds.remove(assignmentId)
    course.put()
    assignmentId.delete()


def deleteExam(request, id=None):
    if id:
        examId = id
    else:
        examId = ndb.Key(urlsafe=getattr(request, 'examId'))
    exam = examId.get()
    course = exam.courseId.get()
    course.examIds.remove(examId)
    course.put()
    examId.delete()


def deleteProfile(request):
    profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
    profile = profile.get()
    for noteBookId in profile.uploadedNoteBookIds:
        deleteNoteBook(id=noteBookId)
    for courseId in profile.administeredCourseIds:
        course = couseId.get()
        if len(course.adminIds) == 1:
            if len(course.studentIds) == 1:
                return Response(resource=1, description="No admins")
            course.adminId.append(course.studentIds[0])
            newAdmin = course.admin
