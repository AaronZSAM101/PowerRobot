# PowerRobot

## 简介  
  
电费查询脚本，稍微修改代码可用于其他查询。  
  
## 安装  
  
项目使用python 3.11.7进行编写，使用到requests库。如您的环境中没有该库，请使用`pip install requests`进行安装。

如因网络问题导致requests包无法安装，可使用[清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)进行下载。

## 功能
### 推送功能
当前支持邮件及[企业微信机器人](https://developer.work.weixin.qq.com/document/path/91770#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E7%BE%A4%E6%9C%BA%E5%99%A8%E4%BA%BA)两种方式推送
### 配置文件
为保证个人信息的隐私安全，涉及个人的信息通过用户交互输入将存储在`config.json`中，并且在后续脚本运行中自动调用。如遇脚本更新，脚本也会检查配置文件的内容以确保其完整性不会影响脚本运行。
### 自动运行
支持各终端的自动运行，搜索引擎的结果非常完备，参照任一方式操作即可。
### 画饼
- 加入更多的推送方式支持。理论上，只要有推送api，稍微修改代码即可使用。