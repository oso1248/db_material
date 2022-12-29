# Material Metadata
addition_add_update_delete = """
## ✅ Permissions Required: 5
## ✅ Consumes A LIST Objects
## ✅ Returns A LIST IDs Of Created Updated Or Deleted
* **
#### Injest Schema: BridgeAdditionCreate
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


addition_view_list = """
## ✅ Permissions Required: 1
* **
#### Injest Schema: Optional Path Search
#### Return Schema: BridgeAdditionGet
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


addition_update_list = """
## ✅ Permissions Required: 1
## ✅ Returns A List Used For The Add Update Delete Route
* **
#### Injest Schema: Path brand
#### Return Schema: BridgeAdditionUpdateGet
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


kettle_hop_add_update_delete = """
## ✅ Permissions Required: 5
## ✅ Consumes A LIST Objects
## ✅ Returns A LIST IDs Of Created Updated Or Deleted
* **
#### Injest Schema: BridgeKettleHopCreate
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


kettle_hop_view_list = """
## ✅ Permissions Required: 1
* **
#### Injest Schema: Optional Path Search
#### Return Schema: BridgeKettleHopGet
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


kettle_hop_update_list = """
## ✅ Permissions Required: 1
## ✅ Returns A List Used For The Add Update Delete Route
* **
#### Injest Schema: Path brand
#### Return Schema: BridgeKettleHopUpdateGet
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


dry_hop_add_update_delete = """
## ✅ Permissions Required: 5
## ✅ Consumes A LIST Objects
## ✅ Returns A LIST IDs Of Created Updated Or Deleted
* **
#### Injest Schema: BridgeDryHopCreate
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


dry_hop_view_list = """
## ✅ Permissions Required: 1
* **
#### Injest Schema: Optional Path Search
#### Return Schema: BridgeDryHopGet
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


dry_hop_update_list = """
## ✅ Permissions Required: 1
## ✅ Returns A List Used For The Add Update Delete Route
* **
#### Injest Schema: Path brand
#### Return Schema: BridgeDryHopUpdateGet
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