#!/usr/bin/env python
"""
lag.py - Yota lag module
"""


from time import time

def lag(m5, input):
    if input.group(2) == None:
        nick = input.nick
    elif input.group(2) != None:
        nick = input.group(2)
    lag = str(time())
    m5.lag[nick] = input.sender
    ctcp = "\x01PING %s\x01" % lag
    m5.msg(nick, ctcp)
lag.commands = ["lag"]
lag.priority = 'low'

def ctcp_lag(m5, input):
    ping = input.group()
    ping = ping.replace("PING", "")
    ping = ping.replace("\x01", "")
    lag = time() - float(ping)
    channel = m5.lag[input.nick]
    m5.msg(channel, "%s lag: %ss" % (input.nick, str(round(lag, 2))))
    del m5.lag[input.nick]
ctcp_lag.event = "NOTICE"
ctcp_lag.rule = "\x01PING *.*\x01"
ctcp_lag.priority = "low"

