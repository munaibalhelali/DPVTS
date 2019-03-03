from sklearn.cluster import KMeans
import imutils
import numpy as np

'this class is to manipulate the color of a given image'

def find_histogram(clt):
	"""
	create a histogram with k clusters
	:param: clt
	:return:hist
	"""
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins=numLabels)

	hist = hist.astype("float")
	hist /= hist.sum()

	return hist
	
	
def extractColor ( img):
	file_object=open("color_record.txt","a")
	#img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

	img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
	clt = KMeans(n_clusters=3) #cluster number
	clt.fit(img)
	hist = find_histogram(clt)
	currentPercent=0
	carColor=0
	percent_list=[]
	car_color_list=[]
	for (percent, color) in zip(hist, clt.cluster_centers_):
		percent_list.append(percent)
		car_color_list.append(color)

	for g in range (len(percent_list)):
		for i in range(g+1):
			try:
				if (percent_list[i+1]<percent_list[i]):
					currentPercent = percent_list[i]
					carColor = car_color_list[i]
					percent_list[i] = percent_list[i+1]
					car_color_list[i] = car_color_list[i+1]
					percent_list[i+1] = currentPercent
					car_color_list[i+1] = carColor
			except:
				pass


	Hm0,Sm0,Vm0= car_color_list[1]			
	Hm1,Sm1,Vm1= car_color_list[2]

	if(Vm0 < Vm1):
		returnValue= car_color_list[2]
	else:
		returnValue= car_color_list[1]

	file_object.write("carColor is :\n")
	for i in range (len(car_color_list)):

		file_object.write("{},percent:{} %\n".format(car_color_list[i],int(percent_list[i]*100)))
	file_object.close()
	return returnValue
	
def RGBtoHSV(color):
	r,g,b=color
	R = r/255
	G = g/255
	B = b/255
	
	Cmax= max(R,G,B)
	Cmin= min(R,G,B)
	delta = Cmax - Cmin
	
	# calculate H value
	if (delta == 0):
		H=0
	elif (Cmax == R):
		H = (G - B)/delta
		H = (H % 6 ) *60
	elif (Cmax == G):
		H = (B - R)/delta
		H = (H + 2 ) *60
	elif (Cmax == B):
		H = (R - G)/delta
		H = int((H + 4 ) *60)
	
	#calculate S value
	if(Cmax==0):
		S = 0
	else:
		S = int((delta/Cmax)*100)
		
	#calculate V value
	V = int(Cmax*100)
	
	HSV_color=(int(H),S,V)
	
	return HSV_color
	
def decideColor(color):
	H,S,V = color		
	#if (V<=40):
	#	color= "black"
	#elif (S<=10):
		#color= "white"
	if (H>=0 and H<16 or H>240 and H <= 16):
		color= "red"
	elif (H > 16 and H<= 48):
		color= "orange"
	elif (H > 48 and H<= 80):
		color= "yello"
	elif (H > 80 and H<= 112):
		color= "green"
	elif (H > 112 and H<= 144):
		color= "aqua"
	elif (H > 144 and H<= 176):
		color= "blue"
	elif (H > 176 and H<= 208):
		color= "purple"
	elif (H > 208 and H<= 240):
		color= "pink"		
	

	return color	
	
def avrgColor( color_q):
	
	L = len(color_q)
	tx = 0
	ty = 0
	tz = 0
	for i in range (L):
		x,y,z= color_q[i]
		tx += x
		ty += y
		tz += z
	try:		
		return (tx/L, ty/L, tz/L)
	except:
		return (-1);
	
	
	
	
	
