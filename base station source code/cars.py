
from collections import deque
import numpy as np
import cv2 as cv
import color as colorIns
import zone as zoneA
import stateMachine as state_machine
import match
import draw
from time import sleep
import time
from parkingStatus import ParkingStatus
class Cars(object):	
	""" this class is to represent the individual cars that 
	are detected while coming into the parking area """

	parkingStatus=ParkingStatus()

	def __init__(self):
		self.color=[]
		self.car_number= None
		self.start_time=0 
		self.pts =[]
		self.cnt_chain=[] 
		self.state="HYPO"
		self.avrg_color = None
		self.zone = None
		self.zoneP= None
		self.frame_NO=1
		self.lot0=[] #keep record of the parking lots the car passed through
		self.lot1=None
		self.isParked=None
		self.recorededFlag=False
		self.statusPair=[] # hold the transition pair of status
		self.frameCores={}
		self.movingDirection_x=""
		self.movingDirection_y=""
		self.frameArea={}
	def setColor(self, incolor):
		self.color.append(incolor)
		avg_color= colorIns.avrgColor(self.color)
		if (avg_color is not -1):
			self.avrg_color = avg_color
	def setStartTime(self,time):
		self.start_time=time
	
	def addCNT(self,cnt):
		self.cnt_chain.append(cnt)
		
	def getStartTime(self):
		return self.start_time
	def updateFrameCores(self,cores_num):
		print('length in car', cores_num)
		if (cores_num in self.frameCores):
			self.frameCores[cores_num]+=1
		else:
			self.frameCores[cores_num]=1
		self.validateCar()
	def updateQ(self,center):
		if (type(center) is list):
			if(len(self.pts)>0):
				if (self.pts[-1] is not center[-1]):
					if(not self.checkDistance(self.pts[-1],center[-1])):
						return False
					self.pts.append(center[-1])
			else:
				self.pts.append(center[-1])
		else:
			if(len(self.pts)>0):
				if (self.pts[-1] is not center):
					if(not self.checkDistance(self.pts[-1],center)):
						return False
					self.pts.append(center)
			else:
				self.pts.append(center)
		self.frame_NO+=1
		return True

	def checkDistance(self,point1,point2):
		distance=match.calDist(point1,point2)
		if (distance>50):
			return False
		else:
			return True

	def updateZone(self):
		if (type(self.pts[-1]) is tuple):
			pass_var=self.pts[-1]
		elif(type(self.pts[-1]) is list):
			return
		zoneT = zoneA.decideZone(pass_var)
		# print('received zone: ',zoneT)
		if (zoneT is not None):
			
			self.zoneP=self.zone
			self.zone = zoneT
			# print(self.zone,self.zoneP, self.state)
			if (self.zone == "PZ" and self.state != "HYPO"):
				self.lot1=zoneA.decideLot(self.pts[-1])
				if(self.lot1 is not None):
					
					self.isParked=True
					"""
					this if-else condition is made to take to account the possibilty 
					passing through mutliple lots during parking event
					"""
					if(len(self.lot0)>1):
						self.parkingStatus.updateLotStatus(int(self.lot1),True)	
						self.start_time= int(time.time())
						for lot in self.lot0:
							if(lot is not None):
								self.parkingStatus.updateLotStatus(int(lot),False) 
						del self.lot0[:]
					else:
						self.parkingStatus.updateLotStatus(int(self.lot1),True) 
					if(len(self.lot0)>0):
						if(self.lot0[-1] is not self.lot1):
							self.lot0.append(self.lot1)
					else:
						self.lot0.append(self.lot1)
			elif(self.zoneP is "PZ" and zoneT is "CPA" and self.state is not "HYPO"):
				if(len(self.lot0)>0):
	
					"""
					this loop is implemented to take to account the possibilty 
					of passing through more than one parking lot during leaving event
					"""
					for lot in self.lot0:
						if(lot is not None):
							self.parkingStatus.updateLotStatus(int(lot),False)
					self.isParked=False
					del self.lot0[:]

			if(self.zone == "CPA" ):
				#check if the car is new visitor to the parking area
				self.isNewVisitor()
	'''def parkingStateUpdate(self):
		if(self.lot[1] is self.lot[0]):
			return self.lot[1]+str("in")
		elif(self.lot[1] is not self.lot[0])					
	'''			
	def updateState(self):
		old_state=self.state
		stateT = state_machine.decideState (self.frame_NO, self.zone, self.state)
		if(stateT is not None):
			# self.validateDirection()
			if (old_state is "NORMAL"):
				# print('checking for loop')
				if(("NORMAL",stateT) in self.statusPair):
					# print('old switch')
					self.state=old_state
				else:
					# print('new switch')
					self.statusPair.append(("NORMAL",stateT))
					self.state = stateT
			else :
				# print("not normal")
				self.state = stateT

			if (old_state is not self.state):
				self.frame_NO = 0
			# print('old state: ',old_state,'new state: ',self.state,' zone: ',self.zone)
			# print(self.statusPair)
	def isNewVisitor(self):

		if(self.recorededFlag != True):
			ParkingStatus().newVisitor()	
			self.recorededFlag=True
		# print('new visitor? ',not self.recorededFlag)

	def printCar(self):
		print('\ncar details as follows:')
		print('car number: ',self.car_number)
		print('car average color: ',self.avrg_color)
		print('car zone: ',self.zone)
		print('car state: ',self.state)
		print('car position Q: ',self.pts)
		print('car parked at: ',self.lot1, self.lot0)
		print('car parkState: ',self.isParked)
		print('frame cores rate: ',self.frameCores)
		
			
	def markCar(self,frame):
		if(self.state is "HYPO"):
			zone=self.state
		else:
			zone=self.zone 
		draw.drawRect(frame,self.cnt_chain[-1],zone,self.car_number)

	def validateCar(self):
		x,y=self.pts[0]
		if(y>290):
			self.state="HYPO"
			return
		if(len(self.frameCores)==1):
			if(2 in self.frameCores):
				self.state="HYPO"
		elif(len(self.frameCores)==2):
			if(2 in self.frameCores and 1 in self.frameCores):
				if(self.frameCores[2]>self.frameCores[1]):
					self.state="HYPO"
			if(2 in self.frameCores and 3 in self.frameCores):
				if(self.frameCores[2]>self.frameCores[3]):
					self.state="HYPO"
		elif(len(self.frameCores)==3):
			if(2 in self.frameCores and 3 in self.frameCores):
				if(self.frameCores[2]>self.frameCores[3] or self.frameCores[3]>self.frameCores[2]):
					self.state="HYPO"
		print(self.frameCores)

	def validateDirection(self):
		# direction={'px':0,'py':0,'nx':0,'ny':0}
		# index=42 if len(self.pts)>42 else len(self.pts)
		# k=6 if index%2==0 else 5
		# for i in range(index):
		# 	x1,y1=self.pts[-i]
		# 	try:
		# 		x2,y2=self.pts[-1*(i-k)]
		# 	except:
		# 		break
		# 	if(x1-x2 > y1-y2 and x1>x2 ):
		# 		direction['px']+=1
		# 	elif (y1-y2 > x1-x2 and y1>y2 ):
		# 		direction['py']+=1
		# 	elif(x1-x2 > y1-y2 and x1<x2 ):
		# 		direction['nx']+=1
		# 	elif (y1-y2 > x1-x2 and y1<y2 ):
		# 		direction['ny']+=1
		# if (direction['px']>direction['py']):
		# 	self.movingDirection='px'
		# elif(direction['py']>direction['px']):
		# 	self.movingDirection='py'	
		# elif (direction['nx']>direction['ny']):
		# 	self.movingDirection='nx'
		# elif(direction['ny']>direction['nx']):
		# 	self.movingDirection='ny'	
		x1,y1=self.pts[-1]
		try:
			x2,y2=self.pts[-40]
		except Exception as e:
			print('@@@@@@@@@@@@@@@@@@@@@@',e)
			return
		
		if(x1-x2 > y1-y2 and x1>x2 ):
			self.movingDirection_x='px'
		elif(x1-x2 > y1-y2 and x1<x2 ):
			self.movingDirection_x='nx'
		if (y1-y2 > x1-x2 and y1>y2 ):
			self.movingDirection_y='py'	
		elif (y1-y2 > x1-x2 and y1<y2 ):
			self.movingDirection_y='ny'	
		print('car direction:\n\n\n\n ', self.movingDirection_x,self.movingDirection_y)



		
		
		
		


