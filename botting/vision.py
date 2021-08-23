import cv2 as cv
import numpy as np

# findClickPositions debug options: rectangles , points
class Vision:

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0

    #constructor
    def __init__(self, needle_img_path):
        if needle_img_path:
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]


    def find(self, haystack_img, threshold = 0.8):

        # needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        # needle_w = needle_img.shape[1]
        # needle_h = needle_img.shape[0]

        #method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(haystack_img, self.needle_img, cv.TM_CCOEFF_NORMED)

        # gets the best match position
        #min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        #print('Best match top left position: %s' % str(max_loc))
        #print('Best match confidence: %s' % max_val)

        # threshold = 0.8
        locations = np.where(result >= threshold)
        # print(locations)

        # zipping up array of results into touples & then reverses the lists
        locations = list(zip(*locations[::-1]))

        if not locations:
            return np.array([], dtype=np.int32).reshape(0,4)

        # rectangles expects a list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1],), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)  # Double up on rectangles to ensure grouping

        # groups rectanlges and puts them back into $rectangles, (list, 1, "bounding size")
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        #print(rectangles)

        return rectangles
    def get_click_points(rectangles):
        points = []

        # using a loop to draw rectangles for all toupled matches
        for (x, y, w, h) in rectangles:

            # Determine center positions
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # save the points
            points.append((center_x, center_y))

        return points

    def draw_rectangles(self, haystack_img, rectangles):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # determine position
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw boxes
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
        
        return haystack_img

    def draw_crosshairs(self, haystack_img, points):
        
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_TILTED_CROSS

        for (center_x, center_y) in points:            
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)
        
        return haystack_img
