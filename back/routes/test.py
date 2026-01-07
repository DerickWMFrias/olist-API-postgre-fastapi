from fastapi import APIRouter, Depends


router = APIRouter(prefix="",
                   tags=["Test"],
                   responses={},
                   dependencies=[])

@router.get("/")
def read_root():
    return {"Hello": "World"}