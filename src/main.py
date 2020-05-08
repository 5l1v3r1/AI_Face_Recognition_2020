import face_recognition
import os
import cv2

KNOWN_IMG_DIR = "known_faces"
UNKNOWN_IMG_DIR = "unknown_faces"
CV2FONT = cv2.FONT_HERSHEY_SIMPLEX

print("Loading known images...")
known_faces = []
known_names = []

for name in os.listdir(KNOWN_IMG_DIR):
    for filename in os.listdir(f"{KNOWN_IMG_DIR}"):
        image = face_recognition.load_image_file(f"{KNOWN_IMG_DIR}/{name}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print("Processing unknown faces...")
color = (200, 200, 200)
for filename in os.listdir(UNKNOWN_IMG_DIR):
    print(filename)
    image = face_recognition.load_image_file(f"{UNKNOWN_IMG_DIR}/{filename}")
    locations = face_recognition.face_locations(image, model = "cnn")
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, 0.5)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match founds : {match}")
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0, 255, 0]
            cv2.rectangle(image, top_left, bottom_right, color, 3)

            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            org = (face_location[3] + 11, face_location[2] + 15)
            cv2.putText(image, match, org, CV2FONT, 0.5, color, 2)

    cv2.imshow(filename, image)
    cv2.waitKey(100000)
    # cv2.destroyWindow(filename)
