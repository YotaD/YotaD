#!/usr/bin/env python
"""
info.py - m5 Information Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def doc(m5, input): 
   """Shows a command's documentation, and possibly an example."""
   name = input.group(1)
   name = name.lower()

   if m5.doc.has_key(name): 
      m5.reply(m5.doc[name][0])
      if m5.doc[name][1]: 
         m5.say('e.g. ' + m5.doc[name][1])
doc.rule = ('$nick', '(?i)(?:help|doc) +([A-Za-z]+)(?:\?+)?$')
doc.example = '$nickname: doc tell?'
doc.priority = 'low'

def commands(m5, input): 
   # This function only works in private message
   #if input.sender.startswith('#'): return
   names = ', '.join(sorted(m5.doc.iterkeys()))
   m5.say("I'm sending the commands by pm!")
   m5.msg(input.nick, 'commands it recognizes: ' + names + '.')
   m5.msg(input.nick, ("To get help, do '%s: help ejemplo?' where example is the " + "name the command that you want help.") % m5.nick)
commands.commands = ['commands']
commands.priority = 'low'

def comandos(m5, input): 
   # This function only works in private message
   #if input.sender.startswith('#'): return
   names = ', '.join(sorted(m5.doc.iterkeys()))
   m5.say("Estoy enviando los comandos por pv!")
   m5.msg(input.nick, 'comandos que reconoce: !nsupdate, !frases, !cowsay, !tw, !twitter, !topic, !devoice, !seen, !quit, !stats ' +
                      '!deop, !github_contribs, !flip_reverse, !version, !list_banned_words, !github_search, !msg, !vhost, !tr ' +
					  '!nslogin, !caps, !part, !yota, !fm, !ask, !nsregister, !github_user_info, !github_user_search, !reverse, !me, !commands '+
					  '.join, !color, !github_prs, !flip, !kick, !voice, !mangle, !op' )
   m5.msg(input.nick, ("Para obtener ayuda, hacer '%s: help ejemplo?' donde ejemplo es el " + "name del comando que desea ayuda.") % m5.nick)
comandos.commands = ['comandos']
comandos.priority = 'low'

#def commandsf(m5, input):
#   commands(m5, input)
#commandsf.commands = ['commands']

def ayuda(m5, input): 
   response = (
      'Hola, soy Yota by SantosD :D soy el mejor bot u.u. diga "!comandos" y te enviare un PV con todos mis comandos ' + 
      'Soy administrado por %s '
   ) % m5.config.owner
   m5.reply(response)
ayuda.rule = ('$nick', r'(?i)ayuda(?:[?!]+)?$')
ayuda.priority = 'low'

def help(m5, input): 
   response = (
      'Hi, I m Yota by SantosD :D I m the best bot u.u. Say "!commands" and I will send you a PV with all my commands ' + 
      'I am administered by %s '
   ) % m5.config.owner
   m5.reply(response)
help.rule = ('$nick', r'(?i)help(?:[?!]+)?$')
help.priority = 'low'

def stats(m5, input): 
   """Show information on command usage patterns."""
   commands = {}
   users = {}
   channels = {}

   ignore = set(['f_note', 'startup', 'message', 'noteuri'])
   for (name, user), count in m5.stats.iteritems(): 
      if name in ignore: continue
      if not user: continue

      if not user.startswith('#'): 
         try: users[user] += count
         except KeyError: users[user] = count
      else: 
         try: commands[name] += count
         except KeyError: commands[name] = count

         try: channels[user] += count
         except KeyError: channels[user] = count

   comrank = sorted([(b, a) for (a, b) in commands.iteritems()], reverse=True)
   userank = sorted([(b, a) for (a, b) in users.iteritems()], reverse=True)
   charank = sorted([(b, a) for (a, b) in channels.iteritems()], reverse=True)

   # most heavily used commands
   creply = 'most used commands: '
   for count, command in comrank[:10]: 
      creply += '%s (%s), ' % (command, count)
   m5.say(creply.rstrip(', '))

   # most heavy users
   reply = 'power users: '
   for count, user in userank[:10]: 
      reply += '%s (%s), ' % (user, count)
   m5.say(reply.rstrip(', '))

   # most heavy channels
   chreply = 'power channels: '
   for count, channel in charank[:3]: 
      chreply += '%s (%s), ' % (channel, count)
   m5.say(chreply.rstrip(', '))
stats.commands = ['stats']
stats.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
