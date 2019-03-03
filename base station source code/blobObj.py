import zone as zoneA
import stateMachine as state_machine
class BlobObj(object):

	
	def __init__ (self):
	
		self.pos = []
		self.color = None
		self.blb_rect = None
		self.state='HYPO'
		self.zone= None
		self.counter = 0
		self.area=0 
		self.cores=0
		
	def addPos(self,in_pos):
		if(type(in_pos) is list):
			self.pos.append(in_pos[-1])
		else:
			self.pos.append(in_pos)
		
		self.counter +=1
		
	def addColor(self, color):
		self.color = color
		
	def addRect(self,rect):
		self.blb_rect= rect
	
	def updateZone(self):
		if (type(self.pos[-1]) is tuple):
			pass_var=self.pos[-1]
		elif(type(self.pos[-1]) is list):
			pass_var= self.pos[-1][-1]
		zoneT = zoneA.decideZone(pass_var)
		if (zoneT is not None):
			self.zone = zoneT	
		
	def updateState(self):
		old_state=self.state
		stateT = state_machine.decideState (self.counter, self.zone, self.state)
		if (stateT is not None):
			self.state = stateT
			
	def addCount(self):
		self.counter+=1
			
			
			
			
			
			
			
			
			
