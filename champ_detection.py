import cv2,time
import pytesseract
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class DetectChamp:
    def __init__(self,imName): 
        # Reading the image and saving its height and width
        self.img = cv2.imread(imName)
        self.originalImg = self.img.copy()
        (self.height,self.width) = self.img.shape[:2]

    def preprocess_image(self):
        #Thresholding Image to create binary image 
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        _,bin = cv2.threshold(gray, 215,250,cv2.THRESH_BINARY)

        #Inverting the image and saves image as inv.png
        kernel = np.ones((3,3), np.uint8)
        closing = cv2.morphologyEx(bin, cv2.MORPH_CLOSE, kernel)
        inv = cv2.bitwise_not(closing)
        cv2.imwrite("inv.png", inv)
        self.img = cv2.imread("inv.png")
        self.originalImg = cv2.imread("inv.png")

        # Resizing Image  and saving respective ratios of width and height
        self.rW = self.width / float(320)
        self.rH = self.height / float(320)
        self.img = cv2.resize(self.img, (320,320))
        (self.height,self.width) = self.img.shape[:2]
        
    def text_detection(self):
        # Defining the two ouput lyaer names for the EAST detector model
        # First Layer is the output probabilities 
        # Second Layer is used to derive the bouding box coordinates of text
        layerNames = [
	        "feature_fusion/Conv_7/Sigmoid",
	        "feature_fusion/concat_3"]

        # Loading thee pre-trained East text detector
        net = cv2.dnn.readNet("frozen_east_text_detection.pb")
        blob = cv2.dnn.blobFromImage(self.img, 1.0, (self.width,self.height),
            (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)

        #Scores - stores the probability that actual text is detected
        #Geometry - bounding box coordinate of text
        (scores, geometry) = net.forward(layerNames)

        # grab the number of rows and columns from the scores volume, then
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        # loop over the number of rows
        for y in range(0, numRows):
            # extract the scores and bounding box coordinate of the text
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, numCols):
                # the score(probability) must be above 0.5 
                if scoresData[x] < 0.5:
                    continue

                # compute the offset factor as our resulting feature maps will
                # be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)
                # extract the rotation angle for the prediction and then
                # compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)
                # use the geometry volume to derive the width and height of
                # the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]
                # compute both the starting and ending (x, y)-coordinates for
                # the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)
                # add the bounding box coordinates and probability score to
                # our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])


        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        self.boxes = non_max_suppression(np.array(rects), probs=confidences)
        
       
    def text_recognition(self):
        #Getting the coordinate of the four corner of our bounding box of 
        # the text that is being detected in this case our champion name      
        startX = int(self.boxes[0][0] * self.rW)
        startY = int(self.boxes[0][1] * self.rH)
        endX = int(self.boxes[0][2]* self.rW)
        endY = int(self.boxes[0][3] * self.rH)

        #Cropping the image using the bounding box coordinate and feeding that image
        #into the pytesseract to extract the text from the image
        croppedImg = self.originalImg[startY-15:endY+15, startX-15:endX+15]
        cv2.imwrite("cropped.png", croppedImg)
        text = pytesseract.image_to_string(croppedImg)
        return text

