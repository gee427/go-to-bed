# @Time : 15/7/2024 下午9:53
# @Author : G5116
import smtplib, os
from datetime import datetime
from email.mime.text import MIMEText

import pytz


def get_beijing_time():
    # 设置UTC和北京时间的时区
    utc_zone = pytz.utc
    beijing_zone = pytz.timezone('Asia/Shanghai')
    # 获取当前的UTC时间，并添加UTC时区信息
    utc_time = datetime.now(utc_zone)
    # 将UTC时间转换为北京时间
    beijing_time = utc_time.astimezone(beijing_zone)
    # 格式化北京时间为 "年-月-日 星期几 时:分" 格式
    return beijing_time.strftime('%Y-%m-%d %A %H:%M')


def send_QQ_email_plain(content):
    # 发件邮箱 + SMTP 授权码从环境变量读取（在 GitHub Secrets 中配置，避免硬编码泄露）
    sender = user = os.getenv('SENDER_EMAIL')
    passwd = os.getenv('SENDER_AUTH_CODE')

    # 未配置发件邮箱/授权码时，跳过发送但不中断任务
    if not sender or not passwd:
        print('未配置发件邮箱(SENDER_EMAIL)或授权码(SENDER_AUTH_CODE)，跳过邮件发送。结果：' + content)
        return

    # 格式化北京时间为 "年-月-日 星期几 时:分" 格式
    formatted_date = get_beijing_time()

    # 纯文本内容
    msg = MIMEText(f'签到结果：{content}', 'plain', 'utf-8')

    # 判断签到结果是否成功
    result_status = "✅成功" if "成功" in content else "❌失败"

    # 设置邮件主题为今天的日期和星期以及签到结果状态
    msg['From'] = f'{sender}'
    msg['To'] = os.getenv('EMAIL_ADDRESS')
    msg['Subject'] = f'查寝 {result_status} {formatted_date}'  # 设置邮件主题

    try:
        # 建立 SMTP 、SSL 的连接，连接发送方的邮箱服务器
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)

        # 登录发送方的邮箱账号
        smtp.login(user, passwd)

        # 发送邮件：发送方，接收方，发送的内容
        smtp.sendmail(sender, os.getenv('EMAIL_ADDRESS'), msg.as_string())

        print('邮件发送成功')

        smtp.quit()
    except Exception as e:
        print(e)
        print('发送邮件失败')
