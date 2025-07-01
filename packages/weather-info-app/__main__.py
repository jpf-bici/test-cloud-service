# api-monitor/__main__.py

import os
import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import datetime
import pytz
#from timezonefinder import TimezoneFinder

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
        # --- 2. Fetch data from the API ---
        weather = getWeather()
        print(f"Weather data fetched: {weather}")

        # --- 3. Send Notification Email ---    
        sendEmail(weather)

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
    
# =========================================================================
# getWeather function   
# =========================================================================
def getWeather():

    # --- 1. Get configuration from environment variables ---
    # These variables are set in your project.yml
    target_api_url = os.getenv("TARGET_API_URL")
    api_key = os.getenv("TARGET_API_KEY")


    # hard coded values for api
    # ========================================================
    lat = 37.433 # Latitude for Menlo Park, CA
    lon = -122.207 # Longitude for Menlo Park, CA
    place = "Menlo Park, CA"
    # ========================================================

    print(f'lat: {lat}, lon: {lon}, place: {place}')
    print(f"type(lat): {type(lat)}, type(lon): {type(lon)}")

    # find timezone for the given lat, long
    loc_timezone = find_timezone(lat, lon)
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"  # or "imperial" for Fahrenheit
    }
    target_api_url = f"{target_api_url}?{requests.compat.urlencode(params)}"
    print(f"Target API URL: {target_api_url}")
    
    # Ensure the API key is set
    if not api_key:
        print("Error: TARGET_API_KEY environment variable is not set.")
        return {"statusCode": 500, "body": "Configuration error."}
    # Ensure the target API URL is set
    if not target_api_url:
        print("Error: TARGET_API_URL environment variable is not set.")
        return {"statusCode": 500, "body": "Configuration error."}
    # Ensure the target API URL is valid
    if not target_api_url.startswith("http"):
        print("Error: TARGET_API_URL is not a valid URL.")
        return {"statusCode": 500, "body": "Configuration error."}
    # Ensure the API key is valid
    if not api_key or len(api_key) < 32:  # Assuming a valid API key is at least 32 characters
        print("Error: TARGET_API_KEY is not valid.")
        return {"statusCode": 500, "body": "Configuration error."}  

    print("Configuration is valid. Proceeding with API request...")

    # --- 2. Fetch data from the API ---
    try:
        response = requests.get(target_api_url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        api_data = response.json()
        print(f"Successfully fetched data from API:")

    # --- 3. Process the data (Example: Extract a specific field) ---

        # Extract the 'current' data
        current_weather = api_data["current"]

        # Now you can access specific pieces of information from current_weather
        current_time = current_weather["dt"]
        temperature = current_weather["temp"]
        feels_like = current_weather["feels_like"]
        humidity = current_weather["humidity"]
        wind_speed = current_weather["wind_speed"]
        wind_direction = current_weather["wind_deg"]

        # Convert the timestamp to a human-readable format
        current_time = convert_utc_seconds_to_us_timezone(current_time, loc_timezone)

        # The 'weather' key is a list of dictionaries, so access the first item's description
        weather_description = current_weather["weather"][0]["description"]
        main_weather = current_weather["weather"][0]["main"]

        res = f"""
        Current Weather in {place} ({lat}, {lon})        
        Current Time: {current_time}, {loc_timezone}
        Temperature: {temperature}°C, {round((9/5)*temperature + 32, 2)}°F
        Feels Like: {feels_like}°C, {round((9/5)*feels_like + 32, 2)}°F
        Humidity: {humidity}%
        Wind Speed: {wind_speed} m/s, {round(wind_speed * 2.23694, 2)} mph
        Wind Direction: {wind_direction} deg
        Weather Condition: {main_weather} ({weather_description})"""

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        notification_subject = f"API Monitor Error: Failed to fetch {target_api_url}"
        notification_content = f"Failed to retrieve data from {target_api_url}.\nError: {e}"
    except Exception as e:
        print(f"Error processing API data: {e}")
        notification_subject = f"API Monitor Error: Data processing failed"
        notification_content = f"An unexpected error occurred during data processing.\nError: {e}"

    return res


# =========================================================================
# sendEmail function
# =========================================================================
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

# =========================================================================
# Convert time function
# =========================================================================

def convert_utc_seconds_to_us_timezone(seconds_since_epoch, timezone_name):
    """Converts seconds since epoch (UTC) to a specific US timezone.

    Args:
        seconds_since_epoch: The time in seconds since the Unix epoch (UTC).
        timezone_name: A string representing the desired US timezone (e.g., 'US/Eastern', 'US/Pacific').

    Returns:
        A datetime object in the specified US timezone, or None if an error occurs.
    """
    try:
        # Convert seconds to datetime object in UTC
        utc_datetime = datetime.datetime.fromtimestamp(seconds_since_epoch, tz=pytz.utc)

        # Get the timezone object
        target_timezone = pytz.timezone(timezone_name)

        # Localize the datetime object to the target timezone
        localized_datetime = utc_datetime.astimezone(target_timezone)

        return localized_datetime
        
    except (ValueError, pytz.exceptions.UnknownTimeZoneError) as e:
        print(f"Error during conversion: {e}")
        return None


    # # Example Usage:
    # seconds = 1750200058  # Example: March 15, 2023 00:00:00 UTC
    # timezone = 'US/Central'

    # us_time = convert_utc_seconds_to_us_timezone(seconds, timezone)

    # if us_time:
    #     print(f"Time in {timezone}: {us_time}")
    #     # Output: Time in US/Eastern: 2023-03-14 19:00:00-04:56

# =========================================================================
# find timezone function
# ==========================================================================

def find_timezone(latitude, longitude):
    """
    Find the time zone name for given latitude and longitude.
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :return: Time zone name as a string
    """

    # Initialize TimezoneFinder
    # tf = TimezoneFinder()
    # timezone_name = tf.timezone_at(lng=longitude, lat=latitude)
    return "unknown timezone"  # Placeholder for actual implementation


""" if __name__ == "__main__":
    # Example usage
    latitude = 37.433
    longitude = -122.207
    timezone_name = find_timezone(latitude, longitude)
    print(f"The time zone for ({latitude}, {longitude}) is: {timezone_name}") """

# This part is for local testing if you want to run it without DigitalOcean
# It's not executed when deployed as a DigitalOcean Function
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Call the main function with empty args for local testing
    main({})
