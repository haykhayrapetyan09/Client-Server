import itertools
import re


def encode(s):
    encoded = []
    for char, group in itertools.groupby(s):
        count = len(list(group))
        encoded.append(str(count) + char)
    return ''.join(encoded)


def decode(s):
    decoded = []
    for count, char in re.findall('(\d+)(\D)', s):
        decoded.append(char * int(count))
    return ''.join(decoded)
