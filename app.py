import cv2
import os
from flask import Flask, request, render_template
from datetime import date, datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

#### Defining Flask App
app = Flask(__name__)

#### Saving Date today in 2 different formats
def datetoday():
    return date.today().strftime("%m_%d_%y")

def datetoday2():
    return date.today().strftime("%d-%B-%Y")

#### Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier('E:/OneDrive/Desktop/Final proj/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

#### If these directories don't exist, create them
if not os.path.isdir('E:/OneDrive/Desktop/Final proj/Attendance'):
    os.makedirs('E:/OneDrive/Desktop/Final proj/Attendance')
if not os.path.isdir('E:/OneDrive/Desktop/Final proj/Static/faces'):
    os.makedirs('E:/OneDrive/Desktop/Final proj/Static/faces')
if f'Attendance-{datetoday()}.csv' not in os.listdir('E:/OneDrive/Desktop/Final proj/Attendance'):
    with open(f'E:/OneDrive/Desktop/Final proj/Attendance/Attendance-{datetoday()}.csv', 'w') as f:
        f.write('Name,Roll,Time')

# get a number of total registered users
def totalreg():
    return len(os.listdir('E:/OneDrive/Desktop/Final proj/Static/faces'))

#### extract the face from an image
def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points

#### Identify face using ML model
def identify_face(facearray):
    model = joblib.load('E:/OneDrive/Desktop/Final proj/Static/face_recognition_model.pkl')
    return model.predict(facearray)

# A function which trains the model on all the faces available in faces folder
def train_model():
    faces = []
    labels = []
    userlist = os.listdir('E:/OneDrive/Desktop/Final proj/Static/faces')
    for user in userlist:
        for imgname in os.listdir(f'E:/OneDrive/Desktop/Final proj/Static/faces/{user}'):
            img = cv2.imread(f'E:/OneDrive/Desktop/Final proj/Static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'E:/OneDrive/Desktop/Final proj/Static/face_recognition_model.pkl')

# Extract info from today's attendance file in attendance folder
def extract_attendance():
    df = pd.read_csv(f'E:/OneDrive/Desktop/Final proj/Attendance/Attendance-{datetoday()}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, rolls, times, l

# Add Attendance of a specific user
def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")

    df = pd.read_csv(f'E:/OneDrive/Desktop/Final proj/Attendance/Attendance-{datetoday()}.csv')
    if int(userid) not in list(df['Roll']):
        with open(f'E:/OneDrive/Desktop/Final proj/Attendance/Attendance-{datetoday()}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')

################## ROUTING FUNCTIONS #######################
####### for Face Recognition based Attendance System #######

# Our main page
@app.route('/')
def home():
    names, rolls, times, l = extract_attendance()
    return render_template('E:/OneDrive/Desktop/Final proj/templates/home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg())

# Our main Face Recognition functionality.
# This function will run when we click on Take Attendance Button.
@app.route('/start', methods=['GET'])
def start():
    if 'E:/OneDrive/Desktop/Final proj/Static/face_recognition_model.pkl' not in os.listdir('E:/OneDrive/Desktop/Final proj/Static'):
        return render_template('E:/OneDrive/Desktop/Final proj/templates/home.html', totalreg=totalreg(), mess='There is no trained model in the static folder. Please add a new face to continue.')

    ret = True
    cap = cv2.VideoCapture(0)
    while ret:
        ret, frame = cap.read()
        if len(extract_faces(frame)) > 0:
            (x, y, w, h) = extract_faces(frame)[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (86, 32, 251), 1)
            cv2.rectangle(frame, (x, y), (x+w, y-40), (86, 32, 251), -1)
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            add_attendance(identified_person)
            cv2.putText(frame, f'{identified_person}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('E:/OneDrive/Desktop/Final proj/Attendance', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    names, rolls, times, l = extract_attendance()
    return render_template('E:/OneDrive/Desktop/Final proj/templates/home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg())

# A function to add a new user.
# This function will run when we add a new user.
@app.route('/add', methods=['GET', 'POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    userimagefolder = f'E:/OneDrive/Desktop/Final proj/Static/faces/{newusername}_{newuserid}'
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/50', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                name = f'{newusername}_{i}.jpg'
                cv2.imwrite(f'{userimagefolder}/{name}', frame[y:y+h, x:x+w])
                i += 1
            j += 1
        if j == 50*5:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()
    names, rolls, times, l = extract_attendance()
    return render_template('E:/OneDrive/Desktop/Final proj/templates/home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg())

# Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
