# Glasscast - Weather Forecast Application

Glasscast is a weather forecast application that provides users with accurate and up-to-date weather information. It leverages the OpenWeatherMap API to fetch weather data and offers features such as current weather conditions, 5-day forecasts, and the ability to save favorite cities.

## How to run?

Make sure you have python 3.10+ installed.

```bash
pip install -r requirements.txt
```

```bash
python3 main.py
```

It is recommended to use a virtual environment to avoid dependency conflicts.

```bash
python3 -m venv .venv && source .venv/bin/activate
```

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
OWM_API_KEY=your_openweathermap_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key_for_jwt
```

You can get an OpenWeatherMap API key by signing up at [OpenWeatherMap](https://openweathermap.org/api).
You can get Supabase credentials by signing up at [Supabase](https://supabase.com/).
Make sure to replace `your_openweathermap_api_key`, `your_supabase_url`, `your_supabase_key`, and `your_secret_key_for_jwt` with your actual credentials.

