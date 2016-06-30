from models import CollegeForm, Response
from google.appengine.ext import ndb


def editCollegeMethod(request):
    fields = CollegeForm.all_fields()
    print fields
    return Response(response=1, description='Invalid collegeId' + str(E))