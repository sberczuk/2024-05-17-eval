from fastapi import FastAPI
from sqlmodel import SQLModel, Session

from models import Claim, ClaimInput, ClaimLine
from claims import makeClaim, netFee
from db import engine
app = FastAPI()
SQLModel.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post("/claim")
def create_claim(claim: ClaimInput) :
    print("posting a claim")
    # claim_with_id = makeClaim(claim.lines, engine)
    fee = netFee(claim.lines)
    claim.netFee = fee
    newId = 0
    with Session(engine) as session:
        validated_claim = Claim.model_validate(claim)
        session.add(validated_claim)
        session.commit()
        session.refresh(validated_claim)
        newId = validated_claim.id
        for l in claim.lines:
            l.claimId = validated_claim.id
            validated_line = ClaimLine.model_validate(l)
            session.add(validated_line)
            session.commit()
            session.refresh(validated_line)
    return {"new id": newId}

@app.get("/provider_npis")
async def provider_npis():
    return {"message": "not implemented"}