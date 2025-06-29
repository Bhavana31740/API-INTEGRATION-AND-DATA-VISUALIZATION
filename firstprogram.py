import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import streamlit as st
except ImportError:
    print("streamlit module is not installed. Please install it using 'pip install streamlit'.")
    exit(1)

# Streamlit UI
st.set_page_config(page_title="Weather Dashboard", page_icon=":partly_sunny:", layout="centered")
st.markdown("<h1 style='text-align: center; color: royalblue;'>🌤️ Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Search box for city
city_input = st.text_input("Enter city name:", "London")

# Constants
API_KEY = '3202cd31f99ff876c99a73857118fa72'  # Your OpenWeatherMap API key

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return response, data

if city_input:
    response, data = get_weather_data(city_input)

    if response.status_code == 200:
        # Extract relevant data
        city_name = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description'].capitalize()
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        # Create a DataFrame
        weather_data = pd.DataFrame({
            'City': [city_name],
            'Temperature (°C)': [temperature],
            'Humidity (%)': [humidity],
            'Description': [weather_description]
        })

        # Display the data in a card-like format
        st.markdown(
            f"""
            <div style="background-color:#e3f2fd;padding:20px;border-radius:10px;text-align:center;">
                <h2 style="color:#1565c0;">{city_name}</h2>
                <img src="{icon_url}" alt="Weather icon">
                <p style="font-size:22px;"><b>{weather_description}</b></p>
                <p style="font-size:18px;">🌡️ <b>Temperature:</b> {temperature} °C</p>
                <p style="font-size:18px;">💧 <b>Humidity:</b> {humidity} %</p>
            </div>
            """, unsafe_allow_html=True
        )

        st.markdown("---")
        st.subheader("Raw Weather Data")
        st.dataframe(weather_data, use_container_width=True)

        # Visualization
        st.markdown("---")
        st.subheader("Temperature and Humidity")

        # Only select numeric columns for plotting
        numeric_data = weather_data[['Temperature (°C)', 'Humidity (%)']].melt(var_name='Metric', value_name='Value')

        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(data=numeric_data, x='Metric', y='Value', palette='Blues_d', legend=False)
        plt.title('Temperature & Humidity')
        plt.ylabel('Value')
        plt.xlabel('')
        plt.xticks(rotation=0)
        st.pyplot(fig)

        # Pie chart for weather description (not very meaningful for one city, but included for completeness)
        st.subheader("Weather Description")
        fig2, ax2 = plt.subplots()
        ax2.pie([1], labels=[weather_description], autopct='%1.1f%%', colors=['#90caf9'], startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    else:
        st.error("Error fetching data from OpenWeatherMap API. Please check the city name or try again.")
