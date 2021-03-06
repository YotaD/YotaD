#!/usr/bin/env python
"""
bannedwords.py - Yota banned words module
Copyright 2015, Josh Begleiter (jbegleiter.com)
Licensed under the Eiffel Forum License 2.
Copyright 2016, Santos D. Dominges
^Yota^ by SantosD
"""

import imp, os, re, time

current_warnings = {}

def ban_user(m5, full_ident, channel, bad_nick):
    mask = full_ident
    reason = "You have violated the banned word policy."
    m5.write(['MODE', channel, '+b', mask])
    m5.write(['KICK', channel, bad_nick, ' :{0}'.format(reason)])

    # Reset the warnings
    try: del current_warnings[bad_nick]
    except: pass

def banned_words(m5, input):
    """
    Listens to a channel for bad words. If one is found it first
    warns a user, then after X warnings kickbans them, where
    X defaults to 0, meaning instant ban.

    User warnings are stored only in memory, and as a result
    restarting m5 will eliminate any warnings.

    Currently bad words must be added to the config, as a future
    addition bad words will be editable by admins using a command.
    """
    global current_warnings

    if not hasattr(m5.config, 'bad_word_limit') or not hasattr(m5.config, 'bad_words'):
        return

    bad_word_limit = m5.config.bad_word_limit or 0
    bad_words = m5.config.bad_words or {}

    if len(bad_words) == 0:
        return

    # We only want to execute in a channel for which we have a wordlist
    if not input.sender.startswith("#") or input.sender not in bad_words:
        return

    # Find which word triggered the event
    # Get a unique list of bad words
    if input.sender not in bad_words:
        return

    match_word = False
    words = bad_words[input.sender]
    for word in words:
        if re.match(r'.*(?:%s).*' % word, input.group()):
            match_word = True
            break

    # Wrong channel for the match
    if not match_word:
        return

    # We don't want to warn or kickban admins
    if input.admin:
        return

    channel = input.sender

    chan_ops = []
    chan_hops = []
    chan_voices = []
    if channel in m5.ops:
        chan_ops = m5.ops[channel]

    if channel in m5.hops:
        chan_hops = m5.hops[channel]

    if channel in m5.voices:
        chan_voices = m5.voices[channel]

    # First ensure m5 is an op
    if m5.nick not in chan_ops:
        return

    # Next ensure the sender isn't op, half-op, or voice
    bad_nick = input.nick
    if bad_nick in chan_ops or bad_nick in chan_hops or bad_nick in chan_voices:
        return

    full_ident = input.full_ident
    if bad_word_limit == 0:
        ban_user(m5, full_ident, channel, bad_nick)
    elif bad_nick in current_warnings:
        if current_warnings[bad_nick] >= bad_word_limit:
            ban_user(m5, full_ident, channel, bad_nick)
        else:
            current_warnings[bad_nick] += 1
            m5.say(bad_word_warning(bad_nick, bad_word_limit, current_warnings[bad_nick]))
    else:
        current_warnings[bad_nick] = 1
        m5.say(bad_word_warning(bad_nick, bad_word_limit, 1))
banned_words.rule = r'(.*)'
banned_words.priority = 'high'

def list_banned_words(m5, input):
    # Only executable in channel
    if not input.sender.startswith('#'):
        return

    if input.sender not in m5.config.bad_words:
        m5.say('There are no banned words in this channel.')
    else:
        chan_words = ', '.join(m5.config.bad_words[input.sender])
        m5.say('Banned words: {0}'.format(chan_words))
list_banned_words.commands = ["list_banned_words"]
list_banned_words.example = '.list_banned_words'
list_banned_words.priority = 'low'

# Create the warning message for violation of this policy
def bad_word_warning(nick, bad_word_limit, current_warnings):
    base_warning = "{0}: Please refrain from using that word or phrase. ".format(nick)
    warnings_remaining = bad_word_limit - current_warnings
    if warnings_remaining == 0:
      base_warning += "You will be banned the next time you violate this policy."
    else:
      base_warning += "You will be banned after {0} further violations of this policy.".format(warnings_remaining)

    return base_warning

if __name__ == '__main__':
    print __doc__.strip()

