#!/usr/bin/env python
"""
version.py - m5 Version Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2009-2013, Silas Baronda
Copyright 2018, Santos David
Licensed under the Eiffel Forum License 2.

More info:
 * m5: https://github.com/myano/m5/
 * Phenny: http://inamidst.com/phenny/
"""

from datetime import datetime
from subprocess import *



def ver(m5, input):
        m5.say('YotaD 1.5 by SantosD')
ver.commands = ['version']


def ctcp_version(m5, input):
    commit, author, date = git_info()
    date = date.replace('  ', '')

    m5.write(('NOTICE', input.nick),
            '\x01VERSION Yots 1.5 by SantosD')
ctcp_version.rule = '\x01VERSION\x01'
ctcp_version.rate = 20


def ctcp_source(m5, input):
    m5.write(('NOTICE', input.nick),
            '\x01SOURCE m5 1.5 by SantosD\x01')
    m5.write(('NOTICE', input.nick),
            '\x01SOURCE\x01')
ctcp_source.rule = '\x01SOURCE\x01'
ctcp_source.rate = 10


def ctcp_ping(m5, input):
    text = input.group()
    text = text.replace('PING ', '')
    text = text.replace('\x01', '')
    m5.write(('NOTICE', input.nick),
            '\x01PING {0}\x01'.format(text))
ctcp_ping.rule = '\x01PING\s(.*)\x01'
ctcp_ping.rate = 10


def ctcp_time(m5, input):
    dt = datetime.now()
    current_time = dt.strftime('%A, %d. %B %Y %I:%M%p')
    m5.write(('NOTICE', input.nick),
            '\x01TIME {0}\x01'.format(current_time))
ctcp_time.rule = '\x01TIME\x01'
ctcp_time.rate = 10

if __name__ == '__main__':
    print __doc__.strip()
