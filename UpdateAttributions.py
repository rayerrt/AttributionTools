#! /usr/bin/env python
# -*- coding=utf-8 -*-
#查询数据库中所有的归属地信息


from optparse import OptionParser
import traceback

import MySQLdb

HOST="localhost"
#HOST="172.20.201.58"
USER="root"
PASSWD="bbk12345"
DATABASE="Attributions"

import Common

class UpdateAttributions(object):
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.conn=MySQLdb.connect(self.host,self.user,self.password,self.database,use_unicode=True,charset="utf8")
        self.cursor=self.conn.cursor()

	def updateAttribute(self,attributioninfo):
		if type(attributioninfo) == tuple and len(attributioninfo) == 2:
			key=attributioninfo[0]
			attribution=attributioninfo[1]
			sql_query="select ID from Cities where attribution=%s"
			data_query=(attributioninfo)
			self.cursor.execute(sql_query,data_query)
			result_query=self.cursor.fetchall()
			if not result_query:
				print "查询不到该城市信息%s" %attributioninfo
			else:
				attribution_id=result_query[0][0]
				sql_update="update %s set attribution_id=%s"
				data_update=(attribution_id)
				self.cursor.execute(sql_update,data_update)
				self.conn.commit()

def replaceAttributionFromReference(referencefile):
	with open(referencefile) as f:
		for line in f.readlines():
			pass

def main():
	try:
		parser=OptionParser()
		parser.add_option("-r","--replace",action="store",dest="replace_file",help="")
		options,args=parser.parse_args()
		if not options.replace_file:
			pass

	except Exception:
		traceback.print_exc()

if __name__ == "__main__":
	main()