from Config import is_valid_wx_url
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 推送电量余额通知
def push_power_notification(config, remaining_balance, remaining_power, total_power):
    message_content = f"购买剩余电量: {remaining_power} 度\n总电量: {total_power} 度\n账户剩余金额: {remaining_balance:.2f} 元"
    if remaining_balance <= 25:
        message_content += "\n请及时续费！"
        send_wechat_message(config['wx_robot_url'], message_content)
        send_email(config, message_content)
    else:
        print(f"剩余金额为 {remaining_balance:.2f} 元，足够使用，无需续费。")


# 发送企业微信消息
def send_wechat_message(wx_robot_url, message_content, config):
    if not wx_robot_url:
        print("企业微信机器人URL为空，跳过企业微信消息推送。")
        return

    if not is_valid_wx_url(wx_robot_url):
        print("企业微信机器人URL不符合规范，跳过推送。")
        return
    
    data = {
        "msgtype": "text",
        "text": {
            "content": message_content
        }
    }
    response = requests.post(wx_robot_url, json=data)
    
    if response.status_code == 200:
        print("企业微信消息发送成功")
    else:
        # 构建失败消息内容
        error_message = f"企业微信消息发送失败，状态码: {response.status_code}"
        print(error_message)
        
        # 调整报错信息发送逻辑，发送邮件通知
        send_email(config, error_message, subject="企业微信消息推送失败通知")



# 发送邮件
def send_email(config, message_content, subject="电沸桂de余额提醒"):
    if not config.get('smtp_server'):
        print("邮件服务器未配置，跳过邮件发送。")
        return

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(message_content, 'plain'))

    try:
        # 根据配置选择是否使用 SSL
        if config['use_ssl']:
            server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        else:
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()  # 非SSL需要启动TLS

        server.login(config['smtp_user'], config['smtp_password'])
        # 调整报错信息发送方式
        server.sendmail(config['smtp_user'], config['recipient_email'] + config['admin_email'], msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")
        # 发送企业微信消息通知邮件发送失败
        send_wechat_message(config['wx_robot_url'], f"邮件发送失败: {e}")


# 推送逻辑及文本
def push_notification(config, remaining_balance, remaining_power, total_power):
    message_content = f"您的电费小助手电沸桂提醒您:\n\n购买剩余电量: {remaining_power} 度\n总电量: {total_power} 度\n账户剩余金额: {remaining_balance:.2f} 元"
    
    if remaining_balance <= 25:
        print(f"剩余金额为 {remaining_balance:.2f} 元，再不充钱就等着断电吧。")
        message_content += "\n请及时续费！"
        send_wechat_message(config['wx_robot_url'], message_content, config)
        send_email(config, message_content)

    else:
        print(f"剩余金额为 {remaining_balance:.2f} 元，足够使用，无需续费。")
        message_content += "\n请享受您的美好时光！"
        send_wechat_message(config['wx_robot_url'], message_content, config)
        send_email(config, message_content)
