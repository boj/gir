# Make sure to export the classes
__all__ = ['*']

# Class name must also be the same as the directory name it resides in
class example:

	# Receiving msg is optional, but useful if you want
	# to send messages back to the channel.
	def __init__(self, msg):
		self.msg = msg
		
		self.commands = {}
		# * is the wildcard and will be processed every time
		self.commands["*"] = self.count_words
		# The use of regex in the key is valid.  Anything besides
		# * will be considered as a 'command' and not for general
		# processing.
		self.commands["^!repeat"] = self.repeat
		self.commands["^!count"] = self.say_count
		
		self.word_count = 0
		
	# All methods should receive channel, message, and user parameters	
	def repeat(self, channel, message, user):
		self.msg(channel, "%s said: %s" % (user, message))
		
	def count_words(self, channel, message, user):
		self.word_count += len(message.split(" "))
		
	def say_count(self, channel, message, user):
		self.msg(channel, "Current word count is: %i" % self.word_count)	