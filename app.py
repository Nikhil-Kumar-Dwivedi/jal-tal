from flask import Flask, render_template, request, jsonify, redirect , url_for, session
import folium
from folium.plugins import MarkerCluster 
import pandas as pd
import joblib
import json
import mysql.connector
from flask import session
from flask import Flask, send_file
import os
from geopy.distance import geodesic
from flask import request, jsonify
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'a9d8sf9g7sdg8sdfg98sdf98gsd98g7sdg'  # Use a strong secret key in production



# Load and clean data
file_path = "jan_2023_data.xlsx"
df = pd.read_excel(file_path, sheet_name=0)
df.columns = [col.strip().replace("\n", " ") for col in df.columns]
df["LATITUDE"] = pd.to_numeric(df["LATITUDE"], errors='coerce')
df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"], errors='coerce')
df = df.dropna(subset=["LATITUDE", "LONGITUDE"])

# MySQL DB connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP default password
        database="jaltal"
    )

# Home redirects to aquifer
@app.route('/')
def index():
    return aquifer()

@app.route('/aquifer')
def aquifer():


    m = folium.Map(location=[23.173388, 77.395198], zoom_start=11)
    # folium.Marker(location=[23.173388, 77.395198], popup='Example').add_to(m)
    
    m.get_root().html.add_child(folium.Element("""
    <script>
    setTimeout(() => {
        const mapList = Object.values(window).filter(obj => obj instanceof L.Map);
        if (mapList.length === 0) {
            console.log("Map not found");
            return;
        }
        const map = mapList[0];
        map.on('mousemove', function (e) {
            const lat = e.latlng.lat.toFixed(5);
            const lon = e.latlng.lng.toFixed(5);
            const coordDiv = parent.document.getElementById('coordinateDisplay');
            if (coordDiv) {
                coordDiv.textContent = `Lat: ${lat}, Lon: ${lon}`;
            }
        });
    }, 1000);
    </script>
    """))


    color_map = {
        14: 'orange',
        17: 'red',
        18: 'green',
        19: 'blue',
        20: 'orange',
        21: 'yellow',
        22: 'pink',
        24: 'orange',
        32: 'black',
        31: 'black',
        25: 'orange',
    }

    data_folder = os.path.join(os.getcwd(), 'aquifer_data')

    for file in os.listdir(data_folder):
        if file.endswith('.json'):
            filepath = os.path.join(data_folder, file)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    geojson_data = json.load(f)

                for feature in geojson_data.get('features', []):
                    sym_code = feature.get('properties', {}).get('sym_code', None)
                    geometry = feature.get('geometry', {})
                    coords = geometry.get('coordinates', [])

                    color = color_map.get(sym_code, 'lightgray')

                    def parse_coords(coord_list):
                        return [[lat, lon] for lon, lat in coord_list]

                    if geometry['type'] == 'MultiPolygon':
                        for poly in coords:
                            polygon_coords = parse_coords(poly[0])
                            folium.Polygon(
                                locations=polygon_coords,
                                color=color,
                                fill=True,
                                fill_color=color,
                                fill_opacity=0.6,
                                popup=f"sym_code: {sym_code}"
                            ).add_to(m)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    map_html = m._repr_html_()
    return render_template("aquifer.html", map_html=map_html)




