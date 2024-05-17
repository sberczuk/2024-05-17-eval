from typing import List

from sqlalchemy import func
from sqlmodel import select, Session

from .main import engine
from .models import Claim


def get_top_ten_npi_by_fees()->List[str]:

    with Session(engine) as session:
        statement = select(Claim)
        result = session.exec(statement)
        for row in result:
            print(row)
    return list()



# What I wanted to do was a select with a group by.. I need to learn the syntax better,,
#  with Session(engine) as session:
#         statement = select([Claim.providerNPI, func.sum(Claim.netFee)]).group_by(Claim.providerNPI).order_by(func.sum(Claim.netFee).limit(10))
#         result = session.exec(statement)
#         for row in result:
#             print(row)