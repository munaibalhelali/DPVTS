''' this class contains three methods to test for bolb track matching '''
import math
import cv2 as cv

def predictPos(act_pos_q):
	prev_pos=(0,0)
	M=len(act_pos_q)
	if (M>10):
		M=10	
	S=0
	delta_X = 0
	delta_Y = 0
	for m in range (1,M):

		S = S+m
	
	for m in range (1,M):
		ratio = m/S
		mp=m+1
		# get the position (x,y) components 
		#try:
		# print(m,' ',mp)
		if (len(act_pos_q)>m+1):
			xc,yc= act_pos_q[-m]
			xp,yp= act_pos_q[-mp]
			# print(xc,' ',yc,' ',xp,' ',yp)
		else:
			break 
		#except:
		#	break
		# find the x,y delta between the two positions			
		delta_x = (xc-xp)* ratio
		delta_X += delta_x 
		
		delta_y = (yc-yp)* ratio
		delta_Y += delta_y 
		
	CX,CY= act_pos_q[-1]
	pre_pos = (int(CX+delta_X),int(CY+delta_Y))
	if (pre_pos == (0,0)):
		pre_pos = act_pos_q[0]
	# print("predicted position: ",pre_pos,"\nactual position: ",act_pos_q[0])
	return pre_pos
	  
def calDist( pre_pos, new_pos):
	# print("in dist: " ,pre_pos,new_pos)
	try:
		px,py= pre_pos
		nx,ny= new_pos
	except:
		return 1000

	comp_x_sqr = math.pow(nx-px,2)
	comp_y_sqr = math.pow(ny-py,2)
	
	dist= math.sqrt(comp_x_sqr + comp_y_sqr )

	return dist

def calDistThreshold( bound_rect):
	# distance threshold is assumed to be half 
	# the diagonal length of the bounding rectagel

	x,y,w,h = bound_rect
	diagonal= calDist((x,y),(x+w,y+h))
	dist_thres = int(0.5* diagonal)

	return dist_thres
	

#===========================================================================
# below this line are the methods to test for matching
	 
def posMatch( act_pos_q,new_pos, bound_rect):
	# print('car pts: ',act_pos_q)
	pre_pos = predictPos(act_pos_q)
	print('predicted position: ',pre_pos,' ',new_pos)
	if (pre_pos == (0,0)):
		return False
	dist = calDist(pre_pos, new_pos)
	thres = calDistThreshold(bound_rect)
	
	print ('distance is :',dist)
	print ('threshold is :',thres)
	if (dist <= thres):
		return True
	else:
		return False


def colorMatch ( avrg_color, blb_color):
		
		error=10
		blb_r, blb_g, blb_b = blb_color
		avrg_r, avrg_g, avrg_b = avrg_color
		
		if ((blb_r >= avrg_r -error and blb_r <= avrg_r +error) and 
			(blb_g >= avrg_g -error and blb_g <= avrg_g +error) and
			(blb_b >= avrg_b -error and blb_b <= avrg_b +error)):
			
			return True
		else:
			return False
			
def ovrLapMatch(cntBlb,centerBlb,cntCar,ptsCar):
	nx,ny,nw,nh=cntBlb
	cx,cy=centerBlb
	xcen,ycen =ptsCar
	
	distance = calDist(centerBlb,ptsCar)
	if(distance>50):
		return False
	# print('distance: ',distance)
	# print ('blob pos is :',centerBlb)
	# print ('car pos  is :',ptsCar)

	# if(cx > xcen+10 or cx < xcen-10 or cy > ycen+10 or cy < ycen-10):
	# 	return False

	# else:
	
	ox,oy,ow,oh=cntCar
		
	#if ( abs(nx-ox) > abs(ny-oy)):
	if ((nx < ox+ow and nx > ox) or (nx+nw > ox and nx < ox+ow)):

		return True

	#else:
	elif ((ny < oy+oh and ny > oy) or (ny+nh > oy and ny+nh < oy+oh)):

		return True
	else:
		return False	

	
def ovrLapMatchDisP(cntCar,centerCar,rectparking,centParking):
	"""this function check if the detected car is in a given parking lot"""

	nx,ny,nw,nh=cv.boundingRect(cntCar)
	cx,cy=centerCar
	xcen,ycen =centParking
	'''if(cy > ycen+20 or cy < ycen-20):
		return False

	else:'''
	
	ox,oy,ow,oh=rectparking
	
	if ((ny < oy+oh and ny > oy) or (ny+nh > oy and ny+nh < oy+oh)):
		return True
	else:
		return False

def carIn(point,rect):
	"""this function checks if a given point is located in a given rectangle"""
	px,py=point
	rx,ry,rw,rh =rect
	
	if (px>rx and px<rx+rw and py>ry and py< ry+rh):
		return True
	else:
		return False	
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 
	