@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    return render_template('nearestwell.html')  # Redirect to the nearest well page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_lat'] = user['latitude']
                session['user_lon'] = user['longitude']
                return redirect('/aquifer')
            else:
                return render_template('login.html', error="Invalid email or password")
        except mysql.connector.Error as err:
            print(f"Login Error: {err}")
            return render_template('login.html', error="Error during login. Please try again.")

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Check for existing email
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return render_template('signup.html', error="An account with this email already exists.")

            # Insert user
            cursor.execute("""
                INSERT INTO users (name, number, email, password, dob, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, number, email, password, dob, latitude, longitude))
            conn.commit()

            # Fetch inserted user to auto-login
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            # Store user info in session with consistent keys
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['latitude'] = user['latitude']      
            session['longitude'] = user['longitude']

            return redirect('/aquifer')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('signup.html', error="An error occurred while signing up. Please try again.")

    return render_template('signup.html')



# 🚀 New version of Nearest Well (with dynamic filters)
@app.route('/nearestwell')
def nearest_well():
    states = sorted(df["STATE/UT"].dropna().unique())
    user_lat = session.get('user_lat')
    user_lon = session.get('user_lon')
    return render_template("nearestwell.html", states=states, user_lat=user_lat, user_lon=user_lon)



@app.route('/user_nearestwell_data')
def user_nearestwell_data():
    user_lat = session.get('latitude')
    user_lon = session.get('longitude')

    if not user_lat or not user_lon:
        return jsonify({"error": "User not logged in or location not available"}), 401

    # Ensure float conversion (if session stores as string)
    user_lat = float(user_lat)
    user_lon = float(user_lon)

    wells = df[['LATITUDE', 'LONGITUDE', 'SITE NAME', 'WELL SITE TYPE', 'WATER LEVEL (mbgl)', 'DISTRICT']].dropna()
    wells['distance'] = wells.apply(
        lambda row: geodesic((user_lat, user_lon), (row['LATITUDE'], row['LONGITUDE'])).meters,
        axis=1
    )
    nearest = wells.loc[wells['distance'].idxmin()]

    return jsonify({
        "user_location": {
            "lat": user_lat,
            "lon": user_lon
        },
        "nearest_well": {
            "lat": nearest['LATITUDE'],
            "lon": nearest['LONGITUDE'],
            "popup": f"<b>Site Name:</b> {nearest['SITE NAME']}<br><b>Type:</b> {nearest['WELL SITE TYPE']}<br><b>Water Level:</b> {nearest['WATER LEVEL (mbgl)']} mbgl<br><b>District:</b> {nearest['DISTRICT']}"
        }
    })




@app.route('/get_districts', methods=['POST'])
def get_districts():
    state = request.json.get("state")
    districts = sorted(df[df["STATE/UT"] == state]["DISTRICT"].dropna().unique())
    return jsonify(districts)

@app.route('/get_wells', methods=['POST'])
def get_wells():
    state = request.json.get("state")
    district = request.json.get("district")
    filtered_df = df[(df["STATE/UT"] == state) & (df["DISTRICT"] == district)]

    well_data = []
    for _, row in filtered_df.iterrows():
        well_data.append({
            "lat": row["LATITUDE"],
            "lon": row["LONGITUDE"],
            "popup": f"""
                <b>Site Name:</b> {row['SITE NAME']}<br>
                <b>Type:</b> {row['WELL SITE TYPE']}<br>
                <b>Water Level:</b> {row['WATER LEVEL (mbgl)']} mbgl<br>
                <b>District:</b> {row['DISTRICT']}
            """
        })
    return jsonify(well_data)


@app.route('/submit_boring_data', methods=['POST'])
def submit_boring_data():
    # Get data
    state = request.form.get("state")
    district = request.form.get("district")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    depth = request.form.get("depth")
    boring_year = request.form.get("boring_year")
    submission_year = request.form.get("submission_year")
    feedback = request.form.get("feedback")

    row = {
        "State": state,
        "District": district,
        "Longitude": float(longitude),
        "Latitude": float(latitude),
        "Depth of Bore": float(depth),
        "Boring Year": int(boring_year),
        "Submission Year": int(submission_year),
        "FeedBack": feedback
    }

    # Path to Excel file
    file_path = "boring_data.xlsx"

    # Create or append
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(file_path, index=False)
    return jsonify({"message": "Boring data saved successfully!"})

@app.route('/farmerhelp')
def farmerhelp():
    return render_template("farmerhelp.html")

# Prediction route (unchanged)
model = joblib.load('random_forest_model.pkl')
@app.route('/predict_water_level', methods=['POST'])
def predict_water_level():
    data = request.json
    prediction_input = [[float(data["latitude"]), float(data["longitude"]), int(data["year"])]]
    prediction = model.predict(prediction_input)
    return jsonify({"predicted_water_level": prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
