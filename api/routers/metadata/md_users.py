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
| 200              | Posts Retrieved  | Successful                                      |
| 403              | Forbidden        | Invalid Credentials                             |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""


# User Metadata
user_create = """
## ✅ Permissions Required: 5
## ✅ Users Created Default To Permissions Level 1
* **
#### Ingest Schema: UsersCreate
#### Return Schema: UsersGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 201              | Created          | Created Returns Entry                            |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""

user_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Optional Path Search
#### Return Schema: UsersGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | -----------------   | -------------------------------------------------|
| 200              | Entry Retrieved     | Success                                          |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Insert Produced No Results                       |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""

user_get_one = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Path id
#### Return Schema: UsersGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | -----------------   | -------------------------------------------------|
| 200              | Entry Retrieved     | Success                                          |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Insert Produced No Results                       |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""

user_update = """
## ✅ Permissions Required: 5
* **
#### Ingest Schema: Path id, Body: UsersUpdate
#### Return Schema: UsersGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 200              | Entry Updated    | Updated Returns Entry                            |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""

user_delete = """
## ✅ Permissions Required: 7 Admin Only
## ✅ Deleting Users Is Generally Discouraged. Deletions Cascade To All Releated Objects
* **
#### Ingest Schema: Path id
#### Return Schema: None
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 204              | Entry Deleted       | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""
