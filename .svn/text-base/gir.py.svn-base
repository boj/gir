# Gir - Twisted Matrix IRC Bot
#
# This bot is specifically designed to dynamically load, reload, and unload
# classes written by 3rd parties while the bot is actively running.
#
# Author:: Brian Jones (mailto:mojobojo@gmail.com)
# Copyright:: Copyright (c) 2007 Brian Jones
# License:: Distributed under the same terms as Twisted Matrix

# twisted
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

# system
import re, string, time, sys, threading, pickle, os, ConfigParser, traceback

# define the configuration file
CONFIG_INI = "config.ini"

# Read the data from CONFIG_INI
# config is global...
config = ConfigParser.ConfigParser()
config.read(CONFIG_INI)

class botConfig:

	def __init__(self):
	    # List of modules the bot holds in memory
		self.modules = []

class ircBot(irc.IRCClient):

	def __init__(self):
		self.nickname 		= config.get("bot", "nickname")
		self.channel 		= config.get("server", "default_channel")
		self.password 		= config.get("server", "server_password")
		self.server     	= config.get("server", "server_address")
		self.admin 			= config.get("bot", "admin")
		self.module_dir 	= config.get("bot_config", "module_dir")
		self.module_exec 	= config.get("bot_config", "module_exec")
		self.bot_data_file 	= config.get("bot_config", "bot_data_file")
		
		self.modules = {}
		self.bot_config = None

		# Load Config
		try:
			self.bot_config = self._read_bot_config()
			for module in self.bot_config.modules:
				print "Loading module [ %s ]" % module
				self.load_module(module, 1)
		# Load a new config on exception		
		except:
			self.bot_config = botConfig()

	def signedOn(self):
		print "Connected to: [ %s ]" % self.server
		print "Joining channel: [ %s ]" % self.channel
		self.join(self.channel)

	def privmsg(self, user, channel, message):
		# Get current timestamp for msg
		now = time.asctime()
		# Split out username
		user = string.split(user, '!', 1)[0]
		try:
			hostmask = string.split(user, '!')[1]
		except:
			pass

		# BOT ADMIN
		if user == self.admin:
			if re.search("^!syshelp", message):
				self.msg(self.admin, "!load <module>: Loads specified module")
				self.msg(self.admin, "!reload <module>: Reloads specified module")
				self.msg(self.admin, "!unload <module>: Unloads specified module")
				self.msg(self.admin, "!instmods: Lists loaded modules")
				self.msg(self.admin, "!listmods: Lists all available modules")
				return 0
			# MODULE HANDLING
			if re.search("^!load", message):
				s = message.split(" ")
				if len(s) > 1:
					self.load_module(s[1])
				return 0
			if re.search("^!reload", message):
				s = message.split(" ")
				if len(s) > 1:
					self.reload_module(s[1])
				return 0
			if re.search("^!unload", message):
				s = message.split(" ")
				if len(s) > 1:
					self.unload_module(s[1])
				return 0
			if re.search("^!instmods", message):
				s = 'Modules loaded'
				for i in self.bot_config.modules:
					s = "%s - %s" % (s, i)
				self.msg(self.admin, s)
				return 0
			if re.search("^!listmods", message):
				list = os.listdir(self.module_dir)
				s = "Module list: ["
				for i in list:
					if not re.search(".py", i) and not re.search(".pyc", i) and not re.search("^\.", i):
						s += "%s, " % i
				s = string.rstrip(s, ", ")		
				s += "]"	
				self.msg(self.admin, s)
				return 0

		# NON COMMAND PROCESSING
		if user != self.server: # Don't process the server text
			if not re.search("^!", message): # Don't process commands
				for name, module in self.modules.iteritems():
					for k,v in module.commands.iteritems():
						# IF A MODULE HAS A * COMMAND, RUN IT AGAINST THE MESSAGE
						if k == "*":
							v(channel, message, user)
			# COMMANDS
			else:
				for name, module in self.modules.iteritems():
					for k,v in module.commands.iteritems():
						# try clause escapes "*"
						try:
							if re.search(k, message):
								v(channel, message, user)
						except:
							pass
		return 0

	def load_module(self, module, override = None):
		if not override:
			for mod in self.bot_config.modules:
				if module == mod:
					self.msg(self.admin, "Cannot import module [ " + module + " ] - module already exists")
					return 0

		m = self._get_module_path(module)
		try:
			__import__(m)
			c = getattr(sys.modules[m], module)
			self.modules[module] = c(self.msg)
			if not override and self.modules[module]:
				self.bot_config.modules.append(module)
				self._write_bot_config()
			print "Loaded module [ %s ]" % module
			try:
				self.msg(self.admin, "Loaded module [ " + module + " ]")
			except:
				# Might not be on a channel yet
				pass
		except ImportError:
			traceback.print_exc()
			print "Failed to load module [ %s ]" % module
			self.msg(self.admin, "Cannot load module [ " + module + " ]")

	def reload_module(self, module):
		found = 0
		for mod in self.bot_config.modules:
			if module == mod:
				found = 1
		if found == 0:
			self.msg(user, "Cannot reload module [ " + module + " ] - module does not exist")
		else:
			try:
				m = self._get_module_path(module)
				del(sys.modules[m])
				__import__(m)
				c = getattr(sys.modules[m], module)
				self.modules[module] = c(self.msg)
				self.msg(self.admin, "Reloaded [ " + module + " ]")
			except ImportError:
				traceback.print_exc()
				self.msg(self.admin, "Cannot reload module [ " + module + " ]")

	def unload_module(self, module):
		m = self._get_module_path(module)
		try:
			del(sys.modules[m])
			del(self.modules[module])
			self.bot_config.modules.remove(module)
			self._write_bot_config()
			self.msg(self.admin, "Unloaded module [ " + module + " ]")
		except:
			self.msg(self.admin, "Cannot unload module [ " + module + " ]")
				
	def _get_module_path(self, module):
		"""
		Constructs a valid module path name.
		"""
		return "%s.%s.%s" % (self.module_dir, module, self.module_exec)

	def _write_bot_config(self):
		"""
		The bot configuration gets written out as a serialized botConfig object.
		"""
		f = open(self.bot_data_file, 'w')
		pickle.dump(self.bot_config, f)
		f.close()

	def _read_bot_config(self):
		"""
		The bot configuration gets read from a serialized botConfig object.
		"""
		f = open(self.bot_data_file, 'r')
		data = pickle.load(f)
		f.close()
		return data

class ircBotFactory(protocol.ClientFactory):

	protocol = ircBot

	def clientConnectionLost(self, connector, reason):
		print "Connection lost: [ %s ]" % reason
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "Connection failed: [ %s ]" % reason
		reactor.stop()

if __name__ == '__main__':
	
	ircbot = ircBotFactory()
	reactor.connectTCP(config.get("server", "server_address"), int(config.get("server", "server_port")), ircbot)
	reactor.run()
