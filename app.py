from flask import Flask, render_template, request
from weather_receiver import WeatherReceiver, weather_key_parameters
from convert_from_address_to_coordinates import GetCoords


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    start_city = request.form['start']
    end_city = request.form['end']

    weather_data = {
        'start_city': start_city,
        'end_city': end_city,
        'message': 'Маршрут получен! Информация по погоду будет добавлена.'
    }

    return render_template('result.html', data=weather_data)



api_location_to_coords = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
api_for_weather = '7qfDoG64pnAQyzGmuOQxyP6DcCscJdzd'
if __name__ == '__main__':
    app.run(debug=True)