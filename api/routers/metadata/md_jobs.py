create = """
## ✅ Permissions Required: 5
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 201              | Created          | Job Created Returns Brand                        |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""


order_update = """
## ✅ Permissions Required: 5
## ✅ Consumes A LIST Objects
## ✅ Returns A LIST IDs Of Created Updated Or Deleted
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 202              | Accepted         | List Has Been Added Updated Or Deleted           |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Produced No Results                              |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""


order_list = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 200              | Success          | List Returned                                    |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Produced No Results                              |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""


get_all = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description          | Reason                                           |
| ---------------- | ---------------------| -------------------------------------------------|
| 200              | Job Retrieved        | Successful                                       |
| 401              | Unauthorized         | Not Logged In                                    |
| 403              | Forbidden            | Insufficient Permissions                         |
| 404              | Not Found            | Search Parameters Produced No Results            |
| 409              | Conflict             | Conflict With Database: Description Returned     |
| 422              | Validation Error     | Invalid/Missing Parameters: Description Returned |
"""

get_one = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 200              | Job Retrieved       | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters Description           |
"""

update = """
## ✅ Permissions Required: 5
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 200              | Job Updated         | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""

delete = """
## ✅ Permissions Required: 7 Admin Only
## ✅ Deleting Brands Is Generally Discouraged. Deletions Cascade To All Releated Objects
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 204              | Job Deleted         | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""
