import json


# Функция по определению типа погоды
def check_bad_weather():
    try:
        with open('weather_key_parameters.json', 'r') as file:
            data = json.load(file)
        day_forecast = data['day_forecast']
        night_forecast = data['night_forecast']
        day_ans = ''
        night_ans = ''

        # Обработка экстремальных значений
        if data['max_temp'] > 50:
            return 'ALERT!!!\nБудет жарковато\n'
        if data['min_temp'] < -30:
            return 'ALERT!!!\nОденьтесь потеплее, будет очень холодно\n'

        # Обработка обычных значений днем
        if day_forecast['humidity'] > 50:
            day_ans += 'За бортом повышенная влажность\n'

        if day_forecast['rain_probability'] > 90 or day_forecast['humidity'] > 80 and day_forecast['rain_probability'] > 80:
            day_ans += 'Есть шансы намокнуть, возьмите зонтик\n'

        if day_forecast['wind_speed'] > 36:
            day_ans += 'На улице очень ветрено\n'

        if day_ans == '' and 10 < data['avg_temp'] < 35:
            day_ans += 'Погодка отличная\n'
        else:
            day_ans += 'Погодка не из лучших\n'

        # Обработка обычных значений ночью
        if night_forecast['humidity'] > 50:
            night_ans += 'За бортом повышенная влажность\n'

        if night_forecast['rain_probability'] > 90 or night_forecast['humidity'] > 80 and night_forecast['rain_probability'] > 80:
            night_ans += 'Есть шансы намокнуть, возьмите зонтик\n'

        if night_forecast['wind_speed'] > 36:
            night_ans += 'На улице очень ветрено\n'

        if night_ans == '' and 10 < data['avg_temp'] < 35:
            night_ans += 'Погодка отличная\n'
        else:
            night_ans += 'Погодка не из лучших\n'


        return [day_ans, night_ans]

    except FileNotFoundError:
        print('Файл weather_key_parameters не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')