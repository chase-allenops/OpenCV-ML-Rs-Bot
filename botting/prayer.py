import cv2 as cv
import pyautogui
from threading import Thread, Lock
import numpy as np

class Prayer:
    # constants
    # threading properties
    stopped = True
    lock = None
    # properties
    screenshot = None

    def __init__(self):
        
        self.lock = Lock()
        self.pp = cv.imread('pp40.JPG', cv.IMREAD_UNCHANGED)
        self.suppray = cv.imread('suppray.jpg', cv.IMREAD_UNCHANGED)
        self.needle_w = self.suppray.shape[1]
        self.needle_h = self.suppray.shape[0]

    def checkPray(self, screenshot):
        self.screenshot = screenshot
        level = cv.matchTemplate(self.screenshot, self.pp, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(level)
        if max_val >= 0.80:
            print("Prayer is at 40.")
            potions = cv.matchTemplate(self.screenshot, self.suppray, cv.TM_CCOEFF_NORMED)
            locations = np.where(potions >= 0.8)
            locations = list(zip(*locations[::-1]))
            if not locations:
                return np.array([], dtype=np.int32).reshape(0,4)
            rectangles = []
            for loc in locations:
                rect = [int(loc[0]), int(loc[1],), self.needle_w, self.needle_h]
                rectangles.append(rect)
                rectangles.append(rect) 
            rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
            points = []
            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
            points.append((center_x, center_y))
            target = points[0]
            pyautogui.moveTo(x=target[0], y=target[1])
            pyautogui.click()
        else:
            False
            
    def start(self):
        self.stopped = False
        t = Thread(target=self.checkPray)
        t.start()

    # def run(self):
    #     while not self.stopped:
    #         if self.checkPray == True:
    #             self.usePotion
    #         continue


    def stop(self):
        self.stopped = True
