from datetime import datetime, timedelta
import os
import json
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler


load_dotenv()


def start():
    time_to_run_job = datetime.now() + timedelta(seconds=15)

    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_access_token) # To run on startup

    scheduler.add_job(refresh_weather_data, 'date', run_date=time_to_run_job) #To run after access token has been aquired
    scheduler.add_job(refresh_ETA_data, 'date', run_date=time_to_run_job) #To run after access token has been aquired

    # scheduler.add_job(refresh_access_token, 'interval', minutes=45) # To run every 45 mins
    # scheduler.add_job(refresh_weather_data, 'interval', minutes=50) #To run every 50 mins
    # scheduler.add_job(refresh_ETA_data, 'interval', minutes=30) #To run every 30 mins
    #scheduler.start()

def refresh_access_token():
    from SeaYou_Models.models import AccessToken
    try:

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("REFRESH TOKEN _ TASK STARTED: " + formatted_datetime)
        

        # get access token
        api_url = os.getenv("NXTPORT_GET_TOKEN")
        form_data = {
            "username" : os.getenv("NXTPORT_USERNAME"),
            "password" : os.getenv("NXTPORT_PASSWORD"),
            "grant_type" : "password",
            "client_id" : os.getenv("NXTPORT_ID"),
            "client_secret" : os.getenv("NXTPORT_SECRET"),
            "scope" : "openid"
        }

        response = requests.post(api_url, data=form_data)
        if response.status_code == 200:
            # Request was successful
            print("API call successful!")
            data = response.json()
            new_access_token = data['access_token']
            valid_for = data['expires_in']
            expires = datetime.now() + timedelta(seconds = valid_for)

            AccessToken.objects.update_or_create(defaults={'token': new_access_token, 'exp_date': expires}) 

        else:
            # Handle errors
            print(f"API call to refresh token failed with status code: {response.status_code}")
            print(response.text)  # Print the response content for debugging
    except Exception as e:
         print(f"Error in refresh_access_token task: {e}")


def refresh_weather_data():
    from SeaYou_Models.models import AccessToken, WeatherCache

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print("WEATHER _ TASK STARTED: " + formatted_datetime)

    locations = ["bos", "kas", "kis", "ros", "zas", "k102"]
    accumulated_data = []

    # Make an API call for every weather station location
    current_access_token = AccessToken.objects.first().token
    weather_url = os.getenv("NXTPORT_METEO_URL")

    weather_headers = {
        "Authorization" : "Bearer " + current_access_token,
        "Accept" : "*/*",
        "Accept-Encoding" : "gzip,deflate,br",
        "Connection" : "keep-alive",
        "Content-Type": "application/json",
    }

    for location in locations:
        weather_params = {
            "location": location,
            "subscription-key": os.getenv("NXTPORT_METEO_SUBKEY")
        }

        weather_response = requests.get(weather_url, params=weather_params, headers=weather_headers)

        if weather_response.status_code == 200:
            # Request was successful
            print(f"WEATHER API call for location {location} successful!")
            weather_data = weather_response.json()
            # Add the data to the accumulated_data dict
            accumulated_data.append(dict(weather_data[0]))
            
        else:
            print(f"WEATHER API call for location {location} failed with status code: {weather_response.status_code}")
            print(weather_response.text)
            continue
    
    WeatherCache.objects.update_or_create(defaults={'cashed_weather_data': json.dumps(accumulated_data), 'updated_at': datetime.now()})


def refresh_ETA_data():
    from SeaYou_Models.models import ETACache, AccessToken

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print("ETA _ TASK STARTED: " + formatted_datetime)

    current_access_token = AccessToken.objects.first().token
    eta_url = os.getenv("NXTPORT_ETA_URL")
    eta_headers = {
        "Authorization" : "Bearer " + current_access_token,
        "Ocp-Apim-Subscription-Key" : os.getenv("NXTPORT_ETA_SUBKEY"),
        "Accept" : "*/*",
        "Accept-Encoding" : "gzip,deflate,br",
        "Connection" : "keep-alive",
        "Content-Type": "application/json",
    }
    eta_params = {
        "portLoCode" : "BEANR" #BElgie ANtwerpen Rechteroever
    }

    eta_response = requests.get(eta_url, headers=eta_headers, params=eta_params)
    eta_data = eta_response.text

    if eta_response.status_code == 200:
        # Request was successful
        print(f"ETA API call successful!")
        ETACache.objects.update_or_create(name = 'BEANR', defaults={"cashed_eta_data" : eta_data, "updated_at" : datetime.now()})
    else:
        print(f"ETA API call failed with status code: {eta_response.status_code}")
        print(eta_response.text)
        

