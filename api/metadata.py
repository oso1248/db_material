description = """
### Auth
| Route            | Description    | Required Permissions                           |
| ---------------- | ---------------| -----------------------------------------------|
| Login            | Login          | Permissions: 1   Edit Current User Users Only  |

### Users
| Route            | Description    | Required Permissions                           |
| ---------------- | ---------------| -----------------------------------------------|
| Users Get All    | Get All Users  | Permissions: 1                                 |
| Users Create     | Create Post    | Permissions: 1                                 |
| Users Get One    | Get Post By ID | Permissions: 1                                 |
| Users Update     | Update a post  | Permissions: 1   Edit Current User Users Only  |
| Users Delete     | Delete a post  | Permissions: 1   Delete Current User Users Only|

### Posts
| Route            | Description    | Required Permissions                           |
| ---------------- | ---------------| -----------------------------------------------|
| Posts Get All    | Get All Posts  | Permissions: 1                                 |
| Posts Create     | Create Post    | Permissions: 1                                 |
| Posts Get One    | Get Post By ID | Permissions: 1                                 |
| Posts Update     | Update a post  | Permissions: 1   Edit Current User Posts Only  |
| Posts Delete     | Delete a post  | Permissions: 1   Delete Current User Posts Only|


"""


tags_metadata = [
    {"name": "Auth", "description": "Authentication Endpoints", "externalDocs": {"description": "¿Would You Like To Know More?", "url": "https://www.google.com"}},
    {"name": "Users", "description": "Users Endpoints", "externalDocs": {"description": "¿Would You Like To Know More?", "url": "https://www.google.com"}},
    {"name": "Posts", "description": "Posts Endpoints", "externalDocs": {"description": "¿Would You Like To Know More?", "url": "https://www.google.com"}},
    {"name": "Votes", "description": "Votes Endpoints", "externalDocs": {"description": "¿Would You Like To Know More?", "url": "https://www.google.com"}},
]


title_metadata = "Model baseAPI (͡• ͜ʖ ͡•) 》🇺🇲"
version_metadata = "0.0.1"
terms_metadata = "https://www.google.com"
contact_metadata = {"name": "Adam Coulson", "url": "https://github.com/oso1248/budAPI", "email": "oso1248@gmail.com"}
licence_metadata = {"name": "MIT License Copyright (c) 2022 Adam Coulson", "url": "https://github.com/oso1248/budAPI/blob/master/LICENSE"}
ui_metadata = {"syntaxHighlight": False}


# ##### Options:
# * **Get All Posts**
# * **Create Post**
# **The below table defines the HTTP Status codes that this API may return**