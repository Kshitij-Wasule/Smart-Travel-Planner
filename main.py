import requests
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SmartTravel_API_KEY = os.getenv("SmartTravel_API_KEY")

genai.configure(api_key=SmartTravel_API_KEY)

st.set_page_config(page_title="Smart Travel Planner", page_icon="🌍")

st.title("🌍 Smart Travel Weather Planner")

st.write("Enter a destination to get weather and AI travel suggestions.")

city = st.text_input("Enter Destination")

API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

if st.button("Generate Travel Plan"):

    with st.spinner("🌍 Fetching weather and generating AI travel guide..."):

        response = requests.get(API_URL)

        if response.status_code == 200:

            data = response.json()

            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            weather = data["weather"][0]["main"]

            st.success("Weather Data Fetched Successfully!")

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            col1.metric("🌡 Temperature", f"{temperature} °C")
            col2.metric("💧 Humidity", f"{humidity}%")
            col3.metric("💨 Wind Speed", f"{wind_speed} m/s")
            col4.metric("🌤 Weather", weather)

            prompt = f"""
            I am planning a trip to {city}.

            Current Weather:
            🌡 Temperature: {temperature}°C
            💧 Humidity: {humidity}%
            🌤 Weather: {weather}
            💨 Wind Speed: {wind_speed} m/s

            Please provide:

            📍 Best Places to Visit
            🎒 Packing Checklist
            🎯 Activities to Do
            🍽 Famous Local Food
            ✈ Travel Tips

            Keep the answer short and use bullet points.
            """

            model = genai.GenerativeModel("gemini-flash-latest")

            result = model.generate_content(prompt)

            st.subheader("🤖 AI Travel Guide")
            st.markdown(result.text)

        else:
            st.error("Invalid City Name.")


            