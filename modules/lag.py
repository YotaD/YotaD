#!/usr/bin/env python
"""

lag.py - Yota lag module
"""


from time import time

def lag(m5, input):
    nick = input.nick
    lag = str(time())
    ctcp = "\x01PING %s\x01" % lag
    m5.msg(nick, ctcp)
lag.commands = ["lag"]
lag.priority = 'low'

def ctcp_lag(m5, input):
    pass
