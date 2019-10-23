import re

import requests

# requests - https://realpython.com/python-requests/
res = requests.post("http://www.api.com", json={"param": "value"})
data = res.json()

# oauth Client
# response is a dictionary with HTTP headers and status code (response["status")
# data is a byte array
response, data = client.request("http://www.seznam.cz")
assert response["status"] == 200
print(data)

# regex
pattern = r'(\d+),-'
test_string = '123,-'
result = re.match(pattern, test_string)
print(result.group(1))
