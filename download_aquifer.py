import requests
import json

# URL for Bhopal aquifer GeoJSON
url = "https://bhuvan-app3.nrsc.gov.in/jjm_ver2/tools/draw_measure_tools/getDataForLegend.php?layerName=gwp_barddhaman"

# Make the request
response = requests.get(url)

# Check for success
if response.status_code == 200:
    data = response.json()
    with open("aquifer_barddhaman.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Aquifer data saved to aquifer_bhopal.json")
else:
    print("❌ Failed to fetch data. Status code:", response.status_code)
