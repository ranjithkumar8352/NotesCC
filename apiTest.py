import urllib2
import json


projectId = 'uploadnotes-2016.appspot.com'
collegeList = []
collegeIdList = []
profileList = []
courseList = []
courseIdList = []
profileIdList = []
notesList = []
noteBookIdList = []
assignmentList = []
assignmentIdList = []
examList = []
examIdList = []


def createCollegeList():
    collegeList.append({'abbreviation': 'TC1', 'collegeName': 'Test College 1', 'collegeType': 'Test Type 1',
                        'location': 'Test Location 1', 'semStartDate': '22-07-2016', 'semEndDate': '23-12:2016',
                        'branchNameList': ['CSE', 'ECE', 'MECH']})
    collegeList.append({'abbreviation': 'TC2', 'collegeName': 'Test College 2', 'collegeType': 'Test Type 2',
                        'location': 'Test Location 2', 'semStartDate': '21-07-2016', 'semEndDate': '29-11-2016',
                        'branchNameList': ['CSE', 'ECE']})
    collegeList.append({'abbreviation': 'TC3', 'collegeName': 'Test College 3', 'collegeType': 'Test Type 3',
                        'location': 'Test Location 3', 'semStartDate': '01-08-2016', 'semEndDate': '24-12-2016',
                        'branchNameList': ['CSE', 'ECE', 'MECH']})
    collegeList.append({'abbreviation': 'TC4', 'collegeName': 'Test College 4', 'collegeType': 'Test Type 4',
                        'location': 'Test Location 4', 'semStartDate': '24-06-2016', 'semEndDate': '23-01-2016',
                        'branchNameList': ['CSE', 'ECE', 'MECH']})


