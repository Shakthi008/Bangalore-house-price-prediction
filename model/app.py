import streamlit as st
import pickle
import numpy as np


with open('banglore_home_prices_model.pickle', 'rb') as file:
    model = pickle.load(file)


st.title('Bangalore House Price Prediction')
st.write("""
    This is a simple web app to predict the price of a house in Bangalore based on the area (sqft),
    the number of BHKs, the number of bathrooms, and the location.
    """)


area = st.number_input("Area (Square Feet)", min_value=100, max_value=10000, step=50)
bhk = st.selectbox("BHK", [1, 2, 3, 4, 5])
bath = st.selectbox("Bath", [1, 2, 3, 4, 5])
location = st.selectbox("Location", ["1st block jayanagar", "Koramangala", "Whitefield", "Indiranagar", "MG Road"])


if st.button("Estimate Price"):
   
    input_data = np.array([[area, bhk, bath, location]])
    
    
    location_dict = {
        "1st block jayanagar": 0,
        "Koramangala": 1,
        "Whitefield": 2,
        "Indiranagar": 3,
        "MG Road": 4
    }
    location_num = location_dict.get(location, 0)  
    input_data[:, 3] = location_num  
    
  
    prediction = model.predict(input_data)
    predicted_price = prediction[0]
    
   
    st.write(f"The estimated price for the property is: {predicted_price:.2f} Lakh")
