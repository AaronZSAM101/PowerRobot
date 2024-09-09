from Config import load_config, init_config, validate_config
from GetInfo import login_and_query, extract_power_info
from Notification import push_notification

def main():
    # 加载配置，如果配置无效则重新初始化
    config = load_config()
    if not config or not validate_config(config):
        config = init_config()

    # 登录并查询电费信息
    response_text = login_and_query(config)
    if response_text:
        # 提取电量信息
        remaining_power, total_power, remaining_balance = extract_power_info(response_text, config['price_per_kwh'])
        if remaining_power and remaining_balance:
            # 推送电量余额通知
            push_notification(config, remaining_balance, remaining_power, total_power)
        else:
            print("未找到匹配的电量信息")

if __name__ == "__main__":
    main()