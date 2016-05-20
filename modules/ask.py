#!/usr/bin/env python
"""
ask.py - Yota ask Module
Copyright 2016, Santos D. Dominges
Primer modulo que hago xD
"""

import re, time

r_username = re.compile(r'^[a-zA-Z0-9_]{1,15}$')
r_link = re.compile(r'^https?://ask.fm/\S+$')
r_p = re.compile(r'(?ims)(<p class="js-ask-text.*?</p>)')
r_tag = re.compile(r'(?ims)<[^>]+>')
r_anchor = re.compile(r'(?ims)(<a.*?</a>)')
r_expanded = re.compile(r'(?ims)data-expanded-url=["\'](.*?)["\']')
r_whiteline = re.compile(r'(?ims)[ \t]+[\r\n]+')
r_breaks = re.compile(r'(?ims)[\r\n]+')

def entity(*args, **kargs):
   return web.entity(*args, **kargs).encode('utf-8')

def decode(html): 
   return web.r_entity.sub(entity, html)

def expand(ask):
   def replacement(match):
      anchor = match.group(1)
      for link in r_expanded.findall(anchor):
         return link
      return r_tag.sub('', anchor)
   return r_anchor.sub(replacement, ask)

def read_ask(url):
   bytes = web.get(url)
   shim = '<div class="content clearfix">'
   if shim in bytes:
      bytes = bytes.split(shim, 1).pop()

   for text in r_p.findall(bytes):
      text = expand(text)
      text = r_tag.sub('', text)
      text = text.strip()
      text = r_whiteline.sub(' ', text)
      text = r_breaks.sub(' ', text)
      return decode(text)
   return "Sorry, couldn't get a ask from %s" % url

def format(ask, username):
   return '%s (@%s)' % (ask, username)

def user_ask(username):
   ask = read_ask('http://ask.fm/' + username + "?" + str(time.time()))
   return format(ask, username)

def id_ask(tid):
   link = 'http://ask.fm/' + tid
   data = web.head(link)
   message, status = tuple(data)
   if status == 301:
      url = message.get("Location")
      if not url: return "Sorry, couldn't get a ask from %s" % link
      username = url.split('/')[3]
      ask = read_ask(url)
      return format(ask, username)
   return "Sorry, couldn't get a ask from %s" % link

def ask(m5, input):
   arg = input.group(2)
   if not arg:
      return m5.reply("Give me a link, a username, or a ask id")

   arg = arg.strip()
   if isinstance(arg, unicode):
      arg = arg.encode('utf-8')

   if arg.isdigit():
      m5.say(id_ask(arg))
   elif r_username.match(arg):
      m5.say(user_ask(arg))
   elif r_link.match(arg):
      username = arg.split('/')[3]
      ask = read_ask(arg)
      m5.say(format(ask, username))
   else: m5.reply("Give me a link, a username, or a ask id")

ask.commands = ['fm', 'ask']
ask.thread = True

if __name__ == '__main__':
   print __doc__
