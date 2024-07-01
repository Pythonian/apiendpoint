"""
This module sets up a Flask web server that provides an API endpoint
to greet visitors and give the current temperature in their location.
"""

import os

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .flaskenv
load_dotenv('.flaskenv')

# Retrieve the WeatherAPI key from environment variables
weatherapi_key = os.getenv("WEATHERAPI_KEY")

app = Flask(__name__)

# def get_public_ip() -> str:
#     """
#     Retrieves the public IP address of the server.

#     Returns:
#         str: The public IP address.
#     """
#     response = requests.get('https://api.ipify.org?format=json')
#     data = response.json()
#     return data['ip']
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For header format: client, proxy1, proxy2, ...
        client_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        client_ip = request.remote_addr
    return client_ip

def get_location_and_temperature(ip: str) -> tuple[str, str]:
    """
    Retrieves the location and temperature for a given IP address.

    Args:
        ip (str): The IP address to look up.

    Returns:
        tuple[str, str]: A tuple containing the city and temperature.
    """
    api_key = weatherapi_key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={ip}'
    response = requests.get(url)
    data = response.json()

    if 'location' in data and 'current' in data:
        city = data['location']['name']
        temperature = data['current']['temp_c']
    else:
        print(f"Error: Unable to get location and temperature for IP {ip}. API response: {data}")
        city = "Unknown"
        temperature = "N/A"

    return city, temperature

@app.get('/api/hello')
def hello() -> str:
    """
    Handles the /api/hello endpoint, returning a greeting message
    along with the visitor's IP address, location, and current temperature.

    Returns:
        str: A JSON response containing the client's IP, location, and greeting.
    """
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = get_client_ip()
    location, temperature = get_location_and_temperature(client_ip)
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    return jsonify({
        'client_ip': client_ip,
        'location': location,
        'greeting': greeting
    })
