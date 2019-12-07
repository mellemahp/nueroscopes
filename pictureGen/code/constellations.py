from imageai.Prediction import ImagePrediction

import numpy as np

import cv2
import imutils
import os
import time

img = cv2.imread('sdss.jpg')

# Number of stars to find
numStars = 10

# Determine the center point
centerPoint = (img.shape[0]/2, img.shape[1]/2)

# Convert the image to grayscale, then blur and threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]

# Find the contours in the thresholded image and pick out the brightest
conts = cv2.findContours(thresh.copy(), 
                          cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)
conts = imutils.grab_contours(conts);
conts = sorted(conts, key=cv2.contourArea, reverse=True)[:numStars]

# Pull out the center of each contour
stars = np.array([[1,2,3]])
for c in conts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(img, (cX, cY), 5, (255, 255, 0), -1)
    # For each star, add the center and the angle wrt x-axis of the ray pointing
    # to the center
    angle = np.arctan2(cY-centerPoint[1], cX-centerPoint[0])
    stars = np.append(stars,[[cX,cY,angle]], axis=0)

# Sort the stars by the angle
stars = stars[1:,:]
stars = stars[stars[:,-1].argsort()]
stars = stars[:,:-1].astype(np.int32)
print(stars)

# Connect the dots
cv2.fillPoly(img, np.array([stars]), (255,0,0))

cv2.imshow('image', img); cv2.waitKey(1); # cv2.destroyAllWindows()
cv2.imwrite('test.jpg', img)

executionPath = os.getcwd()

prediction = ImagePrediction()
prediction.setModelTypeAsSqueezeNet()
prediction.setModelPath(os.path.join(executionPath,
    "squeezenet_weights_tf_dim_ordering_tf_kernels.h5"))
prediction.loadModel()
predictions, probabilities = prediction.predictImage(os.path.join(executionPath,"test.jpg"), result_count=10)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)

time.sleep(10)
