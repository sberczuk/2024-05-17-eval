import csv
import re
from typing import List
import json


# Utility to parse the sample input CSV and generate a JSON file



def parser( fileName: str):
    claims :List = []

    with open(fileName, newline='') as csvfile:

        # assume that the CSV file is always in the same order. If this wasn't true we could read the first row,
        # normalize the headers (casing, spacing) and pass the result to the dictReader
        reader = csv.DictReader(csvfile, fieldnames=['date', 'submittedProcedure', 'quadrant', 'planId', 'subscriberId', 'providerNPI', 'providerFees', 'allowedFees', 'coInsurance', 'memberCoPay'])
        # skip header row
        next(reader)
        for row in reader:

            # handle currency values. This isn't ideal as we want a decimal but we can improve this later
            for key in ['providerFees', 'allowedFees', 'coInsurance', 'memberCoPay']:
                row[key] = currency_to_value(row[key])
            claims.append(row)

    return claims



# TODO: Convert the date into a parseable format.

# Convert the value to a float to serialize in JSON. CHeck for decimals elsewhere
def currency_to_value(currency_string: str) -> float:
    leaned_string = re.sub(r'[^\d.]', '', currency_string)
    return float(leaned_string)

# generate the sample JSON Data File
if __name__ == '__main__':
    lines = parser("claim_1234.csv")
    claim:dict = {'lines': lines}


    # write the JSON File
    dumps = json.dumps(claim)
    with open("claims.json", "w") as jsonFile:
        jsonFile.write(dumps)

    print(dumps)