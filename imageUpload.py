import webapp2
import urllib2
import json
import cloudstorage as gcs
import datetime
from config import PROJECT_URL, BUCKET_NAME


class ProfilePicUpload(webapp2.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        try:
            profileId = self.request.get('profileId')
        except Exception, E:
            print "profileId Missing in request\n" + self.request + '\n' + str(E)
            return self.response.write("profileId Missing in request\n" + self.request + '\n' + str(E))
        file = self.request.POST.get('file')
        bucketName = BUCKET_NAME
        fileName = bucketName + '/ProfilePic/' + profileId + '.jpg'
        gcsFile = gcs.open(fileName, mode='w', content_type='image/jpeg',
                           options={'x-goog-acl': 'public-read'})
        gcsFile.write(file.value)
        url = 'https://storage.googleapis.com' + fileName
        gcsFile.close()
        obj = {
            'response': 0,
            'url': str(url)
        }
        self.response.out.write(json.dumps(obj))

    def get(self):
        self.response.out.write("""<form method="POST" enctype="multipart/form-data">
                                    <input type="file" name="file">
                                    <input type="text" name="profileId">
                                    <input type="submit" name="submit">
                                   </form>""")


class ImageUploadAndroid(webapp2.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        flag = 0
        print self.request.POST
        try:
            urlList = []
            try:
                fileList = self.request.POST.getall('file')
            except Exception, E:
                print "file Missing in request\n"+self.request+'\n'+str(E)
                return self.response.write("file Missing in request\n"+self.request+'\n'+str(E))
            try:
                profileId = self.request.get('profileId')
            except Exception, E:
                print "profileId Missing in request\n"+self.request+'\n'+str(E)
                return self.response.write("profileId Missing in request\n"+self.request+'\n'+str(E))
            try:
                courseId = self.request.get('courseId')
            except Exception, E:
                print "courseId Missing in request\n"+self.request+'\n'+str(E)
                return self.response.write("courseId Missing in request\n"+self.request+'\n'+str(E))
            try:
                title = self.request.get('title')
            except Exception, E:
                print "title Missing in request\n"+self.request+'\n'+str(E)
                return self.response.write("title Missing in request\n"+self.request+'\n'+str(E))
            try:
                desc = self.request.get('desc')
            except Exception, E:
                print "desc Missing in request\n"+self.request+'\n'+str(E)
                return self.response.write("desc Missing in request\n"+self.request+'\n'+str(E))
            print "Number of files to be uploaded" + str(len(fileList))
            try:
                type = self.request.get('type')
            except Exception, E:
                print "type Missing in request\n"+self.request+'\n'+str(E)
                return self.response.write("type Missing in request\n"+self.request+'\n'+str(E))
            bucketName = BUCKET_NAME
            if len(fileList)==0:
                urlList.append("http://guiaquebueno.com/Images/Restaurantes/Restaurante_no_image.jpg")
            try:
                for file in fileList:
                    timestamp = "".join(str(datetime.datetime.now()).split())
                    fileName = bucketName + '/' + courseId + '/' + profileId + '/' + timestamp + '.jpg'
                    gcsFile = gcs.open(fileName, mode='w', content_type='image/jpeg',
                                       options={'x-goog-acl': 'public-read'})
                    gcsFile.write(file.value)
                    url = 'https://storage.googleapis.com' + fileName
                    urlList.append(url)
                    gcsFile.close()
            except Exception, E:
                if str(E) == "'unicode' object has no attribute 'value'":
                    print "0 image\n"+self.request
                    urlList.append("http://guiaquebueno.com/Images/Restaurantes/Restaurante_no_image.jpg")
                else:
                    print "Upload Failed!!!\n"+self.request + '\n' + str(E)
                    return self.response.write("UPLOAD FAILED\nRequest\n" + self.request + '\n' + str(E))
            if type == 'notes':
                try:
                    date = self.request.get('date')
                except Exception, E:
                    print "date Missing from request\n" + self.request + '\n'+str(E)
                    return self.response.write("date Missing from request\n"+self.request+'\n'+str(E))
                url = PROJECT_URL + "/_ah/api/notesapi/v1/createNotes"
                data = {'profileId': profileId, 'courseId': courseId, 'title': title, 'notesDesc': desc,
                        'urlList': urlList, 'date': date}
                header = {'Content-Type': 'application/json; charset=UTF-8'}
                flag = 1
                req = urllib2.Request(url, json.dumps(data), header)
                flag = 2
                response = urllib2.urlopen(req)
                response = json.loads(response.read())
                key = response.get('key')
                self.response.headers['Content-Type'] = 'application/json'
                obj = {
                    'response': 0,
                    'noteBookId': str(key)
                }
                self.response.out.write(json.dumps(obj))
            if type == 'assignment':
                try:
                    dueDate = self.request.get('dueDate')
                except Exception, E:
                    print "dueDate Missing from request\n" + self.request + '\n' + str(E)
                    self.response.write("dueDate Missing from request\n" + self.request + '\n' + str(E))
                try:
                    dueTime = self.request.get('dueTime')
                except:
                    print "dueTime Missing from request\n" + self.request+'\n'+str(E)
                    self.response.write("dueTime Missing from request\n" + self.request+'\n'+str(E))
                url = PROJECT_URL + "/_ah/api/notesapi/v1/createAssignment"
                data = {'uploaderId': profileId, 'courseId': courseId, 'assignmentTitle': title, 'assignmentDesc': desc,
                        'urlList': urlList, 'dueDate': dueDate, 'dueTime': dueTime}
                header = {'Content-Type': 'application/json; charset=UTF-8'}
                req = urllib2.Request(url, json.dumps(data), header)
                response = urllib2.urlopen(req)
                response = json.loads(response.read())
                key = response.get('key')
                self.response.headers['Content-Type'] = 'application/json'   
                obj = {
                    'response': 0,
                    'assignmentId': str(key)
                  } 
                self.response.out.write(json.dumps(obj))
            if type == 'exam':
                try:
                    dueDate = self.request.get('dueDate')
                except Exception, E:
                    print "dueDate Missing from request\n" + self.request+'\n'+str(E)
                    self.response.write("dueDate Missing from request\n" + self.request+'\n'+str(E))
                try:
                    dueTime = self.request.get('dueTime')
                except Exception, E:
                    print "dueTime Missing from request\n" + self.request+'\n'+str(E)
                    self.response.write("dueTime Missing from request\n" + self.request+'\n'+str(E))
                url = PROJECT_URL + "/_ah/api/notesapi/v1/createExam"
                data = {'uploaderId': profileId, 'courseId': courseId, 'examTitle': title, 'examDesc': desc,
                        'urlList': urlList, 'dueDate': dueDate, 'dueTime': dueTime}
                header = {'Content-Type': 'application/json; charset=UTF-8'}
                req = urllib2.Request(url, json.dumps(data), header)
                response = urllib2.urlopen(req)
                response = json.loads(response.read())
                key = response.get('key')
                self.response.headers['Content-Type'] = 'application/json'   
                obj = {
                    'response': 0,
                    'examId': str(key)
                  } 
                self.response.out.write(json.dumps(obj))
        except Exception, E:
            print E
            if flag == 1 or flag == 2:
                self.response.headers['Content-Type'] = 'application/json'   
                obj = {
                    'response': 0,
                    'error': 'Upload done time limit exceeded'
                  } 
                self.response.out.write(json.dumps(obj))

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write("""<html>
                    <head>
                    <style type="text/css">.thumb-image{float:left;width:100px;position:relative;padding:5px;}</style>
                    </head>
                    <body>
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
                    <form enctype="multipart/form-data" method="POST">

                    <input type="file" id="fileUpload" name="file" multiple>
                    <input type="text" name="profileId">
                    <input type="text" name="courseId">
                    <input type="text" name="title">
                    <input type="text" name="desc">
                    <input type="text" name="date">
                    <input type="text" name="classNumber">
                    <input type="text" name="dueDate">
                    <input type="text" name="dueTime">
                    <input type="text" name="type">
                            <input type="submit" value="Submit">
                    </form>
                    <div id="image-holder"></div>

                    </div>

                    <script>
                    $(document).ready(function() {
                            $("#fileUpload").on('change', function() {
                              //Get count of selected files
                              var countFiles = $(this)[0].files.length;
                              var imgPath = $(this)[0].value;
                              var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
                              var image_holder = $("#image-holder");
                              image_holder.empty();
                              if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
                                if (typeof(FileReader) != "undefined") {
                                  //loop for each file selected for uploaded.
                                  for (var i = 0; i < countFiles; i++)
                                  {
                                    var reader = new FileReader();
                                    reader.onload = function(e) {
                                      $("<img />", {
                                        "src": e.target.result,
                                        "class": "thumb-image"
                                      }).appendTo(image_holder);
                                    }
                                    image_holder.show();
                                    reader.readAsDataURL($(this)[0].files[i]);
                                  }
                                } else {
                                  alert("This browser does not support FileReader.");
                                }
                              } else {
                                alert("Pls select only images");
                              }
                            });
                          });
                    </script>
                    </body>
                    </html>""")


class ImageUploadWeb(webapp2.RequestHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        try:
            fileList = self.request.POST.getall('file')
        except Exception, E:
            print "file Missing in request\n"+self.request+'\n'+str(E)
            obj = {'response': 1, 'description': "file Missing in request\n"+self.request+'\n'+str(E)} 
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(obj))
        try:
            profileId = self.request.get('profileId')
        except Exception, E:
            print "profileId Missing in request\n"+self.request+'\n'+str(E)
            obj = {'response': 1, 'description': "profileId Missing in request\n"+self.request+'\n'+str(E)} 
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(obj))
        try:
            courseId = self.request.get('courseId')
        except Exception, E:
            print "courseId Missing in request\n"+self.request+'\n'+str(E)
            obj = {'response': 1, 'description': "courseId Missing in request\n"+self.request+'\n'+str(E)} 
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(obj))
        bucketName = BUCKET_NAME
        urlList = []
        for file in fileList:
            timestamp = "".join(str(datetime.datetime.now()).split())
            fileName = bucketName + '/' + courseId + '/' + profileId + '/' + timestamp + '.jpg'
            gcsFile = gcs.open(fileName, mode='w', content_type='image/jpeg',
                               options={'x-goog-acl': 'public-read'})
            gcsFile.write(file.value)
            url = 'https://storage.googleapis.com' + fileName
            urlList.append(url)
            gcsFile.close()
        self.response.headers['Content-Type'] = 'application/json'
        obj = {'response': 0, 'url': urlList} 
        self.response.out.write(json.dumps(obj))
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write("""<html>
                    <head>
                    <style type="text/css">.thumb-image{float:left;width:100px;position:relative;padding:5px;}</style>
                    </head>
                    <body>
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
                    <form enctype="multipart/form-data" method="POST">

                    <input type="file" id="fileUpload" name="file" multiple>
                    <input type="text" name="profileId">
                    <input type="text" name="courseId">
                    <input type="submit" value="Submit">
                    </form>
                    <div id="image-holder"></div>

                    </div>

                    <script>
                    $(document).ready(function() {
                            $("#fileUpload").on('change', function() {
                              //Get count of selected files
                              var countFiles = $(this)[0].files.length;
                              var imgPath = $(this)[0].value;
                              var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
                              var image_holder = $("#image-holder");
                              image_holder.empty();
                              if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
                                if (typeof(FileReader) != "undefined") {
                                  //loop for each file selected for uploaded.
                                  for (var i = 0; i < countFiles; i++)
                                  {
                                    var reader = new FileReader();
                                    reader.onload = function(e) {
                                      $("<img />", {
                                        "src": e.target.result,
                                        "class": "thumb-image"
                                      }).appendTo(image_holder);
                                    }
                                    image_holder.show();
                                    reader.readAsDataURL($(this)[0].files[i]);
                                  }
                                } else {
                                  alert("This browser does not support FileReader.");
                                }
                              } else {
                                alert("Pls select only images");
                              }
                            });
                          });
                    </script>
                    </body>
                    </html>""")
app = webapp2.WSGIApplication([('/img', ImageUploadAndroid),
                               ('/imgweb', ImageUploadWeb),
                               ('/changePic', ProfilePicUpload)], debug=True)
