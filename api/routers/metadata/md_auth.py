user_login = """
## ✅ Login Via From Data
## ✅ JWT Bearer Token Required For All API Requests
## ✅ Returns Invalid Credentials For All Incorrect Login Attempts
* **
#### Ingest Schema: OAuth2PasswordRequestForm
#### Return Schema: JWT
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 200              | JWT Returned     | Successful                                      |
| 403              | Forbidden        | Invalid Credentials                             |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""

reset = """
## ✅ Permissions Required: 5
## ✅ Sends Email Using YaGmail, A Gmail Client
* **
#### Ingest Schema: Path id, Body ResetEmail
#### Return Schema: ResetPassword
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 205              | Password Reset   | Successful                                      |
| 403              | Forbidden        | Invalid Credentials                             |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""


change = """
## ✅ Change Via From Data
## ✅ Returns Invalid Credentials For All Incorrect Credentials
## ✅ Use‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‎‎ *client_secret*‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ‎‎‎‎‎In Form Data To Send New Password
* **
#### Ingest Schema: OAuth2PasswordRequestForm
#### Return Schema: None
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description        | Reason                                          |
| ---------------- | -------------------| ------------------------------------------------|
| 200              | Posts Retrieved    | Successful                                      |
| 403              | Forbidden          | Invalid Credentials                             |
| 417              | Expectation Failed | Invalid New Password                            |
| 422              | Validation Error   | Invalid/Missing Parameters Description          |
"""
