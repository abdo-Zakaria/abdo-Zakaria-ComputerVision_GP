
# import cv2
# import numpy as np
# import mediapipe as mp
# import freenect

# # --- 3. دالة سحب الصورة من كاميرا Kinect ---
# def get_kinect_frame():
#     # freenect ترجع الصورة بصيغة RGB افتراضياً
#     frame_rgb, _ = freenect.sync_get_video()
#     if frame_rgb is None:
#         return None
#     # تحويلها إلى BGR لتتوافق مع معالجة OpenCV الرسم والعرض
#     frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
#     return frame_bgr
# print("جاري تشغيل Kinect مع MediaPipe Pose... اضغط 'q' للخروج.")
# # --- 1. إعداد مكتبة MediaPipe القديمة (Solutions) ---
# mp_pose = mp.solutions.pose
# mp_drawing = mp.solutions.drawing_utils

# # --- 2. دالة حساب الزاوية بين 3 نقاط ---
# def calculate_angle(a, b, c):
#     a = np.array([a.x, a.y])
#     b = np.array([b.x, b.y])
#     c = np.array([c.x, c.y])
    
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
    
#     if angle > 180.0:
#         angle = 360 - angle
        
#     return angle


# # تحديد سماحية انحراف الكتفين (Shoulder Z Alignment Tolerance)
# SHOULDER_Z_TOLERANCE = 0.08  


# with mp_pose.Pose(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as pose:

#     while True:
#         # جلب الفريم من الكينكت بدلاً من الكاميرا المحلية
#         frame_raw = get_kinect_frame()
#         if frame_raw is None:
#             print("خطأ في قراءة الصورة من Kinect!")
#             break
            
#         frame = cv2.flip(frame_raw, 1)  # عكس الصورة كمرآة
#         h, w, _ = frame.shape
        
#         # تحويل الصورة إلى RGB لميديا بايب
#         image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(image_rgb)
        
#         status_text = "INITIALIZING"
#         status_color = (255, 255, 255)  # أبيض
        
#         if results.pose_landmarks:
#             landmarks = results.pose_landmarks.landmark
            
#             # استخراج النقاط المطلوبة
#             l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
#             r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
#             r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
#             r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            
#             # 1. حساب الفرق في العمق Z بين الكتفين
#             shoulder_z_diff = abs(r_shoulder.z - l_shoulder.z)
            
#             # 2. حساب متوسط Z للكتفين
#             avg_shoulder_z = (r_shoulder.z + l_shoulder.z) / 2.0
            
#             # 3. حساب Z الكوع بالنسبة لمستوى الكتفين
#             relative_elbow_z = r_elbow.z - avg_shoulder_z
            
#             # 4. حساب زاوية الكوع الأيمن
#             elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            
#             # --- التقييم والحسابات ---
#             if shoulder_z_diff > SHOULDER_Z_TOLERANCE:
#                 status_text = "WRONG: Keep Shoulders Straight!"
#                 status_color = (0, 0, 255)  # أحمر
#             else:
#                 if (90 <= elbow_angle <= 100) and (abs(relative_elbow_z) < 0.05):
#                     status_text = "START POSITION (Ready)"
#                     status_color = (255, 255, 0)  # أصفر
                
#                 elif (130 <= elbow_angle <= 160) and (relative_elbow_z < -0.05):
#                     status_text = "RIGHT"
#                     status_color = (0, 255, 0)  # أخضر
                
#                 else:
#                     status_text = "WRONG"
#                     status_color = (0, 0, 255)  # أحمر
            
#             # رسم الهيكل العظمي على الشاشة
#             mp_drawing.draw_landmarks(
#                 frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
#             # عرض البيانات على الشاشة
#             cv2.putText(frame, f"Elbow Angle: {int(elbow_angle)} deg", (30, 40), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#             cv2.putText(frame, f"Elbow Rel Z: {relative_elbow_z:.2f}", (30, 70), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#             cv2.putText(frame, f"Shoulders Z Diff: {shoulder_z_diff:.2f}", (30, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

#         # عرض النتيجة أسفل الشاشة
#         cv2.putText(frame, status_text, (w - 480, h - 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 3)
        
