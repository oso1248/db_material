from ..utils.utils_uuid import get_uuid, check_last_brews, check_hop_inventory, check_material_inventory
from fastapi import status, Depends, APIRouter, Response, Query
from ..models import mdl_commodity, mdl_inventory
from ..validators import val_auth, val_inventory
from ..utils.utils import convert_skalar_list
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..database.database import get_db
from sqlalchemy.orm import Session
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


# Inventory Bit
@router.get("/bit", response_model=List[val_inventory.InvBitGet], description=md_inventory.inv_bit_get, tags=['Inventory Bit'])
@logger.catch()
def inventory_bit_get(uuid: val_inventory.InvRetrieve, inventory: str = Query('%___', enum=['Brw', 'Fin', 'Log']), db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.execute("""
        SELECT inventory, name_bit, sap, SUM(final_total) AS final_total, unit_of_measurement AS uom, inv.inventory_date
        FROM
        (SELECT com.name_bit, com.sap, inv.final_total, com.unit_of_measurement, com.inventory, inv.uuid
        FROM commodity AS com
        INNER JOIN inventory_material AS inv ON inv.id_commodity = com.id
        WHERE inv.uuid = :val
        UNION ALL
        SELECT com.name_bit, com.sap, inv.final_total, com.unit_of_measurement, com.inventory, inv.uuid
        FROM commodity AS com
        INNER JOIN inventory_hop AS inv ON inv.id_commodity = com.id
        WHERE inv.uuid = :val) AS Z
        INNER JOIN inventory_uuid AS inv on inv.uuid = z.uuid
        WHERE inventory ILIKE :inv
        GROUP BY inventory, name_bit, sap, unit_of_measurement, inv.inventory_date
        ORDER BY name_bit;
        """, {'val': uuid.uuid, 'inv': inventory}).fetchall()

        if len(data) == 0:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
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
        is_inventory = check_material_inventory(current_uuid, db)

        if is_inventory:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': "inventory already exists. delete privious inventory first"})

        item_list = convert_skalar_list(commodity, current_user.id, current_uuid)

        data = db.scalars(insert(mdl_inventory.InventoryMaterial).returning(mdl_inventory.InventoryMaterial), item_list)
        db.commit()
        data = data.all()

        if len(data) == 0:
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


@router.get("/material/{id}", response_model=val_inventory.InvMaterialGet, description=md_inventory.inv_material_get_one, tags=['Inventory Material'])
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


@router.delete("/material/delete", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_material_delete_all, tags=['Inventory Material'])
@logger.catch()
def inventory_material_delete_all(uuid: val_inventory.InvRetrieve, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryMaterial).filter(mdl_inventory.InventoryMaterial.uuid == uuid.uuid)
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


### Hop Inventory ###
@router.post("/hop", status_code=status.HTTP_201_CREATED, description=md_inventory.inv_hop_create, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_create(commodity: List[val_inventory.InvHopCreate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        current_uuid: UUID4 = get_uuid(current_user.id, db)
        is_last_brews = check_last_brews(current_uuid, db)
        is_inventory = check_hop_inventory(current_uuid, db)
        
        if not is_last_brews:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': "must add last brews first"})
        elif is_inventory:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': "inventory already exists. delete privious inventory first"})

        item_list = convert_skalar_list(commodity, current_user.id, current_uuid)

        data = db.scalars(insert(mdl_inventory.InventoryHop).returning(mdl_inventory.InventoryHop), item_list)
        db.commit()
        data = data.all()

        if len(data) == 0:
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
        is_last_brews = check_last_brews(uuid, db)

        if not is_last_brews:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': "must add last brews first"})

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


@router.delete("/hop/delete", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_hop_delete_all, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_delete_all(uuid: val_inventory.InvRetrieve, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_inventory.InventoryLastBrews).filter(mdl_inventory.InventoryLastBrews.uuid == uuid.uuid)
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


@router.delete("/hop/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_inventory.inv_hop_delete, tags=['Inventory Hop'])
@logger.catch()
def inventory_hop_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
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


### Last Brews Inventory ###
@router.post("/lastbrews", status_code=status.HTTP_201_CREATED, response_model=val_inventory.InvLastBrewsGet, description=md_inventory.inv_last_brews_create, tags=['Inventory Last Brews'])
@logger.catch()
def inventory_last_brews_create(brews: val_inventory.InvLastBrewsCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        current_uuid = get_uuid(current_user.id, db)
        is_last_brews = check_last_brews(current_uuid, db)

        if is_last_brews:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': "inventory already exists. delete privious inventory first"})

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

    if current_user.permissions < 4:
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

    if current_user.permissions < 4:
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
