import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time, sleep
from vision import Vision
from windowcapture import WindowCapture
from threading import Thread
from detection import Detection
from prayer import Prayer
#from bot import AbbyBot, BotState

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# load in the trained cascade model
#cascade_abbydemons = cv.CascadeClassifier('C:/Users/chase/Desktop/Python/OpenCVBots/machine-learning/cascade/cascade.xml')
# load empty Vision class
detector = Detection('C:/Users/chase/Desktop/Python/OpenCVBots/machine-learning/cascade/cascade.xml')
vision = Vision(None)
wincap = WindowCapture()
prayer = Prayer()

#bot = AbbyBot()

bot_in_action = False
# bot actions
def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = Vision.get_click_points(rectangles)
        target = targets[0]
        pyautogui.moveTo(x=target[0], y=target[1], duration=0.1)
        pyautogui.click()
        sleep(33)
    global bot_in_action
    bot_in_action = False

detector.start()
#bot.start()
wincap.start()
# prayer.start()

loop_time = time()
while(True):

    if wincap.screenshot is None:
        continue

    # do object detection
    detector.update(wincap.screenshot)

    wincap.screenshot = vision.draw_rectangles(wincap.screenshot, detector.rectangles)

    cv.imshow('Matches', wincap.screenshot)

    prayer.checkPray(wincap.screenshot)

    #bot action function, using multi thread
    if not bot_in_action:
        bot_in_action = True
        t = Thread(target = bot_actions, args = (detector.rectangles,))
        t.start()

    

    # if bot.state == BotState.INITIALIZING:
    #     targets = vision.get_click_points(detector.rectangles)
    #     bot.update(screenshot, targets)

    # if bot.state == BotState.SEARCHING:
    #     targets = vision.get_click_points(detector.rectangles)
    #     bot.update_targets(targets)
    #     bot.update_screenshot(screenshot)
    
    # elif bot.state == BotState.MOVING:
    #     bot.update_screenshot(screenshot)
    
    # elif bot.state == BotState.COMBAT:
    #     pass

    #debug loop rate 
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #press 'q' with the output window focused to exit. 
    #waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        detector.stop()
        #bot.stop()
        wincap.stop()
        prayer.stop()
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), wincap.screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), wincap.screenshot)
        
print('Done.')

