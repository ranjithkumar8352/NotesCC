from sparkpost import SparkPost


def send():
    sp = SparkPost('d5eda063a40ae19610612ea5d0804f20d294e62d')
    response = sp.transmissions.send(recipients=['saurav24081996@gmail.com', 'aayush@campusconnect.cc'],
                                     html='<H1> Good to know that I am coming<br>https://storage.googleapis.com/uploadnotes-2016.appspot.com/summary.csv </H1>',
                                     from_email={'email': 'aayush@campusconnect.cc', 'name': 'Campus Connect'},
                                     subject='OOOOH!!! YEAHHHH',
                                     )
    print(response)
