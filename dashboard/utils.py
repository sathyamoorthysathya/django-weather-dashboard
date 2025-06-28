import requests

API_KEY = 'ed6941ec10f1f66fe499bd76a3866729'

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    print("Requesting:", url)
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print("API Error:", response.status_code, response.text)
        return None
