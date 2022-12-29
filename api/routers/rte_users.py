from .metadata import md_users
from fastapi import status, Depends, APIRouter, Response
from ..validators import val_users, val_auth
from ..oauth2.oauth2 import get_current_user
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..models import mdl_users
from ..utils import utils
from loguru import logger
from typing import List


router = APIRouter(prefix="/users", tags=['Users'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_users.UsersGet, description=md_users.user_create)
@logger.catch()
def users_create(user: val_users.UsersCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        is_user = db.query(mdl_users.Users).filter(mdl_users.Users.eid == user.eid).first()
        
        if is_user:
            return Response(status_code=status.HTTP_409_CONFLICT)

        user.password = utils.hash_password(user.password)
        data = mdl_users.Users(created_by=current_user.id, updated_by=current_user.id, **user.dict())
        db.add(data)
        db.commit()
        db.refresh(data)

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", response_model=List[val_users.UsersGet], description=md_users.user_get_all)
@logger.catch()
def users_get_all(db: Session = Depends(get_db), active: bool = True, current_user: val_auth.UserCurrent = Depends(get_current_user)):
    
    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    
    try:
        data = db.query(mdl_users.Users).filter(mdl_users.Users.is_active == active, mdl_users.Users.id != 1).order_by(mdl_users.Users.name_first.asc()).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id}", response_model=val_users.UsersGet, description=md_users.user_get_one)
@logger.catch()
def users_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    if id == 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = db.query(mdl_users.Users).filter(mdl_users.Users.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{id}", response_model=val_users.UsersGet, description=md_users.user_update)
@logger.catch()
def users_update(post: val_users.UsersUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    if id == 1:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        query = db.query(mdl_users.Users).filter(mdl_users.Users.id == id)
        is_user = query.first()

        if not is_user:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        if is_user.id == current_user.id:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        new_dict = post.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        data = query.first()

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_users.user_delete)
@logger.catch()
def users_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 7:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        query = db.query(mdl_users.Users).filter(mdl_users.Users.id == id)
        is_user = query.first()

        if not is_user:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        if is_user.eid == 'aa00000':
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        query.delete(synchronize_session=False)
        db.commit()

        return

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
