from models import CollegeForm, ProfileForm, CourseForm, Response
from models import AssignmentForm, ExamForm, NotesForm
from google.appengine.ext import ndb
from google.appengine.api import memcache


def editCollegeMethod(request):
    try:
        fields = CollegeForm.all_fields()
        collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
        college = collegeId.get()
        for field in fields:
            value = getattr(request, field.name, None)
            if value is None or value == "" or value == []:
                continue
            setattr(college, field.name, value)
        for courseId in college.courseIds:
            cacheVal = memcache.get(courseId.urlsafe())
            if cacheVal is not None:
                cacheVal[14] = college.collegeName
                memcache.set(courseId.urlsafe(), cacheVal)
        college.put()
        return Response(response=0, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editProfileMethod(request):
    try:
        fields = ProfileForm.all_fields()
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
        profile = profileId.get()
        for field in fields:
            value = getattr(request, field.name, None)
            if field.name == 'collegeId':
                continue
            if value is None or value == "" or value == []:
                continue
            setattr(profile, field.name, value)
        profile.put()
        return Response(response=0, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editCourseMethod(request):
    try:
        fields = CourseForm.all_fields()
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
        course = courseId.get()
        for field in fields:
            value = getattr(request, field.name, None)
            if field.name == 'collegeId' or field.name == 'profileId':
                continue
            if value is None or value == "" or value == []:
                continue
            setattr(course, field.name, value)
        for assignmentId in course.assignmentIds:
            cacheVal = memcache.get(assignmentId.urlsafe())
            if cacheVal is not None:
                cacheVal[7] = course.courseName
                memcache.set(assignmentId.urlsafe(), cacheVal)
        for examId in course.examIds:
            cacheVal = memcache.get(examId.urlsafe())
            if cacheVal is not None:
                cacheVal[7] = course.courseName
                memcache.set(examId.urlsafe(), cacheVal)
        memcache.delete(courseId.urlsafe())
        print course
        course.put()
        return Response(response=0, description="OK")
    except Exception, E:
        print str(E)
        return Response(response=1, description=str(E))


def editAssignmentMethod(self, request):
    try:
        fields = AssignmentForm.all_fields()
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
        assignment = assignmentId.get()
        for field in fields:
            value = getattr(request, field.name, None)
            if value is None or value == "" or value == []:
                continue
            setattr(assignment, field.name, value)
        cacheVal = memcache.get(assignmentId.urlsafe())
        if cacheVal is not None:
            cacheVal[0] = assignment.assignmentTitle
            cacheVal[1] = assignment.assignmentDesc
            cacheVal[4] = assignment.dueDate
            cacheVal[5] = assignment.dueTime
            cacheVal[6] = assignment.urlList
            memcache.set(assignmentId.urlsafe(), cacheVal)
        assignment.put()

        return Response(response=0, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editExamMethod(self, request):
    try:
        fields = ExamForm.all_fields()
        examId = ndb.Key(urlsafe=getattr(request, 'examId'))
        exam = examId.get()
        for field in fields:
            value = getattr(request, field.name, None)
            if value is None or value == "" or value == []:
                continue
            setattr(exam, field.name, value)
        cacheVal = memcache.get(examId.urlsafe())
        if cacheVal is not None:
            cacheVal[0] = exam.examTitle
            cacheVal[1] = exam.examDesc
            cacheVal[4] = exam.dueDate
            cacheVal[5] = exam.dueTime
            cacheVal[6] = exam.urlList
            memcache.set(examId.urlsafe(), cacheVal)
        exam.put()
        return Response(response=0, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editNotesMethod(request):
    try:
        fields = NotesForm.all_fields()
        notesId = ndb.Key(urlsafe=getattr(request, 'notesId'))
        notes = notesId.get()
        numUrls = len(getattr(request, 'urlList'))
        diff = numUrls - len(notes.urlList)
        for field in fields:
            value = getattr(request, field.name, None)
            if value is None or value == "" or value == []:
                continue
            setattr(notes, field.name, value)
        memcache.delete(notes.noteBookId.urlsafe())
        noteBook = notes.noteBookId.get()
        noteBook.pages += diff
        noteBook.put()
        notes.put()
        return Response(response=0, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))
