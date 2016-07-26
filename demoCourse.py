import traceback

from config import PROJECT_URL
from apiclient.discovery import build


def test():
	apiRoot = PROJECT_URL + '/_ah/api'
   	# apiRoot = 'http://localhost:8080' + '/_ah/api'
   	api = 'notesapi'
	version = 'v1'
	discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (apiRoot, api, version)
	service = build(api, version, discoveryServiceUrl=discovery_url)
	collegeIdList = ['ahJzfnVwbG9hZG5vdGVzLTIwMTZyFAsSB0NvbGxlZ2UYgICAwKCApQoM']
	profileList = [{'profileName': 'Ranjith kumar', 'collegeId': collegeIdList[0], 'email':'ranjith@campusconnect.cc', 'gcmId':'2319',
	    'photoUrl':'https://lh4.googleusercontent.com/-NBieJIeIn0s/AAAAAAAAAAI/AAAAAAAAAks/sqeMBjMxpPI/s96-c/photo.jpg', 'sectionName':'A', 'batchName':'2014', 'branchName':'CSE'}]
	profileIdList = ['ahJzfnVwbG9hZG5vdGVzLTIwMTZyFAsSB1Byb2ZpbGUYgICAwPj29gsM','ahJzfnVwbG9hZG5vdGVzLTIwMTZyFAsSB1Byb2ZpbGUYgICAgP3f3AsM','ahJzfnVwbG9hZG5vdGVzLTIwMTZyFAsSB1Byb2ZpbGUYgICAgPCFyQoM','ahJzfnVwbG9hZG5vdGVzLTIwMTZyFAsSB1Byb2ZpbGUYgICAgNTB9wgM']
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

	courseList = [{'courseName': 'Demo Course', 'courseCode': 'DMC', 'professorName': 'Ranjith kumar', 'colour': '#4cb5ab', 'batchNames': ['2014'], 'branchNames':['CSE'], 'sectionNames':[
	    'A'], 'semester':'Odd', 'date':['3', '4', '5'], 'startTime':['15:00', '15:00', '12:00'], 'endTime':['16:00', '16:00', '13:00'], 'profileId':profileIdList[0], 'collegeId':collegeIdList[0], 'elective':'0'}]
	courseIdList = []
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

	notesList = []
	noteBookIdList = []
	notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples of surveying', 'profileId': profileIdList[0], 'title': 'Surveying - 1', 'urlList':['https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:01:26.242370.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:03:11.826720.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:05:11.597220.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:06:00.565970.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:06:54.280550.jpg']})
	notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples of surveying - part 2', 'profileId': profileIdList[1], 'title': 'Surveying - 2', 'urlList':['https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:07:44.984010.jpg', 'https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:08:08.144730.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:08:31.610860.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:08:52.834920.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:09:43.787030.jpg']})
	notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples of surveying - part 3', 'profileId': profileIdList[2], 'title': 'Surveying - 3', 'urlList':['https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:10:11.910010.jpg', 'https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:10:44.228190.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:11:14.265110.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:11:48.651940.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:12:14.430140.jpg']})
	notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples of surveying - part 4', 'profileId': profileIdList[3], 'title': 'Surveying - 4', 'urlList':['https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:12:55.521800.jpg', 'https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:13:35.860370.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:14:11.537480.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:15:00.858670.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:15:21.568040.jpg']})
	notesList.append({'courseId':courseIdList[0], 'date': '28/06/2016', 'notesDesc': 'Examples of surveying - part 5', 'profileId': profileIdList[4], 'title': 'Surveying - 5', 'urlList':['https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:15:50.191550.jpg', 'https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:16:21.905490.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:16:54.656770.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:17:19.883760.jpg','https://storage.googleapis.com/uploadnotes-2016.appspot.com/demo/demo/2016-07-2513:17:43.056640.jpg']})

	print "CREATING NOTES..."
	for notes in notesList:
		response = service.createNotes(body=notes).execute()
		print response
		noteBookIdList.append(response.get('key'))
	print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


test()
