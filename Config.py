import json
import re

# 正则表达式检查企业微信 URL 是否有效
def is_valid_wx_url(url):
    pattern = r"https://qyapi\.weixin\.qq\.com/cgi-bin/webhook/send\?key=.*"
    return re.match(pattern, url) is not None

# 检查并加载配置文件
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# 验证正则表达式输入格式是否正确
def validate_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False

# 验证价格输入是否为浮点数
def validate_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def init_config():
    print('正在初始化配置文件，请根据提示进行操作')
    config = {}
    config['username'] = input("请输入用户名:").strip()
    config['password'] = input("请输入密码:").strip()
    config['user_agent'] = input("请输入登陆时的User-Agent（默认值建议保持不变，按回车留空即可）:").strip() or "Mozilla/5.0"
    config['content_type'] = input("请输入Content-Type（默认值建议保持不变，按回车留空即可）:").strip() or "application/x-www-form-urlencoded"
    config['login_url'] = input("请输入登陆时的api url:").strip()
    config['login_referer'] = input("请输入登录时的Referer:").strip()
    config['login_origin'] = input("请输入登录时的Origin:").strip()
    config['query_url'] = input('请输入查询地址的api url:').strip()
    config['query_referer'] = input('请输入查询时的Referer:').strip()

    # 验证正则表达式输入并进行反斜杠转义
    while True:
        power_info_regex = input('请输入查询的正则表达式:').strip()
        if validate_regex(power_info_regex):
            # 转换反斜杠为双反斜杠
            config['power_info_regex'] = power_info_regex.replace('\\', '\\\\')
            break
        else:
            print("无效的正则表达式，请重新输入。")

    # 验证电价输入
    while True:
        price_per_kwh = input("请输入单位电价:").strip()
        if validate_float(price_per_kwh):
            config['price_per_kwh'] = float(price_per_kwh)
            break
        else:
            print("无效的电价，请输入有效的浮点数。")

    # 其他配置项
    config['wx_robot_url'] = input("请输入企业微信机器人URL（如不使用企业微信推送可留空）:").strip()
    config['smtp_server'] = input("请输入SMTP服务器地址（如不使用邮件推送可留空）:").strip()

    if config['smtp_server']:
        config['smtp_port'] = int(input("请输入SMTP端口号:").strip())
        config['use_ssl'] = input("该端口是否为SSL连接？请输入 yes 或 no:").strip().lower() == 'yes'
        config['smtp_user'] = input("请输入邮箱用户名:").strip()
        config['smtp_password'] = input("请输入邮箱密码:").strip()
        config['admin_email'] = input("请输入机器人管理员邮箱（多个邮箱用英文逗号分隔）:").strip().split(',')
        config['recipient_email'] = input("请输入收件人邮箱（多个邮箱用英文逗号分隔）:").strip().split(',')

    # 保存配置
    with open('config.json', 'w') as f:
        json.dump(config, f, indent="\t")
    return config

# 验证配置文件的完整性
def validate_config(config):
    required_keys = ['username', 'password', 'user_agent', 'content_type', 'login_url', 'login_referer', 'login_origin', 'query_url', 'query_referer', 'power_info_regex', 'price_per_kwh']
    email_required_keys = ['smtp_server', 'smtp_port', 'use_ssl', 'smtp_user', 'smtp_password', 'recipient_email']

    # 检查必填项是否存在
    missing_keys = [key for key in required_keys if key not in config or not config[key]]

    # 如果存在 email相关字段 配置，检查相关字段是否完整
    if any(config.get(key) for key in email_required_keys):
        print("检测到邮件字段配置...")
        missing_email_keys = [key for key in email_required_keys if key not in config or not config[key]]
        missing_keys.extend(missing_email_keys)
    else:
        print("未配置邮件相关字段，跳过邮件检查。")

    # 检查企业微信 URL 的有效性
    wx_robot_url = config.get('wx_robot_url', '')
    if wx_robot_url:
        if is_valid_wx_url(wx_robot_url):
            print("企业微信URL配置有效。")
        else:
            print("企业微信URL配置无效。")
            missing_keys.append('wx_robot_url')

    # 如果有缺失的键或值为空，返回 False
    if missing_keys:
        print(f"配置文件中缺少以下字段或值为空: {missing_keys}")
        return False
    
    return True
