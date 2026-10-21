#import cv2
#import mediapipe as mp
#import time
#
#cap = cv2.VideoCapture("ali/1.mp4")
#mpPose = mp.solutions.pose
#pose = mpPose.Pose()
#mpDraw = mp.solutions.drawing_utils
#while True:
#    success, img = cap.read()
#    results = pose.process(img)
#    if results.pose_landmarks:
#        mpDraw.draw_landmarks(img,results.pose_landmarks, mpPose.POSE_CONNECTIONS)
#    if not success: 
#        print("Camera read failed")
#        break
#
#    cv2.imshow("Image", img)
#    
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
#cap.release()
#cv2.destroyAllWindows()
import cv2
import mediapipe as mp

cap = cv2.VideoCapture("1.mp4")
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    
    # 1. التحقق أولاً من أن الفريم تم قراءته بنجاح
    if not success or img is None: 
        print("Video ended or file not found")
        break

    # 2. تحويل الصورة إلى RGB لأن OpenCV يقرؤها بـ BGR
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # 3. رسم النقاط على الصورة الأصلية BGR
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()