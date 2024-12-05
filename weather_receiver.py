import requests
import json


class WeatherReceiver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
        self.forecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'

    # Достаем locationKey, чтобы дальше получить данные о погоде
    def get_location_key(self, lat, lon):
        params = {
            'format': json,
            'apikey': self.api_key,
            'q': f'{lat},{lon}'
        }
        response = requests.get(self.location_url, params=params)
        if response.status_code == 200:
            return response.json()['Key']
        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    # Получаем все данные о погоде в текущий момент
    def get_weather(self, lat, lon):
        params = {
            'apikey': self.api_key,
            'metric': True,
            'details': True
        }
        location_key = self.get_location_key(lat, lon)
        response = requests.get(self.forecast_url + f'{location_key}', params=params)
        if response.status_code == 200:
            data = response.json()
            with open('weather_forecast.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

# Оставляем лишь ключевые параметры
def weather_key_parameters():
    try:
        with open('weather_forecast.json', 'r') as file:
            data = json.load(file)
        daily_forecast = data['DailyForecasts'][0]

        # так как мы не знаем, когда поедут люди в путешествие, целесообразно брать прогноз погоды как на день, так и на ночь
        key_parameters = {
            'max_temp': daily_forecast['Temperature']['Maximum']['Value'],
            'min_temp': daily_forecast['Temperature']['Minimum']['Value'],
            'avg_temp': (daily_forecast['Temperature']['Maximum']['Value'] +
                         daily_forecast['Temperature']['Minimum']['Value']) / 2,
            'day_forecast': {
                'humidity': daily_forecast['Day']['RelativeHumidity']['Average'],
                'wind_speed': daily_forecast['Day']['Wind']['Speed']['Value'],
                'rain_probability': daily_forecast['Day']['RainProbability'],
            },
            'night_forecast': {
                'humidity': daily_forecast['Night']['RelativeHumidity']['Average'],
                'wind_speed': daily_forecast['Night']['Wind']['Speed']['Value'],
                'rain_probability': daily_forecast['Night']['RainProbability']
            }
        }

        with open('weather_key_parameters.json', 'w', encoding='utf-8') as file:
            json.dump(key_parameters, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('Файл "weather_forecast" не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

api_key = '7qfDoG64pnAQyzGmuOQxyP6DcCscJdzd'
location = WeatherReceiver(api_key)
lat, lon = 55.768740, 37.588835
location.get_weather(lat, lon)
weather_key_parameters()
