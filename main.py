import webapp2
import urllib2
import json
import cloudstorage as gcs
import datetime


class ImageUploadWeb(webapp2.RequestHandler):
    def post(self):
        urlList = []
        try:
            fileList = self.request.POST.getall('file')
        except Exception:
            print "file Missing in request"
            return self.response.write("file Missing in request")
        try:
            profileId = self.request.get('profileId')
        except Exception:
            print "profileId Missing in request"
            return self.response.write("profileId Missing in request")
        try:
            courseId = self.request.get('courseId')
        except Exception:
            print "courseId Missing in request"
            return self.response.write("courseId Missing in request")
        try:
            title = self.request.get('title')
        except Exception:
            print "title Missing in request"
            return self.response.write("title Missing in request")
        try:
            desc = self.request.get('desc')
        except Exception:
            print "desc Missing in request"
            return self.response.write("desc Missing in request")
        print "Number of files to be uploaded" + str(len(fileList))
        try:
            type = self.request.get('type')
        except Exception:
            print "type Missing in request"
            return self.response.write("type Missing in request")
        bucketName = "/uploadnotes-2016.appspot.com"
        try:
            for file in fileList:
                timestamp = str(datetime.datetime.now())
                fileName = bucketName + '/' + courseId + '/' + profileId + '/' + timestamp + '.jpg'
                gcsFile = gcs.open(fileName, mode='w', content_type='image/jpeg', options={'x-goog-acl': 'public-read'})
                gcsFile.write(file.value)
                url = 'https://storage.googleapis.com' + fileName
                urlList.append(url)
                gcsFile.close()
        except Exception, E:
            if str(E) == "'unicode' object has no attribute 'value'":
                print "0 image"
                urlList.append("http://guiaquebueno.com/Images/Restaurantes/Restaurante_no_image.jpg")
            else:
                print "Upload Failed!!!"
                return self.response.write("UPLOAD FAILED" + str(E))
        if type == 'notes':
            try:
                date = self.request.get('date')
            except:
                print "date Missing from request"
                return self.response.write("date Missing from request")
            try:
                classNumber = self.request.get('classNumber')
            except:
                print "classNumber Missing from request"
                self.response.write("classNumber Missing in request")
            url = "https://uploadnotes-2016.appspot.com/_ah/api/notesapi/v1/createNotes"
            data = {'profileId': profileId, 'courseId': courseId, 'title': title, 'notesDesc': desc,
                    'urlList': urlList, 'classNumber': classNumber, 'date': date}
            header = {'Content-Type': 'application/json; charset=UTF-8'}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            key = response.get('key')
            redirectUrl = str('https://campusconnect-2016.herokuapp.com/notebook?id=') + str(key)
            redirectUrl += str('&cId=') + str(courseId)
            self.redirect(redirectUrl)
        if type == 'assignment':
            try:
                dueDate = self.request.get('dueDate')
            except:
                print "dueDate Missing from request"
                self.response.write("dueDate Missing from request")
            try:
                dueTime = self.request.get('dueTime')
            except:
                print "dueTime Missing from request"
                self.response.write("dueTime Missing from request")
            url = "https://uploadnotes-2016.appspot.com/_ah/api/notesapi/v1/createAssignment"
            data = {'uploaderId': profileId, 'courseId': courseId, 'assignmentTitle': title, 'assignmentDesc': desc,
                    'urlList': urlList, 'dueDate': dueDate, 'dueTime': dueTime}
            header = {'Content-Type': 'application/json; charset=UTF-8'}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            key = response.get('key')
            redirectUrl = str('https://campusconnect-2016.herokuapp.com/assignment?id=') + str(key)
            redirectUrl += str('&cId=') + str(courseId)
            self.redirect(redirectUrl)
        if type == 'exam':
            try:
                dueDate = self.request.get('dueDate')
            except:
                print "dueDate Missing from request"
                self.response.write("dueDate Missing from request")
            try:
                dueTime = self.request.get('dueTime')
            except:
                print "dueTime Missing from request"
                self.response.write("dueTime Missing from request")
            url = "https://uploadnotes-2016.appspot.com/_ah/api/notesapi/v1/createExam"
            data = {'uploaderId': profileId, 'courseId': courseId, 'examTitle': title, 'examDesc': desc,
                    'urlList': urlList, 'dueDate': dueDate, 'dueTime': dueTime}
            header = {'Content-Type': 'application/json; charset=UTF-8'}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            key = response.get('key')
            redirectUrl = str('https://campusconnect-2016.herokuapp.com/exam?id=') + str(key)
            redirectUrl += str('&cId=') + str(courseId)
            self.redirect(redirectUrl)

    def get(self):
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

app = webapp2.WSGIApplication([('/img', ImageUploadWeb)], debug=True)
