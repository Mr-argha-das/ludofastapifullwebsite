import base64
import os
import random
import string
from dotenv import load_dotenv
import requests

from login.model.userfund import UserFundTable
from login.model.userupi import UserUPITable

load_dotenv()
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # Letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def createContact(name, phone, userid):

    auth_string = f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    url = "https://api.razorpay.com/v1/contacts"  # Replace with the actual API URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_encoded}"  # Replace with actual API key if needed
    }
    random_str = generate_random_string(4)
    payload = {
        "name": name,
        "email": f"{name}.{random_str}bigbuddy.com",
        "contact": f'91{phone}',
        "type": "User",
        "reference_id": f"Acme Contact ID {userid}",
        "notes": {
            "random_key_1": "Thank you user",
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 2001:
        print("Data sent successfully!")
        data = response.json()
        createRozarPayFPA(userid, data["id"])
    else:
        print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")

    return response.json()



def createRozarPayFPA(userid, contactid):
    findUpiId = UserUPITable.objects(userid=userid).first()
    url = "https://api.razorpay.com/v1/fund_accounts"
    auth_string = f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_encoded}"  # Replace with actual API key if required
    }
    
    # Payload data (the JSON body)
    payload = {
        "contact_id": contactid,
        "account_type": "vpa",
        "vpa": {
            "address": f"{findUpiId.upiID}"
        }
    }
    
    # Send POST request to the external API
    response = requests.post(url, json=payload, headers=headers)
    
    # Handle the response
    if response.status_code == 200 or response.status_code == 201:
        print("Data sent successfully!")
        print("Response:", response.json())
        responseData = response.json()
        findUSerfundAccont = UserFundTable.objects(userid=userid).first()
        if(findUSerfundAccont):
            UserFundTable.objects(userid=userid).update_one(
        set__userid=userid,
        set__fund_acc_id=responseData["id"],
        set__contact_id=contactid,
        upsert=True  # Ensures the document is created if it doesn't exist
    )
        else:
            savedata = UserFundTable(userid=userid, fund_acc_id=responseData["id"], contact_id=contactid)
            savedata.save()
            
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print("Error:", response.text)