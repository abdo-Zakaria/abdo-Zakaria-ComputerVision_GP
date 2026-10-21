#import cv2
#import mediapipe as mp
#import numpy as np
#
## Setup mediapipe solutions
#mp_drawing = mp.solutions.drawing_utils
#mp_pose = mp.solutions.pose
#
#
## Function to calculate angle between three points
#def calculate_angle(a, b, c):
#    a = np.array(a)  # First point
#    b = np.array(b)  # Mid point
#    c = np.array(c)  # End point
#
#    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
#        a[1] - b[1], a[0] - b[0]
#    )
#    angle = np.abs(radians * 180.0 / np.pi)
#
#    if angle > 180.0:
#        angle = 360 - angle
#
#    return angle
#
#
## Initialize variables for counter and webcam feed
#counter = 0
#stage = None
#
#cap = cv2.VideoCapture(0)
#
### Setup mediapipe instance
#with mp_pose.Pose(
#    min_detection_confidence=0.5, min_tracking_confidence=0.5
#) as pose:
#    while cap.isOpened():
#        ret, frame = cap.read()
#        if not ret:
#            break
#
#        # Recolor image to RGB
#        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        image.flags.writeable = False
#
#        # Make detection
#        results = pose.process(image)
#
#        # Recolor back to BGR
#        image.flags.writeable = True
#        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#
#        # Extract landmarks
#        try:
#            landmarks = results.pose_landmarks.landmark
#
#            # Get coordinates
#            shoulder = [
#                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
#                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
#            ]
#            elbow = [
#                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
#                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
#            ]
#            wrist = [
#                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
#                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
#            ]
#
#            # Calculate angle
#            angle = calculate_angle(shoulder, elbow, wrist)
#
#            # Visualize angle
#            cv2.putText(
#                image,
#                str(angle),
#                tuple(np.multiply(elbow, [640, 480]).astype(int)),
#                cv2.FONT_HERSHEY_SIMPLEX,
#                0.5,
#                (255, 255, 255),
#                2,
#                cv2.LINE_AA,
#            )
#
#            # Curl counter logic
#            if angle > 160:
#                stage = "down"
#            if angle < 30 and stage == "down":
#                stage = "up"
#                counter += 1
#                print(counter)
#
#        except:
#            pass
#
#        # Render detections
#        mp_drawing.draw_landmarks(
#            image,
#            results.pose_landmarks,
#            mp_pose.POSE_CONNECTIONS,
#            mp_drawing.DrawingSpec(
#                color=(245, 117, 66), thickness=2, circle_radius=2
#            ),
#            mp_drawing.DrawingSpec(
#                color=(245, 66, 230), thickness=2, circle_radius=2
#            ),
#        )
#
#        cv2.imshow("Mediapipe Feed", image)
#
#        if cv2.waitKey(10) & 0xFF == ord("q"):
#            break
#
#cap.release()
#cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp
# import numpy as np
# 
# # Setup mediapipe solutions
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose
# 
# # Initialize webcam feed
# cap = cv2.VideoCapture(0)
# 
# ## Setup mediapipe instance
# with mp_pose.Pose(
#     min_detection_confidence=0.5, min_tracking_confidence=0.5
# ) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
# 
#         # Recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False
# 
#         # Make detection
#         results = pose.process(image)
# 
#         # Recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# 
#         # Extract landmarks
#         try:
#             landmarks = results.pose_landmarks.landmark
# 
#             # Get Left Elbow Landmark
#             elbow_landmark = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
# 
#             # Get normalized X, Y, Z
#             x_norm = elbow_landmark.x
#             y_norm = elbow_landmark.y
#             z_val = (
#                 elbow_landmark.z
#             )  # depth coordinate (negative = closer to camera)
# 
#             # Convert X and Y to pixel coordinates
#             x_px = int(x_norm * 640)
#             y_px = int(y_norm * 480)
# 
#             # Format the 3D position text
#             pos_text = f"X:{x_px} Y:{y_px} Z:{z_val:.2f}"
# 
#             # Visualize 3D coordinates on image
#             cv2.putText(
#                 image,
#                 pos_text,
#                 (x_px, y_px),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5,
#                 (255, 255, 255),
#                 2,
#                 cv2.LINE_AA,
#             )
# 
#         except:
#             pass
# 
#         # Render detections
#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             mp_drawing.DrawingSpec(
#                 color=(245, 117, 66), thickness=2, circle_radius=2
#             ),
#             mp_drawing.DrawingSpec(
#                 color=(245, 66, 230), thickness=2, circle_radius=2
#             ),
#         )
# 
#         cv2.imshow("Mediapipe Feed", image)
# 
#         if cv2.waitKey(10) & 0xFF == ord("q"):
#             break
# 
# cap.release()
# cv2.destroyAllWindows()
# import cv2
# import mediapipe as mp

