from fastapi import status, Depends, APIRouter, Response, Query
from ..validators import val_auth, val_commodity
from ratelimit import limits, sleep_and_retry
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..models import mdl_commodity
from .metadata import md_commodity
from typing import List
from loguru import logger
import re


LIMIT_SECONDS = 10
LIMIT_CALLS = 20


router = APIRouter(prefix="/commodity", tags=['Commodity'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_commodity.CommodityGet, description=md_commodity.commodity_create)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def commodity_create(commodity: val_commodity.CommodityCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_commodity.Commodity(created_by=current_user.id, updated_by=current_user.id, **commodity.dict())
        db.add(data)
        db.commit()
        db.refresh(data)
        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", response_model=List[val_commodity.CommodityGet], description=md_commodity.commodity_get_all)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def commodity_get_all(db: Session = Depends(get_db), active: bool = True, type: str = Query("", enum=['Hop', 'Addition', 'Injection', 'Chemical']), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})
    try:
        data = db.query(mdl_commodity.Commodity).order_by(mdl_commodity.Commodity.name_local).filter(mdl_commodity.Commodity.is_active == active, mdl_commodity.Commodity.type.ilike(f"%{type}%")).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id}", response_model=val_commodity.CommodityGet, description=md_commodity.commodity_get_one)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def commodity_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_commodity.Commodity).filter(mdl_commodity.Commodity.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{id}", response_model=val_commodity.CommodityGet, description=md_commodity.commodity_update)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def commodity_update(supplier: val_commodity.CommodityUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_commodity.Commodity).filter(mdl_commodity.Commodity.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = supplier.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        data = query.first()

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_commodity.commodity_delete)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
def commodity_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_commodity.Commodity).filter(mdl_commodity.Commodity.id == id)
        does_exist = data.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        data.delete(synchronize_session=False)
        db.commit()

        return

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
