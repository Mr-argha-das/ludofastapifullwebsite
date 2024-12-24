from fastapi import APIRouter, Request, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth
from login.model.userupi import UserUPIModel, UserUPITable
from starlette.config import Config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
from login.model.login_model import LoginBody, LoginTable
from starlette.middleware.sessions import SessionMiddleware

from wallet.wallet_model import WalletModel, WalletTable
from bson import ObjectId
from login.routes.rozarpay import createContact
import random
from twilio.rest import Client
# Initialize Firebase Admin SDK with the service account credentials




router = APIRouter()

class LoginBodyLogin(BaseModel):
    email : str
    password: str


# OAuth Configuration


@router.post("/api/user/create")
async def create_user(request: Request, body: LoginBody):
    phone = request.session.get("phonenumber")
    findata = LoginTable.objects(email=phone["number"]).first()
    if findata:
        return {
            "message": "user already exist",
            "data": None,
            "status": False
        }
    else:
        saveData = LoginTable(email=phone["number"], name=body.name, password=phone["number"])
        saveData.save()
        wallet = WalletTable(userid=str(ObjectId(saveData.id)), balance=49, totalWithdrawal=0)
        wallet.save()
        walletJson = wallet.to_json()
        walletFromjson = json.loads(walletJson)
        tojson = saveData.to_json()
        fromjson = json.loads(tojson)
        request.session["user"] = {
                "data":fromjson,
            }
        request.session["wallet"] = {
            "balance":walletFromjson,
            }
        return {
            "message": "User Created Succes",
            "data": fromjson,
            "status": True
        }




@router.get("/api/user/get-users")
async def get_User():
    findata = LoginTable.objects.all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Here is all users",
        "data": fromjson,
        "status": True
    }

@router.post("/api/user/login")
async def login_user(request: Request, body: LoginBodyLogin):
    findUser = LoginTable.objects(email=body.email).first()
    if findUser:
        if findUser.password == body.password:
            tojson = findUser.to_json()
            fromjson = json.loads(tojson)
            request.session["user"] = {
                "data":fromjson,
            }
            wallet = WalletTable.objects(userid=str(ObjectId(findUser.id))).first()
            walletTojson = wallet.to_json()
            walletFromJson = json.loads(walletTojson)
            request.session["wallet"] = {
            "balance":walletFromJson,
            }
            return {
                "message": "User Login Suces",
                "data":fromjson,
                "status": True
            }
        else:
            return {
                "message": "User password Inccorect",
                "data": None,
                "status": False
            }
    else:
        return {
                "message": "User not found",
                "data": None,
                "status": False
            }

@router.get("/api/user/{userid}")
async def getUserData(userid: str):
    findata = LoginTable.objects.get(id=ObjectId(userid))
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "here is user details",
        "data": fromjson,
        "status": True
        
    }



otp_storage = {}

# Define Pydantic models for requests
class OTPRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    otp: str

@router.post("/send-otp/")
async def send_otp(request: Request, body: OTPRequest):
    phone_number = body.phone_number
    otp = str(random.randint(100000, 999999))  # Generate 6 digit OTP

    # Save OTP temporarily
    otp_storage[phone_number] = otp
    account_sid = 'AC68d3bdc009b153d3e6c29eaa029799a6'
    auth_token = 'c43ed867127cb62e39129a06acfb0035'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                from_='+15744440027',
                body=f'Your Ludo Buddy login code {otp}',
                to=f'+91{phone_number}'
                )
    print(message.sid)
    # Here you can integrate with an SMS gateway like Twilio or Firebase to send OTP to user
    request.session["phonenumber"] = {
       "number": phone_number
    }
    print(phone_number)
    return {"message": "OTP sent", "otp": otp}  # In practice, don’t return OTP in response!

@router.post("/verify-otp/")
async def verify_otp(request: Request, body: OTPVerifyRequest):
    phone_number= request.session.get("phonenumber")
    print(phone_number)
    otp = body.otp

    # Check if OTP is valid
    stored_otp = otp_storage.get(phone_number["number"])

    if stored_otp == otp:
        findUser = LoginTable.objects(email=phone_number["number"]).first()
        if findUser:
            tojson = findUser.to_json()
            fromjson = json.loads(tojson)
            request.session["user"] = {
                "data":fromjson,
            }
            wallet = WalletTable.objects(userid=str(ObjectId(findUser.id))).first()
            walletTojson = wallet.to_json()
            walletFromJson = json.loads(walletTojson)
            request.session["wallet"] = {
            "balance":walletFromJson,
            }
            return {
                "message": "User Login Suces",
                "data":fromjson,
                "status": True
            }
        else:
             return {
                "message": "You dont have account register first",
                "data": None,
                "status": False
            }
    else:
        return {
                "message": "otp Incorrect",
                "data": None,
                "status": False
            }


@router.put("/api/update-upi")
async def updateUPI(request: Request, body: UserUPIModel):
    user= request.session.get("user")
    findata = UserUPITable.objects(userid=str(user["data"]["_id"]["\u0024oid"])).first()
    if(findata):
        findata.upiID = body.upiId
        findata.save()
        return {
            "message": "Upi updated succes",
            "status": True
        }
    else:
        savedata = UserUPITable(**body.dict())
        savedata.save()
        createContact(str(user["data"]["name"]), str(user["data"]["email"]), str(user["data"]["_id"]["\u0024oid"]))
        return {
            "message": "Upi id added succes",
            "status": True
        }
@router.get("/api/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")