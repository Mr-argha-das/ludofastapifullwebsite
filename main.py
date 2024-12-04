from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect
from mongoengine import connect
from login.routes import login_routes
from ludoboard.routes import game_routes
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from starlette.staticfiles import StaticFiles
from passbook.routes import passbook_routes
from wallet.wallet_model import WalletTable
from passbook.models.passbook_model import PassbookTable
from bson import ObjectId
from categoryy.routes import mainCategoryroutes
import json
from categoryy.model.main_category import MainCateGoryModel, MainCategoryTable
from categoryy.model.sub_category import SubCategoryModel, SubCategoryTable
from ludoboard.models.gameall import GamePlayedTable
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


# If SECRET_KEY is not found, raise an error
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in .env file")
else:
    print("found" + SECRET_KEY)
    
connect('LudoTest', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/LudoTest")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    session_cookie="your_session_cookie",
)



templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(login_routes.router, tags=["Home"])
app.include_router(game_routes.router, tags=["Game"])
app.include_router(passbook_routes.router, tags=["payments"])
app.include_router(mainCategoryroutes.router, tags=["categorys"])
# page Routes
@app.get("/")
async def landingPage(request: Request):
    user= request.session.get("user")
    if(user):
      wallet = WalletTable.objects.get(userid=str(user["data"]["_id"]["\u0024oid"]))
      wallettojson = wallet.to_json()
      walletFromjson = json.loads(wallettojson)
      category  = MainCategoryTable.objects.all()
      tojson = category.to_json()
      fromjson = json.loads(tojson)
      print(fromjson)
      data = {
          "user": user,
          "wallet": walletFromjson,
          "category":fromjson
      }
      print(fromjson)
      return templates.TemplateResponse('home.html', {"request": request, **data})
    else:
      return templates.TemplateResponse('index.html', {"request": request})


@app.get("/login")
async def loginRoute(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

@app.get("/signup")

async def signuproute(request: Request):
    phone_number= request.session.get("phonenumber")
    data = {
        "number" : phone_number["number"]
    }
    print(data)
    return templates.TemplateResponse('signup.html', {"request": request, **data})

@app.get("/verfyotp")
async def verfyotp(request: Request):
    return templates.TemplateResponse('verfyotp.html', {"request": request})

@app.get("/game/")
async def landingPage(request: Request, userid: str, priceid: str):
    if (userid and priceid):
       return templates.TemplateResponse('ludo_4player.html', {"request": request})
    else:
        return {
            "page not found"
        }
@app.get("/deposit")
async def landingPage(request: Request):
    return templates.TemplateResponse('deposit.html', {"request": request})
@app.get("/home")
async def landingPage(request: Request):
    user= request.session.get("user")
    wallet = WalletTable.objects.get(userid=str(user["data"]["_id"]["\u0024oid"]))
    wallettojson = wallet.to_json()
    walletFromjson = json.loads(wallettojson)
    category  = MainCategoryTable.objects.all()
    tojson = category.to_json()
    fromjson = json.loads(tojson)
    print(fromjson)
    data = {
        "user": user,
        "wallet": walletFromjson,
        "category":fromjson
    }
    print(fromjson)
    return templates.TemplateResponse('home.html', {"request": request, **data})
@app.post("/home")
async def landingPage(request: Request):
    user= request.session.get("user")
    wallet = WalletTable.objects.get(userid=str(user["data"]["_id"]["\u0024oid"]))
    wallettojson = wallet.to_json()
    walletFromjson = json.loads(wallettojson)
    category  = MainCategoryTable.objects.all()
    tojson = category.to_json()
    fromjson = json.loads(tojson)
    print(fromjson)
    data = {
        "user": user,
        "wallet": walletFromjson,
        "category":fromjson     
    }
    print(fromjson)
    return templates.TemplateResponse('home.html', {"request": request, **data})

@app.get("/passbook")
async def homepost(request: Request):
    user= request.session.get("user")
    wallet = PassbookTable.objects(userid=str(user["data"]["_id"]["\u0024oid"])).all()
    wallettojson = wallet.to_json()
    walletFromjson = json.loads(wallettojson)
    data = {
        
        "wallet": walletFromjson
    }
    print(data)
    return templates.TemplateResponse('passbook.html', {"request": request, "items": walletFromjson})

@app.get("/price/{id}")
async def homepost(request: Request, id: str):
    user= request.session.get("user")
    wallet = SubCategoryTable.objects(maincategoryid=str(id)).all()
    wallettojson = wallet.to_json()
    walletFromjson = json.loads(wallettojson)
    
    print(walletFromjson)
    return templates.TemplateResponse('pricelist.html', {"request": request, "items": walletFromjson, "userid" :str(user["data"]["_id"]["\u0024oid"]) })


@app.get("/profile")
async def profile(request: Request):
    user= request.session.get("user")
    playedgames = GamePlayedTable.objects(userid=str(user["data"]["_id"]["\u0024oid"])).all()
    playedGamesCount = len(playedgames)
    return templates.TemplateResponse('profile.html', {"request": request, "playedGamesCount": playedGamesCount})
# Websoket
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)