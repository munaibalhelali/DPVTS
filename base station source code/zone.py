from time import sleep
from parkingStatus import ParkingStatus 
import cv2 as cv
' this class is used to identify the zone in which a car is detected '
LAYOUT = 0 # 0 is the original layout
			# 1 is the edited layout

if(LAYOUT is 0):
	from orgLayout import *
elif(LAYOUT is 1):
	from editedLayout import *

def decideZone(pos):
	x,y=pos
	# print('given pos: ',pos)
	for zone in zones:
		zx1,zy1=zoneCoord[zone]['start']
		zx2,zy2=zoneCoord[zone]['end']
		# print(zone,' :','({},{})({},{})'.format(zx1,zy1,zx2,zy2))
		
		if ((x>zx1 and x < zx2) and (y>zy1 and y<zy2)):
			# print(zone)
			if(zone is "PZ1" or zone is "PZ2"):
				return "PZ"
			else:
				return zone
	
	else:
		return None

def decideLot(center):
	
	if (center is None):
		return None
	return isInLot(center)
		

def decideLotSDash(center):
	
	if (center is None):
		return None
	x,y=center
	if(y>300):
		y-=300
	center=(x,y)
	print(center,"dash")
	return isInLot(center)

def isInLot(center):
	xc,yc=center
	# print("in isInLot: ",center)
	if(yc<=70):
		"""
		each four points in the left_side_coordinates list represent one parking lot
		hence the increase in the index will be muliplied by 2 as each 
		dividing line is shares with adjecent lots

		in this function line equation is used to check if the given 
		center is located with in a certain lot
		"""
		for lotNo in range(1,13):
			try:
				if (lotNo==1):
					pointIndex=0
				else:
					pointIndex=lotNo-1
					pointIndex*=2

				x1,y1= left_side_coordinates[pointIndex]
				x2,y2= left_side_coordinates[pointIndex+1]
				x3,y3= left_side_coordinates[pointIndex+2]
				x4,y4= left_side_coordinates[pointIndex+3]	

				invSlop1 = (x2-x1)/(y2-y1)
				invSlop2 = (x4-x3)/(y4-y3)
				
				X1=((yc-y1)*(invSlop1))+x1 
				X2=((yc-y3)*(invSlop2))+x3
				# print('x range :' ,X1,X2)
				if(xc>X1 and xc <X2):
					return lotNo
			except:
				pass

		return None

	elif(yc>=180 and yc<=275):
		for lotNo in range(13,19):
			try:
				pointIndex=lotNo-13
				pointIndex*=2

				
				x1,y1= right_side_coordinates[pointIndex]
				x2,y2= right_side_coordinates[pointIndex+1]
				x3,y3= right_side_coordinates[pointIndex+2]
				x4,y4= right_side_coordinates[pointIndex+3]	

				invSlop1 = (x2-x1)/(y2-y1)
				invSlop2 = (x4-x3)/(y4-y3)
				
				X1=((yc-y1)*(invSlop1))+x1 
				X2=((yc-y3)*(invSlop2))+x3
				# print('x range :' ,X1,X2)
				if(xc>X1 and xc <X2):
					return lotNo
			except:
				pass
		return None

def printZoneArea(frame):
	for zone in zones:
		x1,y1=zoneCoord[zone]['start']
		x2,y2=zoneCoord[zone]['end']
		cv.rectangle(frame,(x1,y1),(x2,y2),(133,80,200),3) 