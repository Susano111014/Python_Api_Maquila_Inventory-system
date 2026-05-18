from ast import List
from urllib.request import Request

from fastapi import APIRouter, File, UploadFile, HTTPException
from service.service_stock import upload_file as process_stock


router = APIRouter(prefix="/stock", tags=["stocks"])

@router.post("/uploadFile")
async def preview_file(file: UploadFile = File(...)):
    if not (isinstance(file.filename, str) and  file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Not a xlsx file")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="file must not be empty")

    try:
        return process_stock(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))