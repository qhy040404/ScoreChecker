import json
import os
import smtplib
from email.mime.text import MIMEText

import sso

userid = os.getenv("ID")
passwd = os.getenv("PASSWD")
solutionId = os.getenv("SID")
mailId = os.getenv("MAIL_ID")
mailPass = os.getenv("MAIL_PASS")
semester = os.getenv("SEMESTER")

scoreUrl = "http://jxgl.dlut.edu.cn/student/for-std/grade/sheet/info/" + solutionId + "?semester="

s = sso.login(userid, passwd)


def send_email():
    mail_user = mailId
    mail_pass = mailPass
    sender = mailId
    receiver = mailId
    mail_temp_data = mail_user.split('@')
    mail_host_pre = 'smtp.'
    mail_host = mail_host_pre + mail_temp_data[1]

    print('Sending email...')

    context = "出现了，新成绩"

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
    originalData = s.get(scoreUrl, headers={'Accept': '*/*'}).text
    data = json.loads(originalData).get("semesterId2studentGrades").get("241")
    return len(data)


def main():
    with open("current.txt", "r") as current:
        a = current.read()

    new = get_score()

    print(a)
    print(new)

    if new > int(a):
        with open("current.txt", "w") as current:
            current.write(str(new))
        send_email()


if __name__ == "__main__":
    main()
