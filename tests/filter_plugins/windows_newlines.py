from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def windows_newlines(value):
    lines = value.splitlines()
    return "\r\n".join(lines)


class FilterModule(object):

    def filters(self):
        return {
            'windows_newlines': windows_newlines
        }
