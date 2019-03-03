from firebase import firebase
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import  datetime
today=datetime.now()
year= str(today.year)
month=str(today.month)
day=str(today.day)
timeIndex=str(today.hour)+'_'+str(today.minute)


try:
	firebase = firebase.FirebaseApplication('https://pvts-afc67.firebaseio.com', None)
except Exception as e:
	print('Erorr: ',e)



# Use a service account
cred = credentials.Certificate('pvts-afc67-firebase-adminsdk-3zyel-5b90b51de2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def updateDataBase(lot,status,timeIn=int(time.time())):
	if(lot == 13 or lot == 14):
		lotType="disabled"
	else:
		lotType = "normal"

	result = firebase.put('/parking_lots', lot,{'type':lotType,'status': status,'time': timeIn})
	# print (result == None)
	db.collection(u'parking_lots').document(str(lot)).collection(u'year').document(year).collection(u'month').document(month).collection(u'day').document(day).collection(u'data').document(timeIndex).set({u'state':status, u'type':lotType,u'timestamp':timeIn})
	
