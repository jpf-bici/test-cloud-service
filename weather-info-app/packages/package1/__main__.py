# api-monitor/__main__.py

import os

# No 'import dotenv' or 'dotenv.load_dotenv()' needed here
# DigitalOcean Functions injects environment variables directly from project.yml
# ====
# from dotenv import load_dotenv
# load_dotenv()
# ====

import getWeather 
import sendEmail


def main(lat, lon):
    """
    Main function for the DigitalOcean Function.
    This function will be triggered by the schedule.
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
    if not all([target_api_url, sender_email, sender_password, receiver_email, smtp_server]):
        print("Error: Missing one or more required environment variables.")
        return {"statusCode": 500, "body": "Configuration error."}

    # --- 2. Fetch data from the API ---
    weather = getWeather.getWeather(lat, lon) # Example coordinates for testing
    print(f"Weather data fetched: {weather}")

    # --- 3. Send Notification Email ---    
    sendEmail.sendEmail(weather)

# This part is for local testing if you want to run it without DigitalOcean
# It's not executed when deployed as a DigitalOcean Function
if __name__ == "__main__":

    from dotenv import load_dotenv
    load_dotenv()

    # # Set dummy environment variables for local testing
    # os.environ["TARGET_API_URL"] = "https://jsonplaceholder.typicode.com/posts/1"
    # os.environ["SENDER_EMAIL"] = "your_test_sender_email@example.com"
    # os.environ["SENDER_EMAIL_PASSWORD"] = "your_test_password"
    # os.environ["RECEIVER_EMAIL"] = "your_test_receiver_email@example.com"
    # os.environ["SMTP_SERVER"] = "smtp.your_provider.com" # E.g., smtp.gmail.com
    # os.environ["SMTP_PORT"] = "587"

    # Call the main function
    # Menlo Park latitude and Longitude at our house
    lat = 37.433
    lon = -122.207
    main(lat=lat, lon=lon)
