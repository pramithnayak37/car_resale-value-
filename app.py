import streamlit as st
import pandas as pd
import numpy as np
import pickle as pk
import time


st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="wide")


model = pk.load(open('modelfinal1.pkl', 'rb'))
cd = pd.read_csv('2.csv')

def get(car_name):
    return car_name.split(' ')[0].strip()

def clean(value):
    if isinstance(value, str):
        value = value.split(' ')[0].strip()
    return float(value) if value != '' else 0

cd['name'] = cd['name'].apply(get)
cd['mileage'] = cd['mileage'].apply(clean)
cd['engine'] = cd['engine'].apply(clean)
cd['max_power'] = cd['max_power'].apply(clean)

st.markdown("""
    <style>
    .main {
        background-color: #f4f7fa;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    h1 {
        font-size: 36px;
        color: #333;
        text-align: center;
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
    }
    .header {
        background-color: #53a8b6;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .popup {
        padding: 20px;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        font-size: 18px;
        text-align: center;
        margin-top: 20px;
    }
    .sidebar .sidebar-content {
        font-size: 16px;
        font-family: 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<div class='header'> 🚗 Estimate your wheels</div>", unsafe_allow_html=True)


st.sidebar.header('Enter Car Details')
st.sidebar.markdown("Fill out the details below to get an estimated price for your car!")


name = st.sidebar.selectbox('Select Car Brand', cd['name'].unique())
Color = st.sidebar.selectbox('Select Car Color', cd['Color'].unique())
year = st.sidebar.slider('Car Manufactured Year', 1994, 2024)
km_driven = st.sidebar.slider('KMs Driven', 0, 200000)
fuel = st.sidebar.selectbox('Fuel Type', cd['fuel'].unique())
seller_type = st.sidebar.selectbox('Seller Type', cd['seller_type'].unique())
transmission = st.sidebar.selectbox('Transmission Type', cd['transmission'].unique())
owner = st.sidebar.selectbox('Owner Type', cd['owner'].unique())
mileage = st.sidebar.slider('Car Mileage (km/l)', 10, 40)
engine = st.sidebar.slider('Engine (cc)', 700, 5000)
max_power = st.sidebar.slider('Max Power (bhp)', 0, 200)
seats = st.sidebar.slider('Number of Seats', 5, 10)
accident = st.sidebar.selectbox('Has it had an Accident?', cd['accident'].unique())
insurance_claimed = st.sidebar.selectbox('Has Insurance Claim?', cd['Insurance_claimed'].unique())


car_image = st.sidebar.file_uploader("Upload a photo of your car", type=["jpg", "jpeg", "png"])


image_files = ['OIP (1).jpeg', 'OIP (2).jpeg', 'OIP (3).jpeg', 'OIP (4).jpeg', 'OIP (5).jpeg', 'OIP (6).jpeg', 'OIP.jpeg','OIP (1).jpeg', 'OIP (2).jpeg', 'OIP (3).jpeg', 'OIP (4).jpeg', 'OIP (5).jpeg', 'OIP (6).jpeg', 'OIP.jpeg']  # Replace with your image paths

if st.sidebar.button("Predict Car Price"):
    ipdm = pd.DataFrame([[name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats, Color, accident, insurance_claimed]],
        columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats', 'Color', 'accident', 'Insurance_claimed']
    )
    
    ipdm['accident'].replace(['At least 1 accident or damage reported', 'None reported', 'At least 1 accident reported'], [1, 2, 3], inplace=True)
    ipdm['Insurance_claimed'].replace(['Insurance_claimed', 'Insurance claimed', 'Not claimed'], [1, 2, 3], inplace=True)
    ipdm['owner'].replace(['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'], [1, 2, 3, 4, 5], inplace=True)
    ipdm['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    ipdm['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
    ipdm['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
    ipdm['name'].replace(cd['name'].unique(), range(1, len(cd['name'].unique())+1), inplace=True)
    ipdm['Color'].replace(cd['Color'].unique(), range(1, len(cd['Color'].unique())+1), inplace=True)
    
    ipdm = ipdm.astype({
        'name': 'int',
        'year': 'int',
        'km_driven': 'int',
        'fuel': 'int',
        'seller_type': 'int',
        'transmission': 'int',
        'owner': 'int',
        'mileage': 'float',
        'engine': 'float',
        'max_power': 'float',
        'seats': 'int',
        'Color': 'int',
        'accident': 'int',
        'Insurance_claimed': 'int'
    })
    
   
    car_price = model.predict(ipdm)
    
   
    st.markdown(f'### Estimated Car Price: **₹{car_price[0]:,.2f}**')
    st.markdown('<div class="popup">Best Website for Car Price Predictions! We assure high precision with our AI models!</div>', unsafe_allow_html=True)

    if car_image is not None:
        st.image(car_image, caption="Your Car Photo", use_container_width=True)


st.markdown("<hr>", unsafe_allow_html=True)

image_container = st.empty()


for i in range(14): 
    image_container.image(image_files[i], use_container_width=True)
    time.sleep(2)
special_image_path = "F.png"  
st.image(special_image_path, caption="visuals with respect to price", use_container_width=True)
