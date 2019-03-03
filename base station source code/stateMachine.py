'this class is used to decide the state of a detected bolb'
''' CPA = car parking zone
	PZ = parking zone
	NTZ = non tracking zone
	DZ = danger zone
	
'''
# NEED TO FIND A WAY TO IMPLEMENT THE "MEREGE" STATE

def decideState(n, zone, curr_state):
# n is the number of frames that the given object appeared in	
	if (curr_state is "HYPO"):
		if (n >= 30 and n<100 ):
			# print('it is normal')
			return "NORMAL"
		
		elif (n >= 100):
			print("before delete: ", n)
			return "DELETE"
	
	elif (curr_state is "NORMAL"):
		if (n >= 50 and zone is "PZ"):
			return "PZ"
			
		elif (n >= 10 and zone is "NTZ"):
			return "NTPZ"
			
		elif (n >= 70 and zone is "DZ"):
			return "DZ"
		# merge condition to be add here 
			
		elif (n >= 1000 and zone is "CPA"):
			return "EXIT"

		elif (n >= 40):
			return "MISMATCH"
			
			
	elif (curr_state is "PZ"):
		
		if (n >= 15 and zone is "PZ"):
			return "NORMAL"
	elif (curr_state is "NTPZ"):
		
		if (n >= 10 and zone is "NTZ"):
			return "NORMAL"
		
	elif (curr_state is "DZ"):
		
		if (n >= 5 and zone is "DZ"):
			return "NORMAL"
			
	elif (curr_state is "MISMATCH"):
		
		if (n >= 100):
			return "DELETE"
		else:
			return  "NORMAL"
	
	elif (curr_state is "EXIT"):
		
		if (n >= 10):
			return "DELETE"
			#return None	
			
			
			
			
