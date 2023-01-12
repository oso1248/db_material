from ..validators.regex.regex_users import regex_users_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response
from ..utils.utils_email import reset_password_email
from ratelimit import limits, sleep_and_retry
from ..utils.utils import get_random_password
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from .. database.database import get_db
from sqlalchemy.orm import Session
from .. validators import val_auth
from .. models import mdl_users
from .metadata import md_auth
from .. oauth2 import oauth2
from .. utils import utils
from loguru import logger


LIMIT_SECONDS = 20
LIMIT_CALLS = 5


router = APIRouter(prefix="/login", tags=['Authentication'])


@router.post('', response_model=val_auth.Token, description=md_auth.user_login)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    try:
        user = db.query(mdl_users.Users).filter(mdl_users.Users.eid == user_credentials.username.lower()).first()

        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

        if not user.is_active:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

        if not utils.verify(user_credentials.password, user.password):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

        access_token = oauth2.create_access_token(
            data={'id': user.id, 'eid': user.eid, 'name': user.name_first, 'permissions': user.permissions, "is_active": user.is_active})

        return {'access_token': access_token, 'token_type': 'bearer'}

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/reset/{id}', status_code=status.HTTP_205_RESET_CONTENT, response_model=val_auth.ResetPassword, description=md_auth.reset)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def reset_password(id: int, email: val_auth.ResetEmail, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    if id == 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        query = db.query(mdl_users.Users).filter(mdl_users.Users.id == id)
        user = query.first()

        if not user:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        temporary_password = get_random_password()
        temporary_password_hashed = utils.hash_password(temporary_password)

        new_dict = {'password': temporary_password_hashed, 'updated_by': current_user.id}
        query.update(new_dict, synchronize_session=False)
        db.commit()

        if email.email:
            is_email = reset_password_email(str(temporary_password), email.email)
        else:
            is_email = False

        return {"temporary_password": temporary_password, 'email': is_email}

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/change', status_code=status.HTTP_205_RESET_CONTENT, description=md_auth.change)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def change_password(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    try:
        query = db.query(mdl_users.Users).filter(mdl_users.Users.eid == user_credentials.username.lower())
        user = query.first()

        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

        if not user.is_active:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

        if not utils.verify(user_credentials.password, user.password):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

        if not user_credentials.client_secret:
            return JSONResponse(status_code=status.HTTP_417_EXPECTATION_FAILED, content={'detail': 'invalid new password'})

        is_valid_password = regex_users_password.fullmatch(user_credentials.client_secret)
        if not is_valid_password:
            return JSONResponse(status_code=status.HTTP_417_EXPECTATION_FAILED, content={'detail': 'invalid new password'})

        password_hashed = utils.hash_password(user_credentials.client_secret)

        new_dict = {'password': password_hashed}
        query.update(new_dict, synchronize_session=False)
        db.commit()

        return

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