# # Setup mediapipe hands solutions
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# # Initialize webcam feed
# cap = cv2.VideoCapture(0)

# ## Setup mediapipe hands instance
# with mp_hands.Hands(
#     max_num_hands=2,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5,
# ) as hands:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#         # Make detection
#         results = hands.process(image)

#         # Recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         # Extract landmarks if hand detected
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Get Thumb Tip Landmark (Point 4)
#                 thumb_tip = hand_landmarks.landmark[
#                     mp_hands.HandLandmark.THUMB_TIP
#                 ]

#                 # Convert X and Y to pixel coordinates (assuming 640x480)
#                 x_px = int(thumb_tip.x * 640)
#                 y_px = int(thumb_tip.y * 480)
#                 z_val = thumb_tip.z

#                 # Format position text
#                 pos_text = f"Thumb: X:{x_px} Y:{y_px} Z:{z_val:.2f}"

#                 # Visualize coordinates near the thumb tip
#                 cv2.putText(
#                     image,
#                     pos_text,
#                     (x_px, y_px - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     (0, 255, 0),
#                     2,
#                     cv2.LINE_AA,
#                 )

#                 # Draw Hand Connections
#                 mp_drawing.draw_landmarks(
#                     image, hand_landmarks, mp_hands.HAND_CONNECTIONS
#                 )

#         cv2.imshow("MediaPipe Hands", image)

#         if cv2.waitKey(10) & 0xFF == ord("q"):
#             break

# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp

# # Setup mediapipe hands solutions
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands

# # Create a resizable window
# cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_NORMAL)

# # Initialize webcam feed
# cap = cv2.VideoCapture(0)

# ## Setup mediapipe hands instance
# with mp_hands.Hands(
#     max_num_hands=2,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5,
# ) as hands:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#         # Make detection
#         results = hands.process(image)

#         # Recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         # Extract landmarks if hand detected
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Get Thumb Tip Landmark (Point 4)
#                 thumb_tip = hand_landmarks.landmark[8]
#                   #  mp_hands.HandLandmark.THUMB_TIP
                

#                 # Convert X and Y to pixel coordinates (assuming 640x480)
#                 x_px = int(thumb_tip.x * 640)
#                 y_px = int(thumb_tip.y * 480)
#                 z_val = thumb_tip.z

#                 # Format position text
#                 pos_text = f"Thumb: X:{x_px} Y:{y_px} Z:{z_val:.2f}"

#                 # Visualize coordinates near the thumb tip
#                 cv2.putText(
#                     image,
#                     pos_text,
#                     (x_px, y_px - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     (0, 255, 0),
#                     2,
#                     cv2.LINE_AA,
#                 )

#                 # Draw Hand Connections
#                 mp_drawing.draw_landmarks(
#                     image, hand_landmarks, mp_hands.HAND_CONNECTIONS
#                 )

#         cv2.imshow("MediaPipe Hands", image)

#         if cv2.waitKey(10) & 0xFF == ord("q"):
#             break

# cap.release()
# cv2.destroyAllWindows()



