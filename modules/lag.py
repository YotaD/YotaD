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
    ping = input.group()
    ping = ping.replace("PING", "")
    ping = ping.replace("\x01", "")
    lag = time() - float(ping)
    m5.msg(input.nick, "lag: %s" % str(round(lag, 2)))
ctcp_lag.event = "NOTICE"
ctcp_lag.rule = "\x01PING *.*\x01"
ctcp_lag.priority = "low"
