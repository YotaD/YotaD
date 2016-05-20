#!/usr/bin/env python
"""
seen.py - Yota Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/m5/
---
Copyright 2016, Santos D. Dominges
^Yota^ by SantosD
"""

import time
from tools import deprecated

def seen(m5, input): 
   """.seen <nick> - Reports when <nick> was last seen."""
   nick = input.group(2)
   if not nick:
      return m5.reply("Need a nickname to search for...")
   nick = nick.lower()

   if not hasattr(m5, 'seen'): 
      return m5.reply("?")

   if m5.seen.has_key(nick): 
      channel, t = m5.seen[nick]
      t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))

      msg = "I last saw %s at %s on %s" % (nick, t, channel)
      m5.reply(msg)
   else: m5.reply("Sorry, I haven't seen %s around." % nick)
seen.rule = (['seen'], r'(\S+)')

@deprecated
def f_note(self, origin, match, args): 
   def note(self, origin, match, args): 
      if not hasattr(self.bot, 'seen'): 
         self.bot.seen = {}
      if origin.sender.startswith('#'): 
         # if origin.sender == '#inamidst': return
         self.seen[origin.nick.lower()] = (origin.sender, time.time())

      # if not hasattr(self, 'chanspeak'): 
      #    self.chanspeak = {}
      # if (len(args) > 2) and args[2].startswith('#'): 
      #    self.chanspeak[args[2]] = args[0]

   try: note(self, origin, match, args)
   except Exception, e: print e
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
