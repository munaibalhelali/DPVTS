# import libraries
import match 
import frame 
import cv2 as cv
from time import sleep
from blobObj import BlobObj


#area far from the camera
MIN_AREA1	 = 1600
#area near the camera
MIN_AREA2	 = 1700
#area of exist path
MIN_AREA3	 =1600

MAX_AREA	 = 15000
MIN_RATIO	 = 0.3
MAX_RATIO	 = 0.8
MIN_WIDTH	 = 25
MIN_HIGHT	 = 25
MIN_DIAG 	 = 40
MAX_DIAG 	 = 200

frame=None
def findCenter(cnt):
	M = cv.moments(cnt) 
		
	try:
		x,y = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	except:
		print("ERROR: Divide by zero")
		return (-1,-1)
	return x,y
		
def fltrBlobs( cnt_list):
	fltrd_list1=[]
	fltrd_list1_cores=[]
	fltrd_list=[]		
	center_list=[]
	fltrd_cnt_list=[]
	fltrd_center_indices=[] 
	#skip frame if the number of objects in the frame more than 10 objects
	if(len(cnt_list)>10):
		print('too many objects')
		return
	for cnt in cnt_list:
		x,y,w,h=cv.boundingRect(cnt) 
		M = cv.moments(cnt) 
		try:
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			center_list.append(center)
		except:
			print("ERROR: Divide by zero")
		
		# cv.rectangle(frame,(x,y),(x+w,y+h),(50,123,255),3) # draw rectangle in blue
	# print('list of centers',len(center_list))
		
	for k in range(len(center_list)):
		
		if(k in fltrd_center_indices):
			continue

		cent0=center_list[k]
		# fltrd_cnt_list.append(cv.boundingRect(cnt_list[k]))
		for j in range(len(center_list)):
			if(j in fltrd_center_indices):
				continue
			distance=match.calDist(cent0,center_list[j])
			# print(distance)
			if(distance<=80):
				fltrd_center_indices.append(j)
				fltrd_cnt_list.append(cv.boundingRect(cnt_list[j]))
		

		x,y,w,h = fltrd_cnt_list[0]
		minX=x
		minY=y
		maxX=x+w
		maxY=y+h

		for a in range(len(fltrd_cnt_list)):
			# print(a,len(fltrd_center_indices),len(fltrd_cnt_list))
			x,y,w,h = fltrd_cnt_list[a]
			if(x<minX):
				minX=x
			if(y<minY):	
				minY=y
			if(x+w>maxX):
				maxX=x+w
			if(y+h>maxY):				
				maxY=y+h
		fltrd_list1.append((minX,minY,maxX-minX,maxY-minY))
		fltrd_list1_cores.append(len(fltrd_cnt_list))
		print('cores list',fltrd_list1_cores)
		# cv.rectangle(frame,(minX,minY),(maxX,maxY),(0,0,0),3) # draw rectangle in blue
		del fltrd_cnt_list[:]

	# print('length  of fltrd_list1 ',len(fltrd_list1))
	for i in range(len(fltrd_list1)):
		rect=fltrd_list1[i]
		x,y,w,h = rect 
		area = w*h
		diagonal = match.calDist((x,y),(x+w,y+h)) 
		asp_ratio = (h)/(w) if (w > h) else (w)/(h)

		if(y <100):
			MIN_AREA=MIN_AREA1
		elif(y >170):
			MIN_AREA=MIN_AREA2
		else:
			MIN_AREA=MIN_AREA3
		# print ('area is ', area)
		if(area>MAX_AREA):
			pass
			# print("\n\narea too large\n\n") 
		# 	return
		# print(area,' ',diagonal,' ', asp_ratio)
		if (area > MIN_AREA and area<MAX_AREA):
			# if(len(fltrd_list)>0):
			# 	if(fltrd_list[-1] is cnt_list[i-1]):
			# 		continue
			xc=x+(w/2)
			yc=y+(h/2)
			center=(xc,yc)
			blob=BlobObj()
			blob.addPos(center) 
			blob.addRect(rect) 
			blob.area=area
			blob.cores=fltrd_list1_cores[i]
			fltrd_list.append(blob) 
		for z in range(len(fltrd_list)-1):
			
			# for z in range(len(fltrd_list)-1): 
			xb,yb,wb,hb = fltrd_list[z].blb_rect
			otherX,otherY=fltrd_list[z+1].pos[-1]
				
			if(otherX>xb and otherX<xb+wb ):
				
				xf,yf,wf,hf=fltrd_list[z].blb_rect
				xff,yff,wff,hff=fltrd_list[z+1].blb_rect
				if(xf>xff):
					xf=xff
				if(yf>yff):
					yf=yff
				if(xf+wf<xff+wff):
					wf=(xff+wff)-xf
				if(yf+hf<yff+hff):
					hf=(yff+hff)-yf

				fltrd_list[z].addRect((xf,yf,wf,hf))
				xc1=x+(wf/2)
				yc1=y+(hf/2)
				center=(xc1,yc1)
				fltrd_list[z].addPos(center) 
				del  fltrd_list[z+1] 


	return fltrd_list
		
		
		
			