#         cv2.imshow("Rehab Monitor - Kinect + MediaPipe", frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# cv2.destroyAllWindows()

"""
Rehab Monitor - Kinect (real depth) version
=============================================

This is the same calibration-based design as the webcam version, upgraded to
use a genuine depth sensor. The earlier version's core limitation was that a
single 2D camera cannot fully separate torso yaw rotation from a small
depth-direction shift, and forward-reach could only be estimated from
MediaPipe's noisy monocular Z. With a Kinect we have real per-pixel depth, so
every landmark can be back-projected into true 3D millimeters and the
geometry becomes exact rather than a proxy:

  - Torso ROTATION  -> a genuine yaw angle from the real 3D shoulder vector
                        (no more shoulder-width/torso-length ratio proxy).
  - Torso LEAN       -> one 3D angle from vertical that captures sideways
                        lean AND forward/backward hunching simultaneously
                        (impossible to see with a single 2D camera).
  - Arm REACH        -> a true 3D distance in a torso-local coordinate frame
                        built from real 3D axes (no down-weighted Z hack).
  - Elbow ANGLE       -> computed from real 3D vectors, not just the image
                        plane.

All robustness thresholds are still derived from per-session calibration
statistics (mean +/- STD_MULTIPLIER * std), floored by small noise margins.
The only "designer" numbers are the PROTOCOL parameters (target angle range,
target reach) describing what the prescribed exercise looks like.

Depth caveats (read before relying on this for anything clinical):
  - Kinect v1's usable depth range is roughly 0.5-4.5 m; outside that, depth
    reads as invalid/zero and is filtered out (DEPTH_MIN_MM/DEPTH_MAX_MM).
  - Depth has holes (dark/reflective clothing, edges) - a small neighborhood
    median sample is used, and if no valid depth is found near a landmark,
    the frame is treated as low-confidence, same as low MediaPipe visibility.
  - The RGB and depth (IR) sensors on Kinect v1 are physically offset by a
    few centimeters, so pixel-for-pixel alignment is approximate. This is
    usually small relative to body-part size at 1.2-3.5 m, but for tighter
    precision use a proper RGB-to-depth calibration/registration.
  - The intrinsics below are typical published Kinect v1 factory values, not
    a per-unit calibration. Since every threshold here is a *delta from a
    calibration baseline*, moderate intrinsic error mostly cancels out.

Requires: opencv-python, mediapipe, numpy, and a working freenect / libfreenect
Python binding with the Kinect connected.

Controls: 'q' to quit, 'r' to re-calibrate.
"""

import math
from collections import deque
from statistics import mean, median, pstdev

import cv2
import numpy as np
import mediapipe as mp
import freenect

# ============================================================
# CONFIGURATION
# ============================================================

EXERCISE_SIDE = "RIGHT"  # "RIGHT" or "LEFT" -- which arm is exercising

# --- Protocol parameters (clinically defined, NOT robustness thresholds) ---
TARGET_ELBOW_ANGLE_RANGE = (130, 180)
TARGET_REACH_RATIO = 0.35  # normalized 3D displacement (units of torso length)

# --- Calibration ---
CALIBRATION_FRAMES = 45
CALIB_STABILITY_STD_DEG = 10

# --- Robustness / smoothing ---
SMOOTHING_WINDOW = 7
HYSTERESIS_FRAMES = 6
VISIBILITY_THRESHOLD = 0.5     # mediapipe landmark visibility cutoff
STD_MULTIPLIER = 3.0

# Noise floors (sensor-noise margins, not exercise logic)
MIN_YAW_DEG = 8.0
MIN_LEAN_DEG = 6.0
MIN_ARM_DISP_FRAC = 0.12
MIN_START_ANGLE_MARGIN = 8.0

# --- Kinect depth ---
DEPTH_MIN_MM = 500     # ~0.5 m, below Kinect v1's reliable range
DEPTH_MAX_MM = 4500    # ~4.5 m, above Kinect v1's reliable range
DEPTH_SAMPLE_RADIUS = 2  # neighborhood (pixels) searched for a valid depth read

# Typical published Kinect v1 factory intrinsics (640x480). Not a per-unit
# calibration -- see module docstring for why that's acceptable here.
DEPTH_FX = 594.21
DEPTH_FY = 591.04
DEPTH_CX = 339.5
DEPTH_CY = 242.7

