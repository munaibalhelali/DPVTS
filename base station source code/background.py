import cv2 as cv

'this is to generate and manipulate a referance background'

def subtractBG_MOG(history=200,threshold=0):
	# this function create a background MOG2 subtraction object
	mog = cv.bgsegm.createBackgroundSubtractorMOG(history=history) 			
	return mog
def subtractBG_MOG2(history=100,threshold=50):
	# this function create a background MOG2 subtraction object
	mog = cv.createBackgroundSubtractorMOG2(history=history, varThreshold=threshold, detectShadows=True) 			
	return mog
	
def getBG_model(mog):
	return mog.getBackgroundImage()
	
def bgDifference(prev_frame, cur_frame, next_frame):
	# resize the frames
	prev_frame = imutils.resize(prev_frame, width=600)
	cur_frame = imutils.resize(cur_frame, width=600)
	next_frame = imutils.resize(next_frame, width=600)
	
	# convert frames to gray scale
	prev_frame= cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
	cur_frame= cv.cvtColor(cur_frame, cv.COLOR_BGR2GRAY)
	next_frame= cv.cvtColor(next_frame, cv.COLOR_BGR2GRAY)

	

	cv.imshow("prev_frame_maskIN",prev_frame)
	cv.imshow("cur_frame_maskIN",cur_frame)
	cv.imshow("next_frame_maskIN",next_frame)
	diff_frames1=cv.absdiff(next_frame, cur_frame)
	diff_frames2=cv.absdiff(cur_frame, prev_frame)
	result=cv.bitwise_and(diff_frames1,diff_frames2)
	cv.imshow("img diffrence",result)
	return result
