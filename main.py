import cv2                      #importing the opencv library (camera)
import mediapipe as mp          #importing the mediapipe library (hand tracking)
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()              #initialize the hand tracking model
drawing_utils = mp.solutions.drawing_utils              #initialize the drawing utilities
screen_width, screen_height = pyautogui.size()          #get the screen width and height

index_x, index_y = 0, 0
thumb_x, thumb_y = 0, 0
click_delay = 0.2  # Delay between clicks
last_click_time = time.time()

while True:
    _, frame = cap.read()                               #read the frame
    frame = cv2.flip(frame, 1)                          #flip the frame
    frame_height, frame_width, _ = frame.shape          #get the frame height and width
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  #convert the frame to RGB
    output = hand_detector.process(rgb_frame)           #process the frame
    hands = output.multi_hand_landmarks                 #get the landmarks of the hand
    if hands:                                           #if the hand is detected
        for hand in hands:                              #for each hand
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark                   #get the landmarks
            for id, landmark in enumerate(landmarks):   #for each landmark
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)        #x & y is multiplied by frame width and height 
                                                        #because the landmarks are in the range of 0 to 1

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  #draw a circle on the tip of the index finger
                    index_x = screen_width/frame_width*x            #get the x coordinate of the index finger
                    index_y = screen_height/frame_height*y          #get the y coordinate of the index finger
                    pyautogui.moveTo(index_x, index_y)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  #draw a circle on the tip of the index finger
                    thumb_x = screen_width/frame_width*x            #get the x coordinate of the index finger
                    thumb_y = screen_height/frame_height*y          #get the y coordinate of the index finger
            
            if abs(index_y - thumb_y) < 30 and abs(index_x - thumb_x) < 30:
                current_time = time.time()
                if current_time - last_click_time > click_delay:
                    pyautogui.click()
                    last_click_time = current_time

    cv2.imshow('Virtual Mouse', frame)                  #show the frame
    if cv2.waitKey(1) & 0xFF == 27:  # quit the camera when ESC is pressed
        break

