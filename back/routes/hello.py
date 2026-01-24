from fastapi import APIRouter, Depends


router = APIRouter(prefix="",
                   tags=["Test"],
                   responses={},
                   dependencies=[])

@router.get("/")
def say_hello():
    return {"Hello": "World"}