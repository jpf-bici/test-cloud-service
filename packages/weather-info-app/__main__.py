# api-monitor/__main__.py

import os
import sys

# No 'import dotenv' or 'dotenv.load_dotenv()' needed here
# DigitalOcean Functions injects environment variables directly from project.yml


def main(args):
    """
    Main function for the DigitalOcean Function.
    This function will be triggered by the schedule.
    Args: args - Digital Ocean Functions passes this parameter.
    """
    print("Function started: Fetching data and sending notification...")

    # --- 1. Get configuration from environment variables ---
    # These variables are set in your project.yml
    target_api_url = os.getenv("TARGET_API_URL")
    target_api_key = os.getenv("TARGET_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587)) # Default to 587 if not set

    # Basic validation for essential variables
    if not all([target_api_url, target_api_key, sender_email, sender_password, receiver_email, smtp_server, smtp_port]):
        print("Error: Missing one or more required environment variables.")
        return {"statusCode": 500, "body": "Configuration error."}

    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lib')))
        from getWeather import getWeather 
        from sendEmail import sendEmail

        # --- 2. Fetch data from the API ---
        weather = getWeather()
        print(f"Weather data fetched: {weather}")

        # --- 3. Send Notification Email ---    
        sendEmail(weather)

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

# This part is for local testing if you want to run it without DigitalOcean
# It's not executed when deployed as a DigitalOcean Function
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Call the main function with empty args for local testing
    main({})
