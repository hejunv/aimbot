import cv2
import numpy as np
from mss import mss
import time
import win32api, win32con, win32gui
from win32 import win32api
import win32con
import math

# fixes a bug that appears at over 100% DPI settings
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

monX = 1920
monY = 1080
boxsize = 290

lower = np.array([139,96,129])
upper = np.array([169,255,255])

def get_cursor():
    flags, hcursor, (x,y) = win32gui.GetCursorInfo() # grab current cursor information
    return [x, y]

def find_window_rect(name):
    '''
    Input <-- string
    Output --> list([])
    '''
    try:
        hwnd = win32gui.FindWindow(None, name)
        a, b, c, d = win32gui.GetWindowRect(hwnd)
        window = {
            'top': 395,
            'left': 815,
            'width': 290,
            'height': 290
        }
        return window
    except win32gui.error:
        return 0

def is_activated():
    return win32api.GetAsyncKeyState(0x01) != 0 # 0x06=mouse5, 0x01=left, 0x14=capslock

def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

with mss() as sct:
    dimensions = find_window_rect("Overwatch")
    kernel = np.ones((4, 4), np.uint8)
    lower = np.array([139,96,129], np.uint8)
    upper = np.array([169,255,255], np.uint8)
    mid = 290 / 2
    while True:
        last_time = time.time()

        screen = np.array(sct.grab(dimensions))
        cv2.startWindowThread() # TODO test for performance difference
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        ran = cv2.inRange(hsv, lower, upper)
        contours, hierarchy = cv2.findContours(ran, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        '''
        if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(ran)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(screen, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(screen, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            xf = -(mid - cX)
            yf = -(mid - cY)
            if is_activated():
                mouse_move(int(xf), int(yf))
        '''

        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])
            cv2.drawContours(screen, [c], -1, (0, 255, 255), 2)
            width = extRight[0] - extLeft[0]
            height = extBot[1] - extTop[1]
            if is_activated():
                M = cv2.moments(ran)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(screen, (cX, cY), 5, (255, 255, 255), -1)
                cv2.putText(screen, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                xf = -(mid - cX)
                yf = -(mid - cY) + 13
                mouse_move(int(xf), int(yf))
                
        
        cnt = int(f"{round(1 / (time.time() - last_time))}")
        cv2.putText(screen, f"FPS {cnt}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 2)
        cv2.imshow('--SCREEN--', screen)
        # print(f"fps: {int(cnt)}")

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            cv2.destroyAllWindows()
            break
