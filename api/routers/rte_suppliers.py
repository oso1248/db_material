from fastapi import status, Depends, APIRouter, Response
from ..validators import val_auth, val_suppliers
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..models import mdl_suppliers
from .metadata import md_suppliers
from loguru import logger
from typing import List
import re


router = APIRouter(prefix="/suppliers", tags=['Suppliers'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_suppliers.SupplierGet, description=md_suppliers.suppliers_create)
@logger.catch()
def supplier_create(supplier: val_suppliers.SupplierCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_suppliers.Suppliers(created_by=current_user.id, updated_by=current_user.id, **supplier.dict())
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
        print(error)
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", response_model=List[val_suppliers.SupplierGet], description=md_suppliers.suppliers_get_all)
@logger.catch()
def supplier_get_all(db: Session = Depends(get_db), active: bool = True, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})
    try:
        data = db.query(mdl_suppliers.Suppliers).filter(mdl_suppliers.Suppliers.is_active == active).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id}", response_model=val_suppliers.SupplierGet, description=md_suppliers.suppliers_get_one)
@logger.catch()
def supplier_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_suppliers.Suppliers).filter(mdl_suppliers.Suppliers.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{id}", response_model=val_suppliers.SupplierGet, description=md_suppliers.suppliers_update)
@logger.catch()
def supplier_update(supplier: val_suppliers.SupplierUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_suppliers.Suppliers).filter(mdl_suppliers.Suppliers.id == id)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_suppliers.suppliers_delete)
@logger.catch()
def supplier_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_suppliers.Suppliers).filter(mdl_suppliers.Suppliers.id == id)
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
