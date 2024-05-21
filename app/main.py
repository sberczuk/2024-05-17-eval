from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy import func
from sqlmodel import SQLModel, Session, select, desc
from starlette.responses import PlainTextResponse

from app.models import ClaimInput, Claim, ClaimLine, ProviderFees
from app.claims import netFee

from app.db import engine

app = FastAPI()
SQLModel.metadata.create_all(engine)




@app.get("/")
async def root():
    return {"message": "Hello Claims Processor User"}


# We need a way to deal with duplicate subnmissions.
# one approach would be to figure out what a Natural Key for a claim line is
# (Maybe Date, service type, NPI?) and return 201 if it's a duplicate
# Ideally we can manage the data flow to avoid inconsistencies.
# We want the claim saving (each line) to be in one transaction, so if this fails (except for the duplicate case)
# the caller can retry.

# I'm not clear on how this service interacts with Payments...

# To handle multiple instances, we'd want any caching handleed by a shared service (redsis or memcached?)


@app.post("/claim")
def create_claim(claim: ClaimInput):
    fee = netFee(claim.lines)
    provider: str = ""
    if len(claim.lines) > 0:
        provider = claim.lines[0].providerNPI
    claim.netFee = fee
    if claim.providerNPI is None:
        claim.providerNPI = provider
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
    return {"id": newId, "netFee": fee}


# We might also want endpoints to support the following:
# Recent Payment Amounts
# Payments by NPI

@app.get("/provider_npis")
async def provider_npis():
    by_fees = get_top_ten_npi_by_fees()
    return {'result': by_fees}


def get_top_ten_npi_by_fees():
    ## Not completed but this is what I'd do:
    ## Add a call  to a caching service. The service would also get updated when a new claim comes in
    # if the service had no data, execute the query and update it, either  by local math or re-running the query
    res = []
    with Session(engine) as session:
        statement = select(Claim.providerNPI, func.sum(Claim.netFee).label('fee')).group_by(Claim.providerNPI).order_by(
            desc('fee')).limit(10)

        result = session.exec(statement)
        for row in result:
            res.append({'npi': row[0], 'fees': row[1]})
    return {"data": res}
