from unittest import TestCase
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

claim1 = {
    "lines": [
        {
            "date": "3/28/18 0:00",
            "submittedProcedure": "D0180",
            "quadrant": "",
            "planId": "GRP-1000",
            "subscriberId": "3730189502",
            "providerNPI": "1497775530",
            "providerFees": 100.0,
            "allowedFees": 99.0,
            "coInsurance": 0.0,
            "memberCoPay": 0.0
        },
        {
            "date": "3/28/18 0:00",
            "submittedProcedure": "D0210",
            "quadrant": "",
            "planId": "GRP-1000",
            "subscriberId": "3730189502",
            "providerNPI": "1497775530",
            "providerFees": 108.0,
            "allowedFees": 107.0,
            "coInsurance": 0.0,
            "memberCoPay": 0.0
        }
    ]
}

invalidProcedure = {
    "lines": [
        {
            "date": "3/28/18 0:00",
            "submittedProcedure": "W0180",
            "quadrant": "",
            "planId": "GRP-1000",
            "subscriberId": "3730189502",
            "providerNPI": "1497775530",
            "providerFees": 100.0,
            "allowedFees": 99.0,
            "coInsurance": 0.0,
            "memberCoPay": 0.0
        },

    ]
}

invalidNPI = {
    "lines": [
        {
            "date": "3/28/18 0:00",
            "submittedProcedure": "W0180",
            "quadrant": "",
            "planId": "GRP-1000",
            "subscriberId": "3730189502",
            "providerNPI": "14",
            "providerFees": 100.0,
            "allowedFees": 99.0,
            "coInsurance": 0.0,
            "memberCoPay": 0.0
        },

    ]
}


class Test(TestCase):
    def test_create_claim(self):
        response = client.post("/claim", json=claim1)
        print(response.status_code)
        assert response.status_code == 200
        json = response.json()
        id = json.get("id")
        assert id != None
        assert id != ""
        assert json.get("netFee") is not None

    def test_create_claim_invalid_provider(self):
        response = client.post("/claim", json=invalidProcedure)
        print(response.status_code)
        assert response.status_code == 422


    def test_create_claim_invalid_npi(self):
        response = client.post("/claim", json=invalidNPI)
        print(response.status_code)
        assert response.status_code == 422

    # def test_provider_npis(self):
    #     self.fail()
