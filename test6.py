import requests
from datetime import datetime, timedelta
 
def check_billing(api_key, api_url):
    # 计算起始日期和结束日期
    now = datetime.now()
    start_date = now - timedelta(days=90)
    end_date = now + timedelta(days=1)
    sub_date = now.replace(day=1)
 
    # 设置API请求URL和请求头
    url_subscription = f"{api_url}/v1/dashboard/billing/subscription"
    url_balance = f"{api_url}/dashboard/billing/credit_grants"
    url_usage = f"{api_url}/v1/dashboard/billing/usage?start_date={start_date.strftime('%Y-%m-%d')}&end_date={end_date.strftime('%Y-%m-%d')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
 
    try:
        # 获取API限额
        response = requests.get(url_subscription, headers=headers)
        if response.status_code != 200:
            print("查询返回异常。可能是：\n1. apikey没有余额了\n2. apikey无效\n3. apikey的base_url填写错了")
            return
 
        subscription_data = response.json()
        total_amount = subscription_data['hard_limit_usd']
 
        # 判断总用量是否大于20，若大于则更新start_date为sub_date
        if total_amount > 20:
            start_date = sub_date
 
        # 重新生成url_usage
        url_usage = f"{api_url}/v1/dashboard/billing/usage?start_date={start_date.strftime('%Y-%m-%d')}&end_date={end_date.strftime('%Y-%m-%d')}"
 
        # 获取已使用量
        response = requests.get(url_usage, headers=headers)
        usage_data = response.json()
        total_usage = usage_data['total_usage'] / 100
 
        # 计算剩余额度
        remaining = total_amount - total_usage
 
        # 输出总用量、总额及余额信息
        print(f"Total Amount: {total_amount:.2f}")
        print(f"Used: {total_usage:.2f}")
        print(f"Remaining: {remaining:.2f}")
 
        return [total_amount, total_usage, remaining]
    except Exception as error:
        print(error)
        return [None, None, None]
 
# 使用示例
api_key = "sk-Uie4g7hHVCS7h0q81140Fc336dA844369c8dAe0413D36077"
api_base = "https://apix.ai-gaochao.cn"
 
result = check_billing(api_key, api_base)