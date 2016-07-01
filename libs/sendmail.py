#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import utils
config = utils.UserConfig()
def send_mail(to_list,sub,content,html=False, attach=None):
    smtp = config['smtp_uri']
    mail_postfix = "gamewave.net"
    mail_host = smtp.split("@")[-1].split(":")[0]
    mail_user = smtp.split(":")[1].split("/")[-1]
    mail_pass = smtp.split("@")[0].split(":")[-1]
    mail_from ="AlertCenter"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = mail_from
    msg['To'] = ";".join(to_list)

    if html:
        mail_body = MIMEText(content,_subtype='html',_charset='utf-8')
    else:
        mail_body = MIMEText(content,_charset='utf-8')
    msg.attach(mail_body)

    if attach:
        for f in attach:
            mail_attach = MIMEApplication(f["body"])
            mail_attach.add_header('Content-Disposition', 'attachment', filename=f["filename"])
            msg.attach(mail_attach)

    try:
        s = smtplib.SMTP()
        print mail_host
        print smtp
        print "start  sendmail \n"*2
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(mail_from, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print e
        return False

