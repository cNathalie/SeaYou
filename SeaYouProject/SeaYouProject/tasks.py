from SeaYouProject.celery import shared_task
import os
import requests
from dotenv import load_dotenv

load_dotenv()



@shared_task
def refresh_access_token():

    print("REFRESH TOKEN _ TASK STARTED")

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
        access_token = data.get("access_token")
        os.environ["NXTPORT_CURRENT_TOKEN"] = access_token
        print(access_token)  # Assuming the response is in JSON format
    else:
        # Handle errors
        print(f"API call to refresh token failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging

# To trigger the task on app startup
@shared_task
def on_app_startup():
    refresh_access_token.apply_async((), countdown=10)  # small countdown to ensure it runs shortly after startup
