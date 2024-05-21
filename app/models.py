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
    submittedProcedure: str = Field(default=None, description="Procedure id")
    quadrant: str | None
    planId: str
    subscriberId: str = Field(default=None, description='subscriber id"')
    providerNPI: str = Field(min_length=10, max_length=10, default=None, description='NPI"')
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

    # @field_validator('providerNPI')
    # @classmethod
    # def provider_npi_len(cls, v: str) -> str:
    #     if not len(v) == 10:
    #         raise ValueError('NPI must be 10 digits long')
    #     return v


# I'm  not sure why I can't share a model here, but it's probably not a bad thing to separate the
# HTTP from the persistence layer
# This doc implies that they can be reused: https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/
# but I don't get the web side validation for a nested model
class ClaimLineInput(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    claimId: int | None = Field(default=None, foreign_key="claim.id")
    date: str
    submittedProcedure: str = Field(default=None, description="Procedure id")
    quadrant: str | None
    planId: str
    subscriberId: str = Field(default=None, description='subscriber id"')
    providerNPI: str = Field(min_length=10, max_length=10, default=None, description='NPI"')
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

    # @field_validator('providerNPI')
    # @classmethod
    # def provider_npi_len(cls, v: str) -> str:
    #     if not len(v) == 10:
    #         raise ValueError('NPI must be 10 digits long')
    #     return v



class ClaimInput(BaseModel):
    id: int | None = None
    netFee: float | None = None
    providerNPI: str | None = None
    lines: List[ClaimLineInput] = Field(description="Line items for a claim", min_items=2)


class Claim(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    netFee: float | None = None
    providerNPI: str


class ProviderFees(BaseModel):
    npi: str
    netFee: float
