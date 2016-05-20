#!/usr/bin/env python
''''
services.py - Yota IRC Services Module
Copyright 2016, Santos D. Dominges
^Yota^ by SantosD
'''

def nickservreg(m5, input):
	'''register the bot's nickname with NickServ'''
	# Must be done through privmsg with owner
	email = m5.config.email
	password = m5.config.nickservpass
	if input.sender.startswith('#'): return
	if input.owner:
		m5.write(['PRIVMSG', 'NICKSERV', 'REGISTER', password, email])
nickservreg.commands = ['nsregister'] # Should only have to be used once. Syntax: !nsregister
nickservreg.priority = 'medium'

def nslogin(m5, input):
	'''log in to NickServ'''
	# Admin only command
	password = m5.config.nickservpass
	if input.admin:
		m5.write(['PRIVMSG', 'NICKSERV', 'IDENTIFY', password])
nslogin.commands = ['nslogin'] # Syntax !nslogin
nslogin.priority = 'medium'

def nsupdate(m5, input):
	'''Update m5's NickServ status'''
	# Admin-only command
	if input.admin:
		m5.write(['PRIVMSG', 'NICKSERV', 'UPDATE'])
nsupdate.commands = ['nsupdate'] # Syntax !nsupdate
nsupdate.priority = 'medium'

def hostservrequest(m5, input):
	'''request a vhost'''
	vhost = m5.config.vhost
	if input.sender.startswith('#'): return # Must be done through privmsg and...
	if input.owner: # ...by the owner
		m5.write(['PRIVMSG', 'HOSTSERV', 'REQUEST', vhost])
hostservrequest.commands = ['vhost'] # Syntax !vhost
hostservrequest.priority = 'medium'

def cslogin(m5, input):
	'''log into a channel through ChanServ'''
	channel = m5.config.cschannel
	password = m5.config.chanservpass
	if input.sender.startswith('#'): return # Must be done through privmsg and...
	if input.owner: # ...by the owner
		m5.write(['PRIVMSG', 'CHANSERV', 'IDENTIFY', channel, password])
cslogin.commands = ['cslogin'] # Syntax !cslogin
cslogin.priority = 'medium'

if __name__ == '__main__': 
	print __doc__.strip()
		
