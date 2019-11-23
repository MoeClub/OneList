# 开始使用
## 通过下面URL登录
[https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All)

## 初始化配置文件
```
# 运行
python3 OneList.py

# 在浏览器地址栏中获取 code 字段内容，粘贴并按回车
# 将会自动初始化的配置文件
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

# 默认监听 127.0.0.1:5288 , 可自行在 app.py 中更改.
```
