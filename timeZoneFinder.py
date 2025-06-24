# need to pip install timezonefinder

from timezonefinder import TimezoneFinder

def find_timezone(latitude, longitude):
    """
    Find the time zone name for given latitude and longitude.
    
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :return: Time zone name as a string
    """

    # Initialize TimezoneFinder
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lng=longitude, lat=latitude)
    return timezone_name



if __name__ == "__main__":
    # Example usage
    latitude = 37.433
    longitude = -122.207
    timezone_name = find_timezone(latitude, longitude)
    print(f"The time zone for ({latitude}, {longitude}) is: {timezone_name}")
