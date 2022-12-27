from fastapi import status, Depends, APIRouter, Response, Query
from ..validators import val_auth, val_inventory
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..utils.utils_uuid import get_uuid
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..models import mdl_commodity
from ..models import mdl_inventory
from .metadata import md_inventory
from pydantic.types import UUID4
from sqlalchemy import insert
from loguru import logger
from typing import List
import re


router = APIRouter(prefix="/inventory")


### Inventory Dates ###
@router.get("/dates", response_model=List[val_inventory.InvDatesGet], description=md_inventory.inv_dates_get_all, tags=['Inventory Dates'])
@logger.catch()
def inventory_dates_get_all(limit: int = 10, skip: int = 0, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryUUID).order_by(mdl_inventory.InventoryUUID.inventory_date.desc()).limit(limit).offset(skip).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Material Inventory ###
@router.post("/material", status_code=status.HTTP_201_CREATED, description=md_inventory.inv_material_create, tags=['Inventory Material'])
@logger.catch()
def inventory_material_create(commodity: List[val_inventory.InvMaterialCreate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 3:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        current_uuid = get_uuid(current_user.id, db)

        item_list = []
        for item in commodity:
            item.created_by = current_user.id
            item.updated_by = current_user.id
            item.uuid = current_uuid
            item_list.append(item.dict())

        data = db.scalars(insert(mdl_inventory.InventoryMaterial).returning(mdl_inventory.InventoryMaterial), item_list)
        db.commit()
        data = data.all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/material/{uuid}", response_model=val_inventory.InvMaterialGet, status_code=status.HTTP_201_CREATED, description=md_inventory.inv_material_add, tags=['Inventory Material'])
@logger.catch()
def inventory_material_add(uuid: UUID4, commodity: val_inventory.InvMaterialCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 3:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_inventory.InventoryMaterial(created_by=current_user.id, updated_by=current_user.id, uuid=uuid, **commodity.dict())
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


@router.get("/material", response_model=List[val_inventory.InvMaterialGet], description=md_inventory.inv_material_get_all, tags=['Inventory Material'])
@logger.catch()
def inventory_material_get_all(uuid: val_inventory.InvRetrieve, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryMaterial).filter(mdl_inventory.InventoryMaterial.uuid == uuid.uuid).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/material/{id}", response_model=val_inventory.InvMaterialGet, description=md_inventory.inv_material_get_all, tags=['Inventory Material'])
@logger.catch()
def inventory_material_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryMaterial).filter(mdl_inventory.InventoryMaterial.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/material/{id}", response_model=val_inventory.InvMaterialGet, description=md_inventory.inv_material_update, tags=['Inventory Material'])
@logger.catch()
def inventory_material_update(id: int, commodity: val_inventory.InvMaterialUpdate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 3:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_inventory.InventoryMaterial).filter(mdl_inventory.InventoryMaterial.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = commodity.dict()
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


@router.delete("/material/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_material_delete, tags=['Inventory Material'])
@logger.catch()
def inventory_material_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryMaterial).filter(mdl_inventory.InventoryMaterial.id == id)
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


@router.delete("/material/delete/all/{uuid}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_material_delete_all, tags=['Inventory Material'])
@logger.catch()
def inventory_material_delete_all(uuid: UUID4, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryMaterial).filter(mdl_inventory.InventoryMaterial.uuid == uuid)
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


### Hop Inventory ###
@router.post("/hop", status_code=status.HTTP_201_CREATED, description=md_inventory.inv_hop_create, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_create(commodity: List[val_inventory.InvHopCreate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        current_uuid = get_uuid(current_user.id, db)

        item_list = []
        for item in commodity:
            item.created_by = current_user.id
            item.updated_by = current_user.id
            item.uuid = current_uuid
            item_list.append(item.dict())

        data = db.scalars(insert(mdl_inventory.InventoryHop).returning(mdl_inventory.InventoryHop), item_list)
        db.commit()
        data = data.all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/hop/{uuid}", response_model=val_inventory.InvHopGet, status_code=status.HTTP_201_CREATED, description=md_inventory.inv_hop_add, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_add(uuid: UUID4, commodity: val_inventory.InvHopCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_inventory.InventoryHop(created_by=current_user.id, updated_by=current_user.id, uuid=uuid, **commodity.dict())
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


@router.get("/hop", response_model=List[val_inventory.InvHopGet], description=md_inventory.inv_hop_get_all, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_get_all(uuid: val_inventory.InvRetrieve, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHop).join(mdl_commodity.Commodity, mdl_inventory.InventoryHop.id_commodity == mdl_commodity.Commodity.id).order_by(mdl_commodity.Commodity.name_local.asc()).filter(mdl_inventory.InventoryHop.uuid == uuid.uuid).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/hop/{id}", response_model=val_inventory.InvHopGet, description=md_inventory.inv_hop_get_one, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHop).filter(mdl_inventory.InventoryHop.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/hop/{id}", response_model=val_inventory.InvHopGet, description=md_inventory.inv_hop_update, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_update(id: int, commodity: val_inventory.InvHopUpdate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 3:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_inventory.InventoryHop).filter(mdl_inventory.InventoryHop.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = commodity.dict()
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


@router.delete("/hop/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_hop_delete, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHop).filter(mdl_inventory.InventoryHop.id == id)
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


@router.delete("/hop/delete/all/{uuid}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_hop_delete_all, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_delete_all(uuid: UUID4, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHop).filter(mdl_inventory.InventoryHop.uuid == uuid)
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


### Last Brews Inventory ###
@router.post("/lastbrews", status_code=status.HTTP_201_CREATED, response_model=val_inventory.InvLastBrewsGet, description=md_inventory.inv_last_brews_create, tags=['Inventory Last Brews'])
@logger.catch()
def inventory_last_brews_create(brews: val_inventory.InvLastBrewsCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        current_uuid = get_uuid(current_user.id, db)

        data = mdl_inventory.InventoryLastBrews(created_by=current_user.id, updated_by=current_user.id, uuid=current_uuid, **brews.dict())
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


@router.get("/lastbrews", response_model=List[val_inventory.InvLastBrewsGet], description=md_inventory.inv_last_brews_get_all, tags=['Inventory Last Brews'])
@logger.catch()
def inventory_last_brews_get_all(limit: int = 10, skip: int = 0, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryLastBrews).join(mdl_inventory.InventoryUUID, mdl_inventory.InventoryLastBrews.uuid == mdl_inventory.InventoryUUID.uuid).order_by(mdl_inventory.InventoryUUID.inventory_date.desc()).limit(limit).offset(skip).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/lastbrews/{id}", response_model=val_inventory.InvLastBrewsGet, description=md_inventory.inv_last_brews_get_one, tags=['Inventory Last Brews'])
@logger.catch()
def inventory_last_brews_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryLastBrews).filter(mdl_inventory.InventoryLastBrews.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/lastbrews/{id}", response_model=val_inventory.InvLastBrewsGet, description=md_inventory.inv_last_brews_update, tags=['Inventory Last Brews'])
@logger.catch()
def inventory_last_brews_update(id: int, brews: val_inventory.InvLastBrewsUpdate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_inventory.InventoryLastBrews).filter(mdl_inventory.InventoryLastBrews.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = brews.dict()
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


@router.delete("/lastbrews/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_last_brews_delete, tags=['Inventory Last Brews'])
@logger.catch()
def inventory_last_brews_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryLastBrews).filter(mdl_inventory.InventoryLastBrews.id == id)
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


### Hibernate Inventory ###
@router.post("/hibernate", status_code=status.HTTP_201_CREATED, response_model=val_inventory.InvHibernateGet, description=md_inventory.inv_hibernate_create, tags=['Inventory Hibernate'])
@logger.catch()
def inventory_hibernate_create(hibernate: val_inventory.InvHibernateCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        current_uuid = get_uuid(current_user.id, db)

        data = mdl_inventory.InventoryHibernate(created_by=current_user.id, updated_by=current_user.id, uuid=current_uuid, **hibernate.dict())
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


@router.get("/hibernate", response_model=List[val_inventory.InvHibernateGet], description=md_inventory.inv_hibernate_get_all, tags=['Inventory Hibernate'])
@logger.catch()
def inventory_hibernate_get_all(limit: int = 30, skip: int = 0, complete: bool = Query(False, enum=[True, False]), db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHibernate).order_by(mdl_inventory.InventoryHibernate.time_created.desc()).filter(mdl_inventory.InventoryHibernate.is_complete == complete).limit(limit).offset(skip).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/hibernate/{id}", response_model=val_inventory.InvHibernateGet, description=md_inventory.inv_hibernate_get_one, tags=['Inventory Hibernate'])
@logger.catch()
def inventory_hibernate_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHibernate).filter(mdl_inventory.InventoryHibernate.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/hibernate/{id}", response_model=val_inventory.InvHibernateGet, description=md_inventory.inv_hibernate_update, tags=['Inventory Hibernate'])
@logger.catch()
def inventory_hibernate_update(id: int, hibernated: val_inventory.InvHibernateUpdate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_inventory.InventoryHibernate).filter(mdl_inventory.InventoryHibernate.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        elif does_exist.is_complete:
            return Response(status_code=status.HTTP_208_ALREADY_REPORTED)

        new_dict = hibernated.dict()
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


@router.delete("/hibernate/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_hibernate_delete, tags=['Inventory Hibernate'])
@logger.catch()
def inventory_hibernate_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryHibernate).filter(mdl_inventory.InventoryHibernate.id == id)
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
