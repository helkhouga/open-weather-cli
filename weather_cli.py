
"""
Simple command-line weather app using the OpenWeather API.

Features:
- Search current weather for any city.
- Add up to 3 favourite cities (stored in memory).
- List favourite cities and show their current weather.
- Update favourites by removing one and adding a new city.

Usage:
    export OPENWEATHER_API_KEY="your_api_key_here"
    python weather_cli.py
"""

import os
import sys
import requests
from typing import Optional, Dict, List

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY_ENV_VAR = "OPENWEATHER_API_KEY"


class WeatherError(Exception):
    """Custom exception for weather-related errors."""
    pass


def get_api_key() -> str:
    """Fetch the OpenWeather API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise WeatherError(
            f"API key not found. Please set the {API_KEY_ENV_VAR} environment variable."
        )
    return api_key


def get_weather(city: str) -> Dict:
    """
    Fetch current weather for the given city from OpenWeather.

    Returns a simplified dict:
    {
        "city": str,
        "country": str,
        "temp": float,
        "feels_like": float,
        "description": str,
        "humidity": int,
        "wind_speed": float
    }
    """
    api_key = get_api_key()

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  # Celsius
    }

    try:
        resp = requests.get(API_BASE_URL, params=params, timeout=5)
    except requests.RequestException as e:
        raise WeatherError(f"Network error while contacting OpenWeather: {e}") from e

    if resp.status_code == 404:
        raise WeatherError(f"City '{city}' not found.")
    if resp.status_code != 200:
        raise WeatherError(
            f"OpenWeather API returned status {resp.status_code}: {resp.text}"
        )

    data = resp.json()

    try:
        main = data["main"]
        weather_list = data.get("weather", [])
        weather_desc = weather_list[0]["description"] if weather_list else "N/A"
        wind = data.get("wind", {})
        sys_info = data.get("sys", {})

        simplified = {
            "city": data.get("name", city),
            "country": sys_info.get("country", ""),
            "temp": main["temp"],
            "feels_like": main["feels_like"],
            "description": weather_desc,
            "humidity": main["humidity"],
            "wind_speed": wind.get("speed", 0.0),
        }
    except (KeyError, TypeError) as e:
        raise WeatherError(f"Unexpected API response format: {e}")

    return simplified


def print_weather(info: Dict) -> None:
    """Pretty-print weather information from get_weather()."""
    location = info["city"]
    if info["country"]:
        location += f", {info['country']}"

    print(f"\nWeather for {location}:")
    print("-" * (len(location) + 12))
    print(f"  Description : {info['description'].title()}")
    print(f"  Temperature : {info['temp']} °C")
    print(f"  Feels like  : {info['feels_like']} °C")
    print(f"  Humidity    : {info['humidity']}%")
    print(f"  Wind speed  : {info['wind_speed']} m/s")
    print()


def prompt_city_name() -> Optional[str]:
    """Prompt user for a city name; return None if they enter nothing."""
    city = input("Enter city name (or press Enter to cancel): ").strip()
    return city or None


def search_city_flow() -> None:
    """Handle the 'search for weather details of a city' flow."""
    city = prompt_city_name()
    if not city:
        print("Search cancelled.\n")
        return

    try:
        info = get_weather(city)
    except WeatherError as e:
        print(f"Error: {e}\n")
        return

    print_weather(info)


def add_favourite_flow(favourites: List[str]) -> None:
    """Allow user to add a city to favourites (max 3)."""
    if len(favourites) >= 3:
        print("You already have 3 favourite cities. "
              "Use 'Update Favourite Cities' to change them.\n")
        return

    city = prompt_city_name()
    if not city:
        print("Add favourite cancelled.\n")
        return

    if city in favourites:
        print(f"'{city}' is already in your favourites.\n")
        return

    # Validate by calling the API
    try:
        info = get_weather(city)
    except WeatherError as e:
        print(f"Error: {e}\n")
        return

    favourites.append(info["city"])  # use canonical city name
    print(f"Added '{info['city']}' to favourites.\n")


def list_favourites_flow(favourites: List[str]) -> None:
    """Display the list of favourite cities with their weather."""
    if not favourites:
        print("You have no favourite cities yet.\n")
        return

    print("\nFavourite cities and their current weather:")
    print("-------------------------------------------")
    for idx, city in enumerate(favourites, start=1):
        print(f"\n[{idx}] {city}")
        try:
            info = get_weather(city)
            print_weather(info)
        except WeatherError as e:
            print(f"  Error fetching weather for '{city}': {e}\n")


def update_favourites_flow(favourites: List[str]) -> None:
    """Remove one favourite city and add a new one (still max 3)."""
    if not favourites:
        print("You have no favourite cities to update. "
              "Use 'Add a City to Favourites' first.\n")
        return

    print("\nCurrent favourites:")
    for idx, city in enumerate(favourites, start=1):
        print(f"  {idx}. {city}")

    try:
        choice_str = input("Enter the number of the city to remove: ").strip()
        choice = int(choice_str)
    except ValueError:
        print("Invalid input. Please enter a number.\n")
        return

    if not (1 <= choice <= len(favourites)):
        print("Choice out of range.\n")
        return

    removed_city = favourites.pop(choice - 1)
    print(f"Removed '{removed_city}' from favourites.\n")

    # Now ask for a replacement city
    city = prompt_city_name()
    if not city:
        print("Update cancelled. No new city added.\n")
        return

    if city in favourites:
        print(f"'{city}' is already in your favourites.\n")
        return

    try:
        info = get_weather(city)
    except WeatherError as e:
        print(f"Error: {e}\n")
        return

    favourites.append(info["city"])
    print(f"Added '{info['city']}' to favourites.\n")


def print_menu() -> None:
    """Display main menu."""
    print("Weather CLI")
    print("-----------")
    print("1. Search weather for a city")
    print("2. Add a city to favourites")
    print("3. List favourite cities and their weather")
    print("4. Update favourite cities (remove & add)")
    print("5. Exit")


def main() -> None:
    """Main application loop."""
    favourites: List[str] = []

    print("Welcome to the OpenWeather CLI app!")
    print("Make sure your API key is set in the "
          f"{API_KEY_ENV_VAR} environment variable.\n")

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()
        print()

        if choice == "1":
            search_city_flow()
        elif choice == "2":
            add_favourite_flow(favourites)
        elif choice == "3":
            list_favourites_flow(favourites)
        elif choice == "4":
            update_favourites_flow(favourites)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except WeatherError as e:
        # Handle any API key error at startup cleanly
        print(f"Fatal error: {e}")
        sys.exit(1)