# ============================================================
# MEDIAPIPE SETUP
# ============================================================

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
PL = mp_pose.PoseLandmark

SIDE_MAP = {
    "RIGHT": dict(shoulder=PL.RIGHT_SHOULDER, elbow=PL.RIGHT_ELBOW, wrist=PL.RIGHT_WRIST,
                  other_wrist=PL.LEFT_WRIST),
    "LEFT": dict(shoulder=PL.LEFT_SHOULDER, elbow=PL.LEFT_ELBOW, wrist=PL.LEFT_WRIST,
                 other_wrist=PL.RIGHT_WRIST),
}
SIDE = SIDE_MAP[EXERCISE_SIDE]

LANDMARK_NAMES = {
    "l_sh": PL.LEFT_SHOULDER, "r_sh": PL.RIGHT_SHOULDER,
    "l_hip": PL.LEFT_HIP, "r_hip": PL.RIGHT_HIP,
    "ex_sh": SIDE["shoulder"], "ex_el": SIDE["elbow"], "ex_wr": SIDE["wrist"],
    "ox_wr": SIDE["other_wrist"],
}


# ============================================================
# KINECT FRAME ACQUISITION
# ============================================================

def get_kinect_frames():
    """Returns (bgr_frame, depth_mm) mirror-flipped and pixel-aligned in size.
    depth_mm is a uint16/float array in millimeters (0 = invalid read)."""
    rgb, _ = freenect.sync_get_video()
    depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
    if rgb is None or depth is None:
        return None, None

    frame_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    frame_bgr = cv2.flip(frame_bgr, 1)
    depth = cv2.flip(depth, 1)

    if depth.shape[:2] != frame_bgr.shape[:2]:
        depth = cv2.resize(depth, (frame_bgr.shape[1], frame_bgr.shape[0]),
                            interpolation=cv2.INTER_NEAREST)
    return frame_bgr, depth


# ============================================================
# 3D GEOMETRY HELPERS
# ============================================================

def sample_depth(depth_img, px, py, radius=DEPTH_SAMPLE_RADIUS):
    """Median of valid depth readings in a small window around (px, py)."""
    h, w = depth_img.shape[:2]
    x0, x1 = max(0, px - radius), min(w, px + radius + 1)
    y0, y1 = max(0, py - radius), min(h, py + radius + 1)
    patch = depth_img[y0:y1, x0:x1]
    valid = patch[(patch >= DEPTH_MIN_MM) & (patch <= DEPTH_MAX_MM)]
    if valid.size == 0:
        return None
    return float(np.median(valid))


def backproject(px, py, depth_mm):
    """Pixel + depth -> real-world (X, Y, Z) in millimeters, camera-centered."""
    x = (px - DEPTH_CX) * depth_mm / DEPTH_FX
    y = (py - DEPTH_CY) * depth_mm / DEPTH_FY
    z = float(depth_mm)
    return np.array([x, y, z], dtype=float)


def normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-6 else v


def angle_3d(a, b, c):
    """Angle at point b (a-b-c) using true 3D vectors."""
    v1, v2 = a - b, c - b
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 < 1e-6 or n2 < 1e-6:
        return 0.0
    cosang = np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0)
    return math.degrees(math.acos(cosang))


def get_pts3d(landmarks, w, h, depth_img):
    pts = {}
    for name, idx in LANDMARK_NAMES.items():
        lm = landmarks[idx.value]
        px = int(np.clip(lm.x * w, 0, w - 1))
        py = int(np.clip(lm.y * h, 0, h - 1))
        d = sample_depth(depth_img, px, py)
        p3 = backproject(px, py, d) if d is not None else None
        pts[name] = dict(px=px, py=py, p3=p3, vis=lm.visibility, depth_valid=d is not None)
    return pts


