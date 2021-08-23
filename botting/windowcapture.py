import numpy as np
import pyautogui
import cv2 as cv
from threading import Thread, Lock

class WindowCapture:

    #threading options
    stopped = True
    lock = None
    screenshot = None
    #properties

    def get_screenshot(self):
        screenshot = pyautogui.screenshot(region=(0,0, 800, 550))
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        return screenshot

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
    
    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            screenshot = self.get_screenshot()
            #self.lock.acquire()
            self.screenshot = screenshot
            #self.lock.release()

