from models import CollegeForm, ProfileForm, CourseForm, Response
from models import AssignmentForm, ExamForm
from google.appengine.ext import ndb


def editCollegeMethod(request):
    try:
        fields = CollegeForm.all_fields()
        collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
        college = collegeId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "" or value == []:
                continue
            setattr(college, field.name, value)
        college.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editProfileMethod(request):
    try:
        fields = ProfileForm.all_fields()
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
        profile = profileId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "" or value == []:
                continue
            setattr(profile, field.name, value)
        profile.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editCourseMethod(request):
    try:
        fields = CourseForm.all_fields()
        courseId = ndb.Key(urlsafe=getattr(request, 'courseId'))
        course = courseId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "" or value == []:
                continue
            setattr(course, field.name, value)
        course.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editAssignmentMethod(self, request):
    try:
        fields = AssignmentForm.all_fields()
        assignmentId = ndb.Key(urlsafe=getattr(request, 'assignmentId'))
        assignment = assignmentId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "" or value == []:
                continue
            setattr(assignment, field.name, value)
        assignment.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editExamMethod(self, request):
    try:
        fields = ExamForm.all_fields()
        examId = ndb.Key(urlsafe=getattr(request, 'examId'))
        exam = examId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "" or value == []:
                continue
            setattr(exam, field.name, value)
        exam.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))