def compute_metrics(pts):
    l_sh, r_sh, l_hip, r_hip = pts["l_sh"]["p3"], pts["r_sh"]["p3"], pts["l_hip"]["p3"], pts["r_hip"]["p3"]
    ex_sh, ex_el, ex_wr, ox_wr = pts["ex_sh"]["p3"], pts["ex_el"]["p3"], pts["ex_wr"]["p3"], pts["ox_wr"]["p3"]

    sh_mid = (l_sh + r_sh) / 2.0
    hip_mid = (l_hip + r_hip) / 2.0

    shoulder_vec = r_sh - l_sh
    shoulder_width_mm = float(np.linalg.norm(shoulder_vec))

    torso_vec = sh_mid - hip_mid
    torso_length_mm = max(float(np.linalg.norm(torso_vec)), 1.0)

    # True yaw: angle of the real 3D shoulder vector in the camera's X-Z plane.
    # ~0 deg when squarely facing the camera; grows as the patient rotates.
    yaw_angle = math.degrees(math.atan2(shoulder_vec[2], shoulder_vec[0]))

    # True lean: angle of the torso vector from vertical, in full 3D (catches
    # sideways lean AND forward/backward hunch in one number).
    lean_angle = math.degrees(math.acos(np.clip(-torso_vec[1] / torso_length_mm, -1.0, 1.0)))

    # Torso-local 3D frame.
    up = normalize(torso_vec)
    right = normalize(shoulder_vec)
    right = normalize(right - up * np.dot(right, up))  # orthogonalize vs. up
    forward = normalize(np.cross(right, up))

    def to_local(p3):
        v = p3 - sh_mid
        u = float(np.dot(v, right)) / torso_length_mm
        vv = float(np.dot(v, up)) / torso_length_mm
        f = float(np.dot(v, forward)) / torso_length_mm
        return (u, vv, f)

    ex_el_local = to_local(ex_el)
    ox_wr_local = to_local(ox_wr)

    elbow_angle = angle_3d(ex_sh, ex_el, ex_wr)

    min_vis = min(pts[k]["vis"] for k in LANDMARK_NAMES)

    return dict(
        shoulder_width_mm=shoulder_width_mm, torso_length_mm=torso_length_mm,
        yaw_angle=yaw_angle, lean_angle=lean_angle, elbow_angle=elbow_angle,
        ex_el_local=ex_el_local, ox_wr_local=ox_wr_local, min_vis=min_vis,
    )


def local_dist(a, b):
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


# ============================================================
# CALIBRATION
# ============================================================

class Calibrator:
    def __init__(self):
        self.buffer = []

    def add(self, m):
        self.buffer.append(m)

    def ready(self):
        return len(self.buffer) >= CALIBRATION_FRAMES

    def is_stable(self):
        angles = [m["elbow_angle"] for m in self.buffer]
        return pstdev(angles) <= CALIB_STABILITY_STD_DEG if len(angles) > 1 else True

    def finalize(self):
        def stat(key):
            vals = [m[key] for m in self.buffer]
            return mean(vals), (pstdev(vals) if len(vals) > 1 else 0.0)

        yaw_mean, yaw_std = stat("yaw_angle")
        lean_mean, lean_std = stat("lean_angle")
        angle_mean, angle_std = stat("elbow_angle")

        ox_vals = [m["ox_wr_local"] for m in self.buffer]
        ox_mean = tuple(mean(c) for c in zip(*ox_vals))
        ox_std = tuple(pstdev(c) if len(c) > 1 else 0.0 for c in zip(*ox_vals))

        ex_vals = [m["ex_el_local"] for m in self.buffer]
        ex_start_local = tuple(mean(c) for c in zip(*ex_vals))

        thresholds = dict(
            yaw_thresh=max(STD_MULTIPLIER * yaw_std, MIN_YAW_DEG),
            lean_thresh=max(STD_MULTIPLIER * lean_std, MIN_LEAN_DEG),
            nonex_thresh=max(STD_MULTIPLIER * math.sqrt(sum(s ** 2 for s in ox_std)), MIN_ARM_DISP_FRAC),
            start_angle_low=angle_mean - max(STD_MULTIPLIER * angle_std, MIN_START_ANGLE_MARGIN),
            start_angle_high=angle_mean + max(STD_MULTIPLIER * angle_std, MIN_START_ANGLE_MARGIN),
        )

        return dict(
            yaw_mean=yaw_mean, lean_mean=lean_mean,
            ox_mean=ox_mean, ex_start_local=ex_start_local,
            thresholds=thresholds,
        )


