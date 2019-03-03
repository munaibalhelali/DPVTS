

from tkinter import *
from PIL import Image, ImageTk
import cv2 as cv
import imutils
import numpy as np
import argparse
import datetime
import time
import frame as img
import background as bg
import zone 
import stateMachine 
import color 
import match 
import draw
import blob as blb
from parkingStatus import ParkingStatus
from cars import Cars
from blobObj import BlobObj
from tkinter import messagebox
import yaml
from os import walk
import threading

BG_subtraction_type="MOG2" # can be MOG or MOG2

class MainOperator(object):

	

	def __init__(self,cap):
		self.parkingStatus=ParkingStatus()
		if(BG_subtraction_type == "MOG2"):
			self.mog = bg.subtractBG_MOG2()
		elif(BG_subtraction_type=="MOG"):
			self.mog = bg.subtractBG_MOG()
		self.vid = MyVideoCapture(cap)
		self.car_list=[]	# save the detected moving cars 
		self.car_counter=0  # to keep track of the cars number visited the parking 
		self.prev_pos =None # save the previous position of the blob

		self.frame=None
		self.fgmask=None
		self.simpleDashboard=None
		self.bgmodel=None
		self.processInput()
		self.mergeFlag=0
		self.lastCar=None
		


	def addNewCar(self,blob,car_counter):
		""" this function create an instance of car class and initialize its param """
		# this if condition to prevent the system from 
		#adding cars going out that have been deleted
		x,y=blob.pos[-1]
		new_car = Cars(); 
		# new_car.setColor(blob.color)
		new_car.updateQ(blob.pos[-1])
		new_car.setStartTime(time.time())
		new_car.addCNT(blob.blb_rect)
		new_car.updateZone()
		new_car.car_number =car_counter
		new_car.updateFrameCores(blob.cores)
		self.car_list.append(new_car)

	def updateCar(self,car,blob):
		""" this function updates the car objects"""
		car.updateQ(blob.pos)
		car.addCNT(blob.blb_rect) 
		car.updateZone()
		car.updateState()
		car.setStartTime(time.time())
		car.updateFrameCores(blob.cores)
	
		
			 
	def mark_and_cleanCarList(self):
		""" this function cleans car list"""
		list_size=len(self.car_list)
		del_count=0
		i = 0
		# print('car list: ',len( self.car_list))
		for car in self.car_list:
			car.markCar(self.frame)

			if (car.state is "DELETE"):
				# print("frame no: ", car.frame_NO)
				car.printCar()
				del self.car_list[i]
				del_count+=1
				# print ('car was deleted')
			elif(time.time()-car.start_time >5):
				car.printCar()
				del self.car_list[i]
				del_count+=1
				# print("deleted by time")
			i+=1			


	def processInput(self):
		# for loop is used to skip some frames and 
		# make up for the proccessing time 	
		if(self.vid.vid is None):
			return
		for i in range(1):
			ret,self.frame= self.vid.get_frame()
			if (ret is False):
				return	-1	
		try:
			#resize the frame
			self.frame = imutils.resize(self.frame, height=300, width=600) 
		except:
			return
		
		#pass the current frame to draw
		draw.frame = self.frame
		#pass the current frame to blob
		blb.frame=self.frame
		# convert the frame color to gray
		gray = cv.cvtColor(self.frame, cv.COLOR_RGB2GRAY)
		# make HSV model of the current frame
		hsv_frame = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV) 
	    #get a foregound mask
		self.fgmask = img.createMask(gray,self.mog)
		#filter out the noise from the foreground mask
		self.fgmask=img.fltrFrame(self.fgmask.copy()) 
		#get back ground model

		if(BG_subtraction_type=="MOG2"):
			self.bgmodel=bg.getBG_model(self.mog)
		elif(BG_subtraction_type=="MOG"):
			self.bgmodel=self.fgmask

		# extract moving objects from the frame
		contours = img.findContour(self.fgmask)
		#skip frame is noise was found 
		
		# if(len(contours)>10):
		# 	return
		

		# filter the detected objects 
		fltrd_contours = blb.fltrBlobs(contours)
		# print('length of filtered rects',len(fltrd_contours))
		if (fltrd_contours is not None):
			for blob in fltrd_contours:
				blob.updateState()
				blob.updateZone()
				print('blob cores',blob.cores)
				# print(len(self.car_list))
				# print(blob.pos[-1])
				if (len(self.car_list)>0):
					newCarFlag=True
					# while(newCarFlag):
					print('length of car list: ',len(self.car_list))
					# draw.drawRect(self.frame, blob.blb_rect,blob.zone)
					mergeFlag=0
					for car in self.car_list:
						
						match_state_blb_pos = match.posMatch(car.pts,blob.pos[-1],blob.blb_rect)
						match_state_blb_OVLP = match.ovrLapMatch(blob.blb_rect,blob.pos[-1],car.cnt_chain[-1],car.pts[-1])
						print(match_state_blb_pos,match_state_blb_OVLP,car.car_number,' ',blob.pos[-1])
						
						if (match_state_blb_pos):
						
							self.updateCar(car,blob)
							newCarFlag=False
							mergeFlag+=1
							self.lastCar=car 

						if(match_state_blb_OVLP):
							
							self.updateCar(car,blob)
							newCarFlag=False
							mergeFlag+=1
							self.lastCar=car

					if(newCarFlag):
						self.car_counter+=1
						self.addNewCar(blob,self.car_counter)

				else:
					self.car_counter+=1
					self.addNewCar(blob,self.car_counter)
				


		self.simpleDashboard= self.parkingStatus.drawLayout()
		#clean car list
		self.mark_and_cleanCarList()

		#change fgmask from 1 channel to 3 channels
		self.fgmask = cv.merge((self.fgmask,self.fgmask,self.fgmask))
		self.fgmask=draw.drawParkingLots(self.frame,self.fgmask)
		numpy_vertical_concat1 = np.concatenate((self.simpleDashboard, self.frame), axis=0)
		zone.printZoneArea(self.fgmask)


