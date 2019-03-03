# points are recorded from the left of the screen to the right
#each pair of points represent the starting and ending of a dividing line

left_side_coordinates= [(40, 106),(33, 49),(93, 101),(79, 39),
						(140, 90),(135, 25),(191, 80),(185, 19),
						(244, 79),(240, 15),(293, 82),(290, 17),
						(345, 83),(336, 17),(394, 81),(385, 24),
						(441, 83),(429, 25),(484, 85),(472, 30),
						(525, 86),(511, 31),(568, 94),(549, 35),
						(598, 94),(583, 39)]

right_side_coordinates=[(259, 199),(263, 305),(316, 199),(324, 304),(381, 199),(392, 304),
						(438, 195),(458, 290),(497, 195),(515, 287),
						(543, 200),(559, 286),(587, 196),(598, 276)]
# car parking area
zones=['PZ1','PZ2','DZ','NTZ','CPA']
zoneCoord={ 'CPA':{'start':(0,100),'end':(600,195)}, 
			#parking zone1
			'PZ1':{'start':(33, 30),'end':(598, 94)},
			'PZ2':{'start':(259, 199), 'end':(598, 280)}, 
			#danger zone (illegal parking) 
			'DZ' :{'start':(4, 209), 'end':(255, 300)}, 
			#non-tracking zone 
			'NTZ':{'start':(3, 52),'end':(37, 110)}}