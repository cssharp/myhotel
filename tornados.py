# coding:utf-8
# Created by PyCharm.
# Author  : nick（飞虎队工作室）
# Wechat  : cai9503
# Shop    : https://shop.zbj.com/6463852/
# Date    : 2021/10/6
# Time    : 15:19
import tornado.web  # tornado框架web界面模块
import tornado.ioloop  # tornado框架强大引擎，IO高效核心模块


# 视图层
class IndexHandler(tornado.web.RequestHandler):
    # 在执行get/post请求之前, 都会先执行initialize()方法
    def initialize(self):
        print('this is initialize')

    # 接受get请求
    def get(self):
        print('get。。。。')
        self.write('hello world。。')  # 相当于Django框架中的HttpResponse

    # 接受post请求
    def post(self):
        pass

class NickHandler(tornado.web.RedirectHandler):
    def initialize(self):
        print('this is initialize')
    def get(self):
        self.write('hello nick')
    def post(self):
        self.write('post nick')

if __name__ == "__main__":
    # 配置路由
    app = tornado.web.Application([
        (r'/nick', NickHandler),
        (r'/', IndexHandler),  # 路由匹配试图函数
    ])

    # 绑定端口
    app.listen(8001)  # 绑定端口
    tornado.ioloop.IOLoop.current().start()  # 开始监听端口

