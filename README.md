# 开始使用
## 通过下面URL登录
[https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All)

## 在浏览器地址栏中获取 code 字段内容

## 初始化配置文件
```
# 运行
python3 OneList.py

# 粘贴上一步中获取的code内容并按回车
```

## 自定义配置文件
```
config.json

```
