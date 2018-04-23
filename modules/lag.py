#!/usr/bin/env python
"""

lag.py - Yota lag module
"""


from time import time

def lag(m5, input):
    nick = input.group(2)
    lag = str(time())
    ctcp = "\x01PING %s\x01" % lag
    m5.write(["PRIVMSG", nick, ctcp])
