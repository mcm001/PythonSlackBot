import time
import event
from slackclient import SlackClient

class Bot(object):

	#Attempt to connect to Slack and listen
	def __init__(self):
		self.slack_client = SlackClient("xoxb-****************")
		self.bot_name = "slacktest"
		self.bot_id = self.get_bot_id()
		
		if self.bot_id is None:
			exit("Error, could not find " + self.bot_name)
	
		self.event = event.Event(self)
		self.listen()
	
	#Get the ID of our bot
	def get_bot_id(self):
		api_call = self.slack_client.api_call("users.list")
		if api_call.get('ok'):
			# retrieve all users so we can find our bot
			users = api_call.get('members')
			for user in users:
				if 'name' in user and user.get('name') == self.bot_name:
					return "<@" + user.get('id') + ">"
			
			return None

	#If the Slack RTM is connected, wait for an event.		
	def listen(self):
		if self.slack_client.rtm_connect(with_team_state=False):
			print "Successfully connected, listening for commands"
			while True:
				self.event.wait_for_event()
				
				time.sleep(1)
		else:
			exit("Error, Connection Failed")

#Processes commands
class Command(object):
	def __init__(self):
		
		#Dictionary of known commands and their actions
		self.commands = { 
			"jump" : self.jump,
			"help" : self.help
		}


	def handle_command(self, user, command):
		response = "<@" + user + ">: "

		#Check if recieved command is in the dictionary
		if command in self.commands:
			response += self.commands[command]()
		
		#Else, error
		else: 
			response += "Sorry I don't understand the command: " + command + ". " + self.help()
		
		return response
		
	def jump(self):
		return "Kris Kross will make you jump jump"
	
	def help(self):
		response = "Currently I support the following commands:\r\n"
		
		for command in self.commands:
			response += command + "\r\n"
			
		return response

import command

class Event:
	def __init__(self, bot):
		self.bot = bot
		self.command = command.Command()
	
	def wait_for_event(self):
		events = self.bot.slack_client.()
		
		if events and len(events) > 0:
			for event in events:
				#print event
				self.parse_event(event)
				
	def parse_event(self, event):
		if event and 'text' in event and self.bot.bot_id in event['text']:
			self.handle_event(event['user'], event['text'].split(self.bot.bot_id)[1].strip().lower(), event['channel'])
	
	def handle_event(self, user, command, channel):
		if command and channel:
			print "Received command: " + command + " in channel: " + channel + " from user: " + user
			response = self.command.handle_command(user, command)
			self.bot.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)