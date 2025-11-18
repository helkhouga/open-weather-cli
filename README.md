# OpenWeather CLI – Command Line Weather App

This repository contains a small command-line application that integrates with the **OpenWeather API** to manage and view the current weather for cities. 

## Objective

Create a command-line application that interacts with the OpenWeather API to manage weather details of cities. The application allows a user to:

1. **Search weather details of a city** by name.
2. **Add a city to favourites**, with a maximum of **three** cities.
3. **List favourite cities** along with their current weather details.
4. **Update favourite cities** by removing an existing favourite and adding a new one, while keeping the limit of three cities.

All favourites are stored **in memory** for the duration of the program (no database or file storage).

---

## Tech Stack

- **Language:** Python 3.9+  
- **HTTP client:** `requests`  
- **API:** [OpenWeather Current Weather Data API](https://openweathermap.org/current)

---

## Repository Structure

```text
.
├── README.md          # Project documentation (this file)
├── weather_cli.py     # Main CLI application
├── requirements.txt   # Python dependencies
└── .gitignore         # Standard Python ignore rules
```

---

## Getting Started


### 1. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate    
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Obtain an OpenWeather API key

1. Go to the [OpenWeather website](https://openweathermap.org/).
2. Create a free account (if you do not already have one).
3. Generate an API key from your account dashboard.

### 4. Export the API key as an environment variable

On **macOS** (bash):

```bash
export OPENWEATHER_API_KEY="your_real_api_key_here"
```

---

## Running the Application

From the project root:

```bash
python weather_cli.py
```

You will see a menu like:

```text
Weather CLI
-----------
1. Search weather for a city
2. Add a city to favourites
3. List favourite cities and their weather
4. Update favourite cities (remove & add)
5. Exit
```

Enter the option number and follow the prompts.

---

## Example Usage

### 1. Search weather for a city

- Choose option `1`.
- Enter a city, e.g. `London`.
- The application fetches and displays:

```text
Weather for London, GB:
-----------------------
  Description : Light Rain
  Temperature : 12.3 °C
  Feels like  : 10.5 °C
  Humidity    : 82%
  Wind speed  : 4.1 m/s
```

### 2. Add city to favourites

- Choose option `2`.
- Enter a valid city name, e.g. `Paris`.
- The app validates the city by calling the API before adding.
- Maximum of **3** favourites is enforced.

### 3. List favourite cities

- Choose option `3`.
- For each favourite, the app fetches fresh weather data and prints it.

### 4. Update favourite cities

- Choose option `4`.
- The app lists the current favourite cities with indices.
- Select the index of the city to remove.
- Provide a new city name to add in its place.

---






---

