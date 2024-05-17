import datetime
import numbers
from typing import List

from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field


# service date,"submitted procedure",quadrant,"Plan/Group #",Subscriber#,"Provider NPI","provider fees","Allowed fees","member coinsurance","member copay"

# Use synthetic keys for claim for now; it's not clear what a Natural Key might be
# Also I deferred handling the date as a Date since we don't need it. That shouid be fixed
class ClaimLine(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    claimId: int | None = Field(default=None, foreign_key="claim.id")
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
        if not v.startswith("D"):
            raise ValueError('must start with D')
        return v

    @field_validator('providerNPI')
    @classmethod
    def provider_npi_len(cls, v: str) -> str:
        if not len(v) == 10:
            raise ValueError('NPI must be 10 digits long')
        return v


class ClaimInput(BaseModel):
    id: int | None = None
    netFee: float | None = None
    providerNPI: str | None = None
    lines: List[ClaimLine]


class Claim(SQLModel, table=True):
    id: int | None  = Field(default=None, primary_key=True)
    netFee: float | None = None
    providerNPI: str

