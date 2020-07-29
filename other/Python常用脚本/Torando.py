#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 3:36 下午
# Email    : 506556658@qq.com
# @Author  : Beam
# @Software: PyCharm

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler, url
#从终端模块中导出define模块用于读取参数，导出options模块用于设置默认参数
from tornado.options import define, options
#开始调试模式
import tornado.autoreload
import json

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Content-type", "application/json")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        # self.set_header("Access-Control-Allow-Headers",#"*")
        #   "authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods")


# 定义端口用于指定HTTP服务监听的端口
# 如果命令行中带有port同名参数则会称为全局tornado.options的属性，若没有则使用define定义。
define("port", type=int, default=8999, help="run on the given port")
# 调试模式
define("debug", type=bool, default=True, help="debug mode")


# 创建请求处理器
# 当处理请求时会进行实例化并调用HTTP请求对应的方法
class MainHandler(BaseHandler):
    # 定义get方法对HTTP的GET请求做出响应
    def get(self, *args,  **kwargs):
        # write方法将字符串写入HTTP响应
        self.write("hello world")


class T1(BaseHandler):
    # 定义get方法对HTTP的GET请求做出响应
    def get(self, *args,  **kwargs):
        # write方法将字符串写入HTTP响应
        result = {"isFalse":True,"code":200,"message":"获取成功","data":{"attack":999,"defense":999}}
        self.write(json.dumps(result))

    def options(self, *args,  **kwargs):
        result = {"isFalse":True,"code":200,"message":"success"}
        self.write(json.dumps(result))

class T2(BaseHandler):
    # 定义get方法对HTTP的GET请求做出响应
    def get(self, *args,  **kwargs):
        # write方法将字符串写入HTTP响应
        result = {"isFalse": True, "code": 200, "message": "获取成功", "data": [{"x":"高危","value": 86},{"x":"中危","value": 2312},{"x":"低危","value": 23212}]}
        self.write(json.dumps(result))
    def options(self, *args,  **kwargs):
        result = {"isFalse":True,"code":200,"message":"success"}
        self.write(json.dumps(result))

class T3(BaseHandler):
    # 定义get方法对HTTP的GET请求做出响应
    def get(self, *args,  **kwargs):
        # write方法将字符串写入HTTP响应
        data = [{"name":"总部","noPares":899,"isPares":2883,"newAdd":20},
                {"name":"广东","noPares":667,"isPares":2357,"newAdd":23},
                {"name":"云南","noPares":223,"isPares":2221,"newAdd":56},
                {"name":"贵州","noPares":123,"isPares":6678,"newAdd":67},
                {"name":"海南","noPares":899,"isPares":2883,"newAdd":33},
                {"name":"广西","noPares":899,"isPares":2346,"newAdd":8},
                {"name":"测试1","noPares":899,"isPares":6563,"newAdd":78},
                {"name":"测试2","noPares":899,"isPares":5321,"newAdd":343},
                ]
        result = {"isFalse": True, "code": 200, "message": "获取成功", "data": data}
        self.write(json.dumps(result))
    def options(self, *args,  **kwargs):
        result = {"isFalse":True,"code":200,"message":"success"}
        self.write(json.dumps(result))

class T4(BaseHandler):
    # 定义get方法对HTTP的GET请求做出响应
    def get(self, *args,  **kwargs):
        data = [{"value": "790","xlist": "今天","time": "08:00"},
          { "value": "2000","xlist": "今天","time": "10:00"},
          {"value": "1180","xlist": "今天","time": "12:00"},
          {"value": "1000","xlist": "今天","time": "14:00"},
          {"value": "1100","xlist": "昨天","time": "08:00"},
          {"value": "1400","xlist": "昨天","time": "10:00"},
          {"value": "900","xlist": "昨天","time": "12:00"},
          {"value": "677","xlist": "昨天","time": "14:00"},
          {"value": "550","xlist": "昨天","time": "16:00"},
          {"value": "800","xlist": "昨天","time": "18:00"}
        ]
        # write方法将字符串写入HTTP响应
        result = {"isFalse": True, "code": 200, "message": "获取成功", "data":data}
        self.write(json.dumps(result))
    def options(self, *args,  **kwargs):
        result = {"isFalse":True,"code":200,"message":"success"}
        self.write(json.dumps(result))
# 创建路由表
urls = [
    (r"/", MainHandler),
    (r"/index", MainHandler),
    (r"/t1", T1),
    (r"/t2", T2),
    (r"/t3", T3),
    (r"/t4", T4),
]
# 创建配置
settings = dict(
    debug = options.debug
)

# 创建应用
def make_app():
    return Application(urls, settings)

# 定义服务器
def main():
    # 解析命令行参数
    options.parse_command_line()
    # 创建应用
    app = make_app()
    # 创建HTTP服务器实例
    server = HTTPServer(app)
    # 监听端口
    server.listen(options.port)
    # 创建IOLoop实例并启动
    IOLoop.current().start()

# 应用运行入口，解析命令行参数
if __name__ == "__main__":
    # 启动服务器
    print("开始运行")
    main()
