import requests
from django.shortcuts import render, redirect
from datetime import datetime

API_KEY = '9feddbdf8f4613f8189afa693233f60e'  # <-- replace with your OpenWeather API key

def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data.get("city")
    except:
        return "Chennai"

def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def get_weather_history(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    history = []
    added_dates = set()

    for entry in data.get('list', []):
        date = entry['dt_txt'].split(' ')[0]
        if date not in added_dates:
            history.append({
                'date': date,
                'temp': entry['main']['temp'],
                'humidity': entry['main']['humidity'],
                'wind': entry['wind']['speed'],
                'pressure': entry['main']['pressure'],
            })
            added_dates.add(date)
        if len(history) == 5:
            break

    return history

def dashboard(request):
    city = get_location()

    if request.method == 'POST':
        city = request.POST.get('city') or city

    current_weather = get_weather_data(city)

    if current_weather.get('cod') != 200:
        context = {'error': f"Could not find weather data for {city}"}
        return render(request, 'dashboard/dashboard.html', context)

    history = get_weather_history(city)

    context = {
        'city': city,
        'temperature': current_weather['main']['temp'],
        'humidity': current_weather['main']['humidity'],
        'wind_speed': current_weather['wind']['speed'],
        'pressure': current_weather['main']['pressure'],
        'history': history,
    }
    return render(request, 'dashboard/dashboard.html', context)