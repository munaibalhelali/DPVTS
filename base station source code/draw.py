'this class is to draw different shapes on a given frame'
#import necessary libraries
import cv2 as cv
from cars import Cars
import sys
LAYOUT = 0 # 0 is the original layout
			# 1 is the edited layout

if(LAYOUT is 0):
	from orgLayout import *
elif(LAYOUT is 1):
	from editedLayout import *

car=Cars()
frame = None
p1State= None
p2State= None
lineColor=(150,0,100)




def drawLine(frame,start,end,color=lineColor,lineThikness=3):
	# Draw a line on the provided frame
	line=cv.line(frame,start,end,color,lineThikness)
	
	return line
	
def drawParkingLots(frame,fgmask):

	#draw line at the enterance to detect cars
	font = cv.FONT_HERSHEY_SIMPLEX	
	# draw left side layout
	lineNO=0
	lotNO=0
	for x in range(12):
		startPoint=left_side_coordinates[lineNO]
		endPoint=left_side_coordinates[lineNO+1]
		lineNO+=2
		
		drawLine(fgmask,startPoint,endPoint)

		
		x1,y1=startPoint
		x2,y2=endPoint
		
		try:
			x3,y3=left_side_coordinates[lineNO+2]
		except :
			
			pass
		
		text_x_pos =x3 + x1
		text_x_pos/=2
		text_x_pos-=0.4*(x3-x1) 

		text_y_pos = y1+y2
		text_y_pos/=2
		lotNO+=1
		cv.putText(fgmask, str(lotNO),(int(text_x_pos),int(text_y_pos)),font, 0.5, lineColor,1,cv.LINE_AA)
		drawLine(fgmask,startPoint,(x3,y3))
	
	lineNO=0
	for y in range(6):
		startPoint=right_side_coordinates[lineNO]
		endPoint=right_side_coordinates[lineNO+1]
		lineNO+=2
		
		drawLine(fgmask,startPoint,endPoint)

		
		x1,y1=startPoint
		x2,y2=endPoint
		
		try:
			x3,y3=right_side_coordinates[lineNO+2]
		except :
			
			pass
		
		text_x_pos =x3 + x1
		text_x_pos/=2
		text_x_pos-=0.3*(x3-x1) 

		text_y_pos = y1+y2
		text_y_pos/=2
		lotNO+=1
		cv.putText(fgmask, str(lotNO),(int(text_x_pos),int(text_y_pos)),font, 0.6, lineColor,2,cv.LINE_AA)
		drawLine(fgmask,startPoint,(x3,y3))
		
		

	
	return fgmask
		
def drawRect(frame ,rect ,zone,carN=0):
	"""this function draws rectangle around a given object 
		with different colores according to the zone the object is in """
	if(zone is 'PZ'):
		colorIndex = (0,255,0)
	elif (zone is 'DZ'):
		colorIndex = (255,0,0)
	elif (zone is 'NTZ'):
		colorIndex = (255,255,0)
	elif (zone is 'HYPO'):
		colorIndex = (255,255,255)
	else:
		colorIndex = (0,0,255)
		
	nx,ny,nw,nh = rect
	cv.rectangle(frame,(nx,ny),(nx+nw,ny+nh),colorIndex,3) 
	font = cv.FONT_HERSHEY_SIMPLEX
	cv. putText(frame, str(carN),(nx,int(ny+nh/2)),font, 0.5, colorIndex,1,cv.LINE_AA)
	return frame

def carCounter(frame,counter):
	""" this function display a counter on the screen"""
	font = cv.FONT_HERSHEY_SIMPLEX	
	showCarCounter="Cars NO: "+str(counter)			
	cv. putText(frame, str(showCarCounter),(120,20),font, 0.5, (0,255,255),1,cv.LINE_AA)
	return frame	
	

	
	
	
	
	
	
	
	
	
	
	
		
