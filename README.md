# ScribbleSync

## 项目简介：

ScribbleSync 是一款用于将本地 Markdown 文件上传到社交平台上的工具。用户可以通过该工具方便快捷地将自己的 Markdown 笔记转换为社交平台的文章并保存于草稿箱。

## 主要特点：

- 支持 Markdown 文件批量上传。
- 支持通过命令行界面进行操作，使用方便简单。
- 目前仅支持简书

## 使用方法：

1. 下载代码并安装依赖：

```bash
# 若你有conda最好新建一个虚拟环境用于本程序
conda create --name scribblesync python=3.8

# 下载程序
git clone git@github.com:lantary-w/ScribbleSync.git
cd ScribbleSync

# 安装python依赖
conda activate scribblesync
pip install -r requirements.txt
```

2. 配置账号信息：

在 `conf/config.yaml` 中进行配置文件的设置，目前只支持简书，简书的登录模式分为两种手动登录和自动登录，若选择自动登录则需要输入账户密码的配置，且需要手动输入验证码，更推荐手动模式。

```yaml
# 通过下面的配置开启手动登录模式，auto开启自动登录
jianshu:
	login:
		login_mode: manual
```

3. 运行程序：

双击根目录下 `Start_upload.cmd` 文件即可开始运行，将需要上传的markdown文件拖入命令窗口，回车即可。

## 注意事项：

- 请勿滥用该工具，遵守社区规范。
- 如有问题或建议，欢迎在 issue 中提出。