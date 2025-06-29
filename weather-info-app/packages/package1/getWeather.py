# api-monitor/test-api.py
import timezone 
import timeZoneFinder

import requests

# No 'import dotenv' or 'dotenv.load_dotenv()' needed here
# DigitalOcean Functions injects environment variables directly from project.yml
# ====
# from dotenv import load_dotenv
# load_dotenv()
# ====

import os

api_key = os.getenv("TARGET_API_KEY")

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
    loc_timezone = timeZoneFinder.find_timezone(lat, lon)

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
        current_time = timezone.convert_utc_seconds_to_us_timezone(current_time, loc_timezone)

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


if __name__=="__main__":
    
    from dotenv import load_dotenv
    load_dotenv()
    
    lat=37.433
    lon=-122.207
    place = "Menlo Park, CA"
    weather = getWeather(lat, lon, place)
    print(weather)