from flask import Flask, render_template, request, jsonify
from weather_receiver import WeatherReceiver, weather_key_parameters
from convert_from_address_to_coordinates import GetCoords
from check_bad_weather import check_bad_weather

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    start_city = request.form['start']
    end_city = request.form['end']
    # Стартовый город
    try:
        start_lon, start_lat = GetCoords(api_location_to_coords).get_coords_by_address(start_city)
        WeatherReceiver(api_for_weather).get_weather(start_lat, start_lon)
        data = weather_key_parameters()
        # Дневные параметры
        start_day_temp = data['max_temp']
        start_day_rain = data['day_forecast']['rain_probability']
        start_day_humidity = data['day_forecast']['humidity']
        start_day_wind = data['day_forecast']['wind_speed']
        start_day_message = check_bad_weather()[0].split('\n')
        # Ночные параметры
        start_night_temp = data['min_temp']
        start_night_rain = data['night_forecast']['rain_probability']
        start_night_humidity = data['night_forecast']['humidity']
        start_night_wind = data['night_forecast']['wind_speed']
        start_night_message = check_bad_weather()[1].split('\n')

        # Конечный город
        end_lon, end_lat = GetCoords(api_location_to_coords).get_coords_by_address(end_city)
        WeatherReceiver(api_for_weather).get_weather(end_lat, end_lon)
        data = weather_key_parameters()
        # Дневные параметры
        end_day_temp = data['max_temp']
        end_day_rain = data['day_forecast']['rain_probability']
        end_day_humidity = data['day_forecast']['humidity']
        end_day_wind = data['day_forecast']['wind_speed']
        end_day_message = check_bad_weather()[0].split('\n')
        # Ночные параметры
        end_night_temp = data['min_temp']
        end_night_rain = data['night_forecast']['rain_probability']
        end_night_humidity = data['night_forecast']['humidity']
        end_night_wind = data['night_forecast']['wind_speed']
        end_night_message = check_bad_weather()[1].split('\n')

        weather_data = {
            'start_city': start_city.capitalize(),
            'end_city': end_city.capitalize(),
            'start_day_temp': start_day_temp,
            'start_day_rain': start_day_rain,
            'start_day_humidity': start_day_humidity,
            'start_day_wind': start_day_wind,
            'start_night_temp': start_night_temp,
            'start_night_rain': start_night_rain,
            'start_night_humidity': start_night_humidity,
            'start_night_wind': start_night_wind,
            'start_day_message': start_day_message,
            'start_night_message': start_night_message,

            'end_day_temp': end_day_temp,
            'end_day_rain': end_day_rain,
            'end_day_humidity': end_day_humidity,
            'end_day_wind': end_day_wind,
            'end_night_temp': end_night_temp,
            'end_night_rain': end_night_rain,
            'end_night_humidity': end_night_humidity,
            'end_night_wind': end_night_wind,
            'end_day_message': end_day_message,
            'end_night_message': end_night_message
        }
        return render_template('result.html', data=weather_data)

    except Exception as e:
        return render_template('error.html', message="Такого города не существует")


api_location_to_coords = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
api_for_weather = 'dM0pZhdzjLlvNdVXIjacwVtOaU0tw7zG'
if __name__ == '__main__':
    app.run(debug=True)