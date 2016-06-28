import urllib2
import json


projectId = 'uploadingtest-1344.appspot.com'
collegeList = []
collegeIdList = []
profileList = []
courseList = []
courseIdList = []
profileIdList = []


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
                       'colour': 'BLUE', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[1],
                       'collegeId': collegeIdList[0], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 2', 'courseCode': 'TCourse2', 'professorName': 'Test Professor 2',
                       'colour': 'RED', 'batchNames': ['2014'], 'branchNames': ['ECE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '3', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[0],
                       'collegeId': collegeIdList[0], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 3', 'courseCode': 'TCourse3', 'professorName': 'Test Professor 3',
                       'colour': 'YELLOW', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '4'], 'startTime': ['13: 00', '14: 00'],
                       'endTime': ['14: 00', '15: 00'], 'profileId': profileIdList[1],
                       'collegeId': collegeIdList[0], 'elective': '0'})
    courseList.append({'courseName': 'Test Course 4', 'courseCode': 'TCourse4', 'professorName': 'Test Professor 4',
                       'colour': 'VIOLET', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[2],
                       'collegeId': collegeIdList[1], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 5', 'courseCode': 'TCourse5', 'professorName': 'Test Professor 5',
                       'colour': 'GREEN', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[3],
                       'collegeId': collegeIdList[1], 'elective': '1'})
    courseList.append({'courseName': 'Test Course 6', 'courseCode': 'TCourse6', 'professorName': 'Test Professor 6',
                       'colour': 'BROWN', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '3', '5'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[0],
                       'collegeId': collegeIdList[0], 'elective': '0'})


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
        if c.get('collegeName') == 'Test College 2':
            if 'CIVIL' not in c.get('branchNames'):
                print "Add Branch NOT WORKING"


def addAdmin():
    url = "https://" + projectId + "/_ah/api/notesapi/v1/addAdmin/" + courseIdList[0]
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'profileId': profileIdList[1]}
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


def feed():
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for pid in profileIdList:
        url = "https://" + projectId + "/_ah/api/notesapi/v1/feed/" + pid
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response


def main():
    createCollege()
    createProfile()
    createCourse()
    addBranch()
    addAdmin()
    courseListMethod()
    coursePage()
    feed()
    subscribeCourseList()


main()
