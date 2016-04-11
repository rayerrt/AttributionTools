#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version:
@author: songrui
@license: Apache Licence
@contact: songrui@bbktel.com
"""

import json
import logging
import os
import re
import random
import socket
import sys
import urllib2
import thread
import threading
import time
import traceback

from Queue import Queue

reload(sys)
sys.setdefaultencoding("utf-8")

try:
	os.mkdir("Baidu")
except Exception, e:
	pass

log_file = "Baidu/no_result.txt"

logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w")

ChinaTelecomPrefix = [133, 153, 170, 177, 180, 181, 189]

ChinaUnicomPrefix = [130, 131, 132, 145, 146, 155, 156, 175, 176, 185, 186]

ChinaMobilePrefix = [134, 135, 136, 137, 138, 139, 150, 151, 152, 157, 158, 159, 178, 182, 183, 184, 187, 188]

NumberPrefix = ChinaMobilePrefix + ChinaTelecomPrefix + ChinaUnicomPrefix

WORKER_THREAD_NUM = 3

SHARE_QUEUE = Queue(WORKER_THREAD_NUM)


# 中国移动请求
# request = "http://www1.10086.cn/service/shop/attributionwithcode.jsp?pn=13903030000&verify=85C317&callback
# =jsoncallback&_=1460617540438"
#
# 手机在线请求
# request = "http://v.showji.com/Locating/showji.com2016234999234.aspx?m=%s&output=json&callback
# =querycallback" \
# 	  "&timestamp=1460346780782" % number

# 在0~9999之间生成3各不同的随机数
def makeThreeRandomNumber():
	return random.sample(range(0, 9999), 3)


class QueryThread(threading.Thread):
	def __init__(self, number):
		# threading.Thread.__init__(self)
		super(QueryThread, self).__init__()
		self.number = number
		self.output_txt = "Baidu/%s.txt" % number

	def queryAttribution(self):
		if os.path.exists(self.output_txt):
			os.remove(self.output_txt)

		for suffix in xrange(10000):
			status_list = []
			number = "%s%04d" % (self.number, suffix)
			for extra in makeThreeRandomNumber():
				for i in xrange(100): pass
				request = "http://opendata.baidu.com/api.php?query=%s%04d&co=&resource_id=6004&t=1334456106859&ie" \
						  "=utf8&oe=utf8&cb=bd__cbs__l98142&format=json&tn=baidu" % (number, extra)
				try:
					response = urllib2.urlopen(request, timeout=20)
					result = unicode(response.read(), "utf8")
					regexp = u'"prov":"[\u4e00-\u9fa5]*", "city":"[\u4e00-\u9fa5]+", "type":"[\u4e00-\u9fa5]+"'
					pattern = re.compile(regexp, re.UNICODE)
					group = re.findall(pattern, result)
					if len(group) > 0:
						with open(self.output_txt, "a") as f:
							content = "%s  %s" % (number, group[0])
							f.write(content + os.linesep)
						break
					if number not in status_list:
						status_list.append(number)
						logging.warn(number)
				except Exception, e:
					logging.error(number + " " + e.message)
				# traceback.print_exc()
			time.sleep(1)

	def run(self):
		print self.number
		self.queryAttribution()


def queryAttribution(number):
	output_txt = "Baidu/%s.txt" % number
	if os.path.exists(output_txt):
		os.remove(output_txt)

	for suffix in xrange(10000):
		status_list = []
		area_section = "%s%04d" % (number, suffix)
		for extra in makeThreeRandomNumber():
			for i in xrange(100): pass
			request = "http://opendata.baidu.com/api.php?query=%s%04d&co=&resource_id=6004&t=1334456106859&ie" \
					  "=utf8&oe=utf8&cb=bd__cbs__l98142&format=json&tn=baidu" % (area_section, extra)
			try:
				response = urllib2.urlopen(request, timeout=20)
				result = unicode(response.read(), "utf8")
				regexp = u'"prov":"[\u4e00-\u9fa5]*", "city":"[\u4e00-\u9fa5]+", "type":"[\u4e00-\u9fa5]+"'
				pattern = re.compile(regexp, re.UNICODE)
				group = re.findall(pattern, result)
				if len(group) > 0:
					with open(output_txt, "a") as f:
						content = "%s  %s" % (area_section, group[0])
						f.write(content + os.linesep)
					break
				if area_section not in status_list:
					status_list.append(area_section)
					logging.warn(area_section)
			except Exception, e:
				logging.error(area_section + " " + e.message)
			# traceback.print_exc()
			time.sleep(5)


def worker(number):
	global SHARE_QUEUE
	while True:
		if not SHARE_QUEUE.empty():
			item = SHARE_QUEUE.get()
			queryAttribution(number)
			SHARE_QUEUE.task_done()


def main():
	global SHARE_QUEUE
	threads = []
	for prefix in ChinaTelecomPrefix:
		threads.append(prefix)
		queryThread = threading.Thread(target=worker, args=[prefix])
		queryThread.setDaemon(True)
		queryThread.start()

	for item in threads:
		SHARE_QUEUE.put(item)
	SHARE_QUEUE.join()


if __name__ == "__main__":
	main()
