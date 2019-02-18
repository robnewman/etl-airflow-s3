import requests
import json
import configparser
from datetime import datetime
import os

def get_weather():
    """
    Query openweathermap.org's API
    """

    config = configparser.ConfigParser()
    config.read('configuration.ini')
    api_key = config['api']['key']
    url = config['request']['url']
    bbox = config['request']['bbox']

    parameters = {
        'bbox': bbox,
        'appid': api_key
    }
    result = requests.get(
        url,
        parameters
    )

    if result.status_code == 200:
        json_data = result.json()
        file_name = f"{str(datetime.now().date())}.json"
        tot_name = os.path.join(
            os.path.dirname(__file__),
            'data',
            file_name
        )
        with open(tot_name, 'w') as outputfile:
            json.dump(
                json_data,
                outputfile,
                indent=2
            )
    else:
        print("Error in API call")


if __name__ == "__main__":
    get_weather()
