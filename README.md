# 开始使用 (测试版,更新中...)
## Bug 较多, 推荐使用 [WriteByGolang](https://github.com/MoeClub/OneList/tree/master/WriteByGolang) 版本
## 已知问题
- 文件夹内超过200个文件问题
- 刷新缓存时卡顿
## 已有特征
- 单html,无第三方引用
- 按文件日期排序/倒序

## 所需依赖
```
# 自行安装 python3
pip3 install tornado
```

## 通过下面URL登录 (右键新标签打开)
[https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=78d4dc35-7e46-42c6-9023-2d39314433a5&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=78d4dc35-7e46-42c6-9023-2d39314433a5&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All)

## 初始化配置文件
```
# 运行
python3 OneList.py

# 在浏览器地址栏中获取 code 字段内容
# 粘贴并按回车, 每个 code 只能用一次
# 此操作将会自动初始化的配置文件
```

## 自定义配置文件
```
# config.json

{
    // OneDrive 中的某个需要列出的目录
    "RootPath": "/Document",
    // 网址中的子路径
    "SubPath": "/onedrive",
    // 目录刷新时间
    "FolderRefresh": 900,
    // 下载链接刷新时间
    "FileRefresh": 1200,
    // 认证令牌, 将会自动更新, 保持默认
    "RefreshToken": "",
    // 这个不用管, 保持默认
    "RedirectUri": "http://localhost/onedrive-login"
}
```

## 运行
```
python3 app.py

# 默认监听 127.0.0.1:5288 , 可在 app.py 中自行更改.
```

## 展示
[https://moeclub.org/onedrive/](https://moeclub.org/onedrive/)
