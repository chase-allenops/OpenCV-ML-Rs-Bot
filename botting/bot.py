import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock


class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    COMBAT = 3

class AbbyBot:

    #constants
    INITIALIZING_SECONDS = 3
    COMBAT_SECONDS = 30
    MOVEMENT_STOPPED_THRESHOLD = 0.975

    #threading properties
    stopped = True
    lock = None

    #properties
    state = None
    targets = []
    screenshot = None
    timestamp = None
    movement_screenshot = None

    def __init__(self):
        self.lock = Lock()
        self.state = BotState.INITIALIZING
        self.timestamp = time()

    def have_stopped_moving(self):
        if self.movement_screenshot is None:
            self.movement_screenshot = self.screenshot.copy()
            return False
        result = cv.matchTemplate(self.screenshot, self.movement_screenshot, cv.TM_CCOEFF_NORMED)
        similarity = result[0][0]
        print('Movement detection similarity: {}'.format(similarity))
        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            print('Movement detected stop')
            return True
        self.movement_screenshot = self.screenshot.copy()
        return False

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()
    
    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True
    
    # main logic controller
    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()

            elif self.state == BotState.SEARCHING:
                success = self.click_next_target()
                if success:
                    self.lock.acquire()
                    self.state = BotState.MOVING
                    self.lock.release()

            elif self.state == BotState.MOVING:
                if not self.have_stopped_moving():
                    sleep(0.500)
                else:
                    self.lock.acquire()
                    self.timestamp = time()
                    self.state = BotState.COMBAT
                    self.lock.release()
            
            elif self.state == BotState.COMBAT:
                if time() > self.timestamp + self.COMBAT_SECONDS:
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()




