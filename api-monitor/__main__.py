# api-monitor/__main__.py

import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main(args):
    """
    Main function for the DigitalOcean Function.
    This function will be triggered by the schedule.
    """
    print("Function started: Fetching data and sending notification...")

    # --- 1. Get configuration from environment variables ---
    # These variables are set in your project.yml
    target_api_url = os.getenv("TARGET_API_URL")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587)) # Default to 587 if not set

    # Basic validation for essential variables
    if not all([target_api_url, sender_email, sender_password, receiver_email, smtp_server]):
        print("Error: Missing one or more required environment variables.")
        return {"statusCode": 500, "body": "Configuration error."}

    # --- 2. Fetch data from the API ---
    try:
        response = requests.get(target_api_url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        api_data = response.json()
        print(f"Successfully fetched data from API: {api_data}")

        # --- 3. Process the data (Example: Extract a specific field) ---
        # Replace this with your actual data processing logic
        # For JSONPlaceholder, it returns a post object, let's get the title
        notification_content = f"API Update for '{target_api_url}':\n\n"
        if isinstance(api_data, dict) and 'title' in api_data:
            notification_content += f"Title: {api_data['title']}\n"
            notification_content += f"Body Snippet: {api_data.get('body', '')[:100]}...\n"
        else:
            notification_content += f"Raw Data: {api_data}\n"

        notification_subject = f"API Monitor Alert: Data from {target_api_url}"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        notification_subject = f"API Monitor Error: Failed to fetch {target_api_url}"
        notification_content = f"Failed to retrieve data from {target_api_url}.\nError: {e}"
    except Exception as e:
        print(f"Error processing API data: {e}")
        notification_subject = f"API Monitor Error: Data processing failed"
        notification_content = f"An unexpected error occurred during data processing.\nError: {e}"


    # --- 4. Send Notification Email ---
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
        print("Note: For Gmail, you might need to enable 'Less secure app access' or use an 'App password'.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during email sending: {e}")

    return {"statusCode": 200, "body": "Function execution complete."}

# This part is for local testing if you want to run it without DigitalOcean
# It's not executed when deployed as a DigitalOcean Function
if __name__ == "__main__":
    # Set dummy environment variables for local testing
    os.environ["TARGET_API_URL"] = "https://jsonplaceholder.typicode.com/posts/1"
    os.environ["SENDER_EMAIL"] = "your_test_sender_email@example.com"
    os.environ["SENDER_EMAIL_PASSWORD"] = "your_test_password"
    os.environ["RECEIVER_EMAIL"] = "your_test_receiver_email@example.com"
    os.environ["SMTP_SERVER"] = "smtp.your_provider.com" # E.g., smtp.gmail.com
    os.environ["SMTP_PORT"] = "587"

    # Call the main function
    main({})
