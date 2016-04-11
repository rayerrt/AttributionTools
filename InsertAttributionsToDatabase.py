#! /usr/bin/env python
# -*- coding=utf-8 -*-

import os
import sys

import MySQLdb

import xlrd

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

	def createAttributionTable(self,tableName):
		try:
			sql="""create table if not exists `"""+tableName+"""`(
			`ID` int(5) not null auto_increment,
			`number` int(12) not null,
			`attribution_id` int(5) not null,
			`valid` int(1) not null default 0,
			`carrier_id` int(3) not null default 0,
			`reference` varchar(20) binary default null,
			`company` varchar(20) binary default null,
			`modified_time` timestamp default now(),
			primary key(`ID`),
			unique key(`number`)
			)engine=InnoDB default charset=utf8
			"""
			self.cursor.execute(sql)
		except Warning:
			pass

	def createCitiesTable(self):
		try:
			sql="""create table if not exists `Cities` (
			`ID` int(11) not null auto_increment,
			`name` varchar(100) binary default null,
			`fullname` varchar(100) binary default null,
			`modified_time` timestamp default now(),
			primary key (`ID`)
			unique key(`name`)
			)engine=InnoDB default charset=utf8"""
			self.cursor.execute(sql)
		except Warning:
			pass

	def createCarriesTable(self):
		try:
			sql="""create table if not exists `Carries`(
			`ID` int(11) not null auto_increment,
			`carrier` varchar(20) binary default null,
			primary key (`ID`)
			unique key(`carrier`)
			)engine=InnoDB default charset=utf8"""
			self.cursor.execute(sql)
		except Warning:
			pass

	def uniqueFieldInTable(self,tableName,field):
		sql="alter table "+tableName+" add unique(%s)" %field
		self.cursor.execute(sql)

	def insertDataToCities(self,data):
		try:
			sql="insert into Cities(name,fullname) values(%s,%s)"
			self.cursor.execute(sql,data)
			self.conn.commit()
		except MySQLdb.IntegrityError:
			pass

	def insertDataToAttributions(self,tableName,data):
		try:
			sql="insert into "+tableName+"(number,attribution_id,valid,carrier_id,reference,company) values(%s,%s,%s,%s,%s,%s)"
			self.cursor.execute(sql,data)
			self.conn.commit()
		except MySQLdb.IntegrityError:
			pass

	def queryDataFromAttributionsByNumber(self,tableName,number):
		sql="select * from "+tableName+" where number=%s"
		data=(number)
		self.cursor.execute(sql,data)
		result=self.cursor.fetchall()
		if result:
			return result[0]
		else:
			return None

	def queryIDByCityName(self,name):
		sql="select ID from Cities where name=%s"
		data=(name)
		self.cursor.execute(sql,data)
		result=self.cursor.fetchall()
		if result:
			return result[0][0]
		else:
			return -1

	def __del__(self):
		self.conn.close()

class ExcelInfo(object):
	def __init__(self,filepath):
		self.filepath=filepath

		self.sqlInfo=SqlInfo(HOST,USER,PASSWD,DATABASE)


	def addCities(self):
		with open("songrui.txt") as f:
			for i in f.readlines():
				sql="insert into Cities(name) values(%s)"
				data=(i.strip("\n").encode("UTF-8"),"")
				self.sqlInfo.insertDataToCities(data)

	def readXls(self):
		workbook=xlrd.open_workbook(self.filepath,formatting_info=True)
		sheet_nameslist=workbook.sheet_names()
		for sheet_name in sheet_nameslist:
			sheet=workbook.sheet_by_name(sheet_name)
			print sheet_name
			if not sheet_name.isdigit():
				return

			tableName="Attributions"+sheet_name
			self.sqlInfo.createAttributionTable(tableName)
			rownum=sheet.nrows
			if rownum < 0:
				return

			for i in xrange(2,rownum):
				number=sheet.cell(i,0).value
				if type(number) == float:
					number=int(number)
				attribution=sheet.cell(i,1).value
				attribution_id=-1
				if type(attribution) == unicode:
					attribution_id=self.sqlInfo.queryIDByCityName(attribution)
				if attribution_id < 0:
					print number,attribution
					continue
				valid=0
				note=sheet.cell(i,3).value
				if note.count(u"确认官方数据") > 0:
					valid=1
				carrier=0
				reference=""
				data=(number,attribution_id,valid,carrier,reference)
				self.sqlInfo.insertDataToAttributions(tableName,data)

	def readTxt(self):
		with open(self.filepath,"r") as f:
			for line in f.readlines():
				number=line.split(" ")[0]
				attribution=line.split(" ")[1].strip(os.linesep)
				if not number.isdigit():
					print number
					continue
				tableName="Attributions"+number[:3]
				self.sqlInfo.createAttributionTable(tableName)
				if type(number) == float:
					number=int(number)

				attribution_id=-1
				if type(attribution) == str or type(attribution) == unicode:
					attribution_id=self.sqlInfo.queryIDByCityName(attribution)
				if attribution_id < 0:
					#print line
					continue
				valid=1
				carrier=0
				reference=""
				company=0
				data=(number,attribution_id,valid,carrier,reference,company)
				if self.sqlInto.queryAttributionByNumber(number):
					self.sqlInfo.updateAttribution((number, attribution))
				else:
					self.sqlInfo.insertDataToAttributions(tableName,data)
def main():
	filepath=sys.argv[1]
	excelInfo=ExcelInfo(filepath)
	#excelInfo.addCities()
	#excelInfo.readXls()
	excelInfo.readTxt()

if __name__ == "__main__":
	main()
