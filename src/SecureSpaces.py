from os import listdir
from os.path import isfile, join
import face_recognition
import sys
import cv2
import numpy as np
import PhoneMessaging.send_message as SMS
from firebase import Firebase
from datetime import datetime

config = {
    "apiKey": "AIzaSyCIb7b77N60HaFsUwsxuiiRJMtUfoC0ubs",
    "authDomain": "spaces-f099d.firebaseapp.com",
    "databaseURL": "https://spaces-f099d.firebaseio.com",
    "storageBucket": "spaces-f099d.appspot.com"
}

firebase = Firebase(config)

storage = firebase.storage()
#print(allFiles)

#storage.child

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
class Person:
    hasSentSMS = False
    def __init__(self, imageFile, faceName):
        self.faceName = faceName
        self.image = face_recognition.load_image_file(imageFile)
        self.image_face_encoding = face_recognition.face_encodings(self.image)[0] 
    def flipSentSMS(self):
        self.hasSentSMS = True

# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)
#Add everyone to a persons array
#personArray = [zeak, kyle]
friendsDir = "friends"
intruderDir = "intruders"
friendsOnly = False;
if len(sys.argv) == 2 and sys.argv[1] == 'S':
    friendsOnly = True

friends = [f for f in listdir(friendsDir) if isfile(join(friendsDir, f)) ]
intruders = [f for f in listdir(intruderDir) if isfile(join(intruderDir, f)) ]
personArray = []
video_face_encoding = []    

for friend in friends:
    personArray.append(Person("./"+ friendsDir +"/"+ friend, "friend"))

for intruder in intruders:
    personArray.append(Person("./"+ intruderDir +"/"+ intruder, "Intruder"))

def sendIntruderMessage():
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    message = SMS.Message(dt_string + " - " + " Intruder!")
    message.sendMessage()

video_capture = cv2.VideoCapture(0)


# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
for person in personArray:
    known_face_encodings.append(person.image_face_encoding)
    known_face_names.append(person.faceName)
#known_face_encodings = [obama_face_encoding, biden_face_encoding]
#known_face_names = ["Zeak","Intruder"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
friendsOnlyIntruder = False
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if (name == "Intruder"):
                if personArray[best_match_index].hasSentSMS == False:
                    personArray[best_match_index].flipSentSMS()
                    #sendIntruderMessage()
            if (friendsOnly and name == "Unknown" and friendsOnlyIntruder == False):
                #sendIntruderMessage()
                friendsOnlyIntruder = True
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
