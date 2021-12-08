import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request
import threading
from datetime import datetime
import re

app = Flask(__name__)
# Use the application default credentials
cred = credentials.Certificate(r"C:\Users\ellio\Desktop\my code\chat\chat-app-b2dbe-firebase-adminsdk-ujzhj-1dcc4576ff.json")
firebase_admin.initialize_app(cred, {
  'projectId': 'chat-app-b2dbe',
})

#sorting function
def sort_algo(e):
  time = int(re.sub(':','',e['chat-time']))
  return time

#server starts up, pulling data off firestore
db = firestore.client()
doc = db.collection(u'chat-history').stream()
stuff = []
for i in doc:
  stuff.append(i.to_dict())
stuff.sort(key=sort_algo)

#client logs on
@app.route('/')
def hello_world():
  return render_template('index.html', stuff=stuff)

@app.route('/work', methods=['GET','POST'])
def work():
  if request.method == 'POST':
    submition = str(request.data)
    submition = submition[2:-1]
    print(submition)
    global stuff
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    stuff.append({'chat-content':submition, 'chat-time':current_time})
    db.collection(u'chat-history').add({
      u'chat-content': submition,
      u'chat-time' : current_time
    })
    print(stuff)

    return 'hello'
  return 'hello'

if __name__ == '__main__':
  app.run()

