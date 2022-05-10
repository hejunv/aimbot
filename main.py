from lib import aim
import numpy as np
import cv2
import time

curve = aim("Overwatch", 400, 0x05)

dimensions = curve.find_window_rect()

while True: # check perf diff if mss() as sct here or in lib.py AND TODO add threading here
    last_time = time.time()

    frame = curve.capture_frame(dimensions)
    cv2.rectangle(frame, (100, 180), (1000, 180), (255, 255,255), -1)
    processed = curve.process_frame(frame)
    # contours, conv = curve.find_contours(processed)
    contours = curve.find_contours(processed)
    if len(contours) != 0:
        sort = sorted(contours, key=cv2.contourArea, reverse=True)
        new = []
        for i in sort:
            if cv2.contourArea(i) > 400:
                new.append(i)
        cv2.drawContours(frame, new, -1, (0, 255, 0), 8)
        if len(new) != 0:
            M = cv2.moments(new[-1])
            if M["m00"]:
                cX = (M["m10"] / M["m00"])
                cY = (M["m01"] / M["m00"])
                cv2.circle(frame, (int(cX), int(cY)), 10, (0, 0, 255), -1)
                xf = -(290/2 - cX)
                yf = -(290/2 - cY)
                if curve.is_activated():
                    curve.move_mouse(xf, yf)

    cnt = str(int(f"{round(1 / (time.time() - last_time))}"))
    cv2.putText(frame, f"FPS {cnt}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0, 255), 2)
    cv2.imshow("frame", frame)
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        exit()
