# OLX Parser
## Description
The OLX Parser is a Python script that uses a selenium package to parse Price, Floor, Superficiality, Locality,
and overall Square from the real estate advertisement pages and write all
data in a new Google sheet


## Usage
* Set the EMAIL_ADDRESS variable to email you want to get access to google sheet.

* You also need to provide credentials.json file which contain your Google service accounts key 
here is an example of it:
```json
    {
  "type": "service_account",
  "project_id": "radiant-psyche-375512",
  "private_key_id": "794d9f****23c204253537b2178**9d3af9a1428b",
  "private_key": "-----BEGIN PRIVATE KEY---END PRIVATE KEY-----\n",
  "client_email": "***-****3@radiant-psyche-375512.iam.gserviceaccount.com",
  "client_id": "113069594847815442518",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-task3%40radiant-psyche-375512.iam.gserviceaccount.com"
}

```
