from passlib.context import CryptContext
import string
import random

# Fill Out Enviroment Varibles
# Edit below
admin_password = ""
DATABASE_HOST = ""
DATABASE_NAME = ""
DATABASE_PORT = 5432  # Port For Postgres
DATABASE_PASSWORD = ""
DATABASE_USERNAME = ""
SECRET_KEY = ""  # Leave Empty For Random Generated String
ALGORITHM = "HS256"  # Do Not Change Unless Needed
TOKEN_EXPIRE_MINUTES = 5  # Minutes For Timeout Of JWT
# Edit Above


# Do Not Edit Below
if not admin_password or not DATABASE_HOST or not DATABASE_NAME or not DATABASE_PORT or not DATABASE_PASSWORD or not DATABASE_USERNAME or not ALGORITHM or not TOKEN_EXPIRE_MINUTES:
    print("All Varibles Are Not Filled")
    exit()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_context.hash(password)


if not SECRET_KEY:
    str_length = 100
    str_random = ''.join(random.choices(string.ascii_uppercase + string.digits, k=str_length))
    SECRET_KEY = str_random


hashed_password = hash_password(admin_password)
USER_INSERT = f"INSERT INTO users (name, username, role, password, created_by, updated_by, brewery, permissions) VALUES ('Admin', 'admin', 'Admin', '{hashed_password}', 1, 1, 'FTC', 7);"
L = [
    f"SQLALCHEMY_DATABASE_URL=postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}\n",
    f"DATABASE_HOST={DATABASE_HOST}\n",
    f"DATABASE_NAME={DATABASE_NAME}\n",
    f"DATABASE_PORT={DATABASE_PORT}\n",
    f"DATABASE_PASSWORD={DATABASE_PASSWORD}\n",
    f"DATABASE_USERNAME={DATABASE_USERNAME}\n",
    f"JWT_SECRET_KEY={SECRET_KEY}\n",
    f"JWT_ALGORITHM={ALGORITHM}\n",
    f"JWT_ACCESS_TOKEN_EXPIRE_MINUTES={TOKEN_EXPIRE_MINUTES}\n",
    f"USER_INSERT={USER_INSERT}\n"
]


file1 = open("../env.txt", "w+")
file1.writelines(L)
file1.close()
# file1 = open("../envtest.txt", "r+")
# print(file1.read())
# file1.close()
