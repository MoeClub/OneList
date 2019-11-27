# OneDriveUploader

## 授权
### 通过下面URL登录 (右键新标签打开)
[https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&response_type=code&redirect_uri=http://localhost/onedrive-login&response_mode=query&scope=offline_access%20User.Read%20Files.ReadWrite.All)

### 初始化配置文件
```
# 运行
OneDriveUploader -a "code"

# 在浏览器地址栏中获取 code 字段内容
# 将获取的内容替换命令中的 code 四个字母
# 此操作将会自动初始化的配置文件,只需要操作一次
```

## 使用
```
OneDriveUploader.exe -help
Usage of OneDriveUploader.exe:
  -a string
        Setup auth.json.
  -c string
        Config file. (default "auth.json")
  -n string
        Rename file on upload to remote.
  -r string
        Upload to reomte path.
  -s string
        Upload item.
        
```

## 示例
```
# 一些示例:
# 将同目录下的 mm00.jpg 文件上传到 OneDrive 网盘根目录
OneDriveUploader.exe -s "mm00.jpg"

# 将同目录下的 mm00.jpg 文件上传到 OneDrive 网盘根目录,并改名为 mm01.jpg
OneDriveUploader.exe -s "mm00.jpg" -n "mm01.jpg"

# 将同目录下的 Download 文件夹上传到 OneDrive 网盘根目录
OneDriveUploader.exe -s "Download" 

# 将同目录下的 Download 文件夹上传到 OneDrive 网盘Test目录中
OneDriveUploader.exe -s "Download" -r "Test"
```

