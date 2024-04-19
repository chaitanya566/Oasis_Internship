import requests

class WeatherAPI_Details:
    def __init__(self, api_key):
        self.api_key=api_key
        pass

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data['units'] = {
                'temperature': 'Celsius',
                'wind_speed': 'Kmph'
                }
            return data
        elif response.status_code == 404:
            raise ValueError("City not found.")
        else:
            raise ValueError("Failed to fetch weather data.")

    def convert_weather_data(self,weather_data, temp_units_settings, wind_speed_settings):

        temp_unit = temp_units_settings.currentText()
        wind_speed_unit = wind_speed_settings.currentText()

        # Convert temperature to Celsius if selected unit is Celsius and current unit is Fahrenheit
        if 'units' in weather_data and weather_data['units']['temperature'] == 'Fahrenheit' and temp_unit == 'Celsius':
            weather_data['main']['temp'] = (weather_data['main']['temp'] - 32) * 5/9
            weather_data['main']['temp'] = round(weather_data['main']['temp'], 2)
            weather_data['main']['feels_like'] = (weather_data['main']['feels_like'] - 32) * 5/9
            weather_data['main']['feels_like'] = round(weather_data['main']['feels_like'], 2)
            weather_data['main']['temp_min'] = (weather_data['main']['temp_min'] - 32) * 5/9
            weather_data['main']['temp_min'] = round(weather_data['main']['temp_min'], 2)
            weather_data['main']['temp_max'] = (weather_data['main']['temp_max'] - 32) * 5/9
            weather_data['main']['temp_max'] = round(weather_data['main']['temp_max'], 2)

        # Convert temperature to Fahrenheit if selected unit is Fahrenheit and current unit is Celsius
        elif 'units' in weather_data and weather_data['units']['temperature'] == 'Celsius' and temp_unit == 'Fahrenheit':
            weather_data['main']['temp'] = (weather_data['main']['temp'] * 9/5) + 32
            weather_data['main']['temp'] = round(weather_data['main']['temp'], 2)
            weather_data['main']['feels_like'] = (weather_data['main']['feels_like'] * 9/5) + 32
            weather_data['main']['feels_like'] = round(weather_data['main']['feels_like'], 2)
            weather_data['main']['temp_min'] = (weather_data['main']['temp_min'] * 9/5) + 32
            weather_data['main']['temp_min'] = round(weather_data['main']['temp_min'], 2)


        # Convert wind speed to kmph if selected unit is kmph and current unit is mph
        if 'units' in weather_data and weather_data['units']['wind_speed'] == 'mph' and wind_speed_unit == 'Kmph':
            weather_data['wind']['speed'] *= 1.60934
            # Limiting to 2 decimal places
            weather_data['wind']['speed'] = round(weather_data['wind']['speed'], 2)

        # Convert wind speed to mph if selected unit is mph and current unit is kmph
        elif 'units' in weather_data and weather_data['units']['wind_speed'] == 'Kmph' and wind_speed_unit == 'mph':
            weather_data['wind']['speed'] /= 1.60934
            # Limiting to 2 decimal places
            weather_data['wind']['speed'] = round(weather_data['wind']['speed'], 2)

        weather_data['units'] = {
            'temperature': temp_unit,
            'wind_speed': wind_speed_unit,
        }

        return weather_data
    
    def update_weather_labels(self,weather_data, min_temp_label, feels_like_label, max_temp_label, wind_speed_label, cloud_coverage_label):


        temperature_unit_sign = "°C" if weather_data['units']['temperature'] == 'Celsius' else "°F"
        wind_speed_unit_sign = "Kmph" if weather_data['units']['wind_speed'] == 'Kmph' else "mph"

        if 'main' in weather_data and 'temp_min' in weather_data['main']:
            min_temp_label.setText(f"Min Temp: {weather_data['main']['temp_min']} {temperature_unit_sign}")

        if 'main' in weather_data and 'feels_like' in weather_data['main']:
            feels_like_label.setText(f"Feels Like: {weather_data['main']['feels_like']} {temperature_unit_sign}")

        if 'main' in weather_data and 'temp_max' in weather_data['main']:
            max_temp_label.setText(f"Max Temp: {weather_data['main']['temp_max']} {temperature_unit_sign}")

        if 'wind' in weather_data and 'speed' in weather_data['wind']:
            wind_speed_label.setText(f"{weather_data['wind']['speed']} {wind_speed_unit_sign}")



        if 'clouds' in weather_data and 'all' in weather_data['clouds']:
            cloud_coverage_label.setText(f"{weather_data['clouds']['all']} %")
