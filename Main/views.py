from django.shortcuts import render
import requests
import datetime
from .models import City
from .forms import CityForm
# Create your views here.


def index(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=052c711f61c4d7b6a5b0ba22b2c0492f'
    url1 = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=052c711f61c4d7b6a5b0ba22b2c0492f'
    msg = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            exciting_city = City.objects.filter(name=new_city).count()

            if exciting_city == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    msg = 'City does not exist!!'
            else:
                msg = 'City already exists!!'
    else:
        form = CityForm()

    print(msg)
    cites = City.objects.all()
    weather_data = []

    for city in cites:
        r = requests.get(url.format(city)).json()
        # print(r.text)

        city_weather = {
            'city': city.name,
            # 'temprature': r['main']['temp'],
            'temprature':str(r['coord']['lon'])+'°c',
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        # print(city_weather)
        time = datetime.datetime.now()
        weather_data.append(city_weather)

    print(weather_data)
    # print("This is time:", time)
    conetxt = {'weather_data': weather_data,
               'form': form,
               'time': time,
               'city_weather': city_weather

            }
    return render(request, 'main/index.html', conetxt)
