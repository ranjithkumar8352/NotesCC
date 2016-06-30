import endpoints
from protorpc import messages, message_types, remote

from models import CollegeForm, CourseForm, ProfileForm
from models import NotesForm, Response, AssignmentForm, SubscribeCourseRequest
from models import CourseListRequest, CourseListResponse, FeedResponse
from models import ProfileIdRequest, TimeTableResponse, StudentListResponse
from models import ExamForm, GetAssignmentRequest, GetAssignmentResponse
from models import GetExamRequest, GetExamResponse, NoteBookRequest
from models import NoteBookDetailResponse, NoteBookListRequest
from models import NoteBookListResponse, RatingRequest, CoursePageRequest
from models import CoursePageResponse, GetExamListResponse, GetAssListResponse, DeleteRequest
from models import BookmarkRequest, CollegeListResponse, AddBranchRequest
from models import SearchCourseRequest, BookmarkResponse, SearchNBRequest
from models import UnsubscribeCourseRequest
from apiMethods import createCollegeMethod, addCourseMethod
from apiMethods import createProfileMethod, subscribeCourseMethod
from apiMethods import courseListMethod, feedMethod, addAdminMethod
from apiMethods import timeTableMethod, studentListMethod, createAssignmentMethod
from apiMethods import createExamMethod, getAssignmentMethod, getExamMethod
from apiMethods import createNotesMethod, getNoteBook, getNoteBookListMethod
from apiMethods import rateThisMethod, coursePageMethod
from apiMethods import getAssignmentListMethod, getExamListMethod
from apiMethods import bookmarkMethod, clearAll, collegeListMethod, addBranchMethod
from apiMethods import deleteMethod, unsubscribeCourseMethod
from searchAPI import createCourseDoc, searchCourseMethod, searchNBMethod
from apiTest import runScript