class App:

	lParkingStatus=ParkingStatus().lParkingStatus
	rParkingStatus=ParkingStatus().rParkingStatus
	def __init__(self, window, window_title,source =None):
		self.window = window
		self.window.title(window_title)
		self.inputProc=MainOperator(cap=source if source!=None else cv.VideoCapture(0))
		self.vid=self.inputProc.vid
		
		self.disabledImg = ImageTk.PhotoImage(file="disabled.png")
		self.out=None

		# open video source (by default this will try to open the computer webcam)
		

		# Button that lets the user take a snapshot
		# self.btn_snapshot=Button(window, text="Snapshot", width=50, command=self.snapshot)
		# self.btn_snapshot.pack(anchor=CENTER, expand=True)

		# After it is called once, the update method will be automatically called every delay milliseconds
		self.delay = 15
		self.date_time=""		
		self.initializeFlag=False
		self.startMessege=True
		self.recordFlag=False
		self.activeBackgroundModeFlag=False

		self.mainWin = PanedWindow(window, orient= VERTICAL)
		self.mainWin.pack()

		#info bar panel
		self.infoBarWin = PanedWindow(self.mainWin, orient=HORIZONTAL)

		self.timedateWin = PanedWindow(self.infoBarWin)

		# date_time=datetime.datetime.now().strftime("%A, %d. %B %Y \n %I:%M:%S %p")
		
		self.timedateButt = Button(self.timedateWin,height=4,width=25,bg="grey")
		self.timedateWin.add(self.timedateButt)
		self.timedateWin.pack(side=LEFT)

		self.visitorWin = PanedWindow(self.infoBarWin)
		self.visitorButt = Button(self.visitorWin,height=4,width=25,bg="grey")
		self.visitorWin.add(self.visitorButt)
		self.visitorWin.pack(side=LEFT)

		self.emptyWin = PanedWindow(self.infoBarWin)
		self.emptyButt = Button(self.emptyWin,height=4,width=25, bg="grey" )
		self.emptyWin.add(self.emptyButt)
		self.emptyWin.pack(side=LEFT)

		self.occupiedWin = PanedWindow(self.infoBarWin)
		self.occupiedButt = Button(self.occupiedWin,height=4,width=25,bg="grey")
		self.occupiedWin.add(self.occupiedButt)
		self.occupiedWin.pack(side=LEFT)

		self.infoBarWin.pack()


		#user display panel
		self.displayWin = PanedWindow(self.mainWin, orient=HORIZONTAL)
		self.displayWin.pack()

		self.screensWin = PanedWindow(self.displayWin, orient=VERTICAL)
		self.screensWin.pack(side=LEFT)		

		self.inputWin = PanedWindow(self.screensWin)
		self.inputButt = Button(self.inputWin,height = 18, width=70)
		self.inputWin.add(self.inputButt)
		self.inputWin.pack()
		self.dashboardWin = PanedWindow(self.screensWin,bg="grey")

		self.dashboardWin.pack()

		self.secondDisWin = PanedWindow(self.displayWin, orient= VERTICAL)
		self.secondDisWin.pack(side=LEFT)

		#foregroundWin = PanedWindow(self.secondDisWin)
		self.foregroundButt = Button(self.secondDisWin,height = 18, width=70)
		self.secondDisWin.add(self.foregroundButt)
		# foregroundWin.pack(side=TOP)
		self.backgroundButt = Button(self.secondDisWin,height = 18, width=70)
		self.secondDisWin.add(self.backgroundButt)


		self.controlWin = PanedWindow(self.displayWin, orient=VERTICAL)
		self.controlWin.pack(side=LEFT)

		self.buttonWin = PanedWindow(self.controlWin, orient= VERTICAL,)
		self.buttonWin.pack(side=TOP)	

		self.backgroundModeButt = Button(self.buttonWin,height=10, width=10,bg="grey",text = "Background mode",command=self.backgroundModeCallBack)
		self.buttonWin.add(self.backgroundModeButt) 

		self.calibrateButt = Button(self.buttonWin,bg="grey",text = "Calibrate System",command=self.enableCalibration)
		self.buttonWin.add(self.calibrateButt)

		self.recordButt = Button(self.buttonWin, bg="grey",text = "Record Video",command=self.recordVideoCallBack)
		self.buttonWin.add(self.recordButt)

		self.snapButt = Button(self.buttonWin, bg="grey",text = "Snap Picture",command=self.snapshot)
		self.buttonWin.add(self.snapButt)


		#------------------------
		self.dropListWin = PanedWindow(self.controlWin, orient= VERTICAL,)
		self.dropListWin.pack(side=BOTTOM)	
		# Create a Tkinter variable
		self.tkvar = StringVar(self.buttonWin)
		self.mypath="/home/munaibsadeq/Desktop/FYP2/videoSample"
		self.f = ["From Camera"] 
		for (dirpath, dirnames, filenames) in walk(self.mypath):
		    self.f.extend(filenames)
		    break
		# Dictionary with options
		self.choices = self.f
		self.tkvar.set(self.f[0]) # set the default option
		
		self.popupMenu = OptionMenu(self.dropListWin, self.tkvar, *self.choices)
		Label(self.dropListWin, text="Choose a video").pack()
		self.popupMenu.pack()
		 
		 
		# link function to change dropdown
		self.tkvar.trace('w', self.change_dropdown)
		#------------------------

		# self.showStatButt = Button(self.buttonWin, bg="grey",text = "Show Statistics")
		# self.buttonWin.add(self.showStatButt)

		self.guidButt = Button(self.buttonWin,bg="grey",text = "User Guide")
		self.buttonWin.add(self.guidButt)


		self.lButtonList = []
		self.rButtonList = []

		self.drawDashboard()
		self.update()
		

		self.window.mainloop()
 	
 	# on change dropdown value
	def change_dropdown(self,*args):
		if self.vid.vid.isOpened():
			self.vid.vid.release()
		if(str(self.tkvar.get()) == "From Camera"):
			self.inputProc=MainOperator(cap=cv.VideoCapture(0))
		else:
			self.inputProc=MainOperator(cap=cv.VideoCapture(self.mypath+"/"+str(self.tkvar.get())))
	def snapshot(self):
		# Get a frame from the video source
		
		cv.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv.cvtColor(self.inputProc.frame, cv.COLOR_RGB2BGR))

	def drawDashboard(self):
		leftPanel = PanedWindow(self.dashboardWin, orient= HORIZONTAL)
		for i in range(12):
			self.lButtonList.append(CBut(self.dashboardWin,i+1))

		lLabel=0
		for b in self.lButtonList:
			b.button.configure(text=str(lLabel+1)+"\n\n")
			leftPanel.add(b.button)
			lLabel+=1
		leftPanel.pack(side=TOP)

		self.pathPanel= PanedWindow(self.dashboardWin)
		self.pathLabel= Label(self.pathPanel)
		self.pathLabel.configure(height=5,width=70,bg="grey", text="Exit Path")
		self.pathLabel.pack()
		self.pathPanel.pack()
		
		rightPanel = PanedWindow(self.dashboardWin, orient= HORIZONTAL)

		for i in range(6):
			self.rButtonList.append(CBut(self.dashboardWin,i+13))

		rLabel=12
		for b in self.rButtonList:
			b.button.configure(text=str(rLabel+13)+"\n\n")
			rightPanel.add(b.button)
			rLabel+=1

		rightPanel.pack(side=BOTTOM)
	def updateDashboard(self):
		if(self.startMessege):
			self.initalizeSystem()
			self.startMessege=False
		self.disabledImg = ImageTk.PhotoImage(file="disabled.png")
		for i in range(12):
			if (self.lParkingStatus[i]):
				self.lButtonList[i].configure(bg="red")
				self.lButtonList[i].button.configure(text=str(i+1)+"\n\n"+str(self.lButtonList[i].parkingDuration()))
			else:
				self.lButtonList[i].configure(bg="green")
				self.lButtonList[i].button.configure(text=str(i+1)+"\n\n")
		for i in range(6):
			if (self.rParkingStatus[i]):
				self.rButtonList[i].configure(bg="red")
				if(i==0):
					self.rButtonList[i].button.configure(width=100,text=str(self.rButtonList[i].parkingDuration()) ,image=self.disabledImg)
					self.rButtonList[i].button.image=self.disabledImg
				else:
					self.rButtonList[i].button.configure(text=str(i+13)+"\n\n"+str(self.rButtonList[i].parkingDuration()))
			else:
				self.rButtonList[i].configure(bg="green")
				if(i==0 or i ==1):
					self.rButtonList[i].button.configure(width=100,image=self.disabledImg)
					self.rButtonList[i].button.image=self.disabledImg
				else:
					self.rButtonList[i].button.configure(text=str(i+13)+"\n\n")

	def update(self):
		if(self.vid.vid is not "None"):
			ret=self.inputProc.processInput()
			if(not self.activeBackgroundModeFlag):
				self.lParkingStatus=ParkingStatus().lParkingStatus
				self.rParkingStatus=ParkingStatus().rParkingStatus	

				self.updateTime()
				self.timedateButt.configure(text=self.date_time)
				# Get a frame from the video source
				
				
				if(not self.initializeFlag):
					inputFrame=self.inputProc.frame
				else:
					inputFrame=draw.drawParkingLots(self.inputProc.frame,self.inputProc.frame)
				if(self.recordFlag):
					self.recordVideo(inputFrame)

				fgFrame=self.inputProc.fgmask
				dashboard=self.inputProc.simpleDashboard
				bgFrame=self.inputProc.bgmodel
				if(ret != -1):
					self.updateDashboard()
					self.inputImg = ImageTk.PhotoImage(image = Image.fromarray(inputFrame))
					#self.dashboardImg = ImageTk.PhotoImage(image = Image.fromarray(dashboard))
					self.foregroundImg = ImageTk.PhotoImage(image = Image.fromarray(fgFrame))
					self.backgroundImg = ImageTk.PhotoImage(image = Image.fromarray(bgFrame))
					self.inputButt.configure(height=300,width=600,image=self.inputImg)
					#self.dashboardButt.configure(image=self.dashboardImg)
					self.foregroundButt.configure(height=300,width=600,image=self.foregroundImg)
					self.backgroundButt.configure(height=300,width=600,image=self.backgroundImg)

				availableLots=ParkingStatus().availableLots()
				occupiedLots=18-availableLots
				self.emptyButt.configure(text="NO. of Available Lots: \n"+str(availableLots))
				self.occupiedButt.configure(text="NO. of Occupied Lots: \n"+str(occupiedLots))
				self.visitorButt.configure(text= "No. of parking visitors: \n"+str(ParkingStatus().getParkingVisitors()))

		self.window.after(self.delay, self.update)	
	def updateTime(self):
		
		self.date_time=datetime.datetime.now().strftime("%A, %d. %B %Y \n %I:%M:%S %p")

	def enableCalibration(self):

		if(not CBut.initializeFlag):
			CBut.initializeFlag=True
			self.calibrateButt.configure(bg="red")
			self.initializeFlag=True
		else:
			CBut.initializeFlag=False
			self.calibrateButt.configure(bg="grey")
			self.initializeFlag=False

	def initalizeSystem(self):
		self.initializeMessege=Toplevel()
		self.initializeMessege.title('initalize the system')
		self.initializeMessege.geometry("200x200")
		self.initializeMessege.lift(aboveThis=self.window)
		fromFile =  Button(self.initializeMessege,height = 5, width=20,command=self.fromFile, text="continue session")
		fromFile.pack()
		newSession = Button(self.initializeMessege,height = 5, width=20,command=self.newSession, text="start new session")
		newSession.pack()

	def fromFile(self):
		thread=threading.Thread(target=ParkingStatus().inializeFromFile,args=())
		thread.daemon=True
		thread.start()
		self.initializeMessege.destroy()
	def newSession(self):
		thread=threading.Thread(target=ParkingStatus().newSession,args=())
		thread.daemon=True
		thread.start()
		self.initializeMessege.destroy()

	def recordVideoCallBack(self):
		if(not self.activeBackgroundModeFlag):
			if(not self.recordFlag):
				self.recordButt.configure(bg="red")
				self.recordFlag = True
				self.out = cv.VideoWriter('outpy.avi',cv.VideoWriter_fourcc('M','J','P','G'), 10, (600,300))
			elif(self.recordFlag):
				self.recordButt.configure(bg="grey")
				self.out.release()
				self.recordFlag = False
		else:
			pass
	def recordVideo(self,frame):
		if(self.out is not None):
			frame=cv.cvtColor(frame, cv.COLOR_RGB2BGR)
			self.out.write(frame)	
		else:
			print("Video file is not found")



	def backgroundModeCallBack(self):
		if(not self.activeBackgroundModeFlag):
			self.activeBackgroundModeFlag= True
			self.backgroundModeButt.configure(bg="red")
		else:
			self.activeBackgroundModeFlag=False
			self.backgroundModeButt.configure(bg="grey")

	def closeCurrentVideo(self):
		
		if(self.inputProc.vid.vid is not None):
			self.inputProc.vid.__del__()
		self.window.destroy()


