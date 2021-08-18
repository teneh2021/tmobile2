import smtpd
import smtplib
from email.message import EmailMessage


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'tenehsheriff@gmail.com'
    msg['from'] = user
    password = 'ikzwywldplguhtad'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #server.connect('smtp.gmail.com', 587)

    server.login(user, password)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    email_alert('Message from 8084285094', 'When is the next bill?', 'svangarmoh@gmail.com')
