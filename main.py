from fastapi import FastAPI
from pydantic import BaseModel
import requests
import pandas as pd
import random

app = FastAPI()
API_KEY = "85b6fefb68e749a9aba53727242609"


@app.get("/")
def main_app():
    return {"message": "Welcome to Weatherman API"}


class Location(BaseModel):
    longitude: int|float
    latitude: int|float

def load_clothing_data(file_path):
    return pd.read_csv(file_path)

def recommend_clothing_based_on_temperature(temperature, clothing_data):
    suitable_clothes = clothing_data[(clothing_data['Min Temp'] <= temperature) & (clothing_data['Max Temp'] >= temperature)]
    return suitable_clothes


# Load clothing dataset
clothing_data = load_clothing_data('clothing_data.csv')


@app.post("/api/v1/weather")
def get_weather(location: Location):
    print("LOCATION: ", location)
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location.latitude},{location.longitude}&aqi=no"
    response = requests.get(url)
    weather_data = response.json()
    temperature = weather_data['current']['temp_c']

    recommended_clothes = recommend_clothing_based_on_temperature(temperature, clothing_data).to_dict(orient="records")

    return {"recommended_clothes": random.choice(recommended_clothes), "weather_data": weather_data}