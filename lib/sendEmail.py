## 

# to test send mail functionality

import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# No 'import dotenv' or 'dotenv.load_dotenv()' needed here
# DigitalOcean Functions injects environment variables directly from project.yml
# ====
# from dotenv import load_dotenv
# load_dotenv()
# ====

import os

def sendEmail(notification_content="This is a test email content."):
    """
    Main function for the DigitalOcean Function.
    This function will be triggered by the schedule.
    """
    print("Function started: Fetching data and sending notification...")

    # --- 1. Get configuration from environment variables ---
    # These variables are set in your project.yml
    # target_api_url = os.getenv("TARGET_API_URL")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587)) # Default to 587 if not set
    notification_subject = "Test Email Subject"

    # Basic validation for essential variables; removed api url
    if not all([sender_email, sender_password, receiver_email, smtp_server]):
        print("Error: Missing one or more required environment variables.")
        return {"statusCode": 500, "body": "Configuration error."}

    # --- 2. Fetch data from the API ---
    # removed, not needed for email test

    # --- 4. Send Notification Email ---

    # notification_subject = "Test Email Subject"
    # notification_content = "This is a test email content."

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = notification_subject
        msg.attach(MIMEText(notification_content, 'plain'))

        print(f"Attempting to send email from {sender_email} to {receiver_email} via {smtp_server}:{smtp_port}")

        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Secure the connection
            server.login(sender_email, sender_password) # Login to your email account
            server.send_message(msg) # Send the email
        print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP Authentication failed. Check your email, password, and app password settings.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during email sending: {e}")

    return {"statusCode": 200, "body": "Function execution complete."}

# This part is for local testing if you want to run it without DigitalOcean
# It's not executed when deployed as a DigitalOcean Function
if __name__ == "__main__":

    from dotenv import load_dotenv
    load_dotenv()

    # Set dummy environment variables for local testing
    #os.environ["TARGET_API_URL"] = "https://jsonplaceholder.typicode.com/posts/1"
#     os.environ["SENDER_EMAIL"] = "your_test_sender_email@example.com"
#     os.environ["SENDER_EMAIL_PASSWORD"] = "your_test_password"
#     os.environ["RECEIVER_EMAIL"] = "your_test_receiver_email@example.com"
#     os.environ["SMTP_SERVER"] = "smtp.your_provider.com" # E.g., smtp.gmail.com
#     os.environ["SMTP_PORT"] = "587" 

    notification_subject = "Test Email Subject"
    notification_content = "This is a test email content."

    
    sendEmail(notification_content=notification_content)
