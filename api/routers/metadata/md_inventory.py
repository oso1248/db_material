# Dates Metadata
inv_dates_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Optional Path Search
#### Return Schema: InvDatesGet
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 200              | Dates Retrieved  | Brand Created Returns Brand                      |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 409              | Conflict         | Conflict With Database: Description Returned     |
"""

# Material Metadata
inv_material_create = """
## ✅ Permissions Required: 3
## ✅ Takes A LIST Objects
## ✅ Returns A LIST IDs Of Created
* **
#### Ingest Schema: InvMaterialCreate
#### Return Schema: List
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


inv_material_add = """
## ✅ Permissions Required: 3
* **
#### Ingest Schema: Path uuid, Body InvMaterialCreate
#### Return Schema: InvMaterialGet
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


inv_material_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: InvRetrieve
#### Return Schema: InvMaterialGet
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


inv_material_get_one = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Path id
#### Return Schema: InvMaterialGet
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


inv_material_update = """
## ✅ Permissions Required: 3
* **
#### Ingest Schema: Path id, Body InvMaterialUpdate
#### Return Schema: InvMaterialGet
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


inv_material_delete_all = """
## ✅ Permissions Required: 5
## ✅ Deleting Entries Is Generally Discouraged.
## ✅ THIS DELETES THE ENTIRE INVENTORY AND CANNOT BE UNDONE.
## ✅ All Entries Self DELETE After 3 Years.\
* **
#### Ingest Schema: InvRetrieve
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


inv_material_delete = """
## ✅ Permissions Required: 5
## ✅ Deleting Entries Is Generally Discouraged.
## ✅ All Entries Self DELETE After 3 Years.
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


# Hop Metadata
inv_hop_create = """
## ✅ Permissions Required: 2
## ✅ Takes A LIST Objects
## ✅ Returns A LIST IDs Of Created
* **
#### Ingest Schema: InvHopCreate
#### Return Schema: List
**The below table defines the HTTP Status codes that this API may return**

| Status Code      | Description      | Reason                                           |
| ---------------- | -----------------| -------------------------------------------------|
| 201              | Created          | Created Returns List                             |
| 401              | Unauthorized     | Not Logged In                                    |
| 403              | Forbidden        | Insufficient Permissions                         |
| 404              | Not Found        | Insert Produced No Results                       |
| 409              | Conflict         | Conflict With Database: Description Returned     |
| 422              | Validation Error | Invalid/Missing Parameters: Description Returned |
"""

inv_hop_add = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: Path uuid, Body InvHopCreate
#### Return Schema: InvHopGet
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


inv_hop_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: InvRetrieve
#### Return Schema: InvHopGet
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


inv_hop_get_one = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Path id
#### Return Schema: InvHopGet
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


inv_hop_update = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: Path id, Body InvHopUpdate
#### Return Schema: InvHopGet
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


inv_hop_delete_all = """
## ✅ Permissions Required: 4
## ✅ Deleting Entries Is Generally Discouraged.
## ✅ THIS DELETES THE ENTIRE INVENTORY AND CANNOT BE UNDONE.
## ✅ All Entries Self DELETE After 3 Years.
* **
#### Ingest Schema: InvRetrieve
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


inv_hop_delete = """
## ✅ Permissions Required: 2
## ✅ Deleting Entries Is Generally Discouraged.
## ✅ All Entries Self DELETE After 3 Years.
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


# Last Brews Metadata
inv_last_brews_create = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: InvLastBrewsCreate
#### Return Schema: InvLastBrewsGet
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


inv_last_brews_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Optional Path Search
#### Return Schema: InvLastBrewsGet
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


inv_last_brews_get_one = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Path id
#### Return Schema: InvLastBrewsGet
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


inv_last_brews_update = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: Path id, Body InvLastBrewsUpdate
#### Return Schema: InvLastBrewsGet
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


inv_last_brews_delete = """
## ✅ Permissions Required: 4
## ✅ Deleting Entries Is Generally Discouraged.
## ✅ All Entries Self DELETE After 3 Years.
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


# Hibernate Metadata
inv_hibernate_create = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: InvHibernateCreate
#### Return Schema: InvHibernateGet
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


inv_hibernate_get_all = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Optional Path Search
#### Return Schema: InvHibernateGet
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


inv_hibernate_get_one = """
## ✅ Permissions Required: 1
* **
#### Ingest Schema: Path id
#### Return Schema: InvHibernateGet
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


inv_hibernate_update = """
## ✅ Permissions Required: 2
* **
#### Ingest Schema: Path id, Body InvHibernateUpdate
#### Return Schema: InvHibernateGet
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


inv_hibernate_delete = """
## ✅ Permissions Required: 4
## ✅ Deleting Entries Is Generally Discouraged.
## ✅ All Entries Self DELETE After 3 Years.
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
