#! /usr/bin/env python
# -*- coding=UTF-8 -*-
# Author: songrui
# version:1.0.0
# 2015.10.12

import os
import sys
import traceback
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding("UTF-8")

def formatAttributions(inputfile,mapping,outputfile):
    mappingdict={}
    with open(mapping) as fm:
        mcontent=fm.readlines()
        for m in mcontent:
            key=m.split(":")[0].decode("UTF-8")
            value=m.split(":")[1].decode("UTF-8")
            if key not in mappingdict.keys():
                mappingdict[key]=value

    print mappingdict.values()[0]
    fo=open(outputfile,"w")
    resultlist=[]
    with open(inputfile) as fi:
        for i in fi.readlines():
            third_new=""
            second=i.split("|")[1].strip()
            third=i.split("|")[2].decode("GB2312").encode("UTF-8").strip()
            if second != "":
                thirdlist=third.split(" ")
                if len(thirdlist) > 1:
                    third_part1=third.split(" ")[0].strip()
                    third_part2=third.split(" ")[1].strip()
                    if cmp(third_part1,"北京") == 0 or cmp(third_part1,"天津") == 0 or cmp(third_part1,"上海") ==0 or cmp(third_part1,"重庆") == 0:
                        third_new=third_part1
                    else:
                        third_new=third_part1+third_part2
                    tempkey=third_new.decode("UTF-8")
                else:
                    tempkey=third.decode("UTF-8")
                if tempkey in mappingdict.keys():
                        tempvalue=mappingdict[tempkey].decode("UTF-8")
                        temp="\""+second+"\","+tempvalue
                        resultlist.append(temp.encode("GB2312"))
                else:
                        print "未发现对该归属地映射:%s %s" %(second,third_new)
        resultlist.sort()
        print resultlist[0]
        for item in resultlist:
            fo.write(item)
    fo.close()

def main():
    try:
        parser=OptionParser("python format_attribution.py -i new_number.txt -m citys_mapping.txt -o songrui.txt")
        parser.add_option("-i","--input",action="store",dest="inputfile",help="指定从数据库中导出来的文件")
        parser.add_option("-m","--mapping",action="store",dest="mappingfile",help="指定归属地映射文件")
        parser.add_option("-o","--output",action="store",dest="outputfile",help="指定输出文件")
        (options,args)=parser.parse_args()
        if not options.inputfile or not options.mappingfile or not options.outputfile:
            print "参数为空!!!"
            return

        if not os.path.exists(options.inputfile) or not os.path.exists(options.mappingfile):
            print "文件不存在!!!"
            return

        formatAttributions(options.inputfile,options.mappingfile,options.outputfile)
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
        main()