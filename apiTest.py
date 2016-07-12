mimport urllib2
from config import PROJECT_URL
# PROJECT_URL = 'http://localhost:8080'
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


def runScript():
    collegeList.append({'abbreviation': 'LNMIIT', 'collegeName': 'The LNM Institute of Information Technology',
                        'collegeType': 'Engineering', 'location': 'Jaipur', 'semStartDate': '23-07-2016',
                        'semEndDate': '23-12: 2016', 'branchNameList': ['CSE', 'ECE', 'MME', 'CCE']})
    collegeList.append({'abbreviation': 'BITS', 'collegeName': 'Birla Institute of Technology',
                        'collegeType': 'Engineering', 'location': 'Pilani', 'semStartDate': '24-07-2016',
                        'semEndDate': '29-11-2016', 'branchNameList': ['CSE', 'ECE', 'MECH', 'IT']})
    collegeList.append({'abbreviation': 'NIT-K', 'collegeName': 'National Institute of Technology',
                        'collegeType': 'Engineering', 'location': 'Suratkal', 'semStartDate': '01-08-2016',
                        'semEndDate': '24-12-2016', 'branchNameList': ['CSE', 'CHEM', 'MECH']})
    collegeList.append({'abbreviation': 'IIIT-H', 'collegeName': 'International Institute of Information Technology',
                        'collegeType': 'Engineering', 'location': 'Hyderabad', 'semStartDate': '24-06-2016',
                        'semEndDate': '23-01-2016', 'branchNameList': ['CSE', 'CHEM', 'ECE']})
    collegeList.append({'abbreviation': 'IIT-K', 'collegeName': 'Indian Institute of Technology',
                        'collegeType': 'Engineering', 'location': 'Kanpur', 'semStartDate': '24-07-2016',
                        'semEndDate': '23-01-2016', 'branchNameList': ['CSE', 'CHEM', 'ECE', 'CIVIL']})
    url = PROJECT_URL + "/_ah/api/notesapi/v1/createCollege"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for i in range(5):
        req = urllib2.Request(url, json.dumps(collegeList[i]), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        key = response.get('key')
        collegeIdList.append(key)
        print key

    profileList.append({'profileName': 'Saurav Mehrotra', 'collegeId': collegeIdList[0],
                        'email': 'mehrotra.saurav@gmail.com', 'gcmId': '2408',
                        'photoUrl': 'https: //yt3.ggpht.com/-hs9-C7jg9HY/AAAAAAAAAAI/AAAAAAAAAAA/pJg26_wdsQs/s100-c-k-no-rj-c0xffffff/photo.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'CSE'})
    profileList.append({'profileName': 'Shikhar Mangla', 'collegeId': collegeIdList[0],
                        'email': 'manglashikhar@gmail.com', 'gcmId': '2111',
                        'photoUrl': 'https: //media.licdn.com/mpr/mpr/shrinknp_200_200/AAEAAQAAAAAAAAW8AAAAJDRlZGU3ZmQ4LTgzOTQtNDE2OC1iNTc1LTYyNGZkYzQ0MDc1Mg.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'ECE'})
    profileList.append({'profileName': 'Shruti Sharma', 'collegeId': collegeIdList[0],
                        'email': 'shrutishrm@gmail.com', 'gcmId': '1710',
                        'photoUrl': 'https: //storage.googleapis.com/uploadingtest-2016.appspot.com/2.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'CSE'})
    profileList.append({'profileName': 'Vanshita Tilwani', 'collegeId': collegeIdList[0],
                        'email': 'cutevanshi@gmail.com', 'gcmId': '2309',
                        'photoUrl': 'https: //lh6.googleusercontent.com/-Pb7PYfgobyE/AAAAAAAAAAI/AAAAAAAADTo/EOL9vnlYI00/photo.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'CCE'})
    profileList.append({'profileName': 'Kanuj Prem Arora', 'collegeId': collegeIdList[0],
                        'email': 'kanuj96@gmail.com', 'gcmId': '1111',
                        'photoUrl': 'https: //yt3.ggpht.com/-7YYHiAsNhS0/AAAAAAAAAAI/AAAAAAAAAAA/6N1YAkYoMEk/s900-c-k-no-rj-c0xffffff/photo.jpg',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'CSE'})
    profileList.append({'profileName': 'Shivam Gupta', 'collegeId': collegeIdList[0],
                        'email': 'shivamgpt@gmail.com', 'gcmId': '2319',
                        'photoUrl': 'http: //www.desportivos.lnmiit.ac.in/images/team/shivamgupta.png',
                        'sectionName': 'A', 'batchName': '2014', 'branchName': 'CSE'})

    url = PROJECT_URL + "/_ah/api/notesapi/v1/createProfile"
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

    courseList.append({'courseName': 'DATA STRUCTURE', 'courseCode': 'DS', 'professorName': 'Rajbeer Kaur',
                       'colour': '#ee5451', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2', '3'], 'startTime': ['10: 00', '11: 00', '12: 00'],
                       'endTime': ['11: 00', '12: 00', '13: 00'], 'profileId': profileIdList[0],
                       'collegeId': collegeIdList[0], 'elective': '0'})
    courseList.append({'courseName': 'MATHS', 'courseCode': 'M1', 'professorName': 'Ajit Patel', 'colour': '#e47373',
                       'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'], 'semester': 'Odd',
                       'date': ['2', '3', '4'], 'startTime': ['12: 00', '13: 00', '14: 00'],
                       'endTime': ['13: 00', '14: 00', '15: 00'], 'profileId': profileIdList[0],
                       'collegeId': collegeIdList[0], 'elective': '0'})
    courseList.append({'courseName': 'Optimization Techniques', 'courseCode': 'OT', 'professorName': 'Manish Garg',
                       'colour': '#ed999a', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '3', '5'], 'startTime': ['11: 00', '14: 00', '09: 00'],
                       'endTime': ['13: 00', '15: 00', '10: 00'], 'profileId': profileIdList[2],
                       'collegeId': collegeIdList[0], 'elective': '1'})
    courseList.append({'courseName': 'MICRO ECONOMICS', 'courseCode': 'ECO', 'professorName': 'Surinder Nehra',
                       'colour': '#80cac3', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['1', '2'], 'startTime': ['13: 00', '14: 00'],
                       'endTime': ['14: 00', '15: 00'], 'profileId': profileIdList[1], 'collegeId': collegeIdList[0],
                       'elective': '0'})
    courseList.append({'courseName': 'INTRODUCTION TO C', 'courseCode': 'ITC', 'professorName': 'Preety Singh',
                       'colour': '#4cb5ab', 'batchNames': ['2014'], 'branchNames': ['CSE'], 'sectionNames': ['A'],
                       'semester': 'Odd', 'date': ['3', '4', '5'], 'startTime': ['15: 00', '15: 00', '12: 00'],
                       'endTime': ['16: 00', '16: 00', '13: 00'], 'profileId': profileIdList[2],
                       'collegeId': collegeIdList[0], 'elective': '0'})
    url = PROJECT_URL + "/_ah/api/notesapi/v1/addCourse"
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    for i in range(5):
        req = urllib2.Request(url, json.dumps(courseList[i]), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        key = response.get('key')
        courseIdList.append(key)
        print key

    notesList.append({'courseId': courseIdList[0], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[2], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[2], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction',
                      'profileId': profileIdList[3], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm',
                      'profileId': profileIdList[3], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[5], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[5], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})

    notesList.append({'courseId': courseIdList[1], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[2], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[2], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction',
                      'profileId': profileIdList[3], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm',
                      'profileId': profileIdList[3], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[5], 'title': 'Algorithms',
                      'urlList':['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                 'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[1], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[5], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})

    notesList.append({'courseId': courseIdList[2], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[2], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[2], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction',
                      'profileId': profileIdList[3], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm',
                      'profileId': profileIdList[3], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[5], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[2], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[5], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})

    notesList.append({'courseId': courseIdList[3], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[2], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[2], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction',
                      'profileId': profileIdList[3], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm',
                      'profileId': profileIdList[3], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[5], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[3], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[5], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})

    notesList.append({'courseId': courseIdList[4], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[0], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[2], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[2], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '01/07/2016', 'notesDesc': 'Kruskal Algorithm Introduction',
                      'profileId': profileIdList[3], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/13.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/14.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '03/07/2016', 'notesDesc': 'Examples to Kruskal algorithm',
                      'profileId': profileIdList[3], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '22/06/2016', 'notesDesc': 'Minimum Spanning Trees',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/1.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/2.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/3.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '24/06/2016', 'notesDesc': 'Minimum Spanning Trees cont.',
                      'profileId': profileIdList[4], 'title': 'MST',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/4.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/5.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/6.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '26/06/2016', 'notesDesc': 'Prims Algorithm Introduction',
                      'profileId': profileIdList[5], 'title': 'Algorithms',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/8.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/9.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/10.png']})
    notesList.append({'courseId': courseIdList[4], 'date': '28/06/2016', 'notesDesc': 'Examples to prim algorithm',
                      'profileId': profileIdList[5], 'title': 'Algorithm',
                      'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/11.png',
                                  'https://storage.googleapis.com/uploadingtest-2016.appspot.com/12.png']})
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = PROJECT_URL + "/_ah/api/notesapi/v1/createNotes"
    for data in notesList:
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        else:
            if response.get('key') is not None:
                noteBookIdList.append(response.get('key'))

    assignmentList.append({
        'assignmentTitle': 'Assignment 1', 'assignmentDesc': 'This assignment consists of 2 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'],
        'uploaderId': profileIdList[0], 'courseId': courseIdList[0]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 2', 'assignmentDesc': 'This assignment consists of 3 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'],
        'uploaderId': profileIdList[2], 'courseId': courseIdList[0]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 1', 'assignmentDesc': 'This assignment consists of 2 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'],
        'uploaderId': profileIdList[0], 'courseId': courseIdList[1]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 2', 'assignmentDesc': 'This assignment consists of 3 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'],
        'uploaderId': profileIdList[2], 'courseId': courseIdList[1]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 1', 'assignmentDesc': 'This assignment consists of 2 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'],
        'uploaderId': profileIdList[0], 'courseId': courseIdList[2]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 2', 'assignmentDesc': 'This assignment consists of 3 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'],
        'uploaderId': profileIdList[2], 'courseId': courseIdList[2]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 1', 'assignmentDesc': 'This assignment consists of 2 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'],
        'uploaderId': profileIdList[0], 'courseId': courseIdList[3]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 2', 'assignmentDesc': 'This assignment consists of 3 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'],
        'uploaderId': profileIdList[2], 'courseId': courseIdList[3]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 1', 'assignmentDesc': 'This assignment consists of 2 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png'],
        'uploaderId': profileIdList[0], 'courseId': courseIdList[4]})
    assignmentList.append({
        'assignmentTitle': 'Assignment 2', 'assignmentDesc': 'This assignment consists of 3 pages with each',
        'dueDate': '05-07-2016', 'dueTime': '12:00',
        'urlList': [
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/16.png',
            'https://storage.googleapis.com/uploadingtest-2016.appspot.com/17.png'],
        'uploaderId': profileIdList[2], 'courseId': courseIdList[4]})
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = PROJECT_URL + "/_ah/api/notesapi/v1/createAssignment"
    for data in assignmentList:
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        else:
            if response.get('key') is not None:
                assignmentIdList.append(response.get('key'))

    examList.append({
        'uploaderId': profileIdList[0], 'courseId': courseIdList[0], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[2], 'courseId': courseIdList[0], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[0], 'courseId': courseIdList[1], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[2], 'courseId': courseIdList[1], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[0], 'courseId': courseIdList[2], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[2], 'courseId': courseIdList[2], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[0], 'courseId': courseIdList[3], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[2], 'courseId': courseIdList[3], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[0], 'courseId': courseIdList[4], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    examList.append({
        'uploaderId': profileIdList[2], 'courseId': courseIdList[4], 'examTitle': 'Mid Term Exam',
        'examDesc': 'The paper will be of 50 marks', 'dueDate': '10-07-2016', 'dueTime': '10:00',
        'urlList': ['https://storage.googleapis.com/uploadingtest-2016.appspot.com/15.png']})
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    url = PROJECT_URL + "/_ah/api/notesapi/v1/createExam"
    for data in examList:
        req = urllib2.Request(url, json.dumps(data), header)
        response = urllib2.urlopen(req)
        response = json.loads(response.read())
        if response.get('response') != '0':
            print response
        else:
            if response.get('key') is not None:
                examIdList.append(response.get('key'))
