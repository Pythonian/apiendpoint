"""
This module sets up a Flask web server that provides an API endpoint
to greet visitors and give the current temperature in their location.
"""

import os
import logging

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .flaskenv
load_dotenv(".flaskenv")

# Retrieve the WeatherAPI key from environment variables
weatherapi_token = os.getenv("WEATHERAPI_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


def fetch_public_ip() -> str:
    """
    Retrieves the public IP address of the server.

    Returns:
        str: The public IP address.
    """
    response = requests.get("https://api.ipify.org?format=json")
    data = response.json()
    return data["ip"]


def fetch_client_ip() -> str:
    """
    Retrieves the client's IP address from the request headers.

    Returns:
        str: The client's IP address.
    """
    if request.headers.get("X-Forwarded-For"):
        client_ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
    else:
        client_ip = request.remote_addr
    # If running locally, use the public IP for demonstration purposes
    if client_ip == "127.0.0.1":
        client_ip = fetch_public_ip()
    return client_ip


def fetch_location_and_temp(ip_address: str) -> tuple[str, str]:
    """
    Retrieves the location and temperature for a given IP address.

    Args:
        ip_address (str): The IP address to look up.

    Returns:
        tuple[str, str]: A tuple containing the city and temperature.
    """
    api_token = weatherapi_token
    api_url = (
        f"http://api.weatherapi.com/v1/current.json?key={api_token}&q={ip_address}"
    )
    response = requests.get(api_url)
    data = response.json()

    # Log the entire API response for debugging
    logging.info(f"API response for IP {ip_address}: {data}")

    if "location" in data and "current" in data:
        city = data["location"]["name"]
        temperature = data["current"]["temp_c"]
    else:
        msg = (
            f"Error: Unable to get location and temperature for IP "
            f" {ip_address}. API response: {data}"
        )
        logging.error(msg)
        city = "Unknown"
        temperature = "N/A"

    return city, temperature


@app.get("/api/hello")
def hello() -> str:
    """
    Handles the /api/hello endpoint, returning a greeting message
    along with the visitor's IP address, location, and current temperature.

    Returns:
        str: A JSON response containing client's IP, location, and greeting.
    """
    visitor_name = request.args.get("visitor_name", "").strip('"')
    if not visitor_name:
        visitor_name = "Sapagrammer"
    client_ip = fetch_client_ip()
    location, temperature = fetch_location_and_temp(client_ip)
    greeting_msg = (
        f"Hello, {visitor_name}! The temperature is {temperature} degrees "
        f"Celsius in {location}"
    )
    return jsonify(
        {
            "client_ip": client_ip,
            "location": location,
            "greeting": greeting_msg,
        }
    )
