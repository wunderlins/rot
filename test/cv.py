#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys
import cv2

"""
You first pass in the image and cascade names as command-line arguments. We'll 
use the Abba image as well as the default cascade for detecting faces 
provided by OpenCV.
"""

# Get user supplied values
imagePath = sys.argv[1]
cascPath = sys.argv[2]

"""
Now we create the cascade and initialize it with our face cascade. This loads
the face cascade into memory so it's ready for use. Remember, the cascade 
is just an XML file that contains the data to detect faces.
"""

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

"""
Here we read the image and convert it to grayscale. Many operations in OpenCv are done in grayscale.
"""

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

"""
This function detects the actual face - and is the key part of our code, so 
let's go over the options.

The detectMultiScale function is a general function that detects objects. 
Since we are calling it on the face cascade, that's what it detects. The first 
option is the grayscale image.

The second is the scaleFactor. Since some faces may be closer to the camera, 
they would appear bigger than those faces in the back. The scale factor 
compensates for this.

The detection algorithm uses a moving window to detect objects. minNeighbors 
defines how many objects are detected near the current one before it declares 
the face found. minSize, meanwhile, gives the size of each window.

    I took commonly used values for these fields. In real life, you would experiment with different values for the window size, scale factor, etc., until you find one that best works for you.

The function returns a list of rectangles where it believes it found a face. 
Next, we will loop over where it thinks it found something.
"""

# Detect faces in the image
faces = faceCascade.detectMultiScale(
	gray,
	scaleFactor=1.1,
	minNeighbors=5,
	minSize=(30, 30),
	flags = cv2.cv.CV_HAAR_SCALE_IMAGE
)

"""
This function returns 4 values: the x and y location of the rectangle, and the rectangle's width and height (w , h).

We use these values to draw a rectangle using the built-in rectangle() function.
"""

print "Found {0} faces!".format(len(faces))

largest = 0
rect = (0, 0, 0, 0)
# Draw a rectangle around the faces
for (x, y, w, h) in faces:
	if w+h > largest:
		largest = w+h
		rect = (x, y, w, h)
	print x, y, w, h
	cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

print "Real image: "
print rect

"""
In the end, we display the image, and wait for the user to press a key.
"""

cv2.imshow("Faces found", image)
cv2.waitKey(0)
