from unittest import TestCase
from .claims import netFee
from .models import Claim, ClaimLine


claims1= {
  "lines": [
     ClaimLine()
  ]
}

class Test(TestCase):
    def test_net_fee(self):
        fees = netFee(claims1["lines"])
        assert fees == 10
        self.fail()
