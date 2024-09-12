import re
import requests
from Notification import send_wechat_message, send_email
# 模拟登录、查询
def login_and_query(config):
    session = requests.Session()

    login_url = config['login_url']
    login_data = {
        "username": config['username'],
        "password": config['password'],
    }

    login_headers = {
        "User-Agent": config['user_agent'],
        "Content-Type": config['content_type'],
        "Referer": config['login_referer'],
        "Origin": config['login_origin'],
    }

    response = session.post(login_url, data=login_data, headers=login_headers, allow_redirects=True)

    if response.status_code == 200 or response.status_code == 302:
        print("登录成功！")
        query_url = config['query_url']
        query_headers = {
            "User-Agent": config['user_agent'],
            "Referer": config['query_referer'],
        }

        query_response = session.get(query_url, headers=query_headers)
        query_response.encoding = 'gb2312'
        return query_response.text
    else:
        # 构建失败消息内容
        error_message = f"登录失败，状态码: {response.status_code}"
        print(error_message)
        if config['wx_robot_url'] != "":
            send_email(config, error_message)
        else:
            send_wechat_message(config['wx_robot_url'], error_message, config="")
            send_email(config, error_message)
        return None

# 正则匹配电量数据
def extract_power_info(response_text, config):
    # 从配置中读取正则表达式
    pattern = config['power_info_regex']
    match = re.search(pattern, response_text)
    if match:
        remaining_power = float(match.group(1))
        total_power = match.group(2)
        remaining_balance = remaining_power * config['price_per_kwh']
        return remaining_power, total_power, remaining_balance
    else:
        return None, None, None
