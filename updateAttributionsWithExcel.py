#! /usre/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'songrui'

import os
import sys
import xlrd
import traceback
import attributiondb

reload(sys)
sys.setdefaultencoding("utf-8")


def updateAttributionsDb(xls_file):
	if not os.path.exists(xls_file):
		print "%s 不存在"
		return

	try:
		sqlInfo = attributiondb.SqlInfo(attributiondb.HOST, attributiondb.USER, attributiondb.PASSWD,
										attributiondb.DATABASE)
		workbook = xlrd.open_workbook(filename=xls_file)
		worksheet = workbook.sheet_by_index(0)
		for i in xrange(worksheet.nrows):
			if worksheet.cell(i, 0).value == None or worksheet.cell(i, 0).value == "":
				continue
			number = worksheet.cell(i, 0).value
			if type(number) == float:
				number = int(number)
			attribution = worksheet.cell(i, 1).value
			sqlInfo.updateAttribution((number, attribution))
			sqlInfo.queryAttributionByNumber(number)

	except Exception:
		traceback.print_exc()


def main():
	updateAttributionsDb(sys.argv[1])


if __name__ == "__main__":
	main()
