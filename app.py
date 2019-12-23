#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org

import json
import base64
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.options
import tornado.template
import tornado.httpserver
from threading import Timer, Event
from OneList import OneDrive, Config

config = Config.load()
MS = OneDrive(config['RefreshToken'], config["RootPath"], config["SubPath"], config["FileRefresh"], config["FolderRefresh"], config["RedirectUri"])


class Handler(tornado.web.RequestHandler):
    def realAddress(self):
        if 'X-Real-IP' in self.request.headers:
            self.request.remote_ip = self.request.headers['X-Real-IP']
        return self.request.remote_ip

    def writeString(self, obj):
        if isinstance(obj, (str, int)):
            return obj
        elif isinstance(obj, (dict, list)):
            return json.dumps(obj, ensure_ascii=False)
        else:
            return obj

    def getPath(self, Path):
        Path = str(Path).strip("/").strip()
        Root = str(MS.RootPath).strip("/").strip()
        Sub = str(MS.SubPath).strip("/").strip()
        if Root == "":
            if Path == "":
                return str("/").format(Root)
            else:
                return str("/{}").format(Path)
        else:
            if str(Path).find(Sub) == 0:
                Path = str(Path).replace(Sub, "", 1).strip("/").strip()
            return str("/{}/{}").format(Root, Path)

    def currentPath(self, Path):
        Path = str(Path).strip("/").strip()
        return str("/{}").format(Path)

    @tornado.gen.coroutine
    def get(self, Path):
        try:
            self.realAddress()
            items = MS.pageCache(self.getPath(Path))
            if items is None:
                raise Exception(str("Error: {}; {};").format(Path, self.getPath(Path)))
            if "@link" in items:
                self.redirect(items["@link"], permanent=False)
            else:
                items = base64.b64encode(json.dumps(items).encode('utf-8')).decode('utf-8')
                self.render("index.html", currentPath=self.currentPath(Path), rootPath=self.currentPath(MS.SubPath), items=items)
        except Exception as e:
            print(e)
            self.set_status(404)
            self.write(self.writeString("No Found"))
            self.finish()


class Web:
    @staticmethod
    def main():
        tornado.options.define("host", default='127.0.0.1', help="Host", type=str)
        tornado.options.define("port", default=5288, help="Port", type=int)
        tornado.options.parse_command_line()
        application = tornado.web.Application([(r"/(.*)", Handler)])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()


class LoopRun(Timer):
    def __init__(self, interval, function, args=None, kwargs=None):
        super(LoopRun, self).__init__(interval, function, args=args, kwargs=kwargs)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()

    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class Run:
    @staticmethod
    def Config():
        MS.getAccessToken()
        Config.update(MS)

    @classmethod
    def InitMS(cls):
        cls.Config()
        MS.InCache = False
        MS.listItem()
        MS.checkCacheTmp()
        MS.InCache = True

    @classmethod
    def Refresh(cls, interval, function):
        RefreshTimer = LoopRun(interval, function)
        RefreshTimer.setDaemon(True)
        RefreshTimer.start()


if __name__ == '__main__':
    Run.Refresh(MS.FolderRefresh, Run.InitMS)
    Run.Refresh(60, MS.checkFile)
    Web.main()
