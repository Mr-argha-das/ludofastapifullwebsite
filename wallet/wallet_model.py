from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class WalletTable(Document):
    userid = StringField(required=True)
    balance = IntField(required=True)
    totalWithdrawal = IntField(required=True)


class WalletModel(BaseModel):
    userid : str
    balance : int
    totalWithdrawal : int 