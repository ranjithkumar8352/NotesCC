from models import CourseListResponse, CourseResponse

from google.appengine.api import search
from google.appengine.ext import ndb


def createCourseDoc(request, key):
    courseName = getattr(request, 'courseName')
    professorName = getattr(request, 'professorName')
    courseCode = getattr(request, 'courseCode')
    # semester = getattr(request, 'semester')
    # branchNames = getattr(request, 'branchNames')
    # batchNames = getattr(request, 'batchNames')
    # sectionNames = getattr(request, 'sectionNames')
    # branchNames = branchNames.join(' ')
    # sectionNames = sectionNames.join(' ')
    # batchNames = batchNames.join(' ')
    document = search.Document(
        fields=[
            search.TextField(name='courseName', value=courseName),
            search.TextField(name='professorName', value=professorName),
            search.TextField(name='courseCode', value=courseCode),
            search.TextField(name='key', value=key)
            # search.TextField(name='semester', value=semester),
            # search.TextField(name='branchNames', value=branchNames),
            # search.TextField(name='batchNames', value=batchNames),
            # search.TextField(name='sectionNames', value=sectionNames)
        ])
    search.Index(name='Course').put(document)


def searchCourseMethod(request):
    index = search.Index(name='Course')
    searchString = getattr(request, 'searchString', None)
    if searchString:
        queryString = searchString.split(' ')
        if '' in queryString:
            queryString.remove('')
        queryString = ' AND '.join(queryString)
    print queryString
    results = index.search(queryString)
    courseList = []
    for doc in results:
        key = doc.field('key').value
        courseId = ndb.Key(urlsafe=key)
        course = courseId.get()
        courseResponse = CourseResponse(courseId=key, courseName=course.courseName,
                                        batchNames=course.batchNames, branchNames=course.branchNames,
                                        sectionNames=course.sectionNames, studentCount=len(course.studentIds),
                                        professorName=course.professorName, notesCount=len(course.noteBookIds),
                                        semester=course.semester)
        courseList.append(courseResponse)
    return CourseListResponse(response=0, description='OK', courseList=courseList, completed=1)
