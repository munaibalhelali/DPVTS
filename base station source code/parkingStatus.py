
import cv2 as cv
import numpy as np
import time 
import yaml
from sendData import updateDataBase
import threading
"""
this class is to draw a simple dashboard contains rectangles that represents parking lots
the color of the rectangle will be red when the parking is occupied 
and green when it is available
"""
total_of_parking_visitors =0
class ParkingStatus(object):
		

	last_update=0
	# the X-values of each dividing line between parking lots
	x_leftside =[80,120,160,200,240,280,320,360,400,440,480,520,560] 

	x_rightside= [259,320,381,438,497,543,587]
	#the common Y-value  for both left and right sides
	y_leftside= (20,100)
	y_rightside= (180,250)

	rColor=[]
	lColor=[] 
	RED =(0,0,255)
	GREEN =(0,255,0)
	font = cv.FONT_HERSHEY_SIMPLEX	

	lParkingStatus=[False,False,False,False,False,False,
					False,False,False,False,False,False]

	rParkingStatus=[False,False,False,False,False,False]
	lParkingTimer=[0,0,0,0,0,0,0,0,0,0,0,0] 
	rParkingTimer=[0,0,0,0,0,0]

	windowName = " parking simple dashboard" #window name
	#cv.namedWindow(windowName, cv.WINDOW_NORMAL) # create input window 
	# Create a black image
	frame = np.zeros((300,600,3), np.uint8)
	global total_of_parking_visitors 

	def drawLayout(self):
		"""
		this function is used to draw the rectangle for 
		each parking lot
		"""
		del self.lColor[:]
		del self.rColor[:]
		for lLot in self.lParkingStatus:
			if (lLot is True):
				self.lColor.append(self.RED)
			else:
				self.lColor.append(self.GREEN)
		for rLot in self.rParkingStatus:
			if (rLot is True):
				self.rColor.append(self.RED)
			else:
				self.rColor.append(self.GREEN)

		
		#left side	
		for i in range(1,13):
			lx1=self.x_leftside[i-1] 
			lx2=self.x_leftside[i]
			ly1,ly2= self.y_leftside
			text_pos = lx1+lx2
			text_pos/=2
			# draw rectangle
			cv.rectangle(self.frame,(lx1+5,ly1),(lx2-5,ly2),self.lColor[i-1],-3)
			cv. putText(self.frame, str(i),(int(text_pos),100),self.font, 0.5, (255,0,0) ,2,cv.LINE_AA)
		#right side
		for i in range(1,6):
			rx1=self.x_rightside[i-1] 
			rx2=self.x_rightside[i]
			ry1,ry2= self.y_rightside
			text_pos = rx1+rx2
			text_pos/=2
			# draw rectangle 
			cv.rectangle(self.frame,(rx1+5,ry1),(rx2-5,ry2),self.rColor[i-1],-3)
			cv. putText(self.frame, str(i+12),(int(text_pos),250),self.font, 0.5, (255,0,0),2,cv.LINE_AA)
		
		#cv.imshow(self.windowName,self.frame)
		return self.frame

	def updateLotStatus(self,lotNo,status):
		startTime = self.lParkingTimer[lotNo-1] if lotNo <=12 else self.rParkingTimer[lotNo-12-1]
		timeElapse=int(time.time())-int(startTime)

		if(timeElapse>0):
			
			if(lotNo<=12):
				if(self.lParkingStatus[lotNo-1] == status):
					return		
				self.lParkingStatus[lotNo-1] = status
				self.lParkingTimer[lotNo-1]=time.time()
				
				thread=threading.Thread(target=updateDataBase,args=(lotNo,status))
				thread.start()
			elif(lotNo >12 and lotNo<=17): 
				if(self.rParkingStatus[lotNo-12-1] == status):
					return
				self.rParkingStatus[lotNo-12-1]= status
				self.rParkingTimer[lotNo-12-1]=time.time()
				thread=threading.Thread(target=updateDataBase,args=(lotNo,status))
				thread.start()
			self.backupParkingStatus()
			self.last_update=time.time()
 
			 

		else:
			return
	def toggleStatus(self,lotNo):
		# -61 seconds is used to overcome the constrain of 
		# one minute update during the demo
		if(lotNo<=12):
			if(self.lParkingStatus[lotNo-1] ==True):
				self.lParkingStatus[lotNo-1]= False
				self.lParkingTimer[lotNo-1]=time.time()-61
				thread=threading.Thread(target=updateDataBase,args=(lotNo,False))
				thread.start()
			else:
				self.lParkingStatus[lotNo-1]= True
				self.lParkingTimer[lotNo-1]=time.time()-61
				thread=threading.Thread(target=updateDataBase,args=(lotNo,True))
				thread.start()
		else:
			if(self.rParkingStatus[lotNo-12-1]== True):
				self.rParkingStatus[lotNo-12-1] =False
				self.rParkingTimer[lotNo-12-1]=time.time()-61
				thread=threading.Thread(target=updateDataBase,args=(lotNo,False))
				thread.start()
			else:
				self.rParkingStatus[lotNo-12-1]= True
				self.rParkingTimer[lotNo-12-1]=time.time()-61
				thread=threading.Thread(target=updateDataBase,args=(lotNo,True))
				thread.start()

		self.backupParkingStatus()


	def showTimeCounter(self,lotNo,mode=1):
		counterImage=np.zeros((300,600,3), np.uint8)
		if (lotNo is None):
			return counterImage
		if(lotNo <=12):
			startTime=self.lParkingTimer[lotNo-1]
		else:
			startTime=self.rParkingTimer[lotNo-12-1]
		if(startTime==0):
			hours=0
			minutes=0
			seconds=0
		else:
			currentTime = time.time()

			timeElapse= int(currentTime-startTime)
			hours = int(timeElapse/3600)
			minutes= int(timeElapse-(hours*3600))
			minutes=int(minutes/60)
			seconds = int(timeElapse-(hours*3600)- (minutes*60))

		if(hours<10):
			if(minutes<10):
				
				timeString='0'+str(hours)+':0'+str(minutes)
				
			else:
				
				timeString='0'+str(hours)+':'+str(minutes)
				
		else:
			if(minutes<10):
				
				timeString=str(hours)+':0'+str(minutes)
				
			else:
				
				timeString=str(hours)+':'+str(minutes)
				

		showText1 ="Lot NO: "+str(lotNo)
		showText2= "Have been parked for: "
		showText3=str(timeString)
		cv. putText(counterImage, showText1,(20,80),self.font, 1, (0,0,255),2,cv.LINE_AA)
		cv. putText(counterImage, showText2,(20,140),self.font, 0.8, (0,0,255),2,cv.LINE_AA)
		cv. putText(counterImage, showText3,(20,220),self.font, 2, (0,0,255),2,cv.LINE_AA)
		if(mode==0):
			return counterImage
		else:
			return str(timeString)

	def availableLots(self):
		counter=0
		for status in self.lParkingStatus:
			if(not status):
				counter+=1
		for status in self.rParkingStatus:
			if(not status):
				counter+=1

		return  counter

	def newVisitor(self):
		global total_of_parking_visitors
		total_of_parking_visitors+=1
	def getParkingVisitors(self):
		return total_of_parking_visitors

	def backupParkingStatus(self):
		
		self.ParkingStatus_file=open("ParkingStatusBackup.txt","w")
		self.ParkingStatus_file.write("{")
		self.ParkingStatus_file.write('"lParkingStatus":{}\n,"rParkingStatus":{}\n,"lParkingTimer":{}\n,"rParkingTimer":{} '.format(self.lParkingStatus,self.rParkingStatus,self.lParkingTimer,self.rParkingTimer))
		self.ParkingStatus_file.write("}")
		self.ParkingStatus_file.close()
	
	def inializeFromFile(self):
		file=open("ParkingStatusBackup.txt","r")
		fileContent = file.read()
		fileContent.strip()
		startStatus= yaml.load(fileContent)
		for i in range(len(self.lParkingStatus)):
			self.lParkingStatus[i]=startStatus["lParkingStatus"][i]
		for i in range(len(self.rParkingStatus)):
			self.rParkingStatus[i]=startStatus["rParkingStatus"][i]
		for i in range(len(self.lParkingTimer)):
			self.lParkingTimer[i]=startStatus["lParkingTimer"][i]
		for i in range(len(self.rParkingTimer)):
			self.rParkingTimer[i]=startStatus["rParkingTimer"][i]
		file.close()
		thread=threading.Thread(target=self.updateServerFromFile,args=())
		thread.daemon=True
		thread.start()
	def updateServerFromFile(self):
		for i in range(len(self.lParkingStatus)):
			updateDataBase(i+1,self.lParkingStatus[i],self.lParkingTimer[i])
		for i in range(len(self.rParkingStatus)):
			updateDataBase(i+13,self.rParkingStatus[i],self.rParkingTimer[i])


	def newSession(self):
		for i in range(len(self.lParkingStatus)):
			self.lParkingTimer[i]=int(time.time())
			updateDataBase(i+1,False,self.lParkingTimer[i])
		for i in range(len(self.rParkingStatus)):
			self.rParkingTimer[i]=int(time.time())
			updateDataBase(i+13,False,self.rParkingTimer[i])
		

		

