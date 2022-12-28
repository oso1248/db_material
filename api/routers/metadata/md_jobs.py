job_user_update = """
## ✅ Permissions Required: 5
## ✅ Consumes A LIST Objects
## ✅ Returns A LIST IDs Of Created Updated Or Deleted
#### Injest Schema: UserJobsUpdate
#### Return Schema: List
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


job_user_view_list = """
## ✅ Permissions Required: 5
#### Injest Schema: Optional Path Search
#### Return Schema: BridgeUserJobsGet
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


job_user_update_list = """
## ✅ Permissions Required: 5
#### Injest Schema: Path id
#### Return Schema: UserJobsUpdateList
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


order_update = """
## ✅ Permissions Required: 5
## ✅ Consumes A LIST Objects
## ✅ Returns A LIST IDs Of Created Updated Or Deleted
#### Injest Schema: JobsOrderUpdateList
#### Return Schema: List
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
## ✅ Permissions Required: 5
#### Injest Schema: None
#### Return Schema: JobsOrderUpdateList
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


create = """
## ✅ Permissions Required: 5
#### Injest Schema: JobCreate
#### Return Schema: JobsGet
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


get_all = """
## ✅ Permissions Required: 1
#### Injest Schema: Optional Path Search
#### Return Schema: JobsGet
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
#### Injest Schema: Path id
#### Return Schema: JobsGet
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
#### Injest Schema: Path id, Body JobsUpdate
#### Return Schema: JobsGet
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
## ✅ Permissions Required: 6
## ✅ Deleting Jobs Is Generally Discouraged. Deletions Cascade To All Releated Objects
#### Injest Schema: Path id
#### Return Schema: None
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
