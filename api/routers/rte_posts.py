from .md import post_create, post_get_all, post_get_one, post_update, post_delete
from fastapi import status, Depends, APIRouter, Response
from ..oauth2.oauth2 import get_current_user
from ..validators import val_posts, val_auth
from ..database.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import mdl_post
from sqlalchemy import func
from loguru import logger


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_posts.PostReturn, description=post_create)
@logger.catch()
def post_create(post: val_posts.PostCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = mdl_post.Post(created_by=current_user.id, **post.dict())
        db.add(data)
        db.commit()
        db.refresh(data)
        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", response_model=List[val_posts.PostGet], description=post_get_all)
@logger.catch()
def posts_get_all(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "", current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = db.query(mdl_post.Post, func.count(mdl_post.Votes.id_post).label("votes")).join(mdl_post.Votes, mdl_post.Votes.id_post == mdl_post.Post.id, isouter=True).group_by(mdl_post.Post.id).filter(mdl_post.Post.title.ilike(f"%{search}%")).order_by(mdl_post.Post.id.asc()).limit(limit).offset(skip).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id}", response_model=val_posts.PostGet, description=post_get_one)
@logger.catch()
def posts_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = db.query(mdl_post.Post, func.count(mdl_post.Votes.id_post).label("votes")).join(mdl_post.Votes, mdl_post.Votes.id_post == mdl_post.Post.id, isouter=True).filter(mdl_post.Post.id == id).group_by(mdl_post.Post.id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{id}", response_model=val_posts.PostReturn, description=post_update)
@logger.catch()
def posts_update(post: val_posts.PostUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = db.query(mdl_post.Post).filter(mdl_post.Post.id == id)
        does_exist = data.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        if does_exist.created_by != current_user.id:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        data.update(post.dict(), synchronize_session=False)
        db.commit()

        return data.first()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description=post_delete)
@logger.catch()
def posts_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = db.query(mdl_post.Post).filter(mdl_post.Post.id == id)
        does_exist = data.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        if does_exist.created_by != current_user.id:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        data.delete(synchronize_session=False)
        db.commit()

        return

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
