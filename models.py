from google.appengine.ext import ndb
from protorpc import messages, message_types


class College(ndb.Model):
    """Contains information about college
        Fields: collegeName(required=True),
        abbreviation(required=True)
        location = ndb.StringProperty(required=True)
        representativeId(required=True, kind='Representative')
        branchIds(repeated=True, required=True, kind='Branch')
        courseIds(repeated=True, required=True, kind='Course')"""
    collegeName = ndb.StringProperty(required=True)
    abbreviation = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    courseIds = ndb.KeyProperty(repeated=True, kind='Course')
    collegeType = ndb.StringProperty()
    semStartDate = ndb.StringProperty()
    semEndDate = ndb.StringProperty()
    studentCount = ndb.IntegerProperty()
    noteBookCount = ndb.IntegerProperty()
    branchNameList = ndb.StringProperty(repeated=True)


class CollegeForm(messages.Message):
    collegeName = messages.StringField(1, required=True)
    abbreviation = messages.StringField(2, required=True)
    location = messages.StringField(3, required=True)
    collegeType = messages.StringField(4)
    semStartDate = messages.StringField(5)
    semEndDate = messages.StringField(6)
    branchNameList = messages.StringField(7, repeated=True)


class Profile(ndb.Model):
    profileName = ndb.StringProperty(required=True)
    collegeId = ndb.KeyProperty(required=True, kind='College')
    batchName = ndb.StringProperty()
    branchName = ndb.StringProperty()
    sectionName = ndb.StringProperty()
    availableCourseIds = ndb.KeyProperty(repeated=True, kind='Course')
    subscribedCourseIds = ndb.KeyProperty(repeated=True, kind='Course')
    administeredCourseIds = ndb.KeyProperty(repeated=True, kind='Course')
    photoUrl = ndb.StringProperty(required=True)
    gcmId = ndb.StringProperty()
    uploadedNoteBookIds = ndb.KeyProperty(repeated=True, kind='NoteBook')
    bookmarkedNoteBookIds = ndb.KeyProperty(repeated=True, kind='NoteBook')
    points = ndb.IntegerProperty()
    email = ndb.StringProperty(required=True)


class ProfileForm(messages.Message):
    profileName = messages.StringField(1, required=True)
    collegeId = messages.StringField(2, required=True)
    batchName = messages.StringField(3)
    branchName = messages.StringField(4)
    sectionName = messages.StringField(5)
    subscribedCouseIds = messages.StringField(7, repeated=True)
    availableCourseIds = messages.StringField(8, repeated=True)
    administeredCourseIds = messages.StringField(9, repeated=True)
    photoUrl = messages.StringField(10, required=True)
    uploadedNotes = messages.StringField(11, repeated=True)
    bookmarkedNotes = messages.StringField(12, repeated=True)
    points = messages.IntegerField(13)
    email = messages.StringField(14, required=True)
    gcmId = messages.StringField(15)


class Course(ndb.Model):
    courseName = ndb.StringProperty(required=True)
    collegeId = ndb.KeyProperty(required=True, kind='College')
    batchNames = ndb.StringProperty(repeated=True)
    branchNames = ndb.StringProperty(repeated=True)
    sectionNames = ndb.StringProperty(repeated=True)
    semester = ndb.StringProperty(required=True)
    noteBookIds = ndb.KeyProperty(repeated=True, kind='NoteBook')
    assignmentIds = ndb.KeyProperty(repeated=True, kind='Assignment')
    examIds = ndb.KeyProperty(repeated=True, kind='Exam')
    date = ndb.StringProperty(repeated=True)
    adminIds = ndb.KeyProperty(repeated=True, kind='Profile')
    startTime = ndb.StringProperty(repeated=True)
    endTime = ndb.StringProperty(repeated=True)
    professorName = ndb.StringProperty()
    colour = ndb.StringProperty()
    courseCode = ndb.StringProperty()
    studentIds = ndb.KeyProperty(repeated=True, kind='Profile')


