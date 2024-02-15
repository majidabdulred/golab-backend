import smtplib
from email.mime.text import MIMEText
import os
from starlette.concurrency import run_in_threadpool
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("EMAIL_PASSWORD")

async def send_mail(to,name, otp):
    try:
        msg = MIMEText(create_template(name,otp), 'html')
        msg['Subject'] = f"Email Verification"
        msg['From'] = "otp@golabtest.net"
        msg['To'] = to

        await run_in_threadpool(smtp_send_mail, msg)

    except Exception as e:
        print('Sending mail failed', e)
        raise e


def smtp_send_mail(msg):
    """Synchronous code to send an email using smtplib."""
    s = smtplib.SMTP('smtp.mailgun.org', 587)
    s.login('otp@golabtest.net', password)  # make sure password is defined or passed
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

def create_template(recipient_name, otp_code):
    return """
<html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            .header {
                background-color: #f4f4f4;
                padding: 10px 0;
                text-align: center;
                font-size: 24px;
            }
            .content {
                margin: 20px 0;
            }
            .otp {
                display: inline-block;
                border: 1px solid #ccc;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 2px;
                background-color: #f9f9f9;
            }
            .footer {
                font-size: 12px;
                color: #888;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">OTP Verification</div>
        <div class="content">
            <p>Hello """+f"{recipient_name}"+""",</p>
            <p>Your OTP code for verification is:</p>
            <div class="otp">"""+f"{otp_code}"+"""</div>
            <p>Please enter this code to continue with the verification process. This code is valid for 10 minutes.</p>
        </div>
        <div class="footer">
            If you didn't request this code, please ignore this email.
        </div>
    </body>
</html>
"""

def test():
    import asyncio
    asyncio.run(send_mail("abdulmajidred@gmail.com","Abdul Majid",123456))

if __name__ == '__main__':
    test()