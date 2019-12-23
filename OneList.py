#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org

from urllib import request, error, parse
from threading import Thread
import json
import time
import copy
import os


class Utils:
    sizeUnit = (
        ('B', 2 ** 0),
        ('KB', 2 ** 10),
        ('MB', 2 ** 20),
        ('GB', 2 ** 30),
        ('TB', 2 ** 40),
        ('PB', 2 ** 50),
        ('EB', 2 ** 60),
        ('ZB', 2 ** 70),
        ('YB', 2 ** 80)
    )

    @classmethod
    def getSize(cls, size):
        try:
            size = int(size)
        except:
            return "unknown"
        for k, v in cls.sizeUnit:
            if size <= v * 1024:
                return str("{} {}").format(round(size/v, 2), k)
        return "unknown"

    @staticmethod
    def getTime(t=0):
        if t <= 0:
            return int(time.time())
        else:
            return int(int(time.time()) - t)

    @staticmethod
    def formatTime(s="", f="%Y/%m/%d %H:%M:%S"):
        try:
            assert s
            return time.strftime(f, time.strptime(str(s), "%Y-%m-%dT%H:%M:%SZ"))
        except:
            return str("unknow")

    @staticmethod
    def Target(func, args=()):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    @staticmethod
    def http(url, method="GET", headers=None, data=None, coding='utf-8', redirect=True):
        method = str(method).strip().upper()
        method_allow = ["GET", "HEAD", "POST", "PUT", "DELETE"]
        if method not in method_allow:
            raise Exception(str("HTTP Method Not Allowed [{}].").format(method))

        class RedirectHandler(request.HTTPRedirectHandler):
            def http_error_302(self, req, fp, code, msg, headers):
                pass

            http_error_301 = http_error_303 = http_error_307 = http_error_302

        if headers:
            _headers = headers.copy()
        else:
            _headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": ""}
        if data is not None and method in ["POST", "PUT"]:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            data = str(data).encode(coding)
            if 'content-length' not in [str(item).lower() for item in list(_headers.keys())]:
                _headers['Content-Length'] = str(len(data))
        else:
            data = None
        url_obj = request.Request(url, method=method, data=data, headers=_headers)
        if redirect:
            opener = request.build_opener()
        else:
            opener = request.build_opener(RedirectHandler)
        try:
            res_obj = opener.open(url_obj)
        except error.HTTPError as err:
            res_obj = err
        return res_obj


class Config:
    @staticmethod
    def path():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def load(file="config.json"):
        fd = open(os.path.join(Config.path(), file), "r", encoding="utf-8")
        data = fd.read()
        fd.close()
        return json.loads(data)

    @staticmethod
    def update(Obj, file="config.json"):
        data = {}
        data["RefreshToken"] = Obj.refresh_token
        data["FileRefresh"] = Obj.FileRefresh
        data["FolderRefresh"] = Obj.FolderRefresh
        data["RedirectUri"] = Obj.redirect_uri
        data["RootPath"] = Obj.RootPath
        data["SubPath"] = Obj.SubPath
        fd = open(os.path.join(Config.path(), file), "w", encoding="utf-8")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4))
        fd.close()

    @staticmethod
    def default(refreshToken, file="config.json"):
        data = {}
        data["RefreshToken"] = refreshToken
        data["FileRefresh"] = 60 * 15
        data["FolderRefresh"] = 60 * 12
        data["RedirectUri"] = "http://localhost/onedrive-login"
        data["RootPath"] = "/"
        data["SubPath"] = ""
        fd = open(os.path.join(Config.path(), file), "w", encoding="utf-8")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4))
        fd.close()


