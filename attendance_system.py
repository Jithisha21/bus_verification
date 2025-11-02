import cv2
import mediapipe as mp
import sqlite3
import os
import numpy as np
import pyttsx3
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

# ---------------- Firebase Setup ----------------
cred = credentials.Certificate(
    r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\serviceAccountKey.json"
)  # Path to your Firebase JSON key
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://studentattendancesystem-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# References for attendance and absentee logs
attendance_ref = db.reference("attendance_logs/Class1")
absentees_ref = db.reference("absentees/Class1")

# ---------------- Mediapipe Setup ----------------
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# ---------------- TTS Function (pyttsx3) ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

def speak(message):
    """Speak the given message using pyttsx3 (offline)."""
    engine.say(message)
    engine.runAndWait()

# ---------------- Database Load ----------------
def load_student_data():
    """Fetch student data from the SQLite database."""
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, image_path FROM students")
    students = cursor.fetchall()
    conn.close()

    data = []
    for name, image_path in students:
        if os.path.exists(image_path):
            face_image = cv2.imread(image_path)
            if face_image is not None:
                face_image_gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                data.append({
                    "name": name,
                    "image_path": image_path,
                    "face_image": face_image_gray,
                })
    return data

# ---------------- Face Matching ----------------
def match_face(detected_face, student_data):
    detected_face_gray = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)
    for student in student_data:
        known_face = student["face_image"]
        try:
            known_face_resized = cv2.resize(
                known_face, (detected_face_gray.shape[1], detected_face_gray.shape[0])
            )
        except cv2.error:
            continue
        difference = cv2.absdiff(known_face_resized, detected_face_gray)
        diff_mean = np.mean(difference)
        if diff_mean < 50:
            return student
    return None

# ---------------- Main Attendance System ----------------
def attendance_system():
    print("Attendance System Running... Press 'q' to quit.")

    cap = cv2.VideoCapture(0)
    student_data = load_student_data()
    registered_students = [s["name"] for s in student_data]
    present_students = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                if x < 0 or y < 0 or x + w > iw or y + h > ih:
                    continue

                face = frame[y:y + h, x:x + w]
                if face.size == 0:
                    continue

                matched_student = match_face(face, student_data)
                if matched_student and matched_student["name"] not in present_students:
                    student_name = matched_student["name"]
                    print(f"Present: {student_name}.")
                    speak(f"Attendance marked for {student_name}")
                    cv2.putText(frame, f"Present: {student_name}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    present_students.add(student_name)

                    # Push attendance log to Firebase
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    attendance_ref.push({
                        "student": student_name,
                        "status": "Present",
                        "class": "Class1",
                        "time": timestamp
                    })

        cv2.imshow("Student Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ---------------- Absentees Report ----------------
    absentees = set(registered_students) - present_students
    if absentees:
        print("\nAbsentees List:")
        for student in absentees:
            print(f"- {student}")
            speak(f"Alert! {student} is absent today.")

            # Push absentee alert to Firebase
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            absentees_ref.push({
                "student": student,
                "status": "Absent",
                "class": "Class1",
                "time": timestamp
            })
    else:
        print("\nAll students are present!")
        speak("All students are present today.")

if __name__ == "__main__":
    attendance_system()