@endpoints.api(name='notesapi', version='v1')
class NotesAPI(remote.Service):
    @endpoints.method(
        CollegeForm,
        Response,
        path='createCollege',
        http_method='POST',
        name='createCollege')
    def createCollege(self, request):
        return createCollegeMethod(request)

    @endpoints.method(
        ProfileForm,
        Response,
        path='createProfile',
        http_method='POST',
        name='createProfile')
    def createProfile(self, request):
        return createProfileMethod(request)

    @endpoints.method(
        CourseForm,
        Response,
        path='addCourse',
        http_method='POST',
        name='addCourse')
    def addCourse(self, request):
        response = addCourseMethod(request)
        if response.response == 0:
            createCourseDoc(request, response.key)
        return response

    @endpoints.method(
        SubscribeCourseRequest,
        Response,
        path='subscribeCourse',
        http_method='POST',
        name='subscribeCourse')
    def subscribeCourse(self, request):
        return subscribeCourseMethod(request)

    @endpoints.method(
        UnsubscribeCourseRequest,
        Response,
        path='unsubscribeCourse',
        http_method='POST',
        name='unsubscribeCourse')
    def unsubCourse(self, request):
        return unsubscribeCourseMethod(request)
    courseListResource = endpoints.ResourceContainer(CourseListRequest,
                                                     page=messages.IntegerField
                                                     (1, variant=messages.
                                                      Variant.INT32))

    @endpoints.method(
        courseListResource,
        CourseListResponse,
        path='courseList/{page}',
        http_method='POST',
        name='courseList')
    def courseList(self, request):
        return courseListMethod(request)

    feedResource = endpoints.ResourceContainer(message_types.VoidMessage,
                                               profileId=messages.StringField(1))

    @endpoints.method(
        feedResource,
        FeedResponse,
        path='feed/{profileId}',
        http_method='GET',
        name='feed')
    def feed(self, request):
        return feedMethod(request)

    addAdminResource = endpoints.ResourceContainer(ProfileIdRequest,
                                                   courseId=messages.StringField(2))

    @endpoints.method(
        addAdminResource,
        Response,
        path='addAdmin/{courseId}',
        http_method='POST',
        name='addAdmin')
    def addAdmin(self, request):
        return addAdminMethod(request)

    timeTableResource = endpoints.ResourceContainer(message_types.VoidMessage,
                                                    profileId=messages.StringField(1))

    @endpoints.method(
        timeTableResource,
        TimeTableResponse,
        path='timeTable/{profileId}',
        http_method='GET',
        name='timeTable')
    def timeTable(self, request):
        return timeTableMethod(request)

    studentListResource = endpoints.ResourceContainer(ProfileIdRequest,
                                                      courseId=messages.StringField(1))

    @endpoints.method(
        studentListResource,
        StudentListResponse,
        path='studentList/{courseId}',
        http_method='POST',
        name='studentList')
    def studentList(self, request):
        return studentListMethod(request)

    @endpoints.method(
        AssignmentForm,
        Response,
        path='createAssignment',
        http_method='POST',
        name='createAssignment')
    def createAssignment(self, request):
        return createAssignmentMethod(request)

    @endpoints.method(
        ExamForm,
        Response,
        path='createExam',
        http_method='POST',
        name='createExam')
    def createExam(self, request):
        return createExamMethod(request)

    @endpoints.method(
        GetAssignmentRequest,
        GetAssignmentResponse,
        path='getAssignment',
        http_method='POST',
        name='getAssignment')
    def getAssignment(self, request):
        return getAssignmentMethod(request)

    @endpoints.method(
        GetExamRequest,
        GetExamResponse,
        path='getExam',
        http_method='POST',
        name='getExam')
    def getExam(self, request):
        return getExamMethod(request)

    @endpoints.method(
        NotesForm,
        Response,
        path='createNotes',
        http_method='POST',
        name='createNotes')
    def createNotes(self, request):
        return createNotesMethod(request)

    @endpoints.method(
        NoteBookRequest,
        NoteBookDetailResponse,
        path='getNoteBook',
        http_method='POST',
        name='getNoteBook')
    def getNoteBook(self, request):
        return getNoteBook(request)

    @endpoints.method(
        NoteBookListRequest,
        NoteBookListResponse,
        path='notebookList',
        http_method='POST',
        name='getNoteBookList')
    def getNoteBookList(self, request):
        return getNoteBookListMethod(request)

    @endpoints.method(
        RatingRequest,
        Response,
        path='rateThis',
        http_method='POST',
        name='rateThis')
    def rateThis(self, request):
        return rateThisMethod(request)

    @endpoints.method(
        CoursePageRequest,
        CoursePageResponse,
        path='coursePage',
        http_method='POST',
        name='coursePage')
    def coursePage(self, request):
        return coursePageMethod(request)

    @endpoints.method(
        CoursePageRequest,
        GetAssListResponse,
        path='assignmentList',
        http_method='POST',
        name='assignmentList')
    def assignmentList(self, request):
        return getAssignmentListMethod(request)

    @endpoints.method(
        CoursePageRequest,
        GetExamListResponse,
        path='examList',
        http_method='POST',
        name='examList')
    def examList(self, request):
        return getExamListMethod(request)

    @endpoints.method(
        BookmarkRequest,
        BookmarkResponse,
        path='bookmarkNoteBook',
        http_method='POST',
        name='bookmarkNoteBook')
    def bookmarkNoteBook(self, request):
        return bookmarkMethod(request)

    @endpoints.method(
        message_types.VoidMessage,
        message_types.VoidMessage,
        path='clearAll',
        http_method='GET',
        name='clearAll')
    def clearAll(self, request):
        clearAll()
        return message_types.VoidMessage()

    @endpoints.method(
        message_types.VoidMessage,
        CollegeListResponse,
        path='collegeList',
        http_method='GET',
        name='collegeList')
    def collegeList(self, request):
        return collegeListMethod(request)

    @endpoints.method(
        AddBranchRequest,
        message_types.VoidMessage,
        path='addBranch',
        http_method='POST',
        name='addBranch')
    def addBranch(self, request):
        addBranchMethod(request)
        return message_types.VoidMessage()

    @endpoints.method(
        DeleteRequest,
        Response,
        path='delete',
        http_method='POST',
        name='delete')
    def delete(self, request):
        return deleteMethod(request)

    @endpoints.method(
        SearchCourseRequest,
        CourseListResponse,
        path='searchCourse',
        http_method='POST',
        name='searchCourse')
    def searchCourse(self, request):
        return searchCourseMethod(request)

    @endpoints.method(
        SearchNBRequest,
        NoteBookListResponse,
        path='searchNotes',
        http_method='POST',
        name='searchNotes')
    def searchNotes(self, request):
        return searchNBMethod(request)

    @endpoints.method(
        message_types.VoidMessage,
        message_types.VoidMessage,
        path='runScript',
        http_method='GET',
        name='runScript')
    def runTestScript(self, request):
        runScript()
        return message_types.VoidMessage()
        
    """@endpoints.method(
        message_types.VoidMessage,
        message_types.VoidMessage,
        path='runExamScript',
        http_method='GET',
        name='runExamScript')
    def runExamScript(self, request):
        examScript()
        return message_types.VoidMessage()"""

apiLists = endpoints.api_server([NotesAPI])
