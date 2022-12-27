user_login = """
## ✅ Returns JSON Web Token
* *JWT Bearer Token Required For All API Requests*
## ✅ Returns Invalid Credentials For
* *Incorrect Username*
* *Incorrect Password*
* *User Not Found*<br><br>

**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 200              | Posts Retrieved  | Successful                                      |
| 403              | Forbidden        | Invalid Credentials                             |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""


# User Metadata
user_create = """
## ✅ Permissions Required: 6
## ✅ Users Created Default To Permissions Level 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 201              | Created          | User Created Returns User                       |
| 401              | Unauthorized     | Not Logged In                                   |
| 403              | Forbidden        | Insufficient Permissions                        |
| 404              | Not Found        | Insert Produced No Results                      |
| 409              | Confiict         | User EID Already Exists                         |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""

user_get_all = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 200              | Users Retrieved  | Successful                                      |
| 401              | Unauthorized     | Not Logged In                                   |
| 403              | Forbidden        | Insufficient Permissions                        |
| 404              | Not Found        | Search Parameters Produced No Results           |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""

user_get_one = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 200              | User Retrieved   | Successful                                      |
| 401              | Unauthorized     | Not Logged In                                   |
| 403              | Forbidden        | Insufficient Permissions                        |
| 404              | Not Found        | Search Parameters Produced No Results           |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""

user_update = """
## ✅ Permissions Required: 6
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                          |
| ---------------- | -----------------| ------------------------------------------------|
| 200              | User Updated     | Successful                                      |
| 401              | Unauthorized     | Not Logged In                                   |
| 403              | Forbidden        | Insufficient Permissions                        |
| 404              | Not Found        | Search Parameters Produced No Results           |
| 422              | Validation Error | Invalid/Missing Parameters Description          |
"""

user_delete = """
## ✅ Permissions Required: Admin Only
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 204              | User Deleted     | Successful                                       |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Search Parameters Produced No Results            |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""
