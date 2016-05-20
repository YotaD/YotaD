#!/usr/bin/env python
"""
colours.py - Yots Colour Module
Copyright 2016, Santos D. Dominges
"""

colours = {
    "00": "white",
    "01": "black",
    "02": "blue",
    "03": "green",
    "04": "light red",
    "05": "red",
    "06": "magenta (purple)",
    "07": "orange",
    "08": "yellow",
    "09": "light green",
    "10": "cyan",
    "11": "light cyan",
    "12": "light blue",
    "13": "light magenta (pink)",
    "14": "gray",
    "15": "light grey",
    "16": "unk",
    "17": "unk",
    "18": "unk",
}


def test_colours(m5, input):
    if not input.admin:
        return
    output = str()

    keys = colours.keys()
    keys.sort()
    bold_output = str()
    for colour in keys:
        output += "\x03{0}{1} ({0})\x03, ".format(colour, colours[colour])
        bold_output += "\x02\x03{0}{1} ({0})\x03\x02, ".format(colour,
                                                               colours[colour])

    output = output[:-2]
    bold_output = bold_output[:-2]

    m5.say(output)
    m5.say(bold_output)
test_colours.commands = ['color']
test_colours.priority = 'high'


if __name__ == '__main__':
    print __doc__.strip()
