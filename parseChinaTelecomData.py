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
import xlrd

reload(sys)
sys.setdefaultencoding("utf-8")

MUNICIPALITY_LIST = [u"北京", u"上海", u"天津", u"重庆"]


def genAttribution(province, city):
    if province in MUNICIPALITY_LIST:
        return province
    else:
        return province + city


def parseXlsFile(excel_file):
    all_number_details = []
    try:
        workbook = xlrd.open_workbook(excel_file)
        worksheet = workbook.sheet_by_index(0)
        row_count = worksheet.nrows
        col_count = worksheet.ncols
        offset = 0
        for i in xrange(row_count):
            row_values = worksheet.row_values(i)
            if row_values[0] == u"省份" and row_values[1] == u"城市" and row_values[2] == u"城市区号":
                offset = i
                break
        if offset == 0:
            print "%s excel格式不合法，请检查" % excel_file
            return None
        title_list = worksheet.row_values(offset)
        if row_count <= offset + 1: return None
        if col_count < 3: return None
        for i in xrange(offset + 1, row_count):
            province = worksheet.cell(i, 0).value
            city = worksheet.cell(i, 1).value
            attribution = genAttribution(province, city)
            for j in xrange(3, worksheet.ncols):
                prefix = worksheet.cell(offset, j).value
                # format_prefix = 0
                if type(prefix) == type(1730.0):
                    format_prefix = int(prefix)
                else:
                    print "%s 格式不能转换为整数" % prefix
                    break
                if format_prefix < 1300 or format_prefix > 1899:
                    print format_prefix
                    continue
                details = worksheet.cell(i, j).value
                if not details or details.strip() == "":
                    continue
                number_list = genNumberInfo(format_prefix, details)
                for num in number_list:
                    if len(num) < 7:
                        print "%s存在少于7位的号码： %s  %s" %(excel_file, format_prefix, num)
                        continue
                    num_attr_details = "%s %s" % (num, attribution)
                    if num_attr_details not in all_number_details:
                        all_number_details.append(num_attr_details)
    except:
        traceback.print_exc()

    with open("songrui.txt", "a") as f:
        for x in all_number_details:
            f.write(x + os.linesep)


def genNumberInfo(prefix, details):
    number_list = []
    suffix_list = details.split("、")
    format_suffix_list = []
    for i in suffix_list:
        if i.find("-") > -1:
            start_num = int(i.split("-")[0])
            end_number = int(i.split("-")[1])
            for j in xrange(start_num, end_number + 1):
                temp = "%03d" % j
                if temp not in format_suffix_list:
                    format_suffix_list.append(temp)
        else:
            temp = "%03d" % int(i)
            if temp not in format_suffix_list:
                format_suffix_list.append(temp)
    for k in format_suffix_list:
        number_list.append("%s%s" % (prefix, k))
    return number_list


def main():
    parseXlsFile(sys.argv[1])


if __name__ == "__main__":
    main()