# كود شغال علي حركة واحده من حركات الجسم لكن محتاج تحسنين

import cv2
import numpy as np
import mediapipe as mp

# --- 1. إعداد مكتبة MediaPipe القديمة (Solutions) ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# --- 2. دالة حساب الزاوية بين 3 نقاط (مثل الكتف - الكوع - المعصم) ---
def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# --- 3. تشغيل الكاميرا والمراقبة ---
cap = cv2.VideoCapture(0)

# تحديد سماحية انحراف الكتفين (Shoulder Z Alignment Tolerance)
SHOULDER_Z_TOLERANCE = 0.08  

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)  # عكس الصورة كمرآة
        h, w, _ = frame.shape
        
        # تحويل الصورة إلى RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        status_text = "INITIALIZING"
        status_color = (255, 255, 255)  # أبيض
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # استخراج النقاط المطلوب استخدامها (الجانب الأيمن للذراع كمثال)
            # 11: الكتف الأيسر, 12: الكتف الأيمن, 14: الكوع الأيمن, 16: المعصم الأيمن
            l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            
            # 1. حساب الفرق في العمق Z بين الكتفين لضمان عدم تلفيت الجسم
            shoulder_z_diff = abs(r_shoulder.z - l_shoulder.z)
            
            # 2. حساب متوسط Z للكتفين ليكون نقطة الصفر المرجعية (Reference)
            avg_shoulder_z = (r_shoulder.z + l_shoulder.z) / 2.0
            
            # 3. حساب Z الكوع بالنسبة لمستوى الكتفين
            relative_elbow_z = r_elbow.z - avg_shoulder_z
            
            # 4. حساب زاوية الكوع الأيمن
            elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            
            # --- التحقق من الشروط القاسية والمنطقية ---
            
            # الشرط الأول: التأكد من استقامة الكتفين (عدم دوران الجذع)
            if shoulder_z_diff > SHOULDER_Z_TOLERANCE:
                status_text = "WRONG: Keep Shoulders Straight!"
                status_color = (0, 0, 255)  # أحمر
            else:
                # الحالة الأولى: الوضع الابتدائي (الكوع في مستوى الجسم والزاوية بين 90 و 100)
                if (90 <= elbow_angle <= 100) and (abs(relative_elbow_z) < 0.05):
                    status_text = "START POSITION (Ready)"
                    status_color = (255, 255, 0)  # أصفر
                
                # الحالة الثانية: الحركة الصحيحة (الزاوية بين 130 و 160 والعمق Z بالسالب)
                elif (130 <= elbow_angle <= 160) and (relative_elbow_z < -0.05):
                    status_text = "RIGHT"
                    status_color = (0, 255, 0)  # أخضر
                
                else:
                    status_text = "WRONG"
                    status_color = (0, 0, 255)  # أحمر
            
            # رسم الهيكل العظمي على الشاشة
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # عرض المعلومات على الشاشة للمتابعة والتصحيح
            cv2.putText(frame, f"Elbow Angle: {int(elbow_angle)} deg", (30, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Elbow Rel Z: {relative_elbow_z:.2f}", (30, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Shoulders Z Diff: {shoulder_z_diff:.2f}", (30, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # عرض النتيجة بخط عريض أسفل يمين الشاشة
        cv2.putText(frame, status_text, (w - 480, h - 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 3)
        
        cv2.imshow("Rehab Monitor - Legacy MediaPipe", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
























# """
# Rehab Monitor - Calibration-based posture & movement classification
# =====================================================================

# Design summary
# ---------------
# Instead of one fixed Z threshold deciding everything, this script separates
# the problem into independent, normalized measurements:

#   1. Torso ROTATION   -> shoulder_width / torso_length ratio vs. calibrated
#                           baseline (scale-invariant proxy; see LIMITATION note
#                           below for what a single frontal camera cannot see).
#   2. Torso LEAN        -> angle of hip_mid->shoulder_mid vector vs. vertical,
#                           compared to the calibrated baseline angle.
#   3. EXERCISING ARM     -> elbow angle (already scale-invariant) + elbow
#      movement             position projected into a torso-local coordinate
#                           frame (normalized by torso length), so distance to
#                           camera and standing position don't matter. A small,
#                           down-weighted normalized Z term is added only to
#                           capture pure toward-camera reach, since that one
#                           dimension genuinely cannot be seen in 2D.
#   4. NON-EXERCISING ARM -> wrist position in the same torso-local frame,
#                           compared to its calibrated baseline position, so
#                           small incidental motion doesn't trigger a false
#                           "compensation" flag.

# All robustness thresholds are derived from calibration statistics
# (mean +/- STD_MULTIPLIER * std), floored by a small noise margin so a
# suspiciously noise-free calibration doesn't create a zero-tolerance system.
# The only "designer" numbers are the PROTOCOL parameters in the CONFIG
# section below (target angle range, target reach) -- these describe what the
# prescribed exercise looks like and are meant to be set per-exercise, not
# tuned to make detection work.

# LIMITATION: a single frontal 2D camera cannot fully separate small torso
# yaw rotation from the patient shifting slightly forward/back -- both change
# apparent shoulder width a little. The shoulder/torso ratio used here is the
# best available monocular proxy. For stricter rotation detection, use a
# camera angled ~30-45 degrees to the patient, or a depth camera
# (e.g. RealSense/Kinect).

# Controls: 'q' to quit, 'r' to re-calibrate.
# """

# import math
# from collections import deque
# from statistics import mean, median, pstdev

# import cv2
# import numpy as np
# import mediapipe as mp

# # ============================================================
# # CONFIGURATION
# # ============================================================

# EXERCISE_SIDE = "RIGHT"  # "RIGHT" or "LEFT" -- which arm is exercising

# # --- Protocol parameters (clinically defined, NOT robustness thresholds) ---
# # These describe WHAT the correct movement looks like. They are exercise
# # specific and should be set by whoever designs the rehab protocol.
# TARGET_ELBOW_ANGLE_RANGE = (130, 180)  # elbow angle counted as "movement complete"
# TARGET_REACH_RATIO = 0.35              # min normalized elbow displacement from the
#                                         # calibrated start position (units of torso
#                                         # length) required to count as "reached"

# # --- Calibration ---
# CALIBRATION_FRAMES = 45        # high-confidence frames captured while the patient
#                                 # holds the start pose
# CALIB_STABILITY_STD_DEG = 10   # if elbow-angle std during calibration exceeds this,
#                                 # the patient wasn't holding still -> restart

# # --- Robustness / smoothing ---
# SMOOTHING_WINDOW = 7            # frames used for the median filter
# HYSTERESIS_FRAMES = 6           # consecutive frames required before the displayed
#                                  # state is allowed to change
# VISIBILITY_THRESHOLD = 0.5      # mediapipe landmark visibility cutoff
# STD_MULTIPLIER = 3.0            # calibration threshold = mean +/- STD_MULTIPLIER * std

# # Noise floors: minimum tolerance even if calibration std is ~0. These exist
# # only so a near-perfectly-still calibration doesn't yield an unusably strict
# # system; they are sensor-noise margins, not exercise-logic thresholds.
# MIN_LEAN_DEG = 5.0          # degrees
# MIN_ROTATION_FRAC = 0.06    # fraction of the calibrated shoulder/torso ratio
# MIN_ARM_DISP_FRAC = 0.12    # fraction of torso length
# MIN_START_ANGLE_MARGIN = 8.0  # degrees

# # ============================================================
# # MEDIAPIPE SETUP
# # ============================================================

# mp_pose = mp.solutions.pose
# mp_drawing = mp.solutions.drawing_utils
# PL = mp_pose.PoseLandmark
# cv2.namedWindow("Rehab Monitor", cv2.WINDOW_NORMAL)
# SIDE_MAP = {
#     "RIGHT": dict(shoulder=PL.RIGHT_SHOULDER, elbow=PL.RIGHT_ELBOW, wrist=PL.RIGHT_WRIST,
#                   other_wrist=PL.LEFT_WRIST),
#     "LEFT": dict(shoulder=PL.LEFT_SHOULDER, elbow=PL.LEFT_ELBOW, wrist=PL.LEFT_WRIST,
#                  other_wrist=PL.RIGHT_WRIST),
# }
# SIDE = SIDE_MAP[EXERCISE_SIDE]


# # ============================================================
# # GEOMETRY HELPERS
# # ============================================================

# class Pt:
#     """A landmark converted into pixel-consistent coordinates.
#     z is scaled by frame width, matching MediaPipe's documented convention
#     that z shares roughly the same scale as x."""
#     __slots__ = ("x", "y", "z", "vis")

#     def __init__(self, lm, w, h):
#         self.x = lm.x * w
#         self.y = lm.y * h
#         self.z = lm.z * w
#         self.vis = lm.visibility


# def get_pts(landmarks, w, h):
#     def p(idx):
#         return Pt(landmarks[idx.value], w, h)

#     return {
#         "l_sh": p(PL.LEFT_SHOULDER), "r_sh": p(PL.RIGHT_SHOULDER),
#         "l_hip": p(PL.LEFT_HIP), "r_hip": p(PL.RIGHT_HIP),
#         "ex_sh": p(SIDE["shoulder"]), "ex_el": p(SIDE["elbow"]), "ex_wr": p(SIDE["wrist"]),
#         "ox_wr": p(SIDE["other_wrist"]),
#     }


# def angle_2d(a, b, c):
#     """Angle at point b, formed by a-b-c, using image-plane (x, y) only.
#     Already scale-invariant -- distance to camera does not affect an angle."""
#     ang = math.degrees(
#         math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x)
#     )
#     ang = abs(ang)
#     if ang > 180.0:
#         ang = 360 - ang
#     return ang


# def normalize(v):
#     n = np.linalg.norm(v)
#     return v / n if n > 1e-6 else v


# def compute_metrics(pts):
#     l_sh, r_sh, l_hip, r_hip = pts["l_sh"], pts["r_sh"], pts["l_hip"], pts["r_hip"]

#     sh_mid = np.array([(l_sh.x + r_sh.x) / 2, (l_sh.y + r_sh.y) / 2])
#     hip_mid = np.array([(l_hip.x + r_hip.x) / 2, (l_hip.y + r_hip.y) / 2])

#     shoulder_width = float(np.linalg.norm(
#         np.array([r_sh.x, r_sh.y]) - np.array([l_sh.x, l_sh.y])))
#     torso_length = float(np.linalg.norm(sh_mid - hip_mid))
#     torso_length = max(torso_length, 1e-6)

#     width_torso_ratio = shoulder_width / torso_length

#     # Lean: angle of the hip->shoulder axis vs. vertical (image "up").
#     torso_vec = sh_mid - hip_mid
#     lean_angle = math.degrees(math.atan2(torso_vec[0], -torso_vec[1]))

#     # Torso-local frame: right = shoulder-to-shoulder axis, up = torso axis.
#     basis_right = normalize(np.array([r_sh.x - l_sh.x, r_sh.y - l_sh.y]))
#     basis_up = normalize(torso_vec)

#     def to_local(p):
#         v = np.array([p.x, p.y]) - sh_mid
#         u = float(np.dot(v, basis_right)) / torso_length
#         vv = float(np.dot(v, basis_up)) / torso_length
#         return u, vv

#     ex_el_local = to_local(pts["ex_el"])
#     ox_wr_local = to_local(pts["ox_wr"])

#     elbow_angle = angle_2d(pts["ex_sh"], pts["ex_el"], pts["ex_wr"])

#     avg_sh_z = (l_sh.z + r_sh.z) / 2.0
#     elbow_z_rel = (pts["ex_el"].z - avg_sh_z) / shoulder_width if shoulder_width > 1e-6 else 0.0

#     min_vis = min(l_sh.vis, r_sh.vis, l_hip.vis, r_hip.vis,
#                   pts["ex_sh"].vis, pts["ex_el"].vis, pts["ex_wr"].vis, pts["ox_wr"].vis)

#     return dict(
#         sh_mid=sh_mid, hip_mid=hip_mid, shoulder_width=shoulder_width,
#         torso_length=torso_length, width_torso_ratio=width_torso_ratio,
#         lean_angle=lean_angle, elbow_angle=elbow_angle,
#         ex_el_local=ex_el_local, ox_wr_local=ox_wr_local,
#         elbow_z_rel=elbow_z_rel, min_vis=min_vis,
#     )


# # ============================================================
# # CALIBRATION
# # ============================================================

# class Calibrator:
#     def __init__(self):
#         self.buffer = []

#     def add(self, m):
#         self.buffer.append(m)

#     def ready(self):
#         return len(self.buffer) >= CALIBRATION_FRAMES

#     def is_stable(self):
#         angles = [m["elbow_angle"] for m in self.buffer]
#         return pstdev(angles) <= CALIB_STABILITY_STD_DEG if len(angles) > 1 else True

#     def finalize(self):
#         def stat(key):
#             vals = [m[key] for m in self.buffer]
#             return mean(vals), (pstdev(vals) if len(vals) > 1 else 0.0)

#         lean_mean, lean_std = stat("lean_angle")
#         ratio_mean, ratio_std = stat("width_torso_ratio")
#         angle_mean, angle_std = stat("elbow_angle")
#         z_mean, _ = stat("elbow_z_rel")

#         ox_u = [m["ox_wr_local"][0] for m in self.buffer]
#         ox_v = [m["ox_wr_local"][1] for m in self.buffer]
#         ox_mean = (mean(ox_u), mean(ox_v))
#         ox_std = (pstdev(ox_u) if len(ox_u) > 1 else 0.0,
#                   pstdev(ox_v) if len(ox_v) > 1 else 0.0)

#         ex_u = [m["ex_el_local"][0] for m in self.buffer]
#         ex_v = [m["ex_el_local"][1] for m in self.buffer]
#         ex_start_local = (mean(ex_u), mean(ex_v))

#         thresholds = dict(
#             lean_thresh=max(STD_MULTIPLIER * lean_std, MIN_LEAN_DEG),
#             ratio_thresh=max(STD_MULTIPLIER * ratio_std, MIN_ROTATION_FRAC * ratio_mean),
#             nonex_thresh=max(STD_MULTIPLIER * math.hypot(*ox_std), MIN_ARM_DISP_FRAC),
#             start_angle_low=angle_mean - max(STD_MULTIPLIER * angle_std, MIN_START_ANGLE_MARGIN),
#             start_angle_high=angle_mean + max(STD_MULTIPLIER * angle_std, MIN_START_ANGLE_MARGIN),
#         )

#         return dict(
#             lean_mean=lean_mean, ratio_mean=ratio_mean,
#             ox_mean=ox_mean, ex_start_local=ex_start_local,
#             z_mean=z_mean, thresholds=thresholds,
#         )


# # ============================================================
# # SMOOTHING (temporal median filter)
# # ============================================================

# class Smoother:
#     def __init__(self, window):
#         self.window = window
#         self.buffers = {}

#     def push(self, key, value):
#         self.buffers.setdefault(key, deque(maxlen=self.window)).append(value)

#     def get(self, key):
#         buf = self.buffers.get(key)
#         return median(buf) if buf else None

#     def get_vec(self, key_u, key_v):
#         u, v = self.get(key_u), self.get(key_v)
#         return (u, v) if u is not None and v is not None else None

#     def full(self):
#         return bool(self.buffers) and all(len(b) >= self.window for b in self.buffers.values())


# # ============================================================
# # CLASSIFICATION
# # ============================================================

# def classify(s, calib):
#     th = calib["thresholds"]

#     lean_dev = abs(s["lean_angle"] - calib["lean_mean"])
#     lean_ok = lean_dev <= th["lean_thresh"]
#     rotation_ok = s["width_torso_ratio"] >= calib["ratio_mean"] - th["ratio_thresh"]

#     ox_u, ox_v = s["ox_wr_local"]
#     cal_ox_u, cal_ox_v = calib["ox_mean"]
#     nonex_dev = math.hypot(ox_u - cal_ox_u, ox_v - cal_ox_v)
#     nonex_ok = nonex_dev <= th["nonex_thresh"]

#     posture_ok = rotation_ok and lean_ok and nonex_ok
#     reason = None
#     if not rotation_ok:
#         reason = "Torso Rotating"
#     elif not lean_ok:
#         reason = "Torso Leaning"
#     elif not nonex_ok:
#         reason = "Other Arm Moving"

#     angle = s["elbow_angle"]
#     ex_u, ex_v = s["ex_el_local"]
#     st_u, st_v = calib["ex_start_local"]
#     reach_uv = math.hypot(ex_u - st_u, ex_v - st_v)
#     # Depth term down-weighted (0.5x): z is the only unavoidable use of MediaPipe's
#     # less-reliable depth estimate, kept only as a supplementary reach signal.
#     reach_total = math.hypot(reach_uv, 0.5 * (s["elbow_z_rel"] - calib["z_mean"]))

#     if th["start_angle_low"] <= angle <= th["start_angle_high"] and reach_total < TARGET_REACH_RATIO * 0.5:
#         arm_state = "START"
#     elif TARGET_ELBOW_ANGLE_RANGE[0] <= angle <= TARGET_ELBOW_ANGLE_RANGE[1] and reach_total >= TARGET_REACH_RATIO:
#         arm_state = "TARGET"
#     else:
#         arm_state = "MID"

#     if not posture_ok:
#         label = "WRONG"
#     elif arm_state == "START":
#         label = "START"
#     elif arm_state == "TARGET":
#         label = "RIGHT"
#     else:
#         label = "WRONG"

#     debug = dict(angle=angle, lean_dev=lean_dev, rotation_ratio=s["width_torso_ratio"],
#                  nonex_dev=nonex_dev, reach_total=reach_total)
#     return label, reason, arm_state, debug


# class Hysteresis:
#     """Requires a candidate label to persist for N frames before it is committed
#     (i.e. actually shown), which absorbs single-frame jitter/misdetections."""

#     def __init__(self, frames):
#         self.frames = frames
#         self.candidate = None
#         self.streak = 0
#         self.committed = "INITIALIZING"

#     def update(self, candidate):
#         if candidate == self.candidate:
#             self.streak += 1
#         else:
#             self.candidate = candidate
#             self.streak = 1
#         if self.streak >= self.frames:
#             self.committed = candidate
#         return self.committed


# # ============================================================
# # MAIN LOOP
# # ============================================================

# def main():
#     cap = cv2.VideoCapture(0)
#     smoother = Smoother(SMOOTHING_WINDOW)
#     calibrator = Calibrator()
#     hysteresis = Hysteresis(HYSTERESIS_FRAMES)
#     calib = None
#     mode = "CALIBRATING"

#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             frame = cv2.flip(frame, 1)
#             h, w, _ = frame.shape
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = pose.process(rgb)

#             status_text, status_color = "NO PERSON DETECTED", (255, 255, 255)

#             if results.pose_landmarks:
#                 landmarks = results.pose_landmarks.landmark
#                 pts = get_pts(landmarks, w, h)
#                 m = compute_metrics(pts)

#                 mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 sh_mid_i = tuple(m["sh_mid"].astype(int))
#                 hip_mid_i = tuple(m["hip_mid"].astype(int))
#                 cv2.line(frame, sh_mid_i, hip_mid_i, (255, 200, 0), 2)          # torso axis
#                 cv2.line(frame, (int(pts["l_sh"].x), int(pts["l_sh"].y)),
#                           (int(pts["r_sh"].x), int(pts["r_sh"].y)), (0, 200, 255), 2)  # shoulder line

#                 if m["min_vis"] < VISIBILITY_THRESHOLD:
#                     status_text, status_color = "LOW CONFIDENCE - adjust position", (0, 165, 255)

#                 elif mode == "CALIBRATING":
#                     calibrator.add(m)
#                     status_text = f"CALIBRATING {len(calibrator.buffer)}/{CALIBRATION_FRAMES} - hold start pose"
#                     status_color = (255, 255, 0)
#                     if calibrator.ready():
#                         if calibrator.is_stable():
#                             calib = calibrator.finalize()
#                             mode = "RUNNING"
#                         else:
#                             calibrator.buffer.clear()  # not stable enough, restart

#                 else:
#                     smoother.push("elbow_angle", m["elbow_angle"])
#                     smoother.push("lean_angle", m["lean_angle"])
#                     smoother.push("width_torso_ratio", m["width_torso_ratio"])
#                     smoother.push("ex_el_local_u", m["ex_el_local"][0])
#                     smoother.push("ex_el_local_v", m["ex_el_local"][1])
#                     smoother.push("ox_wr_local_u", m["ox_wr_local"][0])
#                     smoother.push("ox_wr_local_v", m["ox_wr_local"][1])
#                     smoother.push("elbow_z_rel", m["elbow_z_rel"])

#                     if smoother.full():
#                         s = dict(
#                             elbow_angle=smoother.get("elbow_angle"),
#                             lean_angle=smoother.get("lean_angle"),
#                             width_torso_ratio=smoother.get("width_torso_ratio"),
#                             ex_el_local=smoother.get_vec("ex_el_local_u", "ex_el_local_v"),
#                             ox_wr_local=smoother.get_vec("ox_wr_local_u", "ox_wr_local_v"),
#                             elbow_z_rel=smoother.get("elbow_z_rel"),
#                         )
#                         label, reason, arm_state, dbg = classify(s, calib)
#                         candidate = f"{label}:{reason}" if reason else label
#                         committed = hysteresis.update(candidate)

#                         if committed == "INITIALIZING":
#                             status_text, status_color = "ANALYZING...", (200, 200, 200)
#                         elif committed.startswith("RIGHT"):
#                             status_text, status_color = "RIGHT", (0, 255, 0)
#                         elif committed.startswith("START"):
#                             status_text, status_color = "START POSITION", (255, 255, 0)
#                         else:
#                             reason_txt = committed.split(":")[1] if ":" in committed else "Arm Movement"
#                             status_text, status_color = f"WRONG: {reason_txt}", (0, 0, 255)

#                         dbg_lines = [
#                             f"Elbow Angle: {dbg['angle']:.0f} deg",
#                             f"Torso Lean Dev: {dbg['lean_dev']:.1f} deg",
#                             f"Shoulder/Torso Ratio: {dbg['rotation_ratio']:.2f}",
#                             f"Other Arm Dev: {dbg['nonex_dev']:.2f}",
#                             f"Reach: {dbg['reach_total']:.2f} / {TARGET_REACH_RATIO:.2f}",
#                             f"Confidence: {m['min_vis']:.2f}",
#                             f"Arm State: {arm_state}",
#                         ]
#                         for i, line in enumerate(dbg_lines):
#                             cv2.putText(frame, line, (30, 40 + i * 26),
#                                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
#                     else:
#                         status_text, status_color = "WARMING UP", (255, 255, 0)

#             cv2.putText(frame, status_text, (max(10, w - 520), h - 40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 3)

#             cv2.imshow("Rehab Monitor", frame)
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 break
#             if key == ord('r'):
#                 mode, calib = "CALIBRATING", None
#                 calibrator.buffer.clear()
#                 smoother.buffers.clear()
#                 hysteresis.__init__(HYSTERESIS_FRAMES)

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()