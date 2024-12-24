from mongoengine import Document, StringField
from pydantic import BaseModel

class UserFundTable(Document):
    userid = StringField(required=True)
    fund_acc_id = StringField(required=True)
    contact_id = StringField(required=True)
