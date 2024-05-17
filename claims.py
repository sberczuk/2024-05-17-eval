from typing import List

from app_models import Claim
from app_models import ClaimLine
import uuid

def makeClaim(claimLines:List[ClaimLine]) -> Claim:
    new_uuid = str(uuid.uuid4())
    fee = netFee(claimLines)
    return Claim(id=new_uuid, lines=claimLines, netFee=fee)


def netFee(claimLines: List[ClaimLine]):
    fee = 0
    for l in claimLines:
        fee = fee + l.providerFees + l.coInsurance + l.memberCoPay-l.allowedFees
    return fee
