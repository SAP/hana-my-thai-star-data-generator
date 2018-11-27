import random
import datetime
import math
import math_utils
import plotly
import weather
import holiday
from pprint import pprint

def get_model(dish_id, dates, temperatures, holidays):
    temperature_curve = lambda x: 1
    weekday_curve = lambda x: 1
    weekend_holidays_curve = math_utils.characteristic_function(
        lambda date: 5 <= date.weekday() <= 6 or date in holidays,
        off=.8, on=1
    )

    if dish_id == 0:
        # Spicy Fried Rice

        temperature_curve = math_utils.plateaued_gauss_bell(5, 10, 6.7, min=0.1)
    elif dish_id == 1:
        # Salad

        temperature_curve = math_utils.gauss_bell(25, 6.7, min=0.05)
    elif dish_id == 2:
        # Chicken

        weekday_curve = lambda x: .5
    elif dish_id == 3:
        # Beef

        temperature_curve = math_utils.plateaued_gauss_bell(7, 13, 9)
        weekday_curve = math_utils.gauss_bell(6, 0.7, min=0.5)
    elif dish_id == 4:
        # Fish/Prawns

        weekday_curve = math_utils.gauss_bell(4, 0.7, min=0.1)
    elif dish_id == 5:
        # Beer

        temperature_curve = math_utils.gauss_bell(25, 6.7, min=0.2)
        weekday_curve = math_utils.plateaued_gauss_bell(4, 6, 0.7, min=0.5)
    elif dish_id == 6:
        # Tea

        temperature_curve = math_utils.gauss_bell(2.5, 8.8, min=0.05)
    else:
        # Unknown

        temperature_curve = lambda x: 0
        weekday_curve = lambda x: 0

    return [
        temperature_curve(temperatures[i])
            * weekday_curve(dates[i].weekday())
            * weekend_holidays_curve(dates[i])
        for i in range(len(dates))
    ]

def generate_data(dish_ids, weights, dates, temperatures, holidays):
    result = []

    for (dish_id, weight) in zip(dish_ids, weights):
        model = get_model(dish_id, dates, temperatures, holidays)
        result += [
            {
                'dish_id': dish_id,
                'date': date,
                'weekday': date.weekday(),
                'temperature': temperature,
                'holiday': date in holidays,
                'orders': round(max(0, x + random.gauss(0, 0.05)) * weight)
            }
            for (date, temperature, x) in zip(dates, temperatures, model)
        ]

    return result

if __name__ == '__main__':
    n = 365
    base = datetime.date.today()
    dates = [base + datetime.timedelta(days=x) for x in range(n)]
    temperatures = [x['temperature'] for x in weather.get_weather_data()]
    holidays = [x['date'] for x in holiday.get_holiday_data()]
    data = generate_data(range(7), [100 for _ in range(7)], dates, temperatures, holidays)
    dish_id = 3

    plotly.offline.plot([
        *[
            plotly.graph_objs.Scatter(
                x=list(range(n)),
                y=[x['orders'] for x in data if x['dish_id'] == dish_id],
                name='Dish {}'.format(dish_id)
            )
            for dish_id in range(7)
        ],
        plotly.graph_objs.Scatter(
            x=list(range(n)),
            y=temperatures,
            name='Temperature'
        ),
        plotly.graph_objs.Scatter(
            x=list(range(n)),
            y=[date.weekday() for date in dates],
            name='Weekday'
        ),
        plotly.graph_objs.Scatter(
            x=list(range(n)),
            y=[10 if date in holidays else 0 for date in dates],
            name='Holiday'
        )
    ], auto_open=True)
