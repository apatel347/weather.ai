import requests
from urllib.parse import quote
import openai

# Replace with your actual API keys
WEATHER_API_KEY = "enter here "
OPENAI_API_KEY = "enter here "
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

openai.api_key = OPENAI_API_KEY

def get_weather(city):
    try:
        city_encoded = quote(city)  # URL encode the city name
        request_url = f"{BASE_WEATHER_URL}?q={city_encoded}&appid={WEATHER_API_KEY}"
        response = requests.get(request_url)

        print("Request URL:", request_url)
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = round(data["main"]["temp"] - 273.15, 2)
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]

            print(f"Weather: {weather}")
            print(f"Temperature: {temperature} Celsius")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Pressure: {pressure} hPa")

            return {
                "city": city,
                "weather": weather,
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "pressure": pressure
            }
        elif response.status_code == 404:
            print("Error: City not found. Please check the city name.")
        else:
            error_message = response.json().get("message", "An error occurred.")
            print("Error:", error_message)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    return None

def generate_weather_summary(weather_data):
    try:
        prompt = (f"Generate a summary for the following weather data:\n"
                  f"City: {weather_data['city']}\n"
                  f"Weather: {weather_data['weather']}\n"
                  f"Temperature: {weather_data['temperature']} Celsius\n"
                  f"Humidity: {weather_data['humidity']}%\n"
                  f"Wind Speed: {weather_data['wind_speed']} m/s\n"
                  f"Pressure: {weather_data['pressure']} hPa\n")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        summary = response.choices[0].message['content'].strip()
        return summary
    except Exception as e:
        print(f"Error generating weather summary: {e}")
        return None

if __name__ == "__main__":
    while True:
        city = input("Enter a city name (or type 'exit' to stop): ")
        if city.lower() == 'exit':
            print("Exiting the program.")
            break
        
        weather_data = get_weather(city)
        if weather_data:
            summary = generate_weather_summary(weather_data)
            if summary:
                print("\nWeather Summary:")
                print(summary)
