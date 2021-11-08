import json, unittest, datetime

with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):

    # updating address
    adrs = jsonObject["location"]
    ll = adrs.split("/")
    # print(ll)
    jsonObject["location"] = {
        "country": ll[0],
        "city": ll[1],
        "area": ll[2],
        "factory": ll[3],
        "section": ll[4],
    }
    status = jsonObject["operationStatus"]
    temp = jsonObject["temp"]
    del jsonObject["operationStatus"]
    del jsonObject["temp"]
    jsonObject["data"] = {"status": status, "temperature": temp}

    return jsonObject


def convertFromFormat2(jsonObject):
    # updating device id and type
    jsonObject["deviceID"] = jsonObject["device"]["id"]
    jsonObject["deviceType"] = jsonObject["device"]["type"]
    del jsonObject["device"]
    # converting human time to timestamp
    time = jsonObject.timestamp
    date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = str((date - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    timestamp = timestamp[:-2]
    jsonObject["timestamp"] = timestamp
    # updating location
    jsonObject["location"] = {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"],
    }
    del jsonObject["country"]
    del jsonObject["city"]
    del jsonObject["area"]
    del jsonObject["factory"]
    del jsonObject["section"]

    return jsonObject


def main(jsonObject):

    result = {}

    if jsonObject.get("device") == None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):
    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):

        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, "Converting from Type 1 failed")

    def test_dataType2(self):

        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, "Converting from Type 2 failed")


if __name__ == "__main__":
    unittest.main()
