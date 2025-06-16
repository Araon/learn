class User:
	def __init__(self, id, name, email):
		self.id = id
		self.name = name
		self.email = email

	def is_busy(self, start_time, end_time):
		'''
		check with the calender class to check if this person is in other meeting or not
		return True if found else false
		'''

