from fastapi import APIRouter

router = APIRouter()


@router.get("/recommend/")
async def get_recommendation():
    return {"status": 200, "items": ["item1", "item2", "item3"]}
