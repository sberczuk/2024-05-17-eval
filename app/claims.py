from typing import List

from sqlmodel import Session

from models import Claim
from models import ClaimLine
import uuid

def makeClaim(claimLines:List[ClaimLine], engine) -> Claim:
    fee = netFee(claimLines)
    c= Claim( netFee=fee)
    with Session(engine) as session:
        validated_claim = Claim.model_validate(c)
        session.add(validated_claim)
        session.commit()
        session.refresh(validated_claim)
        return validated_claim


def netFee(claimLines: List[ClaimLine]):
    fee = 0
    for l in claimLines:
        fee = fee + l.providerFees + l.coInsurance + l.memberCoPay-l.allowedFees
    return fee
