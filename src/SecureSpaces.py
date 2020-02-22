from os import listdir
from os.path import isfile, join
import face_recognition
import PhoneMessaging.send_message as SMS
#myMessage = SMS.Message("Howdy!")
#myMessage.sendMessage()
friendsDir = "friends"
intruderDir = "intruders"
unknownDir = "unknown"
videoDir = "video"

friends = [f for f in listdir(friendsDir) if isfile(join(friendsDir, f)) ]
unknowns = [f for f in listdir(unknownDir) if isfile(join(unknownDir, f)) ]
intruders = [f for f in listdir(intruderDir) if isfile(join(intruderDir, f)) ]
video = [f for f in listdir(videoDir) if isfile(join(videoDir, f)) ]
friend_face_encoding = []
unknown_face_encoding = []
intruder_face_encoding = []
video_face_encoding = []

for indexF in range(0, len(friends)):
    picture_of_me = face_recognition.load_image_file("./"+friendsDir +"/"+friends[indexF])
    friend_face_encoding.append(face_recognition.face_encodings(picture_of_me)[0])

# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
for indexU in range(0, len(unknowns)):
    unknown_picture = face_recognition.load_image_file("./"+unknownDir+"/"+unknowns[indexU])
    unknown_face_encoding.append(face_recognition.face_encodings(unknown_picture)[0])


for indexI in range(0, len(intruders)):
    intruder_picture = face_recognition.load_image_file("./"+intruderDir+"/"+intruders[indexI])
    intruder_face_encoding.append(face_recognition.face_encodings(intruder_picture)[0])

for indexV in range(0, len(video)):
    video_picture = face_recognition.load_image_file("./"+videoDir+"/"+video[indexV])
    video_face_encoding.append(face_recognition.face_encodings(video_picture)[0])

# Now we can see the two face encodings are of the same person with `compare_faces`!
results = [];
for compIndex in range(0, len(video_face_encoding)):
    #for friendI in range(0, len(friend_face_encoding)):
        results = face_recognition.compare_faces(friend_face_encoding, unknown_face_encoding)
        if results[0] == True:
            print("It's a picture of KJ!")
        else:
            print("It's not a picture of KJ!")