class CourseForm(messages.Message):
    courseName = messages.StringField(1, required=True)
    collegeId = messages.StringField(2, required=True)
    batchNames = messages.StringField(3, repeated=True)
    branchNames = messages.StringField(10, repeated=True)
    sectionNames = messages.StringField(4, repeated=True)
    semester = messages.StringField(5, required=True)
    startTime = messages.StringField(6, repeated=True)
    endTime = messages.StringField(7, repeated=True)
    professorName = messages.StringField(8)
    profileId = messages.StringField(9, required=True)
    colour = messages.StringField(11)
    courseCode = messages.StringField(12)
    date = messages.StringField(13, repeated=True)


class SubscribeCourseRequest(messages.Message):
    profileId = messages.StringField(1, required=True)
    courseIds = messages.StringField(2, repeated=True)


class CourseListRequest(messages.Message):
    profileId = messages.StringField(1)
    courseIds = messages.StringField(2, repeated=True)


class CourseResponse(messages.Message):
    courseId = messages.StringField(11)
    courseName = messages.StringField(3)
    batchNames = messages.StringField(4, repeated=True)
    branchNames = messages.StringField(5, repeated=True)
    sectionNames = messages.StringField(6, repeated=True)
    studentCount = messages.IntegerField(7)
    professorName = messages.StringField(8)
    notesCount = messages.IntegerField(9)
    completed = messages.IntegerField(10)
    semester = messages.StringField(12)


