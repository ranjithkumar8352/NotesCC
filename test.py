import traceback

from apiclient.discovery import build


def main():
    apiRoot = 'https://uploadingtest-1344.appspot.com/_ah/api'
    api = 'notesapi'
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (apiRoot, api, version)
    service = build(api, version, discoveryServiceUrl=discovery_url)
    # service.clearAll().execute()
    # _______________________________________COLLEGE CREATION________________________________________
    collegeIdList = []
    collegeList = []
    collegeList.append({'abbreviation':'TC1', 'collegeName':'Test College 1', 'collegeType':'Test Type 1', 'location':'Test Location 1', 'semStartDate':'22-07-2016', 'semEndDate':'23-12:2016', 'branchNameList':['CSE', 'ECE', 'MECH']})
    collegeList.append({'abbreviation':'TC2', 'collegeName':'Test College 2', 'collegeType':'Test Type 2', 'location':'Test Location 2', 'semStartDate':'21-07-2016', 'semEndDate':'29-11-2016', 'branchNameList':['CSE', 'ECE', 'MECH']})
    collegeList.append({'abbreviation':'TC3', 'collegeName':'Test College 3', 'collegeType':'Test Type 3', 'location':'Test Location 3', 'semStartDate':'01-08-2016', 'semEndDate':'24-12-2016', 'branchNameList':['CSE', 'ECE', 'MECH']})
    collegeList.append({'abbreviation':'TC4', 'collegeName':'Test College 4', 'collegeType':'Test Type 4', 'location':'Test Location 4', 'semStartDate':'24-06-2016', 'semEndDate':'23-01-2016', 'branchNameList':['CSE', 'ECE', 'MECH']})
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
    profileList.append({'profileName':'Test Profile 1', 'collegeId':collegeIdList[0], 'email':'testemail1@gmail.com', 'gcmId':'2408', 'photoUrl':'https://yt3.ggpht.com/-hs9-C7jg9HY/AAAAAAAAAAI/AAAAAAAAAAA/pJg26_wdsQs/s100-c-k-no-rj-c0xffffff/photo.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    profileList.append({'profileName':'Test Profile 2', 'collegeId':collegeIdList[0], 'email':'testemail2@gmail.com', 'gcmId':'1710', 'photoUrl':'https://lh3.googleusercontent.com/-lAnmGukgwJ4/AAAAAAAAAAI/AAAAAAAAAAA/F8UwzppEz7k/photo.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    profileList.append({'profileName':'Test Profile 4', 'collegeId':collegeIdList[1], 'email':'testemail4@gmail.com', 'gcmId':'1310', 'photoUrl':'http://kingofwallpapers.com/boy/boy-025.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
    profileList.append({'profileName':'Test Profile 5', 'collegeId':collegeIdList[1], 'email':'testemail5@gmail.com', 'gcmId':'1410', 'photoUrl':'https://static.pexels.com/photos/6413/people-eyes-playing-young.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'})
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
    profileList.append({'profileName':'Test Profile 3', 'collegeId':collegeIdList[0], 'email':'testemail3@gmail.com', 'gcmId':'1110', 'photoUrl':'https://static.pexels.com/photos/7720/night-animal-dog-pet.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'ECE'})
    profileList.append({'profileName':'Test Profile 6', 'collegeId':collegeIdList[1], 'email':'testemail6@gmail.com', 'gcmId':'1420', 'photoUrl':'http://science-all.com/images/wallpapers/boy-pic/boy-pic-8.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'ECE'})
    # _______________________________________COURSE CREATION__________________________________________
    courseList = []
    courseIdList = []
    courseList.append({'courseName':'Test Course 1', 'courseCode':'TCourse1', 'professorName':'Test Professor 1', 'colour':'BLUE', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '2', '5'], 'startTime':['12:00', '13:00', '14:00'], 'endTime':['13:00', '14:00', '15:00'], 'profileId':profileIdList[1], 'collegeId':collegeIdList[0], 'elective':'1'})
    courseList.append({'courseName':'Test Course 2', 'courseCode':'TCourse2', 'professorName':'Test Professor 2', 'colour':'RED', 'batchNames':['2014'], 'branchNames':['ECE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '3', '5'], 'startTime':['12:00', '13:00', '14:00'], 'endTime':['13:00', '14:00', '15:00'], 'profileId':profileIdList[0], 'collegeId':collegeIdList[0], 'elective':'1'})
    courseList.append({'courseName':'Test Course 3', 'courseCode':'TCourse3', 'professorName':'Test Professor 3', 'colour':'YELLOW', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1','4'], 'startTime':['13:00', '14:00'], 'endTime':['14:00', '15:00'], 'profileId':profileIdList[1], 'collegeId':collegeIdList[0], 'elective':'0'})
    courseList.append({'courseName':'Test Course 4', 'courseCode':'TCourse4', 'professorName':'Test Professor 4', 'colour':'VIOLET', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '2', '5'], 'startTime':['12:00', '13:00', '14:00'], 'endTime':['13:00', '14:00', '15:00'], 'profileId':profileIdList[2], 'collegeId':collegeIdList[1], 'elective':'1'})
    courseList.append({'courseName':'Test Course 5', 'courseCode':'TCourse5', 'professorName':'Test Professor 5', 'colour':'GREEN', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '2', '5'], 'startTime':['12:00', '13:00', '14:00'], 'endTime':['13:00', '14:00', '15:00'], 'profileId':profileIdList[3], 'collegeId':collegeIdList[1], 'elective':'1'})
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
    # ___________________ADDING MORE PROFILES TO CHECK WHETHER AVAILABLE COURSES ARE STORED___________
    print "CREATING 2 MORE PROFILES..."
    for idx in [4, 5]:
        try:
            response = service.createProfile(body=profileList[idx]).execute()
            if response.get('response') == '0':
                profileIdList.append(response.get('key'))
            else:
                print response.get('description')
        except Exception as e:
            print e
            print traceback.print_exc()
    # ___________________ADDING NEW COURSES TO CHECK WORKING IF COURSES ARE CREATED LATER_____________
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    courseList.append({'courseName':'Test Course 6', 'courseCode':'TCourse6', 'professorName':'Test Professor 6', 'colour':'BROWN', 'batchNames':['2014'], 'branchNames':['CSE'], 'sectionNames':['A'], 'semester':'Odd', 'date':['1', '3', '5'], 'startTime':['12:00', '13:00', '14:00'], 'endTime':['13:00', '14:00', '15:00'], 'profileId':profileIdList[0], 'collegeId':collegeIdList[0], 'elective':'0'})
    print "CREATING 1 MORE COURSE..."
    try:
        response = service.addCourse(body=courseList[5]).execute()
        if response.get('response') == '0':
            courseIdList.append(response.get('key'))
        else:
            print response.get('description')
    except Exception as e:
        print e
        print traceback.print_exc()
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
    service.subscribeCourse(body={'profileId':profileIdList[0], 'courseIds':[courseIdList[0], courseIdList[2]]}).execute()
    service.subscribeCourse(body={'profileId':profileIdList[1], 'courseIds':[courseIdList[5]]}).execute()
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
    # _______________________________________DISPLAYING STUDENT LIST__________________________________
    print "STUDENT LIST"
    i = 1
    for courseId in courseIdList:
        response = service.studentList(courseId=courseId, body={'profileId':profileIdList[2]}).execute()
        print "COURSE ", i
        i += 1
        print response
        print "_______________________________________"
    print"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _______________________________________ADDING AS ADMIN_________________________________________
    print "ADDING ADMIN..."
    print service.addAdmin(courseId=courseIdList[5], body={'profileId': profileIdList[1]}).execute()
    print "COURSE STUDENT LIST..."
    print service.studentList(courseId=courseIdList[5], body={'profileId':profileIdList[5]}).execute()
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # ____________________________________CREATING NOTES_____________________________________________
    notesList = []
    noteBookIdList = []
    notesList.append({'classNumber':'1', 'courseId':courseIdList[0], 'date': '22:06:2016', 'notesDesc': 'NotesDescription1', 'profileId': profileIdList[0], 'title': 'Notes Title1', 'urlList':['http://tartarus.org/gareth/maths/Complex_Methods/rjs/cm1_q02vi.jpg', 'http://ds.nahoo.net/Academic/images/Pure3-Integration-Notes.gif', 'http://vle.woodhouse.ac.uk/topicdocs/maths/student%20work/S2%20summary%20notes%20for%20revision%20by%20Damini.jpg', 'http://img10.deviantart.net/cf6b/i/2010/277/8/d/math_notes_by_cptmcmuffinz-d303z7k.jpg']})
    notesList.append({'classNumber':'2', 'courseId':courseIdList[0], 'date': '24:06:2016', 'notesDesc': 'NotesDescription2', 'profileId': profileIdList[0], 'title': 'Notes Title2', 'urlList':['http://www.mathplane.com/yahoo_site_admin/assets/images/additional_derivatives_natural_logs.186145208_large.png', 'http://science.hyde.wikispaces.net/file/view/PolyVision_01_13_12_11_08_03.jpg/292006929/PolyVision_01_13_12_11_08_03.jpg', 'http://leah4sci.com/wp-content/uploads/2014/04/Carboxylic-Acid-Derivative-Study-Guide-Cheat-Sheet-by-Leah4sci.jpg']})
    notesList.append({'classNumber':'3', 'courseId':courseIdList[5], 'date': '21:06:2016', 'notesDesc': 'NotesDescription3', 'profileId': profileIdList[1], 'title': 'Notes Title3', 'urlList':['http://image.slidesharecdn.com/form4addmathsnote-140118081550-phpapp02/95/form-4-add-maths-note-6-638.jpg?cb=1390032984', 'http://image.slidesharecdn.com/basicbusinessmath-studynotes-131221043822-phpapp01/95/basic-business-math-study-notes-2-638.jpg?cb=1388105510', 'http://enlighteninglearnersweblog.com/blogs/media/blogs/b/1.gif']})
    notesList.append({"urlList": ["https://storage.googleapis.com/uploadnotes-2016/1.png",
                      "https://storage.googleapis.com/uploadnotes-2016/2.png",
                      "https://storage.googleapis.com/uploadnotes-2016/3.png",
                      "https://storage.googleapis.com/uploadnotes-2016/4.png",
                      "https://storage.googleapis.com/uploadnotes-2016/5.png",
                      "https://storage.googleapis.com/uploadnotes-2016/6.png",
                      "https://storage.googleapis.com/uploadnotes-2016/7.png"],
                      "classNumber": "3",
                      "courseId": courseIdList[0],
                      "date": "22-06-2016", "notesDesc": "TEST NOTES 4",
                      "profileId": profileIdList[0],
                      "title": "TEST NOTES 4"})
    print "CREATING NOTES..."
    for notes in notesList:
        response = service.createNotes(body=notes).execute()
        noteBookIdList.append(response.get('key'))
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "NOTEBOOK LIST BY upid..."
    print service.getNoteBookList(body={'upid':profileIdList[0]}).execute()
    print "NOTEBOOK LIST BY COURSE..."
    print service.getNoteBookList(body={'courseId':courseIdList[5]}).execute()
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # _____________________________________BOOKMARK NOTEBOOK__________________________________________
    """print "BOOKMARKING NOTEBOOK"
    service.bookmarkNoteBook(body={'profileId':profileIdList[1], 'noteBookId':noteBookIdList[0]}).execute()
    print "NOTEBOOK LIST BY bpid..."
    print service.getNoteBookList(body={'upid':profileIdList[0]}).execute()"""
    print "RATING NOTEBOOK"
    service.rateThis(body={'noteBookId': noteBookIdList[1], 'profileId':profileIdList[0], 'rating':4}).execute()
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # ____________________________________CREATING ASSIGNMENT_________________________________________
    assignmentList = []
    assignmentIdList = []
    assignmentList.append({'assignmentTitle': 'Test assignment 1', 'assignmentDesc':'ASSIGNMent Desc1', 'dueDate': '24-06-2016', 'dueTime': '12:00', 'urlList':['http://thinkswap.com/pdf_thumbnails/22706_maths_notes_2u.jpg?2','https://farm3.staticflickr.com/2929/13941904157_34b15196ea_o.jpg'], 'uploaderId':profileIdList[1], 'courseId': courseIdList[5]})
    assignmentList.append({'assignmentTitle': 'Test assignment 2', 'assignmentDesc':'ASSIGNMent Desc2', 'dueDate': '25-06-2016', 'dueTime': '12:00', 'urlList':['http://1.bp.blogspot.com/-jUULRomYuaI/UUTNRj_UxkI/AAAAAAAABtE/gSNzNqI7Ep4/s1600/010+graphs.jpg', 'http://3.bp.blogspot.com/-1y2JBBZFNVs/UQkRNsmAlYI/AAAAAAAAAnw/AwU0eIqt3uM/s1600/CHAP+4+P01.jpg'], 'uploaderId':profileIdList[0], 'courseId': courseIdList[0]})
    print "CREATING ASSIGNMENT..."
    for assignment in assignmentList:
        response = service.createAssignment(body=assignment).execute()
        assignmentIdList.append(response.get('key'))
    print "DISPLAY FEED..."
    response = service.feed(profileId=profileIdList[0]).execute()
    print response.get('subscribedCourseList')
    response = service.feed(profileId=profileIdList[1]).execute()
    print response.get('subscribedCourseList')
    print "ASSIGNMENT LIST..."
    response = service.assignmentList(body={'courseId':courseIdList[0]}).execute()
    print response  
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    examList = []
    examIdList = []
    examList.append({'uploaderId': profileIdList[1], 'courseId': courseIdList[5], 'examTitle': 'Exam 1', 'examDesc':'Exam Description 1', 'dueDate': '22-07-2016', 'dueTime':'00:00', 'urlList':['http://missschmucker.weebly.com/uploads/3/0/7/9/30797277/log_notes_2.jpg', 'http://www.crystalight.com.sg/wp-content/uploads/2014/09/NB-109-PVC-Exe-Log-Book-notes.jpg', 'http://iblog.dearbornschools.org/aliahms/wp-content/uploads/sites/1468/2016/02/prince-and-pauper-cornell-notes-scene.jpg']})
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[0], 'examTitle': 'Exam 2', 'examDesc':'Exam Description 2', 'dueDate': '23-07-2016', 'dueTime':'00:00', 'urlList':['http://2.bp.blogspot.com/-AT5gDWRGIIU/UvIPt6jOWhI/AAAAAAAAAt4/meRkpX0dbRU/s1600/Picture20.png', 'http://3.bp.blogspot.com/-FFS8S_3tfuc/TaxT-VPTZPI/AAAAAAAABps/SoXbO7aQs0Y/s1600/httpserverinstall.jpg']})
    print "CREATING TEST..."
    for exam in examList:
        response = service.createExam(body=exam).execute()
        examIdList.append(response.get('key'))
    print "DISPLAY FEED..."
    response = service.feed(profileId=profileIdList[0]).execute()
    print response.get('subscribedCourseList')
    response = service.feed(profileId=profileIdList[1]).execute()
    print response.get('subscribedCourseList')
    print "ASSIGNMENT LIST..."
    response = service.examList(body={'courseId':courseIdList[0]}).execute()
    print response  
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    profileList.append({"batchName": "2014", "branchName": "CSE",
                        "collegeId": "ahJzfnVwbG9hZG5vdGVzLTIwMTZyFAsSB0NvbGxlZ2UYgICAgOui3ggM",
                        "email": "testemail7@gmail.com", "gcmId": "2222",
                        "photoUrl": "www.nasa.gov/sites/default/files/styles/image_card_4x3_ratio/public/thumbnails/image/idcs1426.jpg",
                        "profileName": "TEST PROFILE 7", "sectionName": "A"})
    response = service.courseList(page=1, body=profileList[6]).execute()
    print response
    print "_______________________________________"

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
