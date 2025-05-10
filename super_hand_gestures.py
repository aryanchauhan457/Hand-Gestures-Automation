import cv2
from mediapipe import solutions
from psutil import process_iter
from subprocess import Popen, run
from threading import Thread
from time import sleep
from math import sqrt
from keyboard import press_and_release
# Functions work by touching fingers with thumb.
# Below are given functions you can see.
# 
#
def check_app(app):
    for process in process_iter():
        if app in process.name().lower():
            return True
    return False

index_status = 0
thumb_little_base_status = 0
clockwise_status = 0
ring_status = 0
middle_status = 0
flip_status = 0

def index():
    global index_status
    if index_status == 0:
        index_status = 1
        print("Index")
        try:
            press_and_release('windows + d')
        except:
            pass
        sleep(1)
        index_status = 0
        
def middle():
    global middle_status
    if middle_status == 0:
        middle_status = 1
        print("Middle")
        try:
            press_and_release('alt + tab')
            sleep(2)
        except:
            pass
        middle_status = 0
        
def ring():
    global ring_status
    if ring_status == 0:
        ring_status = 1
        print("Ring")
        try:
            press_and_release('alt + f4')
            sleep(2)
        except:
            pass
        ring_status = 0
        
def flip():
    global flip_status
    if flip_status == 0:
        flip_status = 1
        print('Flip')
        try:
            press_and_release('enter')
            sleep(0.1)
            press_and_release('space')
            sleep(1)
        except:
            pass
        flip_status = 0
        
def thumb_little_base():
    global thumb_little_base_status
    if thumb_little_base_status == 0:
        thumb_little_base_status = 1
        print('Thumb_Little_Base')
        try:
            press_and_release('alt + f4')
            sleep(2)
        except:
            pass
        thumb_little_base_status = 0

def clockwise():
    global clockwise_status
    if clockwise_status == 0:
        clockwise_status = 1
        print("Clockwise")
        try:
            press_and_release('alt + tab')
            sleep(2)
        except:
            pass
        clockwise_status = 0

capture_hands = solutions.hands.Hands()
camera = cv2.VideoCapture(0)
x8 = y8 = x12 = y12 = x16 = y16 = x4 = y4 = x20 = y20 = x9 = y9 = x5 = y5 = x0 = y0 = x17 = y17 = 0

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame_height, frame_width, _ = frame.shape
    frame = cv2.flip(frame, 1)
    average = cv2.blur(frame, (5,5))
    gray = cv2.cvtColor(average, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(average, cv2.COLOR_BGR2RGB)

    output_hands = capture_hands.process(rgb)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            for idx, landmark in enumerate(hand.landmark):
                x, y = int(landmark.x * frame_width), int(landmark.y * frame_height)
                if idx == 8:
                    #index
                    x8, y8 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 5:
                    #index base
                    x5, y5 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 12:
                    #middle
                    x12, y12 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 9:
                    #base of middle
                    x9, y9 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 16:
                    #ring
                    x16, y16 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 20:
                    #little
                    x20, y20 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 17:
                    #little base
                    x17, y17 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 4:
                    #thumb
                    x4, y4 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                elif idx == 0:
                    #wrist
                    x0, y0 = x, y
                    cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                # elif idx == 2:
                #     #thumb base
                #     x6, y6 = x, y
                #     cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)

    dist_thumb_index = sqrt(((x4-x8)**2)+((y4-y8)**2))
    dist_thumb_little = max(abs(x4-x20)+1, abs(y4-y20)+1)
    dist_thumb_little_base = max(abs(x17-x4)+1,abs(y17-y4)+1)
    dist_thumb_ring = sqrt(((x4-x16)**2)+((y4-y16)**2))
    dist_thumb_middle = sqrt(((x4-x12)**2)+((y4-y12)**2))
    dist_indexbase_middlebase = sqrt(((x5-x9)**2)+((y5-y9)**2))
    
    # print(dist_thumb_ring//dist_indexbase_middlebase)

    # print(dist_thumb_little,  dist_thumb_little//dist_indexbase_middlebase)
    # sleep(1)
    
    if all_hands:
        if abs(y16-y0)//dist_indexbase_middlebase > 4:
            if dist_thumb_index//dist_indexbase_middlebase < 1:
                if index_status == 0:
                    thread = Thread(target=index)
                    thread.start()
            elif dist_thumb_middle//dist_indexbase_middlebase < 2:
                if ring_status == 0:
                    thread = Thread(target=middle)
                    thread.start()
                    
            elif dist_thumb_little//dist_indexbase_middlebase < 1:
                break
            
            elif dist_thumb_ring//dist_indexbase_middlebase == 0:
                if ring_status == 0:
                    thread = Thread(target=ring)
                    thread.start()
                    
            # elif sqrt(((x5-x17)**2)+((y5-y17)**2))//dist_indexbase_middlebase <2:
            #     if flip_status == 0:
            #         thread = Thread(target=flip)
            #         thread.start()
            # elif dist_thumb_index//dist_indexbase_middlebase > 3 and abs(y8-y4)//dist_indexbase_middlebase < 3:
            #     if clockwise_status == 0:
            #         thread = Thread(target=clockwise)        
            #         thread.start()
            
    # cv2.imshow('Hand Gesture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # sleep(0.3)

camera.release()
cv2.destroyAllWindows()


