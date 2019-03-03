from time import sleep
from serial import Serial
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase
import threading

counter=0
maxwait=3

valueCount = 0
payload="h"

try:
	firebase= firebase.FirebaseApplication('https://pvts-afc67.firebaseio.com', None)
except Exception as e:
	print(e)

# Use a service account
cred = credentials.Certificate('pvts-afc67-firebase-adminsdk-3zyel-5b90b51de2.json')
firebase_admin.initialize_app(cred,{'databaseURL': 'https://pvts-afc67.firebaseio.com'})

def listener(event):

	print(event.event_type)  # can be 'put' or 'patch'
	print(event.path)  # relative to the reference, it seems
	print(event.data)  # new data at /reference/event.path. None if deleted
	print(type(event.data))
	
	if (type(event.data) is list):
		for i in range (1,len(event.data)):
			sendData(event.data[i]['command'],i)
	elif (type(event.data) is dict):
		path=event.path[1:]
		index=path.find('/')
		if (index!=-1):
			path=path[:index]
		print('path is ',path)
		try:
			sendData(event.data['command'],path)
		except:
			pass
	elif ('command' in event.path):
		path=event.path[1:]
		index=path.find('/')
		path=path[:index]
		print('path is ',path)
		sendData(event.data,path)
	
		
		
def sendData(data,b_id):
	RESEND=True
	ERRORFLAG=False
	payload=str(data)
	serialDevice = "/dev/ttyAMA0" # default for RaspberryPi
	ser = Serial(serialDevice, 115200)

	while RESEND:		
		start=time.time()		
		print("start while loop")
		payload_tosend="AT+SEND=1,"+str(len(payload))+","+payload+"\r\n"
		print("payload to sent",payload_tosend.encode('utf-8'))
		ser.write(payload_tosend.encode('utf-8'))
		while(time.time()-start<15):
			sleep(5)
			print('in 2ed loop')
			if ser.inWaiting():
				bytesToRead = ser.inWaiting()
				testData = ser.read(bytesToRead)
				print(testData)
				testData=str(testData)
				commaIndex=testData.find(payload)
				commaIndex1=testData.find("ERROR0")
				print(commaIndex)
				if(commaIndex>0):
					print(time.time()-start)
					RESEND=False
					break
				elif(commaIndex1>0):
					ERRORFLAG=True
					RESEND=False
					break
				elif(commaIndex==-1):
					print('failed to receive responce')
					RESEND=True
					break
				
					
		if(time.time()-start>15):
			ERRORFLAG=True
				
	ser.close()
	print('out of while loop')
	if(ERRORFLAG):
		firebase.patch('/barricade/'+str(b_id),{'response':False} )	
	else:
		firebase.patch('/barricade/'+str(b_id),{'response':True} )



thread=threading.Thread(target=db.reference('barricade/').listen, args=[listener])
thread.start()
while 1:
	pass
		

