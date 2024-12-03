from datetime import datetime
import json
from bson import ObjectId
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from categoryy.model.sub_category import SubCategoryTable
from passbook.models.passbook_model import PassbookTable
from wallet.wallet_model import WalletModel, WalletTable
from login.model.login_model import LoginBody, LoginTable
import random
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates")
@router.get("/4player")
async def player4(request: Request):
    return templates.TemplateResponse('4player.html', {"request": request})

connected_users = []

# Class to handle individual WebSocket connection
class ConnectionManager:
    def __init__(self):
        self.active_connections: list = []

    async def connect(self, websocket: WebSocket, userid: str):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "userid": userid})

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection['websocket'] == websocket:
                self.active_connections.remove(connection)
                break

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)
    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection["websocket"].send_text(message)

manager = ConnectionManager()


connected_users_by_game = {}  
user_opponent_map = {}
@router.websocket("/find-opponent/{userid}/{priceid}")
async def websocket_endpoint(websocket: WebSocket, userid: str, priceid: str):
    userdata = LoginTable.objects.get(id=ObjectId(userid))
    await manager.connect(websocket, userid)

    if priceid not in connected_users_by_game:
        connected_users_by_game[priceid] = []

    connected_users_by_game[priceid].append({"userid": userid, "websocket": websocket})
   
   

    try:
        # Check if there is another user waiting with the same game ID
        if len(connected_users_by_game[priceid]) >= 2:
            # Randomly pick another user
            other_user = random.choice([user for user in connected_users_by_game[priceid] if user["userid"] != userid])
            values = ["P1", "P2"]
            value_a, value_b = random.sample(values, 2)

            # Notify both users about the connection
            opp = LoginTable.objects.get(id=ObjectId(str(other_user["userid"])))
            opponent_json = json.loads(opp.to_json())

            user_data = {
                "message": "Connected with opponent",
                "opponent": other_user["userid"],
                "your_player": value_a,
                "opponent_data": opponent_json,
                "enimidata": None
            }

            userdata_json = json.loads(userdata.to_json())

            opponent_data = {
                "message": "Connected with opponent",
                "opponent": userid,
                "your_player": value_b,
                "opponent_data": userdata_json,
            }

            # Send JSON response to both users
            await manager.send_json(websocket, user_data)
            await manager.send_json(other_user["websocket"], opponent_data)

            # Store opponent's websocket for both users
            user_opponent_map[userid] = other_user["websocket"]
            user_opponent_map[other_user["userid"]] = websocket

            # Remove paired users from the game pool
            connected_users_by_game[priceid] = [
                user for user in connected_users_by_game[priceid]
                if user["userid"] not in [userid, other_user["userid"]]
            ]

            print(f"Users {userid} and {other_user['userid']} paired successfully.")

        else:
            print(f"Waiting for another player for user {userid}")

        while True:
            # Wait for data from the user
            print(user_opponent_map)
            data = await websocket.receive_json()
            print(f"Received JSON data from {userid}: {data}")

            # Forward the data to the opponent if they exist in the map
            if userid in user_opponent_map:
                opponent_ws = user_opponent_map[userid]
                if opponent_ws:  # Ensure the opponent WebSocket exists
                    response = {
                        "message": "game data",
                        "from": userid,
                        "data_received": data
                    }
                    print(f"Sending data from {userid} to opponent.")
                    await manager.send_json(opponent_ws, response)
                else:
                    print(f"Opponent WebSocket not found for {userid}")
            else:
                print(f"No opponent found for {userid}")

    except WebSocketDisconnect:
        print(f"User {userid} disconnected.")
        # Clean up user's connection from the game pool
        connected_users_by_game[priceid] = [
            user for user in connected_users_by_game[priceid]
            if user["userid"] != userid
        ]
        await manager.disconnect(websocket)
        
        # Remove from opponent map
        if userid in user_opponent_map:
            opponent_ws = user_opponent_map.pop(userid, None)
            if opponent_ws:
                print(f"Opponent disconnected for {userid}")
                await manager.disconnect(opponent_ws)


def calculate_percentage(amount, percentage):
    return (amount * percentage) / 100

@router.post("/api/post-winer")
async def postWiner(winerId: str, loserId: str, price: str):
    winerData = WalletTable.objects.get(userid=winerId)
    loserData = WalletTable.objects.get(userid=loserId)
    priceList = SubCategoryTable.objects.get(id=ObjectId(price))
    priceammount = priceList.price
    grandTotal = priceammount+priceammount
    serviceammount = calculate_percentage(grandTotal, 8)
    winerAmmount = grandTotal - serviceammount
    winerData.balance = winerData.balance + winerAmmount
    winerData.save()
    loserData.balance
    loserData.balance= loserData.balance - priceammount
    loserData.save()
    winerUSER = LoginTable.objects.get(id=ObjectId(winerId))
    loserUSER = LoginTable.objects.get(id=ObjectId(loserId))
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    winer = PassbookTable(userid=winerId, title=f"you win a match agganest {loserUSER.name}", amount = f"(+) {winerAmmount}", cre_date=f"{formatted_datetime}")
    winer.save()
    loser = PassbookTable(userid=winerId, title=f"you lose a mach agganest {winerUSER.name}", amount = f"(-) {priceammount}", cre_date=f"{formatted_datetime}")
    loser.save()
    return {
        "message": "balance update",
        "status": True
    }

# when user click on the play button then check her balanece
@router.get("/api/check-user-wallet/{priceid}")
async def checkUserBalacnce(request: Request, priceid: str):
    user= request.session.get("user")
    findWallet = WalletTable.objects.get(userid=str(user["data"]["_id"]["\u0024oid"]))
    gamePrice = SubCategoryTable.objects.get(id=ObjectId(priceid))
    if(findWallet.balance > gamePrice.price):
        return {
            "message": "you have balance to play game",
            "status": True
        } 
    else:
        return {
            "message": "You dont have balance to play",
            "status":False
        }


# /game/?userid={{userid}}&priceid={{item['_id']['\u0024oid']}}