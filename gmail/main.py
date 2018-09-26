import smtplib


class GoogleMail:
    user = None
    password = None
    recipient = None
    subject = None
    number_of_files = None
    body = '%s new files from reddit' % number_of_files

    def __init__(self, user, password, recipient, subject, number_of_files):
        self.user = user
        self.password = password
        self.recipient = recipient
        self.subject = subject
        self.number_of_files = number_of_files

    def send_email(self):
        gmail_user = self.user
        gmail_pwd = self.password
        FROM = self.user
        TO = self.recipient if type(self.recipient) is list else [self.recipient]
        SUBJECT = self.subject
        TEXT = self.body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
