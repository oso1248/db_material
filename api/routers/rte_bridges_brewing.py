from fastapi import status, Depends, APIRouter, Response
from ..validators import val_auth, val_bridges_brewing
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..database.database import get_db
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from ..models import mdl_bridges_brewing
from ..models import mdl_brands
from ..models import mdl_commodity
from .metadata import md_bridges_brewing
from loguru import logger
from typing import List
import re


router = APIRouter(prefix="/bridgesbrewing")


### Brewing Additions ###
@router.post("/addition", status_code=status.HTTP_202_ACCEPTED, description=md_bridges_brewing.add_update_delete, tags=['Brewing Addition'])
@logger.catch()
def brewing_addition_add_update_delete(addition: List[val_bridges_brewing.BridgeAdditionCreate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        item_list = []
        for item in addition:
            item.created_by = current_user.id
            item.updated_by = current_user.id
            item_list.append(item.dict())

        data = insert(mdl_bridges_brewing.BridgeAddition).values(item_list)
        data = data.on_conflict_do_update(constraint="bridge_addition_pkey", set_={"per_brew": data.excluded.per_brew, "updated_by": data.excluded.updated_by})
        data = data.returning(mdl_bridges_brewing.BridgeAddition)
        data = db.scalars(data)
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


@router.get("/addition", response_model=List[val_bridges_brewing.BridgeDryHopGet], description=md_bridges_brewing.view_list, tags=['Brewing Addition'])
@logger.catch()
def brewing_addition_view_list(db: Session = Depends(get_db), brand: str = "", commodity: str = "", limit: int = 20, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_bridges_brewing.BridgeAddition).join(
            mdl_brands.BrandBrewing, mdl_brands.BrandBrewing.id == mdl_bridges_brewing.BridgeAddition.id_brand_brewing).join(
            mdl_commodity.Commodity, mdl_commodity.Commodity.id == mdl_bridges_brewing.BridgeAddition.id_commodity).filter(
            mdl_brands.BrandBrewing.name_brand.ilike(f"%{brand}%"),
            mdl_commodity.Commodity.name_local.ilike(f"%{commodity}%")
            ).order_by(mdl_brands.BrandBrewing.name_brand, mdl_commodity.Commodity.name_local).limit(limit).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/addition/{brand}", response_model=List[val_bridges_brewing.BridgeAdditionUpdateGet], description=md_bridges_brewing.update_list, tags=['Brewing Addition'])
@logger.catch()
def brewing_addition_update_list(brand: str, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.execute("""
        SELECT (SELECT id FROM brand_brewing WHERE name_brand = :val) as id_brand_brewing, com.id as id_commodity, COALESCE(brw.name_brand, :val) AS name_brand, com.name_local, brg.per_brew, brg.note
        FROM brand_brewing AS brw
        FULL OUTER JOIN bridge_addition AS brg ON brg.id_brand_brewing = brw.id
        FULL OUTER JOIN commodity AS com ON com.id = brg.id_commodity
        WHERE (brw.name_brand = :val OR NOT com.name_local IS NULL) AND com.type = 'Addition'
        ORDER BY com.name_local
        """, {'val': brand}).fetchall()

        if data[0].id_brand_brewing == None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Brewing Kettle Hop ###
@router.post("/kettlehop", status_code=status.HTTP_202_ACCEPTED, description=md_bridges_brewing.add_update_delete, tags=['Brewing Kettle Hop'])
@logger.catch()
def brewing_kettle_hop_add_update_delete(addition: List[val_bridges_brewing.BridgeKettleHopCreate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        item_list = []
        for item in addition:
            item.created_by = current_user.id
            item.updated_by = current_user.id
            item_list.append(item.dict())

        data = insert(mdl_bridges_brewing.BridgeKettleHop).values(item_list)
        data = data.on_conflict_do_update(constraint="bridge_kettle_hop_pkey", set_={"per_brew": data.excluded.per_brew, "updated_by": data.excluded.updated_by})
        data = data.returning(mdl_bridges_brewing.BridgeKettleHop)
        data = db.scalars(data)
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


@router.get("/kettlehop", response_model=List[val_bridges_brewing.BridgeKettleHopGet], description=md_bridges_brewing.view_list, tags=['Brewing Kettle Hop'])
@logger.catch()
def brewing_kettle_hop_view_list(db: Session = Depends(get_db), brand: str = "", commodity: str = "", limit: int = 20, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_bridges_brewing.BridgeKettleHop).join(
            mdl_brands.BrandBrewing, mdl_brands.BrandBrewing.id == mdl_bridges_brewing.BridgeKettleHop.id_brand_brewing).join(
                mdl_commodity.Commodity, mdl_commodity.Commodity.id == mdl_bridges_brewing.BridgeKettleHop.id_commodity).filter(
                    mdl_brands.BrandBrewing.name_brand.ilike(f"%{brand}%"),
                    mdl_commodity.Commodity.name_local.ilike(f"%{commodity}%")
                ).order_by(mdl_brands.BrandBrewing.name_brand, mdl_commodity.Commodity.name_local).limit(limit).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/kettlehop/{brand}", response_model=List[val_bridges_brewing.BridgeKettleHopUpdateGet], description=md_bridges_brewing.update_list, tags=['Brewing Kettle Hop'])
@logger.catch()
def brewing_addition_update_list(brand: str, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.execute("""
        SELECT (SELECT id FROM brand_brewing WHERE name_brand = :val) as id_brand_brewing, com.id as id_commodity, COALESCE(brw.name_brand, :val) AS name_brand, com.name_local, brg.per_brew, brg.note
        FROM brand_brewing AS brw
        FULL OUTER JOIN bridge_kettle_hop AS brg ON brg.id_brand_brewing = brw.id
        FULL OUTER JOIN commodity AS com ON com.id = brg.id_commodity
        WHERE (brw.name_brand = :val OR NOT com.name_local IS NULL) AND com.type = 'Hop'
        ORDER BY com.name_local
        """, {'val': brand}).fetchall()

        if data[0].id_brand_brewing == None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Brewing Dry Hop ###
@router.post("/dryhop", status_code=status.HTTP_202_ACCEPTED, description=md_bridges_brewing.add_update_delete, tags=['Brewing Dry Hop'])
@logger.catch()
def brewing_dry_hop_add_update_delete(addition: List[val_bridges_brewing.BridgeDryHopCreate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        item_list = []
        for item in addition:
            item.created_by = current_user.id
            item.updated_by = current_user.id
            item_list.append(item.dict())

        data = insert(mdl_bridges_brewing.BridgeDryHop).values(item_list)
        data = data.on_conflict_do_update(constraint="bridge_dry_hop_pkey", set_={"per_brew": data.excluded.per_brew, "updated_by": data.excluded.updated_by})
        data = data.returning(mdl_bridges_brewing.BridgeDryHop)
        data = db.scalars(data)
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


@router.get("/dryhop", response_model=List[val_bridges_brewing.BridgeDryHopGet], description=md_bridges_brewing.view_list, tags=['Brewing Dry Hop'])
@logger.catch()
def brewing_dry_hop_view_list(db: Session = Depends(get_db), brand: str = "", commodity: str = "", limit: int = 20, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_bridges_brewing.BridgeDryHop).join(
            mdl_brands.BrandBrewing, mdl_brands.BrandBrewing.id == mdl_bridges_brewing.BridgeDryHop.id_brand_brewing).join(
                mdl_commodity.Commodity, mdl_commodity.Commodity.id == mdl_bridges_brewing.BridgeDryHop.id_commodity).filter(
                    mdl_brands.BrandBrewing.name_brand.ilike(f"%{brand}%"),
                    mdl_commodity.Commodity.name_local.ilike(f"%{commodity}%")
                ).order_by(mdl_brands.BrandBrewing.name_brand, mdl_commodity.Commodity.name_local).limit(limit).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/dryhop/{brand}", response_model=List[val_bridges_brewing.BridgeDryHopUpdateGet], description=md_bridges_brewing.update_list, tags=['Brewing Dry Hop'])
@logger.catch()
def brewing_dry_hop_update_list(brand: str, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.execute("""
        SELECT (SELECT id FROM brand_brewing WHERE name_brand = :val) as id_brand_brewing, com.id as id_commodity, COALESCE(brw.name_brand, :val) AS name_brand, com.name_local, brg.per_brew, brg.note
        FROM brand_brewing AS brw
        FULL OUTER JOIN bridge_dry_hop AS brg ON brg.id_brand_brewing = brw.id
        FULL OUTER JOIN commodity AS com ON com.id = brg.id_commodity
        WHERE (brw.name_brand = :val OR NOT com.name_local IS NULL) AND com.type = 'Hop'
        ORDER BY com.name_local
        """, {'val': brand}).fetchall()

        if data[0].id_brand_brewing == None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)