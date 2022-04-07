
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = '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'

class EmailClient(object):
    @staticmethod
    def send_email(to_address, from_address, subject, content):
        message = Mail(
            from_email=from_address,
            to_emails=to_address,
            subject=subject,
            html_content=content)
        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
