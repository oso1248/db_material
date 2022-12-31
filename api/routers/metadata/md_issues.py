create = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: Path assignee, Body IssuesCreate
#### Return Schema: IssuesCreateGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 201              | Created          | Created Returns Entry                            |
| 206              | Partial Content  | Assignee Missing Or Incorrect                    |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""

get = """
## ✅ Permissions Required: 1
## ✅ Returns Prior 3 Months Of Issues
* **
#### Ingest Schema: Optional Path Search
#### Return Schema: IssuesCreateGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description         | Reason                                           |
| ---------------- | -----------------   | -------------------------------------------------|
| 200              | Entry Retrieved     | Success                                          |
| 401              | Unauthorized        | Not Logged In                                    |
| 403              | Forbidden           | Insufficient Permissions                         |
| 404              | Not Found           | Insert Produced No Results                       |
| 422              | Validation Error    | Invalid/Missing Parameters: Description Returned |
"""