# ============================================================
# SMOOTHING
# ============================================================

class Smoother:
    def __init__(self, window):
        self.window = window
        self.buffers = {}

    def push(self, key, value):
        self.buffers.setdefault(key, deque(maxlen=self.window)).append(value)

    def get(self, key):
        buf = self.buffers.get(key)
        return median(buf) if buf else None

    def get_triple(self, k1, k2, k3):
        a, b, c = self.get(k1), self.get(k2), self.get(k3)
        return (a, b, c) if None not in (a, b, c) else None

    def full(self):
        return bool(self.buffers) and all(len(b) >= self.window for b in self.buffers.values())


# ============================================================
# CLASSIFICATION
# ============================================================

def classify(s, calib):
    th = calib["thresholds"]

    yaw_dev = abs(s["yaw_angle"] - calib["yaw_mean"])
    rotation_ok = yaw_dev <= th["yaw_thresh"]

    lean_dev = abs(s["lean_angle"] - calib["lean_mean"])
    lean_ok = lean_dev <= th["lean_thresh"]

    nonex_dev = local_dist(s["ox_wr_local"], calib["ox_mean"])
    nonex_ok = nonex_dev <= th["nonex_thresh"]

    posture_ok = rotation_ok and lean_ok and nonex_ok
    reason = None
    if not rotation_ok:
        reason = "Torso Rotating"
    elif not lean_ok:
        reason = "Torso Leaning"
    elif not nonex_ok:
        reason = "Other Arm Moving"

    angle = s["elbow_angle"]
    reach_total = local_dist(s["ex_el_local"], calib["ex_start_local"])

    if th["start_angle_low"] <= angle <= th["start_angle_high"] and reach_total < TARGET_REACH_RATIO * 0.5:
        arm_state = "START"
    elif TARGET_ELBOW_ANGLE_RANGE[0] <= angle <= TARGET_ELBOW_ANGLE_RANGE[1] and reach_total >= TARGET_REACH_RATIO:
        arm_state = "TARGET"
    else:
        arm_state = "MID"

    if not posture_ok:
        label = "WRONG"
    elif arm_state == "START":
        label = "START"
    elif arm_state == "TARGET":
        label = "RIGHT"
    else:
        label = "WRONG"

    debug = dict(angle=angle, yaw_dev=yaw_dev, lean_dev=lean_dev,
                 nonex_dev=nonex_dev, reach_total=reach_total)
    return label, reason, arm_state, debug


class Hysteresis:
    def __init__(self, frames):
        self.frames = frames
        self.candidate = None
        self.streak = 0
        self.committed = "INITIALIZING"

    def update(self, candidate):
        if candidate == self.candidate:
            self.streak += 1
        else:
            self.candidate = candidate
            self.streak = 1
        if self.streak >= self.frames:
            self.committed = candidate
        return self.committed


# ============================================================
# MAIN LOOP
# ============================================================

