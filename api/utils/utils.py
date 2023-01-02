from passlib.context import CryptContext
from pydantic.types import UUID4
import random
import string
import re


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).capitalize(), s)


def uppercase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).upper(), s)


def lowercase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).lower(), s)


def convert_phone_number(phone):
    return re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', phone)


def strip_non_numeric(num):
    return re.sub('[^0-9]', '', num)


def strip_non_alphanumeric(num):
    return re.sub('[^A-Za-z0-9]', '', num)


def convert_brew_number(brew):
    return re.sub(r'([A-Z\d]{4})(\d{5})', r'\1 \2', brew)


def convert_skalar_list(list, id: int, uuid: UUID4 = None):
    item_list = []
    for item in list:
        item = item.dict()
        item['created_by'] = id
        item['updated_by'] = id
        if uuid:
            item['uuid'] = uuid
        item_list.append(item)

    return item_list


def get_random_password():
    random_source = string.ascii_letters + string.digits # + string.punctuation
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # select 1 special symbol
    # password += random.choice(string.punctuation)

    # generate other characters
    for i in range(6):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password
