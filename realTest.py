import traceback

from config import PROJECT_URL
from apiclient.discovery import build


def main():
    apiRoot = PROJECT_URL + '/_ah/api'
    # apiRoot = 'http://localhost:8080' + '/_ah/api'
    api = 'notesapi'
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (apiRoot, api, version)
    service = build(api, version, discoveryServiceUrl=discovery_url)
    # _______________________________________COLLEGE CREATION________________________________________
    collegeIdList = []
    collegeList = []
    collegeList.append({'abbreviation':'LNMIIT', 'collegeName':'The LNM Institute of Information Technology', 'collegeType':'Engineering', 'location':'Jaipur', 'semStartDate':'23-07-2016', 'semEndDate':'23-12:2016', 'branchNameList':['CSE', 'ECE', 'MME', 'CCE']})
    collegeList.append({'abbreviation':'BITS', 'collegeName':'Birla Institute of Technology', 'collegeType':'Engineering', 'location':'Pilani', 'semStartDate':'24-07-2016', 'semEndDate':'29-11-2016', 'branchNameList':['CSE', 'ECE', 'MECH', 'IT']})
    collegeList.append({'abbreviation':'NIT-K', 'collegeName':'National Institute of Technology', 'collegeType':'Engineering', 'location':'Suratkal', 'semStartDate':'01-08-2016', 'semEndDate':'24-12-2016', 'branchNameList':['CSE', 'CHEM', 'MECH']})
    collegeList.append({'abbreviation':'IIIT-H', 'collegeName':'International Institute of Information Technology', 'collegeType':'Engineering', 'location':'Hyderabad', 'semStartDate':'24-06-2016', 'semEndDate':'23-01-2016', 'branchNameList':['CSE', 'CHEM', 'ECE']})
    collegeList.append({'abbreviation':'IIT-K', 'collegeName':'Indian Institute of Technology', 'collegeType':'Engineering', 'location':'Kanpur', 'semStartDate':'24-07-2016', 'semEndDate':'23-01-2016', 'branchNameList':['CSE', 'CHEM', 'ECE', 'CIVIL']})
    print "CREATING COLLEGES ..."
    for collegeInfo in collegeList:
        try:
            response = service.createCollege(body=collegeInfo).execute()
            if response.get('response') == '0':
                collegeIdList.append(response.get('key'))
            else:
                print response.get('description')
        except Exception as e:
            print e
            print traceback.print_exc()
    print collegeIdList 
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # _______________________________________PROFILE CREATION_________________________________________
    profileIdList = []
    profileList = []
    profileList.append({'profileName':'Saurav Mehrotra', 'collegeId':collegeIdList[0], 'email':'mehrotra.saurav@gmail.com', 'gcmId':'2408', 'photoUrl':'https://yt3.ggpht.com/-hs9-C7jg9HY/AAAAAAAAAAI/AAAAAAAAAAA/pJg26_wdsQs/s100-c-k-no-rj-c0xffffff/photo.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    profileList.append({'profileName':'Shikhar Mangla', 'collegeId':collegeIdList[0], 'email':'manglashikhar@gmail.com', 'gcmId':'2111', 'photoUrl':'https://media.licdn.com/mpr/mpr/shrinknp_200_200/AAEAAQAAAAAAAAW8AAAAJDRlZGU3ZmQ4LTgzOTQtNDE2OC1iNTc1LTYyNGZkYzQ0MDc1Mg.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'ECE'})
    profileList.append({'profileName':'Shruti Sharma', 'collegeId':collegeIdList[0], 'email':'shrutishrm@gmail.com', 'gcmId':'1710', 'photoUrl':'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    profileList.append({'profileName':'Vanshita Tilwani', 'collegeId':collegeIdList[0], 'email':'cutevanshi@gmail.com', 'gcmId':'2309', 'photoUrl':'https://lh6.googleusercontent.com/-Pb7PYfgobyE/AAAAAAAAAAI/AAAAAAAADTo/EOL9vnlYI00/photo.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CCE'})
    profileList.append({'profileName':'Kanuj Prem Arora', 'collegeId':collegeIdList[0], 'email':'kanuj96@gmail.com', 'gcmId':'1111', 'photoUrl':'https://yt3.ggpht.com/-7YYHiAsNhS0/AAAAAAAAAAI/AAAAAAAAAAA/6N1YAkYoMEk/s900-c-k-no-rj-c0xffffff/photo.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    profileList.append({'profileName':'Shivam Gupta', 'collegeId':collegeIdList[0], 'email':'shivamgpt@gmail.com', 'gcmId':'2319', 'photoUrl':'http://www.desportivos.lnmiit.ac.in/images/team/shivamgupta.png', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    print "CREATING PROFILES..."
    for profileInfo in profileList:
        try:
            response = service.createProfile(body=profileInfo).execute()
            if response.get('response') == '0':
                profileIdList.append(response.get('key'))
            else:
                print response.get('description')
        except Exception as e:
            print e
            print traceback.print_exc()
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _______________________________________COURSE CREATION__________________________________________
    courseList = []
    courseIdList = []
    courseList.append({'courseName':'DATA STRUCTURE', 'courseCode':'DS', 'professorName':'Rajbeer Kaur', 'colour':'#ee5451', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '2', '3'], 'startTime':['10:00', '11:00', '12:00'], 'endTime':['11:00', '12:00', '13:00'], 'profileId':profileIdList[0], 'collegeId':collegeIdList[0], 'elective':'0'})
    courseList.append({'courseName':'MATHS', 'courseCode':'M1', 'professorName':'Ajit Patel', 'colour':'#e47373', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['2', '3', '4'], 'startTime':['12:00', '13:00', '14:00'], 'endTime':['13:00', '14:00', '15:00'], 'profileId':profileIdList[0], 'collegeId':collegeIdList[0], 'elective':'0'})
    courseList.append({'courseName':'Optimization Techniques', 'courseCode':'OT', 'professorName':'Manish Garg', 'colour':'#ed999a', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1','3', '5'], 'startTime':['11:00', '14:00', '09:00'], 'endTime':['13:00', '15:00', '10:00'], 'profileId':profileIdList[2], 'collegeId':collegeIdList[0], 'elective':'1'})
    courseList.append({'courseName':'MICRO ECONOMICS', 'courseCode':'ECO', 'professorName':'Surinder Nehra', 'colour':'#80cac3', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '2'], 'startTime':['13:00', '14:00'], 'endTime':['14:00', '15:00'], 'profileId':profileIdList[1], 'collegeId':collegeIdList[0], 'elective':'0'})
    courseList.append({'courseName':'INTRODUCTION TO C', 'courseCode':'ITC', 'professorName':'Preety Singh', 'colour':'#4cb5ab', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['3', '4', '5'], 'startTime':['15:00', '15:00', '12:00'], 'endTime':['16:00', '16:00', '13:00'], 'profileId':profileIdList[2], 'collegeId':collegeIdList[0], 'elective':'0'})
    print "CREATING COURSES..."
    for courseInfo in courseList:
        try:
            response = service.addCourse(body=courseInfo).execute()
            if response.get('response') == '0':
                courseIdList.append(response.get('key'))
            else:
                print response.get('description')
        except Exception as e:
            print e
            print traceback.print_exc()
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _____________________________________AVAILABLE COURSE LIST______________________________________
    print "DISPLAYING AVAILABLE COURSES"
    i = 1
    for profileId in profileIdList:
        body = {'profileId': profileId}
        print "PROFILE ", i
        i = i+1
        response = service.courseList(page=1, body=body).execute()
        print response
        print "_______________________________________"
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # ______________________________________DISPLAYING FEED___________________________________________
    print "DISPLAYING FEED..."
    i = 1
    for profileId in profileIdList:
        body = {'profileId': profileId}
        print "PROFILE ", i
        i = i+1
        response = service.feed(profileId=profileId).execute()
        print response
        print "_______________________________________"
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _______________________________________SUBSCRIBING TO COURSES___________________________________
    print "SUBSCRIBING COURSES..."
    service.subscribeCourse(body={'profileId':profileIdList[0], 'courseIds':[courseIdList[2], courseIdList[3], courseIdList[4]]}).execute()
    service.subscribeCourse(body={'profileId':profileIdList[1], 'courseIds':[courseIdList[2]]}).execute()
    service.subscribeCourse(body={'profileId':profileIdList[2], 'courseIds':[courseIdList[0], courseIdList[1], courseIdList[3]]}).execute()
    service.subscribeCourse(body={'profileId':profileIdList[3], 'courseIds':[courseIdList[0], courseIdList[1], courseIdList[3]]}).execute()
    service.subscribeCourse(body={'profileId':profileIdList[4], 'courseIds':[courseIdList[0], courseIdList[1], courseIdList[2], courseIdList[3], courseIdList[4]]}).execute()
    service.subscribeCourse(body={'profileId':profileIdList[5], 'courseIds':[courseIdList[0], courseIdList[1], courseIdList[2], courseIdList[3], courseIdList[4]]}).execute()
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _______________________________________DISPLAYING FEED__________________________________________
    print "DISPLAYING FEED..."
    i = 1
    for profileId in profileIdList:
        body = {'profileId': profileId}
        print "PROFILE ", i
        i = i+1
        response = service.feed(profileId=profileId).execute()
        print response
        print "_______________________________________"
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # ____________________________________CREATING NOTES_____________________________________________
    notesList = []
    noteBookIdList = []
    notesList.append({'courseId':courseIdList[0], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[2], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[2], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction', 'profileId': profileIdList[3], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm', 'profileId': profileIdList[3], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[5], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[5], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})


    notesList.append({'courseId':courseIdList[1], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[2], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[2], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction', 'profileId': profileIdList[3], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm', 'profileId': profileIdList[3], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[5], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[1], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[5], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})


    notesList.append({'courseId':courseIdList[2], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[2], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[2], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction', 'profileId': profileIdList[3], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm', 'profileId': profileIdList[3], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[5], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[2], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[5], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})


    notesList.append({'courseId':courseIdList[3], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[2], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[2], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction', 'profileId': profileIdList[3], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm', 'profileId': profileIdList[3], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[5], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[3], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[5], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})


    notesList.append({'courseId':courseIdList[4], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[0], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[2], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[2], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction', 'profileId': profileIdList[3], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm', 'profileId': profileIdList[3], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees continued', 'profileId': profileIdList[4], 'title': 'MST', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction', 'profileId': profileIdList[5], 'title': 'Algorithms', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId':courseIdList[4], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm', 'profileId': profileIdList[5], 'title': 'Algorithm', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})


    
    print "CREATING NOTES..."
    for notes in notesList:
        response = service.createNotes(body=notes).execute()
        print response
        noteBookIdList.append(response.get('key'))
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #print "NOTEBOOK LIST BY upid..."
    #print service.getNoteBookList(body={'upid':profileIdList[0]}).execute()
    #print "NOTEBOOK LIST BY COURSE..."
    #print service.getNoteBookList(body={'courseId':courseIdList[5]}).execute()
    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _____________________________________BOOKMARK NOTEBOOK__________________________________________
    """print "BOOKMARKING NOTEBOOK"
    service.bookmarkNoteBook(body={'profileId':profileIdList[1], 'noteBookId':noteBookIdList[0]}).execute()
    print "NOTEBOOK LIST BY bpid..."
    print service.getNoteBookList(body={'upid':profileIdList[0]}).execute()"""
    #print "RATING NOTEBOOK"
    #print noteBookIdList
    #service.rateThis(body={'noteBookId': noteBookIdList[1], 'profileId':profileIdList[0], 'rating':4}).execute()
    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # ____________________________________CREATING ASSIGNMENT_________________________________________
    assignmentList = []
    assignmentIdList = []
    assignmentList.append({'assignmentTitle': 'Assignment 1', 'assignmentDesc':'This assignment consists of 2 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'], 'uploaderId':profileIdList[0], 'courseId': courseIdList[0]})
    assignmentList.append({'assignmentTitle': 'Assignment 2', 'assignmentDesc':'This assignment consists of 3 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'], 'uploaderId':profileIdList[2], 'courseId': courseIdList[0]})
    assignmentList.append({'assignmentTitle': 'Assignment 1', 'assignmentDesc':'This assignment consists of 2 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'], 'uploaderId':profileIdList[0], 'courseId': courseIdList[1]})
    assignmentList.append({'assignmentTitle': 'Assignment 2', 'assignmentDesc':'This assignment consists of 3 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'], 'uploaderId':profileIdList[2], 'courseId': courseIdList[1]})
    assignmentList.append({'assignmentTitle': 'Assignment 1', 'assignmentDesc':'This assignment consists of 2 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'], 'uploaderId':profileIdList[0], 'courseId': courseIdList[2]})
    assignmentList.append({'assignmentTitle': 'Assignment 2', 'assignmentDesc':'This assignment consists of 3 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'], 'uploaderId':profileIdList[2], 'courseId': courseIdList[2]})
    assignmentList.append({'assignmentTitle': 'Assignment 1', 'assignmentDesc':'This assignment consists of 2 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'], 'uploaderId':profileIdList[0], 'courseId': courseIdList[3]})
    assignmentList.append({'assignmentTitle': 'Assignment 2', 'assignmentDesc':'This assignment consists of 3 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'], 'uploaderId':profileIdList[2], 'courseId': courseIdList[3]})
    assignmentList.append({'assignmentTitle': 'Assignment 1', 'assignmentDesc':'This assignment consists of 2 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'], 'uploaderId':profileIdList[0], 'courseId': courseIdList[4]})
    assignmentList.append({'assignmentTitle': 'Assignment 2', 'assignmentDesc':'This assignment consists of 3 pages with each', 'dueDate': '05-07-2016', 'dueTime': '12:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png', 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'], 'uploaderId':profileIdList[2], 'courseId': courseIdList[4]})
    print "CREATING ASSIGNMENT..."
    for assignment in assignmentList:
        response = service.createAssignment(body=assignment).execute()
        assignmentIdList.append(response.get('key'))
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    examList = []
    examIdList = []
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[0], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[2], 'courseId': courseIdList[0], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[1], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[2], 'courseId': courseIdList[1], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[2], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[2], 'courseId': courseIdList[2], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[3], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[2], 'courseId': courseIdList[3], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[4], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({'uploaderId': profileIdList[2], 'courseId': courseIdList[4], 'examTitle': 'Mid Term Exam', 'examDesc':'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime':'10:00', 'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    print "CREATING TEST..."
    for exam in examList:
        response = service.createExam(body=exam).execute()
        examIdList.append(response.get('key'))

    print "collegeId"
    print collegeIdList
    print " "
    print "profileId"
    print profileIdList
    print " "
    print "courseId"
    print courseIdList
    print " "
    print "NoteBookId"
    print noteBookIdList
    print " "
    print "AssignmentId"
    print assignmentIdList
    print " "
    print "examId"
    print examIdList
    print " "

    """for assignmentId in assignmentIdList:
        service.delete(body={'assignmentId': assignmentId}).execute()
    for examId in examIdList:
        service.delete(body={'examId': examId}).execute()
    for noteBookId in noteBookIdList:
        service.delete(body={'noteBookId': noteBookId}).execute()
    for courseId in courseIdList:
        service.delete(body={'courseId': courseId}).execute()
    for profileId in profileIdList:
        service.delete(body={'profileId': profileId}).execute()
    for collegeId in collegeIdList:
        service.delete(body={'collegeId': collegeId}).execute()"""
main()