def main():
    smoother = Smoother(SMOOTHING_WINDOW)
    calibrator = Calibrator()
    hysteresis = Hysteresis(HYSTERESIS_FRAMES)
    calib = None
    mode = "CALIBRATING"

    print("Starting Kinect + MediaPipe Pose... press 'q' to quit, 'r' to re-calibrate.")

    try:
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                frame, depth = get_kinect_frames()
                if frame is None:
                    print("Error reading frame from Kinect!")
                    break

                h, w, _ = frame.shape
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(rgb)

                status_text, status_color = "NO PERSON DETECTED", (255, 255, 255)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    pts = get_pts3d(landmarks, w, h, depth)
                    depth_ok = all(pts[k]["depth_valid"] for k in LANDMARK_NAMES)

                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    cv2.line(frame, (pts["l_sh"]["px"], pts["l_sh"]["py"]),
                              (pts["r_sh"]["px"], pts["r_sh"]["py"]), (0, 200, 255), 2)
                    sh_mid_px = ((pts["l_sh"]["px"] + pts["r_sh"]["px"]) // 2,
                                 (pts["l_sh"]["py"] + pts["r_sh"]["py"]) // 2)
                    hip_mid_px = ((pts["l_hip"]["px"] + pts["r_hip"]["px"]) // 2,
                                  (pts["l_hip"]["py"] + pts["r_hip"]["py"]) // 2)
                    cv2.line(frame, sh_mid_px, hip_mid_px, (255, 200, 0), 2)

                    min_vis = min(pts[k]["vis"] for k in LANDMARK_NAMES)

                    if not depth_ok:
                        status_text = "DEPTH DATA MISSING - move within ~0.8-4m of Kinect"
                        status_color = (0, 165, 255)
                    elif min_vis < VISIBILITY_THRESHOLD:
                        status_text, status_color = "LOW CONFIDENCE - adjust position", (0, 165, 255)

                    elif mode == "CALIBRATING":
                        m = compute_metrics(pts)
                        calibrator.add(m)
                        status_text = f"CALIBRATING {len(calibrator.buffer)}/{CALIBRATION_FRAMES} - hold start pose"
                        status_color = (255, 255, 0)
                        if calibrator.ready():
                            if calibrator.is_stable():
                                calib = calibrator.finalize()
                                mode = "RUNNING"
                            else:
                                calibrator.buffer.clear()

                    else:
                        m = compute_metrics(pts)
                        smoother.push("yaw_angle", m["yaw_angle"])
                        smoother.push("lean_angle", m["lean_angle"])
                        smoother.push("elbow_angle", m["elbow_angle"])
                        smoother.push("ex_u", m["ex_el_local"][0])
                        smoother.push("ex_v", m["ex_el_local"][1])
                        smoother.push("ex_f", m["ex_el_local"][2])
                        smoother.push("ox_u", m["ox_wr_local"][0])
                        smoother.push("ox_v", m["ox_wr_local"][1])
                        smoother.push("ox_f", m["ox_wr_local"][2])

                        if smoother.full():
                            s = dict(
                                yaw_angle=smoother.get("yaw_angle"),
                                lean_angle=smoother.get("lean_angle"),
                                elbow_angle=smoother.get("elbow_angle"),
                                ex_el_local=smoother.get_triple("ex_u", "ex_v", "ex_f"),
                                ox_wr_local=smoother.get_triple("ox_u", "ox_v", "ox_f"),
                            )
                            label, reason, arm_state, dbg = classify(s, calib)
                            candidate = f"{label}:{reason}" if reason else label
                            committed = hysteresis.update(candidate)

                            if committed == "INITIALIZING":
                                status_text, status_color = "ANALYZING...", (200, 200, 200)
                            elif committed.startswith("RIGHT"):
                                status_text, status_color = "RIGHT", (0, 255, 0)
                            elif committed.startswith("START"):
                                status_text, status_color = "START POSITION", (255, 255, 0)
                            else:
                                reason_txt = committed.split(":")[1] if ":" in committed else "Arm Movement"
                                status_text, status_color = f"WRONG: {reason_txt}", (0, 0, 255)

                            dbg_lines = [
                                f"Elbow Angle: {dbg['angle']:.0f} deg",
                                f"Yaw Dev: {dbg['yaw_dev']:.1f} deg",
                                f"Lean Dev: {dbg['lean_dev']:.1f} deg",
                                f"Other Arm Dev: {dbg['nonex_dev']:.2f}",
                                f"Reach: {dbg['reach_total']:.2f} / {TARGET_REACH_RATIO:.2f}",
                                f"Confidence: {min_vis:.2f}",
                                f"Arm State: {arm_state}",
                            ]
                            for i, line in enumerate(dbg_lines):
                                cv2.putText(frame, line, (30, 40 + i * 26),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                        else:
                            status_text, status_color = "WARMING UP", (255, 255, 0)

                cv2.putText(frame, status_text, (max(10, w - 560), h - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 3)

                cv2.imshow("Rehab Monitor - Kinect + MediaPipe", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                if key == ord('r'):
                    mode, calib = "CALIBRATING", None
                    calibrator.buffer.clear()
                    smoother.buffers.clear()
                    hysteresis.__init__(HYSTERESIS_FRAMES)
    finally:
        cv2.destroyAllWindows()
        try:
            freenect.sync_stop()
        except Exception:
            pass


if __name__ == "__main__":
    main()