class MyVideoCapture:
	def __init__(self, source):
		self.vid = source

	def get_frame(self):
		if(self.vid is None):
			return
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			if ret:
				# Return a boolean success flag and the current frame converted to BGR
				return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (False, None)

	# Release the video source when the object is destroyed
	def __del__(self):

		if self.vid.isOpened():
			self.vid.release()
		
            
class CBut(object): # control button class
	initializeFlag=False
	def __init__(self,root,id):
		self.tog=0
		self.ID=id
		self.button = Button(root,bg="green", height=5,width=2, command=self.lotStatus)
	def lotStatus(self):
		if(self.initializeFlag):
			ParkingStatus().toggleStatus(self.ID)
		else:
			self.buttonCounter()
	def configure(self,bg):
		self.button.configure(bg=bg)
	def buttonCounter(self):
		showText ="Lot NO: "+str(self.ID)
		showText+= "\nHave been parked for: \n"
		messagebox.showinfo("Lot Counter", showText+self.parkingDuration())
	def parkingDuration(self):
		timeElapsed= ParkingStatus().showTimeCounter(self.ID)
		return timeElapsed

# #Open the video source
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
# args = vars(ap.parse_args())

# get frames from video or camera
# if a video path was not supplied, grab the reference to the webcam
# if not args.get("video", False):
	# cap = VideoStream(src=0,usePiCamera=True).start()
# cap =  cv.VideoCapture(0)
# otherwise, grab a reference to the video file
# else:
# 	cap = cv.VideoCapture(args["video"])

App(Tk(), "Parking Visual Tracking System (PVTS)")


        






















