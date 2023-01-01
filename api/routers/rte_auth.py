from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response
from ratelimit import limits, sleep_and_retry
from fastapi.responses import JSONResponse
from .. database.database import get_db
from sqlalchemy.orm import Session
from .. validators import val_auth
from .. models import mdl_users
from .metadata import md_users
from .. oauth2 import oauth2
from .. utils import utils
from loguru import logger


LIMIT_SECONDS = 20
LIMIT_CALLS = 5


router = APIRouter(prefix="/login", tags=['Auth'])


@router.post('', response_model=val_auth.Token, description=md_users.user_login)
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
