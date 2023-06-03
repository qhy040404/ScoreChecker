import os
import smtplib
from email.mime.text import MIMEText

import sso

userid = os.getenv("ID")
passwd = os.getenv("PASSWD")
solutionId = os.getenv("SID")
mailId = os.getenv("MAIL_ID")
mailPass = os.getenv("MAIL_PASS")
notify = os.getenv("NOTIFICATION")
notify_solution = os.getenv("NOTIFY_SOLUTION")
notify_solution_failed = os.getenv("NOTIFY_SOLUTION_FAILED")

scoreUrl = "http://jxgl.dlut.edu.cn/student/for-std/grade/sheet/info/" + solutionId + "?semester="
solutionUrl = "http://jxgl.dlut.edu.cn/student/for-std/program-completion-preview/info/" + solutionId

s = sso.login(userid, passwd)


def send_email(result):
    mail_user = mailId
    mail_pass = mailPass
    sender = mailId
    receiver = mailId
    mail_temp_data = mail_user.split('@')
    mail_host_pre = 'smtp.'
    mail_host = mail_host_pre + mail_temp_data[1]

    print('Sending email...')

    context = notify + "出了，焯\n" + result

    message = MIMEText(context, 'plain', 'utf-8')
    message['Subject'] = '死亡降临'
    message['From'] = sender
    message['To'] = receiver

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        print('Email succeed')
    except smtplib.SMTPException as e:
        print('Email error', e)


def get_score():
    originalData = s.get(scoreUrl).text
    if notify in originalData:
        print("Detected.")
        send_email("下一封才刺激doge")
        os.system("mv ../.github/workflows/main.yml ../.github/workflows/main.yml.bak")
    else:
        print("Still alive!")


def get_solution():
    originalData = s.get(solutionUrl).text
    if notify_solution in originalData:
        print(originalData.split(notify_solution)[1].split("'nameEn':'Linear Algebra A'")[0])
        print("Yeah!!!")
        send_email(f"过了哈哈哈哈哈哈\n{originalData.split(notify_solution)[1].split("'nameEn':'Linear Algebra A'")[0]}")
    elif notify_solution_failed in originalData:
        print("芭比Q了")
        send_email("芭比Q了")
    else:
        print("Still alive!")


def main():
    get_score()
    get_solution()


if __name__ == "__main__":
    main()
