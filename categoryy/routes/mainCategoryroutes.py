from fastapi import APIRouter
import json
from bson import ObjectId
from categoryy.model.main_category import MainCateGoryModel, MainCategoryTable
from categoryy.model.sub_category import SubCategoryModel, SubCategoryTable
router = APIRouter()

@router.post("/api/v1/main-category")
async def main_category(body: MainCateGoryModel):
    savedata = MainCategoryTable(**body.dict())
    savedata.save()
    return {
        "message": " Main category added",
        "statuss" : True
    }

@router.get("/api/v1/get-main-cat")
async def get_mainCate():
    data  = MainCategoryTable.objects.all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
    "message": "here is all main category",
    "data": fromjson,
    "status": True
    }

@router.post("/api/v1/sub-category")
async def sub_category(body: SubCategoryModel):
    savedata = SubCategoryTable(**body.dict())
    savedata.save()
    return {
        "message": "sub category added",
        "statuss" : True
    }


@router.get("/api/v1/get-sub-cat")
async def get_mainCate():
    data  = SubCategoryTable.objects.all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
    "message": "here is all sub category",
    "data": fromjson,
    "status": True
    }