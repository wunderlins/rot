#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys
import cv2
import os

thumbnail_width = 300
thumbnail_temp = "out_thumb.jpg"
cropped_temp = "out.jpg"
default_margin = 0.4 # 30%
casc_file = os.path.dirname(os.path.realpath(__file__)) + "/haarcascade_frontalface_default.xml"
test = False

def portrait(input_file, margin=None, width=None, out=None, thumbnail=None):
	if margin == None:
		margin = default_margin
	
	basewidth = width
	if width == None:
		basewidth = thumbnail_width
	
	if out == None:
		out = cropped_temp
	
	if thumbnail == None:
		thumbnail = thumbnail_temp
	
	
	"""
	You first pass in the image and cascade names as command-line arguments. We'll 
	use the Abba image as well as the default cascade for detecting faces 
	provided by OpenCV.
	"""

	# Get user supplied values
	imagePath = input_file
	cascPath = casc_file

	"""
	Now we create the cascade and initialize it with our face cascade. This loads
	the face cascade into memory so it's ready for use. Remember, the cascade 
	is just an XML file that contains the data to detect faces.
	"""

	# Create the haar cascade
	faceCascade = cv2.CascadeClassifier(cascPath)

	"""
	Here we read the image and convert it to grayscale. Many operations in 
	OpenCv are done in grayscale.
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
		scaleFactor=1.2,
		minNeighbors=5,
		minSize=(100, 100),
		flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	"""
	This function returns 4 values: the x and y location of the rectangle, and the rectangle's width and height (w , h).

	We use these values to draw a rectangle using the built-in rectangle() function.
	"""

	found = len(faces)
	print "Found {0} faces!".format(found)
	if found == 0:
		sys.exit(0)

	largest = 0
	rect = (0, 0, 0, 0) # left, top, width, height
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		if w+h > largest:
			largest = w+h
			rect = (x, y, w, h)
		#print x, y, w, h
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	#print "Real image: "
	#print rect

	"""
	In the end, we display the image, and wait for the user to press a key.
	"""
	
	if test:
		cv2.imshow("Faces found", image)
		cv2.waitKey(0)

	"""
	- add margin to the detected rectangle
	- adjust to 1/1 aspect ratio
	- make sure the desired image is not larger than the real image
	"""

	from PIL import Image

	original = Image.open(imagePath)
	(o_width, o_height) = original.size
	(left, top, width, height) = rect
	print "Original size: %d %d" % (o_width, o_height)
	print "Biggest rect: left: %d, top: %d, width: %d, height: %d" % rect

	# let's add 30% of the rect size as padding
	center_x = left + width/2
	center_y = top + height/2

	# need a square canvas
	if width > height:
		height = width
	else:
		width = height
	
	# crop it
	canvas = (int(center_x-width/2-width*margin), int(center_y-height/2-height*margin), int(center_x+width/2+width*margin), int(center_y+height/2+height*margin))
	print canvas
	if canvas[2] > o_width:
		canvas = (canvas[0], canvas[1], o_width, canvas[3])
	if canvas[3] > o_height:
		canvas = (canvas[0], canvas[1], canvas[2], o_height)
	print canvas

	#print canvas
	cropped = original.crop(canvas)
	cropped.save(out)

	# now scale the image down to
	#print basewidth
	wpercent = (basewidth/float(cropped.size[0]))
	hsize = int((float(cropped.size[1])*float(wpercent)))

	print "(%d, %d) - (%f, %d)" % (canvas[2], canvas[3], wpercent, hsize)

	thumbnail = cropped.resize((basewidth, hsize), Image.ANTIALIAS).save(thumbnail)
	#print thumbnail

	# write image
	#thumbnail.save("out_thumb.jpg")

if __name__ == "__main__":
	test = True
	portrait(sys.argv[1])
	sys.exit()
