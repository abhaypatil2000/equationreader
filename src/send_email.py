# # import smtplib
# # from email.mime.multipart import MIMEMultipart
# # from email.mime.text import MIMEText

# # mail_content = "this is the content of the email"

# # #The mail addresses and password
# # sender_address = "blindreader2000@gmail.com"
# # sender_pass = "Djg3114klFOnSwlbLX"
# # # the address of the receiver
# # receiver_address = 'abhaypatil2000@gmail.com'

# # #Setup the MIME
# # message = MIMEMultipart()
# # message['From'] = sender_address
# # message['To'] = receiver_address
# # message['Subject'] = 'Your requested book in audio is here'  #The subject line

# # #The body and the attachments for the mail
# # message.attach(MIMEText(mail_content, 'plain'))
# # #Create SMTP session for sending the mail
# # session = smtplib.SMTP('smtp.gmail.com', 587)  #use gmail with port
# # session.starttls()  #enable security
# # session.login(sender_address, sender_pass)  #login with mail_id and password
# # text = message.as_string()
# # session.sendmail(sender_address, receiver_address, text)
# # session.quit()
# # print('Mail Sent')

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# mail_content = "this is the content of the email"
# #The mail addresses and password
# sender_address = "blindreader2000@gmail.com"
# sender_pass = "Djg3114klFOnSwlbLX"
# # the address of the receiver
# receiver_address = 'blindreader2000@gmail.com'

# #Setup the MIME
# message = MIMEMultipart()
# message['From'] = sender_address
# message['To'] = receiver_address
# message['Subject'] = 'A test mail sent by Python. It has an attachment.'
# #The subject line

# #The body and the attachments for the mail
# message.attach(MIMEText(mail_content, 'plain'))
# # attach_file_name = "/home/abhay/Downloads/audio.mp3"
# attach_file_name = "/home/abhay/Downloads/pledge.jpg"
# attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
# payload = MIMEBase('application', 'octate-stream')
# payload.set_payload((attach_file).read())
# encoders.encode_base64(payload)  #encode the attachment
# #add payload header with filename
# payload.add_header('Content-Decomposition',
#                    'attachment',
#                    filename=attach_file_name)
# message.attach(payload)
# #Create SMTP session for sending the mail
# session = smtplib.SMTP('smtp.gmail.com', 587)  #use gmail with port
# session.starttls()  #enable security
# session.login(sender_address, sender_pass)  #login with mail_id and password
# text = message.as_string()
# session.sendmail(sender_address, receiver_address, text)
# session.quit()
# print('Mail Sent')

# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "blindreader2000@gmail.com"
toaddr = "blindreader2000@gmail.com"
password = "Djg3114klFOnSwlbLX"

# open the file to be sent
filename = "hello.mp4"  # as seen in attachment
attachment = open("/home/abhay/Downloads/SmartVillageVideo.mp4",
                  "rb")  # on computer

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

# storing the receivers email address
msg['To'] = toaddr

# storing the subject
msg['Subject'] = "Subject of the Mail"

# string to store the body of the mail
body = "Body_of_the_mail"

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

print('now auth')
# Authentication
s.login(fromaddr, password)

# Converts the Multipart msg into a string
text = msg.as_string()

print('sending')
# sending the mail
s.sendmail(fromaddr, toaddr, text)
print('sent')

# terminating the session
s.quit()

print("now quit")