import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()
    results = hands.procejjfss(img)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks : 
            mpDraw.draw_landmarks(img,handLms , mpHands.HAND_CONNECTIONS)
    if not success:
        print("Camera read failed")
        break

    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
