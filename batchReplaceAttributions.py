#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version:
@author: songrui
@license: Apache Licence
@contact: songrui@bbktel.com
"""
import os

import sys
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")

RAW_ATTR_FILE = u"2016年9月13日号段汇总.txt"
REPLACE_ATTR_FILE = u"songrui.txt"


class AttributionDetails(object):
    def __init__(self, number, attribution):
        self.number = number
        self.attribution = attribution


def getAttributionsList(txt_file):
    print "*" * 20 + "start" + "*" * 20
    attributions_list = []
    with open(txt_file) as f:
        for i in f.readlines():
            number = i.split(" ")[0]
            attribution = i.split(" ")[1].strip(os.linesep)
            attribution_details = AttributionDetails(number, attribution)
            attributions_list.append(attribution_details)
    print "*" * 20 + "finish" + "*" * 20
    return attributions_list


def getAttributionsDict(txt_file):
    attributions_dict = {}
    with open(txt_file) as f:
        for i in f.readlines():
            number = i.split(" ")[0]
            attribution = i.split(" ")[1].strip(os.linesep)
            if number not in attributions_dict.keys():
                attributions_dict[number] = attribution
            else:
                print "Duplicate number %s" % number
                break
    return attributions_dict


def main():
    old_attr_details = getAttributionsList(sys.argv[1])
    replace_attr_details = getAttributionsDict(sys.argv[2])
    with open(sys.argv[3], "w") as f:
        for i in old_attr_details:
            if i.number in replace_attr_details.keys():
                new_line = i.number + " " + replace_attr_details.get(i.number) + os.linesep
                replace_attr_details.pop(i.number)
            else:
                new_line = i.number + " " + i.attribution + os.linesep
            f.write(new_line)
        for m in replace_attr_details.keys():
            new_line = m + " " + replace_attr_details.get(m) + os.linesep
            f.write(new_line)


if __name__ == "__main__":
    main()
