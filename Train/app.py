import requests
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

api_base_url = "http://20.244.56.144/train"
auth_headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTM3MTk3OTEsImNvbXBhbnlOYW1lIjoiVHJhaW5DZW50cmFsIiwiY2xpZW50SUQiOiI1MmJmY2U3My1jNmQzLTQ1ZDYtOGY1Ni04ZDc0OWY2NWI3ZTQiLCJvd25lck5hbWUiOiIiLCJvd25lckVtYWlsIjoiIiwicm9sbE5vIjoiMTI0MDA0MDc0In0.tBafK4r-D1dV_TyIoQpbdnxtOzODQQuWJ61PzbC9rbI"
}

#Function to retrieve all the trains in the next 12 hours
def get_trains():
    response = requests.get(f"{api_base_url}/trains", headers=auth_headers)
    response.raise_for_status()
    trains = response.json()
    current_time = datetime.now()
    dep_time = current_time + timedelta(minutes=30)
    twelve_hours_from_now = current_time + timedelta(hours=12)

    filtered_trains = []
    for train in trains:
        departure_time = train.get("departureTime", "")
        if departure_time:
            departure_time_hours = int(departure_time.get("Hours", 0))
            departure_time_minutes = int(departure_time.get("Minutes", 0))
        departure_time = datetime(
            year=current_time.year,
            month=current_time.month,
            day=current_time.day,
            hour=departure_time_hours,
            minute=departure_time_minutes,
        )
        print(train)
        if current_time <= departure_time <= twelve_hours_from_now and departure_time > dep_time:
            filtered_trains.append(train)

    return filtered_trains

@app.route('/trains', methods=['GET'])
def trains():
    filtered_trains = get_trains()
    return jsonify(filtered_trains)

if __name__ == '__main__':
    app.run(debug=True)
