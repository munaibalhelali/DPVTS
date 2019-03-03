import cv2 as cv


frame = None
def createMask(Frame,mog):
	
	mask=mog.apply(Frame)
	#cv.imshow("first mask",mask)
	return mask
	
def fltrFrame (Mask,Thresh_min=100,Thresh_max=255,Thresh_type=cv.THRESH_BINARY,Kernel_size=(5,5)):
	retval,fgthres = cv.threshold(Mask, Thresh_min, Thresh_max, Thresh_type)
   
	kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, Kernel_size)

	# Fill any small holes
	closing = cv.morphologyEx(fgthres, cv.MORPH_CLOSE, kernel)
	# Remove noise
	opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)

	# Dilate to merge adjacent blobs
	dilation = cv.dilate(opening, kernel, iterations = 2)		

	return dilation 
	
def findContour(frame):
			
	im,contours,hierarchy = cv.findContours(frame,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	
	return contours
	
def cropCarImage(img,rect):
	x,y,width, hight= rect
	img_crop = img[int(y):int(y+hight), int(x):int(x+width)] 
	return img_crop
