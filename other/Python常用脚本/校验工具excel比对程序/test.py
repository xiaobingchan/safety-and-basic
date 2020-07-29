# -*- coding: utf-8 -*-
# 规则比对
import xlrd
import re
import sys     
import datetime
reload(sys)     
sys.setdefaultencoding('utf8')
# 计算时间
start = datetime.datetime.now()

rule_dataworksheet=xlrd.open_workbook("host_rule.xlsx")
rule_dataworksheet=rule_dataworksheet.sheet_by_index(0)
# 获取规则表里面的所有规则
all_list=[]
rule_dataworksheet_nrows=rule_dataworksheet.nrows
for i in range(rule_dataworksheet_nrows-1):
    item_name=rule_dataworksheet.row_values(i+1)
    is_null=item_name[1]
    grep_ev=item_name[2]
    reg_rule=item_name[3]
    all_rule=str(is_null)+";"+str(grep_ev)+";"+str(reg_rule)
    all_list.insert(i,all_rule)

origin_dataworksheet=xlrd.open_workbook("host.xlsx")
origin_dataworksheet=origin_dataworksheet.sheet_by_index(0)
origin_dataworksheet_nrows=origin_dataworksheet.nrows
i=4 #从第4行数据开始
for i in range(origin_dataworksheet_nrows-1):
    # 检测每一行数据
    is_right=True # 是否为错误数据
    item_name=origin_dataworksheet.row_values(i+1)
    print "lyj:"+ str(item_name)
    i2=0
    # 检测每一行的每一个数据
    for items in item_name:
        print "lyj2:"+ str(items)
        its_rule=all_list[i2]
        is_null_rule=its_rule.split(";")[0] # 非空规则
        if ( is_null_rule == 'y'):
            if ( items == ""):
                is_right=False
                print "空数据："+str(items)
            else:
                grep_ev_rule=its_rule.split(";")[1] # 过滤规则
                if ( grep_ev_rule != ""):
                    theList=grep_ev_rule.split(",")
                    if items in theList:
                        is_right=False
                        print "排除数据："+str(items)
                    else:
                        reg_rulees=its_rule.split(";")[2] # 正则规则
                        if ( reg_rulees != ""):
                            if re.match(str(reg_rulees), str(items)):
                                is_right=True
                            else:
                                is_right=False
                                print "正则数据："+str(items)
        else:
            is_right=True
        i2=i2+1
end = datetime.datetime.now()

print "程序运行时间："+str(end-start)