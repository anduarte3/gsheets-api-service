import os 
from dotenv import load_dotenv
import gspread
import requests
import time

# Load environment variables from .env file
load_dotenv()

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
AVIATION_API_KEY = os.getenv("AVIATION_API_KEY")

gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_PATH)
print(gc)
sh = gc.open("FlightAPI")
wks = sh.worksheet("FlightAPI")

print("Connected to sheet:", wks.title)

flight_api_url = f"https://api.aviationstack.com/v1/flights?access_key={AVIATION_API_KEY}"

wks.clear()
headers = ["Flight Date", "Flight Status", "Departure Airport", "Departure Timezone", "Departure Delay",
           "Departure Scheduled", "Arrival Airport", "Arrival Timezone","Arrival Delay",
           "Arrival Scheduled", "Airline Name", "Flight Number"]
wks.append_row(headers)
print("Headers added to the sheet:", headers)

try:
    response = requests.get(flight_api_url)
    response.raise_for_status()  # Raise an error for bad responses
except requests.exceptions.RequestException as e:
    print("Error fetching flight data:", e)
    exit()

# Display empty json values
def empty_values(value, *keys):
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return ""
    return value if value is not None else ""

# Change delay value to hours and minutes
def delay_calc(value):          
    try:
        delay = int(value)
        delay_hours = delay // 60
        delay_minutes = delay % 60
        return f"{delay_hours}h {delay_minutes}m"
    except:
        return "On time"

def get_flight_data():
    if response.status_code == 200:
        data = response.json()
        flights = data.get("data", [])
        
        if flights:
            for flight in flights:
                flight_data = [
                    empty_values(flight, "flight_date"),
                    empty_values(flight, "flight_status"),
                    empty_values(flight, "departure", "airport"),
                    empty_values(flight, "departure", "timezone"),
                    delay_calc(empty_values(flight, "departure", "delay")),
                    empty_values(flight, "departure", "scheduled"),
                    empty_values(flight, "arrival", "airport"),
                    empty_values(flight, "arrival", "timezone"),
                    delay_calc(empty_values(flight, "arrival", "delay")),
                    empty_values(flight, "arrival", "scheduled"),
                    empty_values(flight, "airline", "name"),
                    empty_values(flight, "flight", "number")
                ]
                wks.append_row(flight_data)
                print("Appending:", len(flight_data), flight_data)

                time.sleep(2)
            print("Flight data successfully written to the sheet.")
        else:
            print("No flight data found.")

get_flight_data()