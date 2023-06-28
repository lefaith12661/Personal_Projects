# import modules/libraries
from flask import Flask, render_template, request
import math
from dotenv import load_dotenv
import requests
import re

def create_app():
    # __name__ just refers to the name of the current file
    # Initialize the app
    app = Flask(__name__)

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Load environment variables from .env file to set the environment FLASK_APP=project.py
    load_dotenv()

    # main function that calls the other functions
    def main():
        get_temp()
        check_string()
        home()
        result()
        get_clothes_rec()

    # get weather temp using API
    def get_temp(city):
        # get weather API
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "94d44a7721287d4f2b70c7af8dc4f3b3"
        # url for API call
        url = BASE_URL + "appid=" + API_KEY + "&q=" + city
        # convert into json for versatile format
        response = requests.get(url).json()
        # get kelvin temp in the json file
        temperature = response['main']['temp']
        return temperature

    # check for str input only
    def check_string(city):
        if re.fullmatch(r"[a-zA-Z\s]*", city):
            return city
        else:
            raise ValueError

    # check for valid city in the USA
    def check_city(city):
        with open('us-cities.txt', 'r') as file:
            valid_cities = file.read().splitlines()

        if city in valid_cities:
            return city
        else:
            raise ValueError

    # show recommendation based on temperature
    def get_clothes_rec(temp):
        # temp <= 40
        if temp <= 40:
            return "Thick sweaters, a winter jacket, scraf, winter gloves, and insulated boots."
        # 41 <= temp <= 50
        elif 41 <= temp <= 50:
            return "Long-sleeved, fitted top with a thick sweater, possibly with a light jacket over top, and closed-toed shoes."
        # 51 <= temp <= 60
        elif 51 <= temp <= 60:
            return "lighter long-sleeved sweater, top paired with jeans, loafers, and closed-toed shoes."
        # 61 <= temp <= 70
        elif 61 <= temp <= 70:
            return "Short-sleeved, three-quarter length, or long-sleeved, jeans, and sneakers or slip-ons."
        # 71 <= temp <= 80
        elif 71 <= temp <= 80:
            return "Airy cotton or silk tops, shorts or pants made of light materials, and sneakers or any open-toed shoes."
        # temp => 81
        else:
            return "Shorts, tank tops, tube tops, dresses, and flip flops or open-toed shoes"

    # home page
    @app.route("/")
    def home():
        return render_template("home.html")

    # show results
    @app.route("/result", methods=["POST"])
    def result():
        if request.method == "POST":
            message = "INVALID LOCATION"
            try:
                city = request.form['city_input'].title()
                check_string(city)
                check_city(city)
                kelvin = get_temp(city)
                # kelvin to Fahrenheit and Celsius
                def kelvin_to_celsius_fahrenheit(kelvin):
                    celsius = kelvin - 273.15
                    fahrenheit = celsius * (9/5) + 32
                    return celsius, fahrenheit
                # convert into C and F
                celsius, fahrenheit = kelvin_to_celsius_fahrenheit(kelvin)
                # format temp
                temperature_in_C = math.ceil(celsius)
                temperature_in_F = math.ceil(fahrenheit)
                # show clothes recommendation based on weather
                recommendation = get_clothes_rec(temperature_in_F)
            except requests.exceptions.RequestException as e:
                return render_template("error.html", message=message)
            except (KeyError, ValueError):
                return render_template("error.html", message=message)
            return render_template("result.html", city=city, temperature_in_C=temperature_in_C, temperature_in_F=temperature_in_F, recommendation = recommendation)
        return render_template("result.html")


    if __name__ == '__main__':
        main()
        # automatically reload on code changes, provides detailed error messages with stack traces
        app.run(debug=True)

    return app