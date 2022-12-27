# Commodity Metadata
commodity_create = """
## ✅ Permissions Required: 5
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 201              | Created          | Brand Created Returns Brand                      |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""

commodity_get_all = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description          | Reason                                           |
| ---------------- | ---------------------| -------------------------------------------------|
| 200              | Commodity Retrieved  | Successful                                       |
| 401              | Unauthorized         | Not Logged In                                    |
| 403              | Forbidden            | Insufficient Permissions                         |
| 404              | Not Found            | Search Parameters Produced No Results            |
| 409              | Conflict             | Conflict With Database: Description Returned     |
| 422              | Validation Error     | Invalid/Missing Parameters: Description Returned |
"""

commodity_get_one = """
## ✅ Permissions Required: 1
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 200              | Commodity Retrieved  | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters Description           |
"""

commodity_update = """
## ✅ Permissions Required: 5
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 200              | Commodity Updated    | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""

commodity_delete = """
## ✅ Permissions Required: 7 Admin Only
## ✅ Deleting Brands Is Generally Discouraged. Deletions Cascade To All Releated Objects
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | --------------------| -------------------------------------------------|
| 204              | Commodity Deleted    | Successful                                       |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Search Parameters Produced No Results            |
| 409              | Conflict            | Conflict With Database: Description Returned     |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""
