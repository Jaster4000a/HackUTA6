import requests
import configparser

API_KEY = config["WEATHER_API"]


# get weather data for specific coordinates
def get_weather_data(lat, lon):
    latitude = 32.7357
    longitude = -97.1081

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'imperial'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        print(f"Location: ({lat}, {lon})")
        print(f"Temperature: {data['main']['temp']} °F")
        print(f"Weather: {data['weather'][0]['description']}")
        print(f"Humidity: {data['main']['humidity']}%")
    else:
        print("Error:", data.get("message", "Unable to fetch data"))

# Call the function with specific coordinates
#print("\nHouston")
#get_weather_data(29.763, -95.363) # Houston
print("\nEuless")
get_weather_data(32.8371, 97.0820)

print("\nArlington")
get_weather_data(32.736, -97.108) # Arlington


#print("\nAustin")
#get_weather_data(30.267, -97.743) # Austin
print("\nGrand Prairie")
get_weather_data(32.7460, 96.9978)

#print("\nCorpus Christi")
#get_weather_data(27.801, -97.396) # Corpus Christi
print("\nPantego")
get_weather_data(32.7143, 97.1564)

print("\nFort Worth")
get_weather_data(32.7555, 97.3308)
#print("\nLubbock")
#get_weather_data(33.578, -101.855) # Lubbock

