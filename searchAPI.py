from models import CourseListResponse, CourseResponse, NoteBookResponse, NoteBookListResponse

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
        doc_id=key,
        fields=[
            search.TextField(name='courseName', value=courseName),
            search.TextField(name='professorName', value=professorName),
            search.TextField(name='courseCode', value=courseCode)
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
        results = index.search(queryString)
    else:
        results = index.search("")
    courseList = []
    for doc in results:
        key = doc.doc_id
        print key
        courseId = ndb.Key(urlsafe=key)
        print courseId
        course = courseId.get()
        print course
        if course is None:
            continue
        courseResponse = CourseResponse(courseId=key, courseName=course.courseName,
                                        batchNames=course.batchNames, branchNames=course.branchNames,
                                        sectionNames=course.sectionNames, studentCount=len(course.studentIds),
                                        professorName=course.professorName, notesCount=len(course.noteBookIds),
                                        semester=course.semester, colour=course.colour,
                                        elective=course.elective)
        courseList.append(courseResponse)
    if len(courseList) == 0:
        return CourseListResponse(response=1, description="NOTHING")
    return CourseListResponse(response=0, description='OK', courseList=courseList, completed=1)


def createNBDoc(title, desc, date, uploaderName, key):
    # if noteBook already exists
    index = search.Index('NoteBook')
    existingDoc = index.get(key)
    noteBookId = ndb.Key(urlsafe=key)
    noteBook = noteBookId.get()
    course = noteBook.courseId.get()
    if existingDoc:
        newDesc = existingDoc.fields[1].value
        newDesc += desc
        newTitle = existingDoc.fields[0].value
        newTitle += title
        document = search.Document(
            doc_id=key,
            fields=[
                search.TextField(name='title', value=newTitle),
                search.TextField(name='desc', value=newDesc),
                search.TextField(name='date', value=date),
                search.TextField(name='courseName', value=course.courseName),
                search.TextField(name='uploaderName', value=uploaderName)
            ])
    else:
        document = search.Document(
            doc_id=key,
            fields=[
                search.TextField(name='title', value=title),
                search.TextField(name='desc', value=desc),
                search.TextField(name='date', value=date),
                search.TextField(name='courseName', value=course.courseName)
                search.TextField(name='uploaderName', value=uploaderName)
            ])
    index.put(document)


def searchNBMethod(request):
    index = search.Index('NoteBook')
    searchString = getattr(request, 'searchString')
    if searchString:
        queryString = searchString.split(' ')
        if '' in queryString:
            queryString.remove('')
        queryString = ' AND '.join(queryString)
        results = index.search(queryString)
    else:
        results = index.search("")
    noteBookList = []
    for doc in results:
        key = doc.doc_id
        noteBookId = ndb.Key(urlsafe=key)
        noteBook = noteBookId.get()
        if noteBook is None:
            continue
        uploader = noteBook.uploaderId.get()
        courseName = doc.field('courseName').value
        pages = 0
        for notesId in noteBook.notesIds:
            notes = notesId.get()
            pages += len(notes.urlList)
        noteBookList.append(NoteBookResponse(noteBookId=key, courseName=courseName, uploaderName=uploader.profileName,
                                             pages=pages, totalRating=noteBook.totalRating,
                                             views=noteBook.views,
                                             frequency=noteBook.frequency, lastUpdated=noteBook.lastUpdated))
    if len(noteBookList) == 0:
        return NoteBookListResponse(response=1, description="NOTHING")
    return NoteBookListResponse(response=0, noteBookList=noteBookList, description='OK')
