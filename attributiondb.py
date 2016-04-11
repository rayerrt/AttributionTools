__author__ = 'songrui'
# -*- coding=utf-8 -*-
import MySQLdb

HOST = "localhost"
USER = "root"
PASSWD = "bbk12345"
DATABASE = "Attributions"


class SqlInfo(object):
	def __init__(self, host, user, password, database):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.conn = MySQLdb.connect(self.host, self.user, self.password, self.database, use_unicode=True,
									charset="utf8")
		self.cursor = self.conn.cursor()

	def createAttributionTable(self, tableName):
		sql = """create table if not exists `""" + tableName + """`(
        `ID` int(5) not null auto_increment,
        `number` int(12) not null,
        `attribution_id` int(5) not null,
        `valid` int(1) not null default 0,
        `carrier_id` int(3) not null default 0,
        `reference` varchar(20) binary default null,
        `modified_time` timestamp default now(),
        primary key(`ID`)
        )engine=InnoDB default charset=utf8
        """
		self.cursor.execute(sql)

	def createCitiesTable(self):
		sql = """create table if not exists `Cities` (
        `ID` int(11) not null auto_increment,
        `name` varchar(100) binary default null,
        `fullname` varchar(100) binary default null,
        `modified_time` timestamp default now(),
        primary key (`ID`)
        )engine=InnoDB default charset=utf8"""
		self.cursor.execute(sql)

	def createCarriesTable(self):
		sql = """create table if not exists `Carries`(
        `ID` int(11) not null auto_increment,
        `carrier` varchar(20) binary default null,
        primary key (`ID`)
        )engine=InnoDB default charset=utf8"""
		self.cursor.execute(sql)

	def insertDataToCities(self, data):
		sql = "insert into Cities(name,fullname) values(%s,%s)"
		self.cursor.execute(sql, data)
		self.conn.commit()

	def insertDataToAttributions(self, tableName, data):
		sql = "insert into " + tableName + "(number,attribution_id,valid,carrier_id,reference) values(%s,%s,%s,%s,%s)"
		self.cursor.execute(sql, data)
		self.conn.commit()

	def queryDataFromAttributionsByNumber(self, tableName, number):
		sql = "select * from " + tableName + " where number=%s"
		data = (number)
		self.cursor.execute(sql, data)
		result = self.cursor.fetchall()
		if result:
			return result[0]
		else:
			return None

	def queryIDByCityName(self, name):
		sql = "select ID from Cities where name=%s"
		data = (name)
		self.cursor.execute(sql, data)
		result = self.cursor.fetchall()
		if result:
			return result[0][0]
		else:
			print name
			return -1

	def updateAttribution(self, attrubiton_pair):
		attribution = attrubiton_pair[1]
		number_prefix = attrubiton_pair[0] / 10000
		tableName = "Attributions%s" % (number_prefix)
		attribution_id = self.queryIDByCityName(attribution)
		if attribution_id == -1:
			print "发现未知归属地：%s" % attribution
		else:
			sql = "update " + tableName + " set attribution_id=%s,modified_time=now() where number=%s"
			data = (attribution_id, attrubiton_pair[0])
			self.cursor.execute(sql, data)
			self.conn.commit()

	def queryAttributionByNumber(self, number):
		number_prefix = number / 10000
		tableName = "Attributions%s" % (number_prefix)
		sql = "select " + tableName + ".number,Cities.name from " + tableName + ",Cities where Cities.ID=" + tableName + ".attribution_id and " + tableName + ".number=%s"
		data = (number)
		self.cursor.execute(sql, data)
		result = self.cursor.fetchone()
		if result:
			print "number=%s, attribution=%s" % result
			return result
		else:
			return None

	def __del__(self):
		self.conn.close()
