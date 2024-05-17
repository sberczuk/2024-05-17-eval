from fastapi import FastAPI

from app_models import Claim
from claims import makeClaim

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post("/claim")
def create_claim(claim: Claim) -> Claim:
    print("posting a claim")
    claim_with_id = makeClaim(claim.lines)
    return claim_with_id

@app.get("/provider_npis")
async def provider_npis():
    return {"message": "not implemented"}