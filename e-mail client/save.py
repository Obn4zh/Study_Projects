import smtplib
import re
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox
import svertoch
import email
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
from PyQt5 import QtWidgets
from interf import Ui_MainWindow
import sys


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        global user, password,sender, usr, pasw
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send)
        self.ui.pushButton_2.clicked.connect(self.recive)
        usr, ok = QInputDialog().getText(self, "Авторизация", "Введите логин:", QLineEdit.Normal)
        if ok and usr:
            user=usr
        pasw, ok = QInputDialog().getText(self, "Авторизация", "Пароль:", QLineEdit.Normal)
        if ok and pasw:
            password=pasw
            sender=usr
        if len(usr)==0 or len(pasw)==0:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Ошибка")
            error.setInformativeText("Не введён логин/пароль")
            error.setWindowTitle("Messenger")
            error.exec_()
            exit()



    def send(self):
        try:
            server = 'smtp.yandex.ru'
            recipients = [self.ui.lineEdit_2.text()]
            subject = '...'
            texty = self.ui.lineEdit.text()
            self.ui.lineEdit.clear()


            text1=svertoch.encode(texty)

            html = '<html><head></head><body><p>' + text1 + '</p></body></html>'


            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = '<' + sender + '>'
            msg['To'] = ', '.join(recipients)
            msg['Reply-To'] = sender
            msg['Return-Path'] = sender
            msg['X-Mailer'] = 'Python/' + (python_version())

            part_text = MIMEText(text1, 'plain')
            part_html = MIMEText(html, 'html')


            msg.attach(part_text)
            msg.attach(part_html)

            mail = smtplib.SMTP_SSL(server)
            mail.login(user, password)
            mail.sendmail(sender, recipients, msg.as_string())
            print("Отправлено пользователю ",recipients[0])
            self.ui.textBrowser.append("Вы:"+texty)

            mail.quit()
        except:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Ошибка")
            error.setInformativeText("Не удалось отправить сообщение")
            error.setWindowTitle("Messenger")
            error.exec_()


    def recive(self):
        try:
            print("Чтото происходит")
            mail = imaplib.IMAP4_SSL('imap.yandex.ru')
            mail.login(usr, pasw)
            mail.list()
            mail.select("inbox")


            result, data = mail.search(None, "ALL")

            ids = data[0]
            id_list = ids.split()
            latest_email_id = id_list[-1]

            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            print("Сообщение пользователю ",email_message['To'])
            print("От ",email.utils.parseaddr(email_message['From'])[1])
            print(email_message['Date'])

            email_message = email.message_from_string(raw_email_string)

            listMessage=[]
            if email_message.is_multipart():
                for payload in email_message.get_payload():
                    body = payload.get_payload(decode=True).decode('utf-8')
                    listMessage.append(body)
            else:
                body = email_message.get_payload(decode=True).decode('utf-8')
                listMessage.append(body)
            Body = re.split("([<>])", body)
            message=Body[20]
            Message=message.split()

            str_message = Message[0]
            helper = []
            for i in range(len(str_message)):
                helper.append(str_message[i])
            # print(c)
            kk = []
            for i in range(0, len(helper), 2):
                kk.append(helper[i] + helper[i + 1])

            message_from=email.utils.parseaddr(email_message['From'])[1]
            rec_message=svertoch.decode(kk)

            self.ui.textBrowser.append(message_from +": "+ rec_message)
            print("Сообщение: ",rec_message)
        except:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Ошибка")
            error.setInformativeText("Не удалось принять сообщение!")
            error.setWindowTitle("Messenger")
            error.exec_()
            exit()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())