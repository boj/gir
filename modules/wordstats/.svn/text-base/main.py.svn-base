import pickle, os, ConfigParser, random

__all__ = ['*']

class userStats:

	def __init__(self, user, hostmask=None):
		self.hostmask = hostmask
		self.username = user
		self.letter_count = 0
		self.word_count = 0
		self.sentence_count = 0

class wordstats:

	def __init__(self, msg):
		self.msg = msg
		
		self.config = ConfigParser.ConfigParser()
		self.config.read("modules/wordstats/wordstats.ini")
		
		self.userdir = self.config.get("data", "userdir")
		
		self.commands = {}
		self.commands["*"] = self.process_count
		self.commands["^!help"] = self.help
		self.commands["^!stats"] = self.stats
		self.commands["^!top10"] = self.topten

	def help(self, channel, message, user):
		self.msg(channel, "wordstats !help:")
		self.msg(channel, "!stats <optional user> - Shows text stats for calling user, or specified user")
		self.msg(channel, "!top10 - Shows the top talkers and their stats")

	def stats(self, channel, message, user):
		s = message.split(" ")
		if len(s) > 1:
			self.print_stats(channel, s[1], user)
		else:	
			self.print_stats(channel, message, user)

	def topten(self, channel, message, user):
		users = []
		data = os.listdir(self.userdir)
		for u in data:
			try:
				f = open(self.userdir + u, 'r')
				user_data = pickle.load(f)
				f.close()
				
				# Insert into array
				if len(users) > 1:
					pos = 1
					ins = False
					for ud in users:
						if ud.word_count < user_data.word_count:
							users.insert(pos, user_data)
							break
				else:
					users.append(user_data)	
			except: # might be a wacky directory
				pass	
				
		msg = "Top 10 talkers (words): "
		count = 1
		for u in users:
			msg = msg + "%i. %s (%i), " % (count, u.username, u.word_count)
			count += 1
		self.msg(channel, msg[:-2])

	def process_count(self, channel, message, user):
		try:
			f = open(self.userdir + user, 'r')
			user_data = pickle.load(f)
			f.close()
		except:
			user_data = userStats(user)
		words = message.split(' ')
		wc = 0
		lc = 0
		for word in words:
			wc = wc + 1
			for letter in word:
				lc = lc + 1
		user_data.letter_count = user_data.letter_count + lc
		user_data.word_count = user_data.word_count + wc
		user_data.sentence_count = user_data.sentence_count + 1

		try:
			f = open(self.userdir + user, 'w')
			pickle.dump(user_data, f)
			f.close()
		except:
			pass	

	def print_stats(self, channel, message, user):
		try:
			f = open(self.userdir + user, 'r')
			user_data = pickle.load(f)
			f.close()
			msg = "%s has typed %i sentences, using %i words, consisting of %i letters, at an average of %i words per sentence." % (user, user_data.sentence_count, user_data.word_count, user_data.letter_count, (user_data.word_count / user_data.sentence_count))
			self.msg(channel, msg)
		except:
			self.msg(channel, "Currently no statistics for " + user)
