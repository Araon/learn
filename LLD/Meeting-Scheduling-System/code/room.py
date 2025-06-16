class Room:
	"""docstring for Room"""
	def __init__(self, id, capacity):
		self.id = id
		self.capacity = capacity

		def can_accomodate(self, num_people):
			return num_people <= self.capacity

		def is_available(self, start_time, end_time):
			'''
			Check with the calender class to check if the room is booked for the day
			return True if not else false
			'''