import webapp2
from sparkpost import SparkPost


class Emailer(webapp2.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def post(self):
        try:
            emailFile = self.request.POST.get('emailFile')
            str(emailFile)
            textFile = self.request.POST.get('textFile')
            emailIds = self.request.get('emailIds')
            text = self.request.get('text')
            fromId = 'aayush@campusconnect.cc'
            if len(self.request.get('from')) != 0:
                fromId = self.request.get('from') + '@campusconnect.cc'
            subject = self.request.get('subject')
            if "FieldStorage" in str(emailFile):
                temp = emailFile.value
                temp = temp.replace('\n', ',')
                idList = temp.split(',')
            else:
                idList = emailIds.split(',')
            if "FieldStorage" in str(textFile):
                body = textFile.value
            else:
                body = text
            sp = SparkPost('d5eda063a40ae19610612ea5d0804f20d294e62d')
            sp.transmissions.send(recipients=idList,
                                  html=body,
                                  from_email={'email': fromId, 'name': 'Campus Connect'},
                                  subject=subject,
                                  )
            self.response.out.write("Successfully\nSent to " + str(len(idList)) + " peoples")
        except Exception, E:
            self.response.out.write("Failed\n" + str(E))

    def get(self):
        self.response.out.write("""<form method="POST" enctype="multipart/form-data">
                                    <label>from</label>            <input type="text" name="from"><label>@campusconnnect.cc</label><br>
                                    <label>Id List File(*.csv)</label>       <input type="file" name="emailFile"><br>
                                    <label>Email Ids</label>           <input type="text" name="emailIds"><br>
                                    <label>Email Subject</label>        <input type="text" name="subject"><br>
                                    <label>Email Body File(*.txt)</label>     <input type="file" name="textFile"><br>
                                    <label>Email Body</label>              <input type="text" name="text"><br>
                                    <input type="submit" name="submit">
                                   </form>""")

app = webapp2.WSGIApplication([('/email', Emailer)], debug=True)