class CourseListResponse(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    courseList = messages.MessageField(CourseResponse, 3, repeated=True)
    completed = messages.IntegerField(12)


class FeedCourseResponse(messages.Message):
    courseId = messages.StringField(8)
    courseName = messages.StringField(1)
    dueAssignments = messages.IntegerField(2)
    dueExams = messages.IntegerField(3)
    recentNotes = messages.IntegerField(4)
    date = messages.StringField(5, repeated=True)
    startTime = messages.StringField(6, repeated=True)
    endTime = messages.StringField(7, repeated=True) 


class FeedResponse(messages.Message):
    collegeId = messages.StringField(8)
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    profileName = messages.StringField(3)
    points = messages.IntegerField(4)
    photoUrl = messages.StringField(5)
    availableCourseList = messages.MessageField(FeedCourseResponse, 6, repeated=True)
    subscribedCourseList = messages.MessageField(FeedCourseResponse, 7, repeated=True)


class ProfileIdRequest(messages.Message):
    profileId = messages.StringField(1)


class TTCourseResponse(messages.Message):
    courseName = messages.StringField(1)
    colour = messages.StringField(2)
    courseId = messages.StringField(3)
    date = messages.StringField(4, repeated=True)
    startTime = messages.StringField(5, repeated=True)
    endTime = messages.StringField(6, repeated=True)


class TimeTableResponse(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    courseList = messages.MessageField(TTCourseResponse, 3, repeated=True)


class StudentResponse(messages.Message):
    profileId = messages.StringField(1)
    profileName = messages.StringField(2)
    photoUrl = messages.StringField(3)
    isAdmin = messages.IntegerField(4)


class StudentListResponse(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    isAdmin = messages.IntegerField(3)
    studentList = messages.MessageField(StudentResponse, 4, repeated=True)


class Assignment(ndb.Model):
    assignmentTitle = ndb.StringProperty(required=True)
    assignmentDesc = ndb.StringProperty(required=True)
    dueDate = ndb.StringProperty(required=True)
    dueTime = ndb.StringProperty()
    courseId = ndb.KeyProperty(required=True, kind='Course')
    uploaderId = ndb.KeyProperty(kind='Profile')
    assignmentViews = ndb.IntegerProperty()
    dateUploaded = ndb.StringProperty()
    urlList = ndb.StringProperty(repeated=True)
    remindProfileIds = ndb.KeyProperty(repeated=True, kind='Profile')


class AssignmentForm(messages.Message):
    assignmentTitle = messages.StringField(1, required=True)
    assignmentDesc = messages.StringField(2, required=True)
    courseId = messages.StringField(3, required=True)
    uploaderId = messages.StringField(4)
    assignmentViews = messages.IntegerField(5)
    dueDate = messages.StringField(6)
    dueTime = messages.StringField(8)
    urlList = messages.StringField(7, repeated=True)


class Exam(ndb.Model):
    examTitle = ndb.StringProperty()
    courseId = ndb.KeyProperty(kind='Course')
    uploaderId = ndb.KeyProperty(kind='Profile')
    dateUploaded = ndb.StringProperty()
    dueDate = ndb.StringProperty(required=True)
    dueTime = ndb.StringProperty()
    examDesc = ndb.StringProperty()
    examViews = ndb.IntegerProperty()
    urlList = ndb.StringProperty(repeated=True)
    remindProfileIds = ndb.KeyProperty(repeated=True, kind='Profile')


class ExamForm(messages.Message):
    examTitle = messages.StringField(1)
    courseId = messages.StringField(2)
    uploaderId = messages.StringField(3)
    dueDate = messages.StringField(5)
    examDesc = messages.StringField(6)
    views = messages.IntegerField(7)
    dueTime = messages.StringField(8)
    urlList = messages.StringField(9, repeated=True)


class GetAssignmentRequest(messages.Message):
    profileId = messages.StringField(1)
    assignmentId = messages.StringField(2)


class GetAssignmentResponse(messages.Message):
    response = messages.IntegerField(9)
    description = messages.StringField(10)
    isAuthor = messages.IntegerField(1)
    assignmentTitle = messages.StringField(2)
    assignmentDesc = messages.StringField(3)
    lastUpdated = messages.StringField(4)
    views = messages.IntegerField(5)
    uploaderName = messages.StringField(6)
    dueDate = messages.StringField(7)
    dueTime = messages.StringField(8)
    urlList = messages.StringField(11, repeated=True)
    courseName = messages.StringField(12)


class AssignmentResponse(messages.Message):
    assignmentId = messages.StringField(10)
    isAuthor = messages.IntegerField(1)
    assignmentTitle = messages.StringField(2)
    assignmentDesc = messages.StringField(3)
    lastUpdated = messages.StringField(4)
    views = messages.IntegerField(5)
    uploaderName = messages.StringField(6)
    dueDate = messages.StringField(7)
    dueTime = messages.StringField(8)
    pages = messages.IntegerField(9)
    courseName = messages.StringField(11)


class ExamResponse(messages.Message):
    examId = messages.StringField(10)
    isAuthor = messages.IntegerField(1)
    examTitle = messages.StringField(2)
    examDesc = messages.StringField(3)
    lastUpdated = messages.StringField(4)
    views = messages.IntegerField(5)
    uploaderName = messages.StringField(6)
    dueDate = messages.StringField(7)
    dueTime = messages.StringField(8)
    pages = messages.IntegerField(9)
    courseName = messages.StringField(11)


class GetAssListResponse(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    assList = messages.MessageField(AssignmentResponse, 3, repeated=True)


class GetExamListResponse(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    examList = messages.MessageField(ExamResponse, 3, repeated=True)


class GetExamRequest(messages.Message):
    profileId = messages.StringField(1)
    examId = messages.StringField(2)


class GetExamResponse(messages.Message):
    response = messages.IntegerField(9)
    description = messages.StringField(10)
    isAuthor = messages.IntegerField(1)
    examTitle = messages.StringField(2)
    examDesc = messages.StringField(3)
    lastUpdated = messages.StringField(4)
    views = messages.IntegerField(5)
    uploaderName = messages.StringField(6)
    dueDate = messages.StringField(7)
    dueTime = messages.StringField(8)
    urlList = messages.StringField(11, repeated=True)
    courseName = messages.StringField(12)


class NoteBook(ndb.Model):
    courseId = ndb.KeyProperty(required=True, kind='Course')
    uploaderId = ndb.KeyProperty(required=True, kind='Profile')
    notesIds = ndb.KeyProperty(repeated=True, kind='Notes')
    ratedUserIds = ndb.KeyProperty(repeated=True, kind='Profile')
    ratingList = ndb.IntegerProperty(repeated=True)
    totalRating = ndb.StringProperty()
    frequency = ndb.IntegerProperty()
    views = ndb.IntegerProperty()
    lastUpdated = ndb.StringProperty()


class Notes(ndb.Model):
    title = ndb.StringProperty()
    date = ndb.StringProperty()
    urlList = ndb.StringProperty(repeated=True)
    notesDesc = ndb.StringProperty()
    noteBookId = ndb.KeyProperty(kind='NoteBook')
    classNumber = ndb.StringProperty()


class NotesForm(messages.Message):
    profileId = messages.StringField(1)
    date = messages.StringField(2)
    urlList = messages.StringField(3, repeated=True)
    notesDesc = messages.StringField(4)
    classNumber = messages.StringField(5)
    courseId = messages.StringField(6)
    title = messages.StringField(7)


class NoteBookRequest(messages.Message):
    profileId = messages.StringField(1)
    noteBookId = messages.StringField(2)


class NotesResponse(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    date = messages.StringField(3)
    classNumber = messages.StringField(4)
    urlList = messages.StringField(5, repeated=True)


class NoteBookDetailResponse(messages.Message):
    courseName = messages.StringField(12)
    isAuthor = messages.IntegerField(1)
    uploaderName = messages.StringField(2)
    lastUpdated = messages.StringField(3)
    views = messages.IntegerField(4)
    rated = messages.IntegerField(5)
    frequency = messages.IntegerField(6)
    pages = messages.IntegerField(7)
    totalRating = messages.StringField(8)
    notes = messages.MessageField(NotesResponse, 9, repeated=True)
    response = messages.IntegerField(10)
    description = messages.StringField(11)


class NoteBookListRequest(messages.Message):
    noteBookIds = messages.StringField(1, repeated=True)
    bpid = messages.StringField(2)
    upid = messages.StringField(3)
    courseId = messages.StringField(4)
    profileId = messages.StringField(5)


class NoteBookResponse(messages.Message):
    noteBookId = messages.StringField(3)
    courseName = messages.StringField(1)
    uploaderName = messages.StringField(2)
    pages = messages.IntegerField(4)
    views = messages.IntegerField(5)
    totalRating = messages.StringField(6)
    frequency = messages.IntegerField(7)
    lastUpdated = messages.StringField(8)


class NoteBookListResponse(messages.Message):
    response = messages.IntegerField(1)
    noteBookList = messages.MessageField(NoteBookResponse, 2, repeated=True)
    description = messages.StringField(3)


class RatingRequest(messages.Message):
    profileId = messages.StringField(1)
    rating = messages.IntegerField(2)
    noteBookId = messages.StringField(3)


class CoursePageRequest(messages.Message):
    courseId = messages.StringField(1)
    profileId = messages.StringField(2)


class AssExamResponse(messages.Message):
    Id = messages.StringField(1)
    name = messages.StringField(2)
    dueDate = messages.StringField(3)
    dueTime = messages.StringField(8)
    uploaderName = messages.StringField(4)
    dateUploaded = messages.StringField(5)
    views = messages.IntegerField(6)
    description = messages.StringField(7)


class CoursePageResponse(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    isSubscribed = messages.IntegerField(3)
    courseName = messages.StringField(4)
    examCount = messages.IntegerField(5)
    assignmentCount = messages.IntegerField(6)
    notesCount = messages.IntegerField(7)
    date = messages.StringField(8, repeated=True)
    startTime = messages.StringField(9, repeated=True)
    endTime = messages.StringField(10, repeated=True)
    examList = messages.MessageField(AssExamResponse, 11, repeated=True)
    assignmentList = messages.MessageField(AssExamResponse, 12, repeated=True)
    studentCount = messages.IntegerField(13)


class BookmarkRequest(messages.Message):
    profileId = messages.StringField(1)
    noteBookId = messages.StringField(2)


class Response(messages.Message):
    response = messages.IntegerField(1)
    description = messages.StringField(2)
    key = messages.StringField(3)


class CourseInfoMyFeed(messages.Message):
    courseId = messages.StringField(1)
    name = messages.StringField(2)
    numberNewNotes = messages.IntegerField(3)
    numberOpenAssn = messages.IntegerField(4)
    numberOpenExam = messages.IntegerField(5)


class myFeedOutputForm(messages.Message):
    courseInfo = messages.MessageField(CourseInfoMyFeed, 1, repeated=True)
    availableCourseIds = messages.StringField(6, repeated=True)


class CollegeDetails(messages.Message):
    collegeId = messages.StringField(1)
    collegeName = messages.StringField(2)
    branchNames = messages.StringField(3, repeated=True)


class CollegeListResponse(messages.Message):
    collegeList = messages.MessageField(CollegeDetails, 1, repeated=True)


class AddBranchRequest(messages.Message):
    collegeId = messages.StringField(1)
    branchName = messages.StringField(2)
