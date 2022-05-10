import cv2
import numpy as np
from mss import mss
import win32api, win32con, win32gui
import logging
from mss import mss
import math
import time
import threading

logging.basicConfig(
    level=logging.INFO,
    format="[{levelname}] [{asctime}] {message}",
    style="{",
    datefmt="%I:%M:%S",
)

sct = mss()

class aim:
    def __init__(self, window_name, box_size, key):
        self.window_name = window_name
        self.box_size = box_size
        self.key = key

    def find_window_rect(self):
        logging.info(f"""Waiting for 2 seconds. Focus the game window.""")
        time.sleep(2)
        try:
            hwnd = win32gui.FindWindow(None, self.window_name)
            a, b, c, d = win32gui.GetWindowRect(hwnd)
            top = int(((c / 2) - (self.box_size / 2)))
            left = int(((d / 2) - (self.box_size / 2)))
            window = {
                "top": top,
                "left": left,
                "width": self.box_size,
                "height": self.box_size,
            }
            if a==-32000:
                if b==-32000:
                    if c==-31840:
                        if d==-31972:
                            logging.critical(f"""The window {self.window_name} is minimized. Exiting.""")
                            return
                            exit()
            else:
                logging.debug(f"""Dimensions of the window {self.window_name} are {c}x{d}.""")
                logging.debug(f"""Dimensions of the grabbing box are {window.get("width")}x{window.get("height")}.""")
                if self.box_size > 290:
                    logging.warn(f"""The boxsize {self.box_size} is larger than 290. The aimbot will detect the kill text as a contour.""")
                logging.info(f"""Starting up. Press Q on the OpenCV window to exit.""")
                return window
        except:
            logging.critical(f"""The window {self.window_name} is not opened. Exiting.""")
            return
            exit()

    def is_activated(self):
        return win32api.GetAsyncKeyState(self.key) != 0

    def capture_frame(dimensions):
        ret = np.array(sct.grab(dimensions))
        return ret


    def process_frame(frame, kernel=(10, 10), lower=np.array([139, 96, 129], np.uint8), upper=np.array([169, 255, 255], np.uint8)):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper) 
        dilate = cv2.dilate(mask, kernel)
        return dilate
    
    def find_contours(thing):
        contours, hierarchy = cv2.findContours(thing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # conv = map(lambda ct: cv2.convexHull(ct, False), contours)
        # return contours, conv
        return contours

    def click():
        threading.Thread(target=curve._click).start()
    
    def _click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def move_mouse(x, y):
        threading.Thread(target=curve._move_mouse, args=[x, y, 35]).start()

    def _move_mouse(x, y, smooth, h_sens=0.5, v_sens=0.6, speed=10000, time_speed=0.01, steps=300):
        """
        This function accepts x and y distances and moves the mouse accordingly as integers.
        Credit to OverBot for most of this function.
        """"""
        x = x * h_sens # vertical sensitivity multiplier
        y = y * v_sens # horizontal sensitivity multiplier

        rx = 0.0
        ry = 0.0

        for i in range(int(steps)):
            x_frac = rx + x / steps
            y_frac = ry + y / steps
            pix_x = int(x_frac)
            pix_y = int(y_frac)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(pix_x), int(pix_y), 0, 0)
            rx = x_frac - pix_x
            ry = y_frac - pix_y
        curve.click()
        """
        y = y
        a_movex = x / smooth
        a_movey = y / smooth

        for i in range(0, smooth + 1):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(a_movex), int(a_movey), 0, 0)
        curve.click()
