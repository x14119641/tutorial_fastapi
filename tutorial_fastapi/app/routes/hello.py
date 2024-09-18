from fastapi import APIRouter


router = APIRouter()

@router.get("/hello")
async def get_root():
    return {"data": "Hello World!"}