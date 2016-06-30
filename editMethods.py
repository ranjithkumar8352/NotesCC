from models import CollegeForm, ProfileForm, Response
from google.appengine.ext import ndb


def editCollegeMethod(request):
    try:
        fields = CollegeForm.all_fields()
        collegeId = ndb.Key(urlsafe=getattr(request, 'collegeId'))
        college = collegeId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "":
                continue
            setattr(college, field.name, value)
        college.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))


def editProfileMethod(request):
    try:
        fields = ProfileForm.add_fields()
        profileId = ndb.Key(urlsafe=getattr(request, 'profileId'))
        profile = profileId.get()
        for field in fields:
            value = getattr(request, field.name)
            if value is None or value == "":
                continue
            setattr(profile, field.name, value)
        profile.put()
        return Response(response=1, description="OK")
    except Exception, E:
        return Response(response=1, description=str(E))
