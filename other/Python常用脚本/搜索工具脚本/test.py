#!/usr/bin/env python
# coding: utf-8
import os, os.path
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.sorting import FieldFacet

def get_file_path(root_path,file_list,dir_list):
    #获取该目录下所有的文件名称和目录名称
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in(dir_name, schema)
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)
            print dir_file_path
            if "MAIN" not in dir_file_path:
                f = open(dir_file_path)
                content = f.read()
                dir_file_path=dir_file_path.decode('utf-8')
                content=content.decode('utf-8')
                writer = ix.writer()
                writer.add_document(title=dir_file_path, path=dir_file_path,content=content)
                writer.commit()


dir_name="index" # 检测文件夹名
# 检测文件夹是否存在，如果没有则创建
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in(dir_name, schema)

root_path = dir_name
#用来存放所有的文件路径
file_list = []
#用来存放所有的目录路径
dir_list = []
get_file_path(root_path,file_list,dir_list)

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("a*")
    results = searcher.search(query)
    results[0]