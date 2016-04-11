#! /usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'songrui'

import os
import sys
import xlwt
import MySQLdb


reload(sys)
sys.setdefaultencoding("UTF-8")


result1 = []
with open("new_number_1.4.4.txt") as f:
	for line in f.readlines():
		number = line.split(" ")[0]
		attribution = line.split(" ")[1].strip(os.linesep).strip()
		tuple1 = (number, attribution)
		result1.append(tuple1)

result2 = []
with open("new_number_1.4.5.txt") as f:
	for line in f.readlines():
		number = line.split(" ")[0]
		attribution = line.split(" ")[1].strip(os.linesep).strip()
		tuple2 = (number, attribution)
		result2.append(tuple2)

diff_set = list(set(result2) - set(result1))

workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet("Sheet1")
for i in xrange(len(diff_set)):
	worksheet.write(i,0, diff_set[i][0])
	worksheet.write(i,1, diff_set[i][1])

workbook.save("2015年12月变化号段.xls")