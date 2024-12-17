from http.client import HTTPException
from fastapi import FastAPI, APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from passbook.models.passbook_model import PassbookTable, PassBookBody
import json
from bson import ObjectId
from wallet.wallet_model import WalletTable
from datetime import datetime
from pydantic import BaseModel
import razorpay
router = APIRouter()

razorpay_client = razorpay.Client(auth=("rzp_live_o4XEUDdxzgCKM2", "WmNIargE6mAhUMczHy6N94dH"))
class OrderRequest(BaseModel):
    amount: int
    currency: str
    receipt: str

class PaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str


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


@router.post("/create-order/")
async def create_order(order: OrderRequest):
    try:
        # Create an order on Razorpay
        order_data = {
            "amount": order.amount * 100,  # Convert to paise
            "currency": order.currency,
            "receipt": order.receipt,
            "payment_capture": 1  # Auto-capture the payment
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        return {"order_id": razorpay_order['id']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-payment/")
async def verify_payment(payment: PaymentRequest):
    try:
        # Fetch the order to verify its signature
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

        # Return successful response
        return {"message": "Payment verified successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Payment verification failed: " + str(e))
    
