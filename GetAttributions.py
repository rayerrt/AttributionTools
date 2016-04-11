#! /usr/bin/env python
# -*- coding=utf-8 -*-
#查询数据库中所有的归属地信息

import os
import sys
import traceback
from optparse import OptionParser

import MySQLdb

import Common

reload(sys)
sys.setdefaultencoding("UTF-8")

HOST="localhost"
#HOST="172.20.201.58"
USER="root"
PASSWD="bbk12345"
DATABASE="Attributions"

class SqlInfo(object):
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.conn=MySQLdb.connect(self.host,self.user,self.password,self.database,use_unicode=True,charset="utf8")
        self.cursor=self.conn.cursor()

    def queryAttributions(self,tableName,cityName=""):
        try:
            sql="select a.number,b.name from "+tableName+" a,Cities b where a.attribution_id=b.ID"
            data=()
            if cityName:
                sql="select a.number,b.name from "+tableName+" a,Cities b where a.attribution_id=b.ID and b.name=%s"
                data=(cityName)
            if data:
                self.cursor.execute(sql,data)
            else:
                self.cursor.execute(sql)
            result=self.cursor.fetchall()
            if result:
                return result
            else:
                return None
        except MySQLdb.ProgrammingError:
            return None

def main():
    try:
        parser=OptionParser("")
        parser.add_option("-n","--city-name",action="store",dest="cityName",help="指定查询的城市名")
        parser.add_option("-o","--output",action="store",dest="outputfile",help="指定输出文件")
        options,args=parser.parse_args()
        sqlInfo=SqlInfo(HOST,USER,PASSWD,DATABASE)
        output_file=options.outputfile if options.outputfile else "Export.txt"
        f=open(output_file,"w")
        attributionlist=[]
        cityName=options.cityName
        for i in xrange(130,190):
            tableName="Attributions"+str(i)
            result=sqlInfo.queryAttributions(tableName,cityName)
            if result:
                for i in result:
                    attributionlist.append(str(i[0])+" "+i[1]+os.linesep)
        attributionlist.sort()
        for i in attributionlist:
            f.write(i)
        print "导出文件名为%s" %output_file
        f.close()
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()

