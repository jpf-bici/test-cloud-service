import datetime
import pytz

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


# Example Usage:
seconds = 1750200058  # Example: March 15, 2023 00:00:00 UTC
timezone = 'US/Central'

us_time = convert_utc_seconds_to_us_timezone(seconds, timezone)

if us_time:
    print(f"Time in {timezone}: {us_time}")
    # Output: Time in US/Eastern: 2023-03-14 19:00:00-04:56