import os
import time
import cv2
import numpy as np
import mediapipe as mp
import freenect  # مكتبة Kinect v1

# 1. اختيار المفصل المراد تتبعه
joint_choice = input("Enter joint to track (elbow / shoulder): ").strip().lower()

while joint_choice not in ['elbow', 'shoulder']:
    print("Invalid choice! Please type 'elbow' or 'shoulder'.")
    joint_choice = input("Enter joint to track (elbow / shoulder): ").strip().lower()

# 2. مسار حفظ الفيديو
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
output_video_path = os.path.join(DIR_PATH, f"kinect_{joint_choice}_recording.mp4")

# 3. إعداد MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# دالة لجلب إطار الألوان (RGB) من Kinect v1
def get_kinect_video():
    array, _ = freenect.sync_get_video()
    # freenect ترجع الصورة بتنسيق RGB
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array

# 4. إعداد تسجيل الفيديو
frame_width, frame_height = 640, 480  # دقة Kinect v1 القياسية
fps = 20.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

RECORD_DURATION = 60  # مدة التسجيل بالثواني
start_time = time.time()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        # جلب الإطار من Kinect
        frame = get_kinect_video()
        if frame is None:
            break

        elapsed_time = time.time() - start_time
        remaining_time = max(0, int(RECORD_DURATION - elapsed_time))

        if elapsed_time >= RECORD_DURATION:
            print(f"Done! Video saved successfully at: {output_video_path}")
            break

        frame = cv2.flip(frame, 1) # عكس الصورة كمرآة
        h, w, _ = frame.shape

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            r_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

            if joint_choice == 'elbow':
                angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                text_label = f"Elbow Angle: {int(angle)} deg"
            elif joint_choice == 'shoulder':
                angle = calculate_angle(r_hip, r_shoulder, r_elbow)
                text_label = f"Shoulder Angle: {int(angle)} deg"

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.putText(frame, text_label, (40, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 3)

        cv2.putText(frame, f"REC: {remaining_time}s", (w - 150, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        out.write(frame)
        cv2.imshow("Kinect Joint Angle Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

out.release()
cv2.destroyAllWindows()