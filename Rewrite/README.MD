# OneList - Written in GoLang
- 支持 国际版, 个人免费版(家庭版), 中国版(世纪互联).
- 支持同时列出多个盘的目录.(要求每个盘的`SubPath`唯一)
- 支持文件夹内超过 200 个项目
- 支持后台自动刷新缓存.
- 支持路径中含有特殊字符.
- 支持使用不同目录使用不同账户密码加密(HTTP 401).
- 支持隐藏目录和文件(跳过缓存).
- 数据储存在内存中,响应更加迅速.

## 授权
### 通过下面URL登录 (右键新标签打开)
#### 国际版, 个人版(家庭版)
[https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=78d4dc35-7e46-42c6-9023-2d39314433a5&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=78d4dc35-7e46-42c6-9023-2d39314433a5&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All)
#### 中国版(世纪互联)
[https://login.chinacloudapi.cn/common/oauth2/v2.0/authorize?client_id=dfe36e60-6133-48cf-869f-4d15b8354769&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All](https://login.chinacloudapi.cn/common/oauth2/v2.0/authorize?client_id=dfe36e60-6133-48cf-869f-4d15b8354769&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All)

## 添加配置文件
```
# 国际版
OneList -a "url" -s "/onedrive01"
# 个人版(家庭版)
OneList -ms -a "url" -s "/onedrive02"
# 中国版(世纪互联)
OneList -cn -a "url" -s "/onedrive03"

# 在浏览器地址栏中获取以 http://loaclhost 开头的整个url内容
# 将获取的完整url内容替换命令中的 url 三个字母
# 每次产生的 url 只能用一次, 重试请重新获取 url
# 可以一个盘内的多个文件夹分别映射到多个`SubPath`上
# 此操作将会自动添加的配置文件
# 提示 Success! Add config. '/path/to/config.json' 则成功
```

## 修改配置文件
```
[
  {
    // 如果是家庭版或者个人免费版, 此项应为 true.
    "MSAccount": false,
    // 如果是中国版(世纪互联), 此项应为 true.
    "MainLand": false,
    // 授权令牌
    "RefreshToken": "1234564567890ABCDEF",
    // 单配置文件中,此项要唯一.将此OneDrive中设置为`RootPath`目录映射在`http://127.0.0.1:5288/onedrive` 下.
    // (只推荐一个盘位的时候使用根目录"/".)
    "SubPath": "/onedrive",
    // 读取OneDrive的某个目录作为根目录. (支持根目录"/")
    "RootPath": "/Test",
    // 隐藏OneDrive目录中的文件夹和文件, 条目间使用 "|" 分割. (跳过缓存设置的条目.)
    "HidePath": "/Test/Obj01|/Test/Obj02",
    // 使用用户名和密码加密OneDrive目录. 目录和用户名密码间使用 "?" 分割, 用户名密码使用 ":" 分割, 条目间使用 "|" 分割. 无效条目将跳过. 
    "AuthPath": "/Test/Auth01?user01:pwd01|/Test/Auth02?user02:pwd02",
    // 缓存刷新间隔.(所有项目中的刷新时间取最小值为有效刷新间隔)
    "RefreshInterval": 900
  }
]
```

## 使用
```
Usage of OneList:
  -a string
        // 初始化配置文件,添加新配置
        Setup and Init auth.json.
  -bind string
        // 绑定IP地址(公网: 0.0.0.0)
        Bind Address (default "127.0.0.1")
  -port string
        // 绑定端口(HTTP:80)
        Port (default "5288")
  -s string
        // 设置 SubPath 项, 需要与 -a 一起使用.
        Set SubPath. [unique per account] (default "/")
  -c string
        // 配置文件
        Config file. (default "config.json")
  -t string
        // Index.html 目录样式文件
        Index file. (default "index.html")
  -cn
        // 开关
        // 授权中国版(世纪互联), 需要此参数.
        OneDrive by 21Vianet.
  -ms
        // 开关
        // 授权个人版(家庭版), 需要此参数.
        OneDrive by Microsoft.
```

## 运行
```
# 保证 config.json 和 index.html 同目录, 直接运行.
$ OneList
# 监听公网 80 端口
$ OneList -bind 0.0.0.0 -port 80
```

## 注意
- 打开空文件夹, 会提示 No Found.
- 请使用 UTF-8 编码模式手动编辑 config.json 文件.

## Nginx 反代配置
```
    location ^~ /onedrive/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:5288;
    }
```

## Client/Secret (~ 2299/12/31)
```
# 国际版: 78d4dc35-7e46-42c6-9023-2d39314433a5| ZudGl-p.m=LMmr3VrKgAyOf-WevB3p50
# 中国版: dfe36e60-6133-48cf-869f-4d15b8354769| H0-1:6.Sb8:WCW/J-c]K@fddCt[i0EZ2
# ReplyURL: http://localhost/onedrive-login
```