class OneDrive:
    cache = {}
    cacheUrl = {}
    cacheRoot = {}
    cacheOnce = True
    InCache = False

    def __init__(self, refreshToken, rootPath="", subPath="", fileRefresh=60*30, folderRefresh=60*15, redirectUri="http://localhost/onedrive-login"):
        self.RootPath = rootPath
        self.SubPath = subPath
        self.FileRefresh = int(fileRefresh)
        self.FolderRefresh = int(folderRefresh)
        self.redirect_uri = redirectUri
        self.refresh_token = refreshToken
        self.access_token = ""

    @staticmethod
    def accessData(grantType, redirectUri='http://localhost/onedrive-login'):
        return {
            'client_id': '78d4dc35-7e46-42c6-9023-2d39314433a5',
            'client_secret': 'ZudGl-p.m=LMmr3VrKgAyOf-WevB3p50',
            'redirect_uri': redirectUri,
            'grant_type': grantType,
            "scope": "User.Read Files.ReadWrite.All"
        }

    @staticmethod
    def drivePath(path):
        path = str(path).strip(":").split(":", 1)[-1]
        while '//' in path:
            path = str(path).replace('//', '/')
        if path == "/":
            return path
        else:
            return str(":/{}:").format(str(path).strip('/'))

    @staticmethod
    def urlPath(path, hasRoot=False):
        pathArray = str(str(path).strip(":").split(":", 1)[-1]).strip("/").split("/")
        newPath = str("/").join([parse.unquote(str(item).strip()) for item in pathArray if str(item).strip()])
        if hasRoot:
            setRoot = "/drive/root:/"
        else:
            setRoot = "/"
        iPath = str("{}{}").format(setRoot, newPath)
        if iPath != "/":
            return iPath.rstrip("/")
        else:
            return "/"

    def findCache(self, path, useCache=0):
        path = self.urlPath(path, hasRoot=True)
        if useCache == 0:
            _cache = self.cacheRoot
        else:
            _cache = self.cacheUrl
        if path not in _cache:
            pathArray = str(path).rsplit("/", 1)
            try:
                return _cache[pathArray[0]][pathArray[1]]
            except:
                return None
        else:
            return _cache[path]

    @staticmethod
    def getHeader(accessToken=""):
        _header = {
            'User-Agent': 'ISV|OneList/1.1',
            'Accept': 'application/json; odata.metadata=none',
        }
        if accessToken:
            _header['Authorization'] = str("Bearer {}").format(accessToken)
        return _header

    def getToken(self, respCode):
        data = self.accessData('authorization_code')
        data["code"] = respCode
        Data = "&".join([str("{}={}").format(item, data[item]) for item in data])
        page = Utils.http("https://login.microsoftonline.com/common/oauth2/v2.0/token", "POST", data=Data, headers=self.getHeader())
        resp = json.loads(page.read().decode())
        print(resp)
        if "refresh_token" in resp and "access_token" in resp:
            self.access_token = resp["access_token"]
            self.refresh_token = resp["refresh_token"]
        else:
            raise Exception("Error, Get refresh token.")

    def getAccessToken(self, refreshToken=None):
        data = self.accessData('refresh_token')
        if refreshToken is None:
            data["refresh_token"] = self.refresh_token
        else:
            data["refresh_token"] = refreshToken
        Data = "&".join([str("{}={}").format(item, data[item]) for item in data])
        page = Utils.http("https://login.microsoftonline.com/common/oauth2/v2.0/token", "POST", data=Data, headers=self.getHeader())
        resp = json.loads(page.read().decode())
        if "refresh_token" in resp and "access_token" in resp:
            self.access_token = resp["access_token"]
            self.refresh_token = resp["refresh_token"]
        else:
            raise Exception("Error, Get Access.")

    def listItem(self, path=None):
        if path is None:
            path = self.RootPath
        url = str("https://graph.microsoft.com/v1.0/me/drive/root{}?expand=children($select=name,size,file,folder,parentReference,lastModifiedDateTime)").format(parse.quote(self.drivePath(path)))
        print("Cache:", self.urlPath(path))
        page = Utils.http(url, headers=self.getHeader(self.access_token))
        data = json.loads(page.read().decode())
        if "error" in data:
            print(data["error"]["message"])
        else:
            if "@microsoft.graph.downloadUrl" in data:
                self.getItem(data)
            else:
                self.getFolder(data)

    def getFolder(self, Json):
        if "children" in Json:
            for item in Json["children"]:
                parentKey = str("{}").format(item["parentReference"]["path"])
                if parentKey not in self.cache:
                    self.cache[parentKey] = {"@time": Utils.getTime()}
                self.cache[parentKey][item["name"]] = {
                    "name": item["name"],
                    "size": Utils.getSize(item["size"]),
                    "date": Utils.formatTime(item["lastModifiedDateTime"]),
                    "@time": Utils.getTime()
                }
                if "folder" in item:
                    self.cache[parentKey][item["name"]]["@type"] = "folder"
                    self.listItem(str("{}/{}").format(parentKey, item["name"]))
                elif "file" in item:
                    self.cache[parentKey][item["name"]]["@type"] = "file"

    def getItem(self, Json):
        parentKey = Json["parentReference"]["path"]
        if parentKey not in self.cacheUrl:
            self.cacheUrl[parentKey] = {}
        if Json["name"] not in self.cacheUrl[parentKey]:
            self.cacheUrl[parentKey][Json["name"]] = {}
        try:
            self.cacheRoot[parentKey][Json["name"]]["name"] = Json["name"]
            self.cacheRoot[parentKey][Json["name"]]["date"] = Utils.formatTime(Json["lastModifiedDateTime"])
            self.cacheRoot[parentKey][Json["name"]]["size"] = Utils.getSize(Json["size"])
            self.cacheRoot[parentKey][Json["name"]]["@time"] = Utils.getTime()
            self.cacheRoot[parentKey][Json["name"]]["@type"] = "file"
        except:
            print("Cache Error:", str("{}/{}").format(parentKey, Json["name"]))
        self.cacheUrl[parentKey][Json["name"]]["@link"] = Json["@microsoft.graph.downloadUrl"]
        self.cacheUrl[parentKey][Json["name"]]["@time"] = Utils.getTime()

    def itemCache(self, path, cache):
        NotInCache = False
        isFolder = True
        timeOut = self.FolderRefresh
        if "@type" in cache and cache["@type"] == "file":
            timeOut = self.FileRefresh
            isFolder = False
            if not self.findCache(path, 1):
                NotInCache = True
        if self.InCache:
            if NotInCache and not isFolder:
                self.listItem(path)
        else:
            if NotInCache or Utils.getTime(cache['@time']) >= timeOut:
                self.listItem(path)
        return isFolder

    def pageCache(self, path):
        path = self.urlPath(path)
        cache = self.findCache(path, 0)
        if self.cacheOnce and self.cache:
            self.checkCacheTmp(False)
        if cache:
            isFolder = self.itemCache(path, cache)
        else:
            return None
        if isFolder:
            return self.findCache(path, 0)
        else:
            return self.findCache(path, 1)

    def checkCacheTmp(self, clear=True):
        if self.cache:
            self.cacheRoot = self.cache.copy()
        if clear:
            if self.cacheOnce:
                self.cacheOnce = False
            self.cache = {}

    def checkFile(self):
        if not self.cacheUrl:
            return
        tmpCache = copy.deepcopy(self.cacheUrl)
        for parentItem in tmpCache:
            if not tmpCache[parentItem]:
                del self.cacheUrl[parentItem]
            for Item in tmpCache[parentItem]:
                try:
                    if Utils.getTime(tmpCache[parentItem][Item]['@time']) >= self.FileRefresh:
                        del self.cacheUrl[parentItem][Item]
                except:
                    continue


if __name__ == "__main__":
    while True:
        code = str(input("code:").strip())
        if code: break
    ms = OneDrive("")
    ms.getToken(code)
    Config.default(ms.refresh_token)
    print("Success, Init config.")
