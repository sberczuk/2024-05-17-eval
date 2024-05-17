from fastapi import FastAPI
from sqlmodel import SQLModel, Session

from app.models import ClaimInput, Claim, ClaimLine
from app.claims import netFee

from app.db import engine
from app.npi_service import get_top_ten_npi_by_fees

app = FastAPI()
SQLModel.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello Claims Processor User"}




@app.post("/claim")
def create_claim(claim: ClaimInput) :
    print("posting a claim")
    fee = netFee(claim.lines)
    provider: str = ""
    if len(claim.lines) > 0:
        provider = claim.lines[0].providerNPI
    claim.netFee = fee
    if claim.providerNPI is None:
        claim.providerNPI = provider
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
    get_top_ten_npi_by_fees()
    return {"message": "not implemented"}