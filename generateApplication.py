import json
import requests

# Load json file
application = json.loads(open('applicationInfo.json').read())

# Create subject token
url = "https://localhost:443/v1/auth/tokens"
data = {'name': application["adminUsername"], 'password': application["adminPassword"]}
head = {'Content-Type': 'application/json'}
r = requests.post(url, json=data, headers=head, verify=False)

subjectToken = r.headers['X-Subject-Token']

# Register application in keyrock
url = "https://localhost:443/v1/applications"
payload = json.dumps({
    "application": {
        "name": "Shakeit UI",
        "description": "Interface for controlling ShakeIt component",
        "url": "http://localhost",
        "redirect_uri": "http://localhost/login",
        "redirect_sign_out_uri": "http://localhost/logout",
        "grant_type": [
            "authorization_code",
            "implicit",
            "password"
        ],
        "token_types": [
            "jwt",
            "permanent"
        ]
    }
})
headers = {
    'Content-Type': 'application/json',
    'X-Auth-token': subjectToken
}
response = requests.request("POST", url, headers=headers, data=payload, verify=False)
print(response.text)

# Save application id and secret
application["clientID"] = response.json()['application']['id']
application["clientSecret"] = response.json()['application']['secret']

# Save changed info to json file
json.dump(application, open("applicationInfo.json", "w"))
