from fastapi import APIRouter, status, Depends, FastAPI, HTTPException
from sql.schemas.costumer import Costumer
from sqlalchemy.orm import Session

from sql import models
from sql.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
    },
)


@router.post("/add")
async def createCostumer(costumer:Costumer,  db: Session = Depends(get_db))->Costumer:
    acc = models.User(**costumer.dict())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return {**costumer.dict()}



@router.get("/getcostumer", status_code=status.HTTP_200_OK)
async def get(db: Session = Depends(get_db))->Costumer:
    return db.query(models.User).all()