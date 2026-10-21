# # import os
# # import time
# # import cv2
# # import numpy as np
# # import mediapipe as mp

# # # --- 1. إعداد مجلد حفظ الفيديو ---
# # DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# # OUTPUT_DIR = os.path.join(DIR_PATH, "output_videos")
# # os.makedirs(OUTPUT_DIR, exist_ok=True)  # إنشاء المجلد إن لم يكن موجوداً

# # # اسم ملف الفيديو المحفوظ
# # output_video_path = os.path.join(OUTPUT_DIR, "rehab_session.mp4")

# # # --- 2. إعداد MediaPipe ---
# # mp_pose = mp.solutions.pose
# # mp_drawing = mp.solutions.drawing_utils

# # def calculate_angle(a, b, c):
# #     a = np.array([a.x, a.y])
# #     b = np.array([b.x, b.y])
# #     c = np.array([c.x, c.y])
    
# #     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
# #     angle = np.abs(radians * 180.0 / np.pi)
    
# #     if angle > 180.0:
# #         angle = 360 - angle
        
# #     return angle

# # # --- 3. تشغيل الكاميرا والمُسجّل ---
# # cap = cv2.VideoCapture(0)

# # # قراءة أبعاد الكاميرا والـ FPS
# # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# # fps = 20.0  # معدل الإطارات عند الحفظ

# # # إعداد كائن حفظ الفيديو (VideoWriter)
# # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# # out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# # SHOULDER_Z_TOLERANCE = 0.08  

# # RECORD_DURATION = 60  # مدة التسجيل بالثواني (دقيقة واحدة)
# # start_time = time.time()  # تسجيل وقت بداية التشغيل

# # with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #         if not ret:
# #             break
            
# #         # حساب الوقت المنقضي
# #         elapsed_time = time.time() - start_time
# #         remaining_time = max(0, int(RECORD_DURATION - elapsed_time))
        
# #         # إذا انتهت الدقيقة، اخرج من الحلقة واغلق الكاميرا
# #         if elapsed_time >= RECORD_DURATION:
# #             print(f"Done! Video saved successfully at: {output_video_path}")
# #             break

# #         frame = cv2.flip(frame, 1)
# #         h, w, _ = frame.shape
        
# #         image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #         results = pose.process(image_rgb)
        
# #         status_text = "INITIALIZING"
# #         status_color = (255, 255, 255)
        
# #         if results.pose_landmarks:
# #             landmarks = results.pose_landmarks.landmark
            
# #             l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
# #             r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
# #             r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
# #             r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            
# #             shoulder_z_diff = abs(r_shoulder.z - l_shoulder.z)
# #             avg_shoulder_z = (r_shoulder.z + l_shoulder.z) / 2.0
# #             relative_elbow_z = r_elbow.z - avg_shoulder_z
# #             elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            
# #             # الشروط المنطقية
# #             if shoulder_z_diff > SHOULDER_Z_TOLERANCE:
# #                 status_text = "WRONG: Keep Shoulders Straight!"
# #                 status_color = (0, 0, 255)
# #             else:
# #                 if (90 <= elbow_angle <= 100) and (abs(relative_elbow_z) < 0.05):
# #                     status_text = "START POSITION (Ready)"
# #                     status_color = (255, 255, 0)
# #                 elif (130 <= elbow_angle <= 160) and (relative_elbow_z < -0.05):
# #                     status_text = "RIGHT"
# #                     status_color = (0, 255, 0)
# #                 else:
# #                     status_text = "WRONG"
# #                     status_color = (0, 0, 255)
            
# #             mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
# #             cv2.putText(frame, f"Elbow Angle: {int(elbow_angle)} deg", (30, 40), 
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
# #             cv2.putText(frame, f"Elbow Rel Z: {relative_elbow_z:.2f}", (30, 70), 
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
# #             cv2.putText(frame, f"Shoulders Z Diff: {shoulder_z_diff:.2f}", (30, 100), 
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# #         # عرض العداد التنازلي للمدة المتبقية في أعلى اليمين
# #         cv2.putText(frame, f"REC: {remaining_time}s", (w - 160, 40), 
# #                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# #         # عرض نتيجة التمرين أسفل اليمين
# #         cv2.putText(frame, status_text, (w - 480, h - 40), 
# #                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 3)
        
# #         # 4. كتابة الإطار الحالي في ملف الفيديو
# #         out.write(frame)

# #         # عرض النافذة الحية
# #         cv2.imshow("Rehab Monitor - Auto Save", frame)
        
# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break

# # # إغلاق الكاميرا والمُسجّل والنوافذ
# # cap.release()
# # out.release()
# # cv2.destroyAllWindows()

# import os
# import time
# import cv2
# import numpy as np
# import mediapipe as mp

