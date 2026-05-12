import geocoder


def get_location():
    """Fetch current location using IP-based geolocation."""
    g = geocoder.ip('me')

    # geocoder.ip('me') relies on a third-party service and may fail.
    if not g.ok or not g.latlng:
        raise ValueError('Unable to determine location from IP address.')

    return {
        'city': g.city or 'Unknown',
        'state': g.state or 'Unknown',
        'country': g.country or 'Unknown',
        'latitude': g.latlng[0],
        'longitude': g.latlng[1],
    }


def main():
    print('Location Detector')
    print('-----------------')
    print('Detecting your current location using IP-based geolocation...')

    try:
        location = get_location()
        print('\nCurrent Location:')
        print(f"City: {location['city']}")
        print(f"State: {location['state']}")
        print(f"Country: {location['country']}")
        print(f"Latitude: {location['latitude']}")
        print(f"Longitude: {location['longitude']}")
    except ImportError:
        print('Error: The geocoder library is not installed.')
        print('Install it using: pip install geocoder')
    except Exception as error:
        print(f'Error: {error}')
        print('Please check your internet connection and try again.')


if __name__ == '__main__':
    main()
