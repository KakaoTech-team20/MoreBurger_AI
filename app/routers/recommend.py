from fastapi import APIRouter

router = APIRouter()


# andrew 작업물

@router.get("/recommend/")
async def get_recommendation():
    return {"status": 200, "items": ["item1", "item2", "item3"]}