def createProfileList():
    profileList.append({'profileName': 'Test Profile 1', 'collegeId': collegeIdList[0], 'email': 'testemail1@gmail.com',
                        'gcmId': '2408', 'sectionName': 'A', 'batchName': '2014', 'branchName': ' CSE',
                        'photoUrl': 'https://s-media-cache-ak0.pinimg.com/avatars/shrutishrm512_1451826368_140.jpeg'
                        })
    profileList.append({'profileName': 'Test Profile 2', 'collegeId': collegeIdList[0], 'email': 'testemail2@gmail.com',
                        'gcmId': '1710', 'sectionName': 'A', 'batchName': '2014', 'branchName': 'CSE',
                        'photoUrl': 'http://cdn.wonderfulengineering.com/wp-content/uploads/2016/01/cool-wallpaper-3.jpg'})
    profileList.append({'profileName': 'Test Profile 4', 'collegeId': collegeIdList[1], 'email': 'testemail4@gmail.com',
                        'photoUrl': 'http://kingofwallpapers.com/boy/boy-025.jpg', 'sectionName': 'A', 'batchName': '2014',
                        'branchName': 'CSE', 'gcmId': '1310'})
    profileList.append({'profileName': 'Test Profile 5', 'collegeId': collegeIdList[1], 'email': 'testemail5@gmail.com',
                        'gcmId': '1410', 'photoUrl': 'https://static.pexels.com/photos/6413/people-eyes-playing-young.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'CSE'})
    profileList.append({'profileName': 'Test Profile 3', 'collegeId': collegeIdList[0], 'email': 'testemail3@gmail.com',
                        'gcmId': '1110', 'photoUrl': 'https://static.pexels.com/photos/7720/night-animal-dog-pet.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'ECE'})
    profileList.append({'profileName': 'Test Profile 6', 'collegeId': collegeIdList[1], 'email': 'testemail6@gmail.com',
                        'gcmId': '1420', 'photoUrl': 'http://science-all.com/images/wallpapers/boy-pic/boy-pic-8.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'ECE'})


def createCourseList():
    courseList.append({'courseName': 'Test Course 1', 'courseCode': 'TCourse1', 'professorName': 'Test Professor 1',
                       'colour': '#ee5451', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[1],
                       'collegeId': collegeIdList[0], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 2', 'courseCode': 'TCourse2', 'professorName': 'Test Professor 2',
                       'colour': '#e47373', 'batchNames': ['2014'], 'branchNames': ['ECE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '3', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[0],
                       'collegeId': collegeIdList[0], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 3', 'courseCode': 'TCourse3', 'professorName': 'Test Professor 3',
                       'colour': '#ed999a', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '4'], 'startTime': ['13: 00', '14: 00'],
                       'endTime': ['14: 00', '15: 00'], 'profileId': profileIdList[1],
                       'collegeId': collegeIdList[0], 'elective': '0'})
    courseList.append({'courseName': 'Test Course 4', 'courseCode': 'TCourse4', 'professorName': 'Test Professor 4',
                       'colour': '#80cac3', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[2],
                       'collegeId': collegeIdList[1], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 5', 'courseCode': 'TCourse5', 'professorName': 'Test Professor 5',
                       'colour': '#4cb5ab', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[3],
                       'collegeId': collegeIdList[1], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 6', 'courseCode': 'TCourse6', 'professorName': 'Test Professor 6',
                       'colour': '#25a599', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '3', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[0],
                       'collegeId': collegeIdList[0], 'elective': '0'})


def createNoteList():
    notesList.append({'courseId': courseIdList[0], 'date': '22:06:2016', 'notesDesc': 'NotesDescription1',
                      'profileId': profileIdList[0], 'title': 'Notes Title1',
                      'urlList': ['http://tartarus.org/gareth/maths/Complex_Methods/rjs/cm1_q02vi.jpg',
                                  'http://dronstudy.com/wp-content/uploads/2015/01/Exercise-2.1_opt_02.jpg',
                                  'http://vle.woodhouse.ac.uk/topicdocs/maths/`%20work/S2%20summary%20notes%20for%20revision%20by%20Damini.jpg',
                                  'http://img10.deviantart.net/cf6b/i/2010/277/8/d/math_notes_by_cptmcmuffinz-d303z7k.jpg']})
    notesList.append({'courseId': courseIdList[0], 'date': '24:06:2016', 'notesDesc': 'NotesDescription2',
                      'profileId': profileIdList[0], 'title': 'Notes Title2',
                      'urlList': ['http://www.mathplane.com/yahoo_site_admin/assets/images/additional_derivatives_natural_logs.186145208_large.png',
                                  'http://science.hyde.wikispaces.net/file/view/PolyVision_01_13_12_11_08_03.jpg/292006929/PolyVision_01_13_12_11_08_03.jpg',
                                  'http://leah4sci.com/wp-content/uploads/2014/04/Carboxylic-Acid-Derivative-Study-Guide-Cheat-Sheet-by-Leah4sci.jpg']})
    notesList.append({'courseId': courseIdList[5], 'date': '21:06:2016', 'notesDesc': 'NotesDescription3',
                      'profileId': profileIdList[1], 'title': 'Notes Title3',
                      'urlList': ['http://image.slidesharecdn.com/form4addmathsnote-140118081550-phpapp02/95/form-4-add-maths-note-6-638.jpg?cb=1390032984',
                                  'http://image.slidesharecdn.com/basicbusinessmath-studynotes-131221043822-phpapp01/95/basic-business-math-study-notes-2-638.jpg?cb=1388105510',
                                  'http://dronstudy.com/wp-content/uploads/2015/01/7117.jpg']})


def createAssignmentList():
    assignmentList.append({'assignmentTitle': 'Test assignment 1', 'assignmentDesc': 'ASSIGNMent Desc1',
                           'dueDate': '24-06-2016', 'dueTime': '12: 00',
                           'urlList': ['http: //thinkswap.com/pdf_thumbnails/22706_maths_notes_2u.jpg?2',
                                       'https: //farm3.staticflickr.com/2929/13941904157_34b15196ea_o.jpg'],
                           'uploaderId': profileIdList[1], 'courseId': courseIdList[5]})
    assignmentList.append({'assignmentTitle': 'Test assignment 2', 'assignmentDesc': 'ASSIGNMent Desc2',
                           'dueDate': '25-06-2016', 'dueTime': '12: 00',
                           'urlList': ['http: //1.bp.blogspot.com/-jUULRomYuaI/UUTNRj_UxkI/AAAAAAAABtE/gSNzNqI7Ep4/s1600/010+graphs.jpg',
                                       'http: //3.bp.blogspot.com/-1y2JBBZFNVs/UQkRNsmAlYI/AAAAAAAAAnw/AwU0eIqt3uM/s1600/CHAP+4+P01.jpg'],
                           'uploaderId': profileIdList[0], 'courseId': courseIdList[0]})


def createExamList():
    examList.append({'uploaderId': profileIdList[1], 'courseId': courseIdList[5],
                     'examTitle': 'Exam 1', 'examDesc': 'Exam Description 1',
                     'dueDate': '22-07-2016', 'dueTime': '00:00',
                     'urlList': ['http://missschmucker.weebly.com/uploads/3/0/7/9/30797277/log_notes_2.jpg',
                                 'http://www.crystalight.com.sg/wp-content/uploads/2014/09/NB-109-PVC-Exe-Log-Book-notes.jpg',
                                 'http://iblog.dearbornschools.org/aliahms/wp-content/uploads/sites/1468/2016/02/prince-and-pauper-cornell-notes-scene.jpg']})
    examList.append({'uploaderId': profileIdList[0], 'courseId': courseIdList[0],
                     'examTitle': 'Exam 2', 'examDesc': 'Exam Description 2',
                     'dueDate': '23-07-2016', 'dueTime': '00:00',
                     'urlList': ['http://2.bp.blogspot.com/-AT5gDWRGIIU/UvIPt6jOWhI/AAAAAAAAAt4/meRkpX0dbRU/s1600/Picture20.png',
                                 'http://3.bp.blogspot.com/-FFS8S_3tfuc/TaxT-VPTZPI/AAAAAAAABps/SoXbO7aQs0Y/s1600/httpserverinstall.jpg']})


def createCollege():
    createCollegeList()
    url = "https://" + projectId + "/_ah/api/notesapi/v1/createCollege"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for i in range(4):
        req = urllib2.Request(url, json.dumps(collegeList[i]), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        key = response.get('key')
        collegeIdList.append(key)
        print key
    url = "https://" + projectId + "/_ah/api/notesapi/v1/collegeList"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    clist = response.get('collegeList')
    for c in clist:
        if c.get('collegeName') == 'Test College 1':
            if c.get('branchNames') != ['CSE', 'ECE', 'MECH']:
                print "BUG IN createCollege API/ collegeList API. Test College 1"
        if c.get('collegeName') == 'Test College 2':
            if c.get('branchNames') != ['CSE', 'ECE']:
                print "BUG IN createCollege API/ collegeList API. Test College 2"
        if c.get('collegeName') == 'Test College 3':
            if c.get('branchNames') != ['CSE', 'ECE', 'MECH']:
                print "BUG IN createCollege API/ collegeList API. Test College 3"
        if c.get('collegeName') == 'Test College 4':
            if c.get('branchNames') != ['CSE', 'ECE', 'MECH']:
                print "BUG IN createCollege API/ collegeList API. Test College 4"


def createProfile():
    createProfileList()
    url = "https://" + projectId + "/_ah/api/notesapi/v1/createProfile"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for i in range(6):
        req = urllib2.Request(url, json.dumps(profileList[i]), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        key = response.get('key')
        profileIdList.append(key)
        print key


def createCourse():
    createCourseList()
    url = "https://" + projectId + "/_ah/api/notesapi/v1/addCourse"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for i in range(6):
        req = urllib2.Request(url, json.dumps(courseList[i]), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        key = response.get('key')
        courseIdList.append(key)
        print key


def addBranch():
    url = "https://" + projectId + "/_ah/api/notesapi/v1/addBranch"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'branchName': 'CIVIL', 'collegeId': collegeIdList[1]}
    req = urllib2.Request(url, json.dumps(data), header)
    response = urllib2.urlopen(req)
    url = "https://" + projectId + "/_ah/api/notesapi/v1/collegeList"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    clist = response.get('collegeList')
    for c in clist:
        if c.get('collegeName') == 'Test College 1':
            if c.get('branchNames') != ['CSE', 'ECE', 'MECH']:
                print "BUG IN createCollege API/ collegeList API. Test College 1"
        if c.get('collegeName') == 'Test College 2':
            if c.get('branchNames') != ['CSE', 'ECE', 'CIVIL']:
                print "BUG IN createCollege API/ collegeList API. Test College 2"
        if c.get('collegeName') == 'Test College 3':
            if c.get('branchNames') != ['CSE', 'ECE', 'MECH']:
                print "BUG IN createCollege API/ collegeList API. Test College 3"
        if c.get('collegeName') == 'Test College 4':
            if c.get('branchNames') != ['CSE', 'ECE', 'MECH']:
                print "BUG IN createCollege API/ collegeList API. Test College 4"


def addAdmin():
    url = "https://" + projectId + "/_ah/api/notesapi/v1/addAdmin/" + courseIdList[0]
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'profileId': profileIdList[5]}
    req = urllib2.Request(url, json.dumps(data), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    if response.get('response') != '0':
        print response


def courseListMethod():
    url = "https://" + projectId + "/_ah/api/notesapi/v1/courseList/1"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for id in profileIdList:
        data = {'profileId': id}
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response


def coursePage():
    url = "https://" + projectId + "/_ah/api/notesapi/v1/coursePage/"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for pid in profileIdList:
        for cid in courseIdList:
            data = {'profileId': pid, 'courseId': cid}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            if response.get('response') != '0':
                print response


def subscribeCourseList():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/subscribeCourse/"
    data = {'profileId': profileIdList[0], 'courseIds': [courseIdList[0], courseIdList[2]]}
    req = urllib2.Request(url, json.dumps(data), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    if response.get('response') != '0':
        print response
    data = {'profileId': profileIdList[1], 'courseIds': [courseIdList[5]]}
    req = urllib2.Request(url, json.dumps(data), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    if response.get('response') != '0':
        print response
    data = {'profileId': profileIdList[5], 'courseIds': [courseIdList[0]]}
    req = urllib2.Request(url, json.dumps(data), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    if response.get('response') != '0':
        print response


def feed():
    for pid in profileIdList:
        url = "https://" + projectId + "/_ah/api/notesapi/v1/feed/" + pid
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response


def createNotes():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/createNotes"
    for data in notesList:
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        else:
            if response.get('key') is not None:
                noteBookIdList.append(response.get('key'))


def createAssignment():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/createAssignment"
    for data in assignmentList:
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        else:
            if response.get('key') is not None:
                assignmentIdList.append(response.get('key'))


def createExam():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/createExam"
    for data in examList:
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        else:
            if response.get('key') is not None:
                examIdList.append(response.get('key'))


def assignmentListAPI():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/assignmentList"
    for courseId in courseIdList:
        req = urllib2.Request(url, json.dumps({'courseId': courseId}), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response


def examListAPI():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/examList"
    for courseId in courseIdList:
        req = urllib2.Request(url, json.dumps({'courseId': courseId}), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response


def noteBookListAPI():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/notebookList"
    for courseId in courseIdList:
        req = urllib2.Request(url, json.dumps({'courseId': courseId}), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
    for field in ['bpid', 'upid', 'profileId']:
        for value in profileIdList:
            req = urllib2.Request(url, json.dumps({field: value}), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            if response.get('response') != '0':
                print response


def bookmarkNoteBook():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/bookmarkNoteBook"
    req = urllib2.Request(url, json.dumps({'noteBookId': noteBookIdList[0],
                                           'profileId': profileIdList[1]}), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    if response.get('response') != '0':
        print response


def rateThis(rating):
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = "https://" + projectId + "/_ah/api/notesapi/v1/rateThis"
    req = urllib2.Request(url, json.dumps({'noteBookId': noteBookIdList[0],
                                           'profileId': profileIdList[1],
                                           'rating': rating}), header)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    if response.get('response') != '0':
        print response


def studentList():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for courseId in courseIdList:
        for profileId in profileIdList:
            url = "https://" + projectId + "/_ah/api/notesapi/v1/studentList/" + courseId
            req = urllib2.Request(url, json.dumps({'profileId': profileIdList[1]}), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            if response.get('response') != '0':
                print response


def getNoteBookAPI():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for noteBookId in noteBookIdList:
        for profileId in profileIdList:
            url = "https://" + projectId + "/_ah/api/notesapi/v1/getNoteBook"
            req = urllib2.Request(url, json.dumps({'profileId': profileIdList[1],
                                                   'noteBookId': noteBookId}), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            if response.get('response') != '0':
                print response


def getExamAPI():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for examId in examIdList:
        for profileId in profileIdList:
            url = "https://" + projectId + "/_ah/api/notesapi/v1/getExam"
            req = urllib2.Request(url, json.dumps({'profileId': profileIdList[1],
                                                   'examId': examId}), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            if response.get('response') != '0':
                print response


def getAssignmentAPI():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for assignmentId in assignmentIdList:
        for profileId in profileIdList:
            url = "https://" + projectId + "/_ah/api/notesapi/v1/getAssignment"
            req = urllib2.Request(url, json.dumps({'profileId': profileIdList[1],
                                                   'assignmentId': assignmentId}), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            if response.get('response') != '0':
                print response


def runScript():
    createCollege()
    createProfile()
    createCourse()
    addBranch()
    addAdmin()
    #courseListMethod()
    #coursePage()
    #feed()
    subscribeCourseList()
    createNoteList()
    createNotes()
    createAssignmentList()
    createAssignment()
    createExamList()
    createExam()
    #feed()
    #assignmentListAPI()
    #examListAPI()
    #noteBookListAPI()
    #bookmarkNoteBook()
    #coursePage()
    rateThis(4)
    #studentList()
    #getNoteBookAPI()
    #getAssignmentAPI()
    #getExamAPI()
    print collegeIdList
    print profileIdList
    print courseIdList
    print noteBookIdList
    print assignmentIdList
    print examIdList

