# Import necessary modules
import os 
import requests
from dotenv import load_dotenv
from tkinter import Tk, Entry, Button, Label, PhotoImage

# Load environment variables from .env file
load_dotenv()

# Define constants
FONT = ("Times New Roman", 10, "bold")
BG = "#6c9cf0"
API_KEY = os.getenv("API_KEY")
URL = "https://api.openweathermap.org/data/2.5/weather"
PARAMETER = {
    "q": "",
    "units": "metric",
    "appid": API_KEY
}

# Function to create a label
def create_label(window, text, font, bg, row, column):
    label = Label(window, text=text, font=font, bg=bg)
    label.grid(row=row, column=column)
    label.grid_remove()
    return label

# Function to fetch weather data
def fetch_weather_data(city_name):
    PARAMETER["q"] = city_name
    response = requests.get(url=URL, params=PARAMETER)
    data = response.json()
    return data, response.status_code

# Function to parse weather data
def parse_weather_data(data):
    city_name = data.get("name")
    city_temp = round(data.get("main").get("temp"))
    humidity_val = data.get("main").get("humidity")
    wind_speed = data.get("wind").get("speed")
    weather_description = (data.get("weather")[0].get("description")).title()
    weather_condition = (data.get("weather")[0].get("main")).lower()
    return city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition

# Function to update labels with weather data
def update_labels(city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition):
    city_name_label.config(text=f"{city_name}")
    humidity_value.config(text=f"{humidity_val}%")
    wind_value.config(text=f"{wind_speed}km/h")
    city_temp_label.config(text=f"{city_temp}°c | {weather_description}")

    atmosphere = ["mist", "haze", "smoke", "dust", "fog", "sand", "ash", "squall", "tornado"]

    if weather_condition in atmosphere:
        window.weather_img = PhotoImage(file="./assets/images/atmosphere.png")
    else:
        window.weather_img = PhotoImage(file=f"./assets/images/{weather_condition}.png")
    city_condition_label.config(image=window.weather_img)

# Function to display all the weather data
def display_weather_data():
    city_condition_label.grid()
    city_temp_label.grid()
    city_name_label.grid()
    humidity_icon.grid()
    humidity_value.grid()
    humidity_label.grid()
    wind_icon.grid()
    wind_label.grid()
    wind_value.grid()

# Function to remove all widgets
def remove_widgets():
    city_condition_label.grid_remove()
    city_temp_label.grid_remove()
    city_name_label.grid_remove()
    humidity_icon.grid_remove()
    humidity_value.grid_remove()
    humidity_label.grid_remove()
    wind_icon.grid_remove()
    wind_label.grid_remove()
    wind_value.grid_remove()

# Function to get weather data
def get_weather_data():
    city_name = search_entry.get()
    data, status_code = fetch_weather_data(city_name)
    if status_code == 200:
        city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition = parse_weather_data(data)
        update_labels(city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition)
        display_weather_data()
    else:
        remove_widgets()
        error_label = create_label(window, "City not found. Please try again.", ("Times New Roman", 20, "bold"), BG, 4, 2)
        error_label.grid()


# Create main window
window = Tk()
window.title("Weather App")
window.config(padx=30, pady=30, bg=BG)

# Create search entry
search_entry = Entry(width=65, justify="left", highlightthickness=0)
search_entry.grid(row=0, column=0, columnspan=4)
search_entry.insert(index=0, string="Enter City Name")

# Create search button
search_img = PhotoImage(file="./assets/images/search.png").subsample(3)
search_button = Button(window, image=search_img, highlightthickness=0, command=get_weather_data)
search_button.grid(row=0, column=4)

# Create labels
condition_img = PhotoImage(file="./assets/images/clouds.png")
city_condition_label = Label(image=condition_img, highlightthickness=0, bg=BG)
city_condition_label.grid(row=1, column=2)
city_condition_label.grid_remove()

city_temp_label = create_label(window, "7°c | Sunny", ("Times New Roman", 20, "bold"), BG, 2, 2)
city_name_label = create_label(window, "New York", ("Times New Roman", 25, "bold"), BG, 3, 2)

humidity_image = PhotoImage(file="./assets/images/humidity.png")
humidity_image = humidity_image.subsample(8)
humidity_icon = Label(image=humidity_image, highlightthickness=0, bg=BG)
humidity_icon.grid(row=4, column=0)
humidity_icon.grid_remove()

humidity_value = create_label(window, "48%", ("Times New Roman", 13, "bold"), BG, 4, 1)
humidity_label = create_label(window, "Humidity", FONT, BG, 5, 1)

wind_speed_image = PhotoImage(file="./assets/images/wind.png")
wind_speed_image = wind_speed_image.subsample(3)
wind_icon = Label(image=wind_speed_image, highlightthickness=0, bg=BG)
wind_icon.grid(row=4, column=3)
wind_icon.grid_remove()

wind_value = create_label(window, "10.29 km/h", ("Times New Roman", 13, "bold"), BG, 4, 4)
wind_label = create_label(window, "Wind Speed", FONT, BG, 5, 4)

# Start the main loop
window.mainloop()
