import base64
from http.client import HTTPException
from fastapi import FastAPI, APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from ludoboard.models.gameall import WithdrawalModel
from passbook.models.passbook_model import PassbookTable, PassBookBody
import json
from bson import ObjectId
from wallet.wallet_model import WalletTable
from datetime import datetime
from pydantic import BaseModel
import razorpay
import requests
router = APIRouter()
RAZORPAY_KEY_ID = 'rzp_live_o4XEUDdxzgCKM2'
RAZORPAY_KEY_SECRET = 'WmNIargE6mAhUMczHy6N94dH'
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
class OrderRequest(BaseModel):
    amount: int
    currency: str


class PaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

@router.post("/api/v1/create-order/")
async def create_order(request: Request, order: OrderRequest):
    
    try:
        # Create an order on Razorpay
        order_data = {
            "amount": order.amount * 100,  # Convert to paise
            "currency": order.currency,
            "payment_capture": 1  # Auto-capture the payment
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        request.session["ammont"] = order.amount
        return {"order_id": razorpay_order['id']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/verify-payment/")
async def verify_payment(request: Request, payment: PaymentRequest):
        order_id = payment.razorpay_order_id
        payment_id = payment.razorpay_payment_id
        signature = payment.razorpay_signature

        # Verify the payment signature
        params = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Razorpay SDK verifies the signature
        razorpay_client.utility.verify_payment_signature(params)
        user= request.session.get("user")
        amount= request.session.get("ammont")
        print(user)
        wallet = WalletTable.objects(userid=str(ObjectId(user["data"]["_id"]["\u0024oid"]))).first()
        amountotal = wallet.balance
        print(amount)
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
    

@router.post("/api/withdrawal")
async def withdrawal(body: WithdrawalModel):
    wallet = WalletTable.objects.get(userid=body.userid)
    
    if(body.ammount > 50 and wallet.balance <= body.ammount):
        wallet.balance = wallet.balance - body.ammount
        wallet.save()
        current_datetime = datetime.now()
        passbook =PassbookTable(userid=body.userid, title=f"Withdrawal success", amount = f"(-) {body.ammount}", cre_date=f"{current_datetime}")
        passbook.save()
        return {
            "message": "Your withdrawal succes",
            "status": True
        }
