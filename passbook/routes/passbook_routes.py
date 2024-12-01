from fastapi import FastAPI, APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from passbook.models.passbook_model import PassbookTable, PassBookBody
import json
from bson import ObjectId
from wallet.wallet_model import WalletTable
from datetime import datetime
router = APIRouter()

@router.post("/api/v1/deposit-amount")
async def payment_create(request: Request, amount: int = Form(...)):
    user= request.session.get("user")
    print(user)
    wallet = WalletTable.objects(userid=str(ObjectId(user["data"]["_id"]["\u0024oid"]))).first()
    amountotal = wallet.balance
    wallet.balance = amountotal + amount
    wallet.save()
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    passbook = PassbookTable(userid=str(ObjectId(user["data"]["_id"]["\u0024oid"])), title="Deposit" ,amount=f"+ {amount}", cre_date=f"{formatted_datetime}")
    passbook.save()
    walletJson = wallet.to_json()
    walletFromjson = json.loads(walletJson)
    passbookJson = passbook.to_json()
    passbookFromjson = json.loads(passbookJson)
    return RedirectResponse(url="/home")
    
