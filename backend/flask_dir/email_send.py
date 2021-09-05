from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

FROM_EMAIL = '<FROM_EMAIL>'
TEMPLATE_ID = '<TEMPLATE_ID>'


def send_dynamic(email):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email)
    message.template_id = TEMPLATE_ID

    try:
        sg = SendGridAPIClient('<SEND_GRID_API>')
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
    except Exception as e:
        print("Error: {0}".format(e))
    return str(response.status_code)


if __name__ == "__main__":
    print('From inside')
