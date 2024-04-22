from room import Room
from user import User



class Meeting:
	def __init__(self, name, agenda, start_time, end_time):
		self.name = name
		self.agenda = agenda
		self.start_time = start_time
		self.end_time = end_time
		self.room = None
		self.attendees = []

	def book_meeting(self, rooms, min_capacity):
		# find room with given args
		for room in rooms:
			if User.can_accomodate(min_capacity) 