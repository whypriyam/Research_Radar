import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_email(docx_path, recipients):
    sender = os.environ['GMAIL_FROM']
    password = os.environ['GMAIL_APP_PASSWORD']

    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = '📡 ResearchRadar Weekly AI Digest'

    body = (
        "Hi,\n\n"
        "Your ResearchRadar digest is ready.\n"
        "Please find the attached document.\n\n"
        "— ResearchRadar Bot 📡"
    )

    msg.attach(MIMEText(body, 'plain'))

    # Attach DOCX file
    with open(docx_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())

    encoders.encode_base64(part)
    filename = os.path.basename(docx_path)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

    # Send email
    print("Sending email...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print("Email failed:", e)
if __name__ == "__main__":
    test_file = "test.docx"

    # create dummy docx
    from docx import Document
    d = Document()
    d.add_paragraph("Test email from ResearchRadar")
    d.save(test_file)

    send_email(test_file, ["samarth.00071@gmail.com"])       
