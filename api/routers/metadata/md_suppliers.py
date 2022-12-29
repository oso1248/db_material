# Suppliers Metadata
suppliers_create = """
## ✅ Permissions Required: 5
* **
#### Ingest Schema: SupplierCreate
#### Return Schema: SupplierGet
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

suppliers_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Optional Path Search
#### Return Schema: SupplierGet
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

suppliers_get_one = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Path id
#### Return Schema: SupplierGet
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

suppliers_update = """
## ✅ Permissions Required: 4
* **
#### Ingest Schema: Path id, Body SupplierUpdate
#### Return Schema: SupplierGet
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

suppliers_delete = """
## ✅ Permissions Required: 7 Admin Only
## ✅ Deleting Suppliers Is Generally Discouraged. Deletions Cascade To All Releated Objects
# ✅ *Change All Commodities To A New Supplier Before Deleting A Supplier*
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
