#encoding=utf-8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from email.mime.text import MIMEText
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
def sendemail(email,url):
    try:
        #输入Email地址和口令:
        from_addr = '1055023220@qq.com'
        password = 'woshishuangwei'
        # 输入SMTP服务器地址:
        smtp_server = 'smtp.qq.com'
        # 输入收件人地址:
        #to_addr = 'todolistoffice@163.com'
        to_addr = email
        msg = MIMEText('<html><body><h1>您好!</h1>' +
        '<p>您的check todolist 账户密码找回 <a href="http://'+url+'">链接</a></p>' +
        '<p>您也可以在浏览器中输入以下网址进行密码找回: http://'+url+'</p>'+
        '</body></html>', 'html', 'utf-8')
        msg['From'] = _format_addr(u'Check ToDoList Office <%s>'%from_addr)
        msg['To']= _format_addr(u'Check User <%s>'%to_addr)
        msg['Subject']= Header(u'Check ToDoList 用户密码找回','utf-8').encode()

        #SMTP协议默认端口是25
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        #server.starttls()
        #server.connect(host=smtp_server, port=25)
        #server.esmtp_features["auth"]="AUTH_LOGIN"
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return True
    except:
        return False
#sendemail("826130720@qq.com","www.baidu.com")