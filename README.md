# 🌊 जल-तल (Jal-Tal): A Smart Groundwater Awareness and Prediction Platform

जल-तल (Jal-Tal) is a comprehensive web-based application aimed at educating, assisting, and empowering farmers and citizens with groundwater data, aquifer levels, and predictive insights. It enables users to interact with a map-based interface, predict future water levels using machine learning, and contribute real-world boring data to continuously improve the model accuracy.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Data Sources](#data-sources)
- [Machine Learning Model](#machine-learning-model)
- [Frontend Design](#frontend-design)
- [Backend and Database](#backend-and-database)
- [How the App Works](#how-the-app-works)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## 💡 Project Overview

The goal of जल-तल is to provide an interactive and intelligent interface that:
- Displays aquifer data across Indian towns and districts
- Predicts future water depth at the nearest well to the user
- Allows farmers to contribute real-time boring data with location and feedback
- Offers educational resources and best farming practices (via Farmer Help section)

---

## ✨ Key Features

- 🗺️ **Aquifer Mapping**: Displays aquifer positions using Leaflet maps
- 📍 **Nearest Well Detection**: Automatically locates the nearest well from user's signup location
- 📊 **Future Depth Prediction**: Uses historical well data and Random Forest model for prediction
- 👨‍🌾 **Farmer Help Section**: Provides farming techniques like tied ridging for erosion prevention
- 📌 **User Location Marking**: Registered users can mark their home and download data
- 📥 **Data Contribution**: Allows users to submit boring data with depth & feedback
- 🔐 **Authentication System**: Secure login/signup with MySQL using XAMPP

---

## 🧰 Tech Stack

| Area             | Technology               |
|------------------|---------------------------|
| Frontend         | HTML, CSS, Bootstrap 5, JavaScript, Leaflet.js |
| Backend          | Python (Flask Framework) |
| Database         | MySQL (XAMPP)            |
| Data Storage     | Excel and JSON file handling (via Pandas) |
| Machine Learning | Random Forest Regressor (scikit-learn) |
| Map Rendering    | Leaflet.js                |

---

## 📂 Data Sources

- **Central Ground Water Board (CGWB)**: Well data including location, water levels over years
- **Manual Boring Submissions**: Data collected from users (depth and feedback)
- **Aquifer District Mapping**: Curated GeoJSON files for towns and states

---

## 🤖 Machine Learning Model

- **Model Used**: `RandomForestRegressor` from `sklearn.ensemble`
- **Input Features**: Year, District, Well ID, Previous Water Levels
- **Output**: Predicted Water Depth for a future year
- **Training**: Model trained offline and integrated via Flask API for dynamic use

---

## 🎨 Frontend Design

- Built with **Bootstrap 5** for responsiveness
- **Leaflet.js** used to render interactive maps with markers, zoom, and clustering
- Separate HTML templates:
  - `aquifer.html`: Highlights aquifer data
  - `nearestwell.html`: Shows nearest well + prediction + user uploads
  - `farmerhelp.html`: Farming technique resources
  - `login.html`, `signup.html`: Auth screens with form validation
- Blurred background for visual appeal and readability

---

## 🛠️ Backend and Database

- Flask app structured with `app.py`, templates, static files, and a `utils/` folder
- Boring data is collected and saved into an Excel file (`utils/boring_data.xlsx`)
- Session management used to keep track of logged-in users
- MySQL (via XAMPP) handles:
  - User signup/login
  - User home location (lat/lon)
- Predictive results generated in real-time using pre-loaded ML model

---

## 🔄 How the App Works

1. **User Registration**: Users sign up and select their home location on the map.
2. **Aquifer View**: Opens on default (`aquifer.html`), showing aquifer data by district.
3. **Nearest Well Page**: 
   - Uses session data to show user's nearest well in **pink**
   - Displays all wells using optimized markers (Circle/MarkerCluster)
   - User can **download data** (Excel or JSON)
   - User can **submit boring data** with map-based location
4. **Prediction**: Clicking the pink marker runs a Random Forest prediction for water depth.
5. **Farmer Help**: `farmerhelp.html` shows real-world solutions for soil and water conservation (sourced from Farmpedia).

---

## 🖼️ Screenshots


- 🔷 Aquifer Map with Districts Highlighted
- ![Screenshot 2025-05-03 225848](https://github.com/user-attachments/assets/dd5236c2-c41e-4e19-88e1-1d750987e9f1)

- 🔷 Nearest Well Prediction and Pink Marker Highlight
- 🔷 Submit Boring Data Form with Map Location Picker
- 🔷 Farmer Help Section with Background Image

---

## 🔮 Future Improvements

- 📱 Mobile responsiveness enhancements
- 📈 Live water level updates from IoT sensors
- 🤖 Live model retraining with user-submitted data
- 📬 SMS alerts for predicted drought or low water depth
- 🧑‍🌾 Farmer dashboard for viewing personal boring history

---

## 🚀 How to Run Locally

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/jal-tal.git
