============================================
=======POP==================================
#!/usr/bin/env python

import poplib

username = 'someuser'
password = 'pass'

mail_server = 'mail.somedomain.com'

p = poplib.POP3(mail_server)
p.user(username)
p.pass_(password)

for msg_id in p.list()[1]:
    print (msg_id)
    outf = open('%s.eml' % msg_id, 'w')
    outf.write('\n'.join(p.retr(msg_id)[1]))
    outf.close()
p.quit()

============================================
=======IMAP=================================

#!/usr/bin/env python
import imaplib
username = 'some_user'
password = '70P53Cr37'
mail_server = 'mail_server'
i = imaplib.IMAP4_SSL(mail_server)
print (i.login(username, password))
print (i.select('INBOX'))
for msg_id in i.search(None, 'ALL')[1][0].split():
    print (msg_id)
    outf = open('%s.eml' % msg_id, 'w')
    outf.write(i.fetch(msg_id, '(RFC822)')[1][0][1])
    outf.close()
i.logout()

============================================
=======SMTP=================================
#!/usr/bin/env python

import smtplib


mail_server = 'localhost'
mail_server_port = 25
from_addr = 'sender@example.com'
to_addr = 'receiver@example.com'
from_header = 'From: %s\r\n' % from_addr
to_header = 'To: %s\r\n\r\n' % to_addr
subject_header = 'Subject: nothing interesting'
body = 'This is a not veryinteresting email.'
email_message = '%s\n%s\n%s\n\n%s' % (from_header, to_header,
                                      subject_header, body)
s = smtplib.SMTP(mail_server, mail_server_port)
s.sendmail(from_addr, to_addr, email_message)
s.quit()

============================================
=======SMTP + Authentication================

#!/usr/bin/env python
import smtplib


mail_server = 'smtp.example.com'
mail_server_port = 465

from_addr = 'foo@example.com'
to_addr = 'bar@exmaple.com'

from_header = 'From: %s\r\n' % from_addr
to_header = 'To: %s\r\n\r\n' % to_addr
subject_header = 'Subject: Testing SMTP Authentication'
body = 'This mail tests SMTP Authentication'
email_message = '%s\n%s\n%s\n\n%s' % (from_header, to_header,
                                      subject_header, body)
s = smtplib.SMTP(mail_server, mail_server_port)
s.set_debuglevel(1)
s.starttls()
s.login("fatalbert", "mysecretpassword")
s.sendmail(from_addr, to_addr, email_message)
s.quit()

============================================
=======SMTP + Attachemt=====================
import email

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import smtplib
import mimetypes

from_addr = 'noah.gift@gmail.com'
to_addr = 'jjinux@gmail.com'
subject_header = 'Subject: Sending PDF Attachemt'
attachment = 'disk_usage.pdf'
body = '''
This message sends a PDF attachment created with Report
Lab.
'''
m = MIMEMultipart()
m["To"] = to_addr
m["From"] = from_addr
m["Subject"] = subject_header
ctype, encoding = mimetypes.guess_type(attachment)
print (ctype, encoding)
maintype, subtype = ctype.split('/', 1)
print (maintype, subtype)
m.attach(MIMEText(body))
fp = open(attachment, 'rb')
msg = MIMEBase(maintype, subtype)
msg.set_payload(fp.read())
fp.close()
encoders.encode_base64(msg)
msg.add_header("Content Disposition", "attachment", filename=attachment)
m.attach(msg)
s = smtplib.SMTP("localhost")
s.set_debuglevel(1)
s.sendmail(from_addr, to_addr, m.as_string())
s.quit()

============================================