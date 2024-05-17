import datetime
import numbers
from typing import List

from pydantic import BaseModel, field_validator


# service date,"submitted procedure",quadrant,"Plan/Group #",Subscriber#,"Provider NPI","provider fees","Allowed fees","member coinsurance","member copay"
class ClaimLine(BaseModel):
    date: str
    submittedProcedure: str
    quadrant: str | None
    planId: str
    subscriberId: str
    providerNPI: str
    providerFees: float
    allowedFees: float
    coInsurance: float
    memberCoPay: float

    @field_validator('submittedProcedure')
    @classmethod
    def name_must_start_with(cls, v: str) -> str:
        if not v.startswith("D") :
            raise ValueError('must start with D')
        return v

    @field_validator('providerNPI')
    @classmethod
    def provider_npi_len(cls, v: str) -> str:
        if not len(v) == 10:
            raise ValueError('NPI must be 10 digits long')
        return v


class Claim(BaseModel):
    id: str | None = None
    netFee: float | None = None
    lines: List[ClaimLine]