# # 1. تحديد مسار المجلد الحالي وحفظ الفيديو فيه مباشرة
# DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# output_video_path = os.path.join(DIR_PATH, "elbow_angle_recording.mp4")

# # 2. إعداد MediaPipe Pose
# mp_pose = mp.solutions.pose
# mp_drawing = mp.solutions.drawing_utils

# # دالة حساب الزاوية بين (الكتف - الكوع - المعصم)
# def calculate_angle(a, b, c):
#     a = np.array([a.x, a.y])
#     b = np.array([b.x, b.y])
#     c = np.array([c.x, c.y])
    
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
    
#     if angle > 180.0:
#         angle = 360 - angle
        
#     return angle

# # 3. تشغيل الكاميرا وإعداد مُسجّل الفيديو
# cap = cv2.VideoCapture(0)

# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = 20.0

# # كائن حفظ الفيديو صيغة MP4
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# RECORD_DURATION = 60  # مدة التسجيل بالثواني (دقيقة واحدة)
# start_time = time.time()

# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
            
#         # التحقق من الوقت المنقضي
#         elapsed_time = time.time() - start_time
#         remaining_time = max(0, int(RECORD_DURATION - elapsed_time))
        
#         # عند انتهاء الدقيقة يُغلق البرنامج تلقائياً
#         if elapsed_time >= RECORD_DURATION:
#             print(f"Done! Video saved successfully at: {output_video_path}")
#             break

#         frame = cv2.flip(frame, 1) # عكس الصورة كمرآة
#         h, w, _ = frame.shape
        
#         image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(image_rgb)
        
#         if results.pose_landmarks:
#             landmarks = results.pose_landmarks.landmark
            
#             # استخراج نقاط الذراع الأيمن (12: shoulder, 14: elbow, 16: wrist)
#             r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
#             r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
#             r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            
#             # حساب زاوية الكوع
#             elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            
#             # رسم الهيكل العظمي
#             mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
#             # عرض زاوية الكوع بخط أزرق عريض (255, 0, 0)
#             cv2.putText(frame, f"Elbow Angle: {int(elbow_angle)} deg", (40, 70), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

#         # عرض عداد الوقت المتبقي في الأعلى باللون الأحمر
#         cv2.putText(frame, f"REC: {remaining_time}s", (w - 150, 50), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

#         # كتابة الإطار داخل ملف الفيديو
#         out.write(frame)

#         cv2.imshow("Elbow Angle Monitor - 1 Min Recorder", frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# # تنظيف الموارد وإغلاق الكاميرا والملف
# cap.release()
# out.release()
# cv2.destroyAllWindows()
import os
import time
import cv2
import numpy as np
import mediapipe as mp

# 1. إدخال الاختيار من المستخدم
joint_choice = input("Enter joint to track (elbow / shoulder): ").strip().lower()

while joint_choice not in ['elbow', 'shoulder']:
    print("Invalid choice! Please type 'elbow' or 'shoulder'.")
    joint_choice = input("Enter joint to track (elbow / shoulder): ").strip().lower()

# 2. تحديد مسار حفظ الفيديو في نفس مجلد الكود
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
output_video_path = os.path.join(DIR_PATH, f"{joint_choice}_angle_recording.mp4")

# 3. إعداد MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# دالة حساب الزاوية بين 3 نقاط
def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# 4. تشغيل الكاميرا وإعداد مُسجّل الفيديو
cap = cv2.VideoCapture(0)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 20.0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

RECORD_DURATION = 60  # مدة التسجيل بالثواني (دقيقة واحدة)
start_time = time.time()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
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
            
            # النقاط المستخدمة:
            # 12: Right Shoulder, 14: Right Elbow, 16: Right Wrist, 24: Right Hip
            r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            r_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            
            # حساب الزاوية بناءً على اختيارك
            if joint_choice == 'elbow':
                # زاوية الكوع: بين (الكتف - الكوع - المعصم)
                angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                text_label = f"Elbow Angle: {int(angle)} deg"
            elif joint_choice == 'shoulder':
                # زاوية الكتف: بين (الحوض - الكتف - الكوع)
                angle = calculate_angle(r_hip, r_shoulder, r_elbow)
                text_label = f"Shoulder Angle: {int(angle)} deg"
            
            # رسم الهيكل العظمي
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # عرض الزاوية بخط أزرق عريض (255, 0, 0)
            cv2.putText(frame, text_label, (40, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 3)

        # عرض عداد الوقت المتبقي بالأحمر
        cv2.putText(frame, f"REC: {remaining_time}s", (w - 150, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # حفظ الإطار في الفيديو
        out.write(frame)

        cv2.imshow("Joint Angle Monitor", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()