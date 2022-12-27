from fastapi import status, Depends, APIRouter, Response
from ..validators import val_brands, val_auth
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..models import mdl_brands
from .metadata import md_brands
from loguru import logger
from typing import List
import re


router = APIRouter(prefix="/brand")


# Brand Brewing
@router.post("/brewing", status_code=status.HTTP_201_CREATED, response_model=val_brands.BrewingBrandGet, tags=['Brands Brewing'], description=md_brands.brewing_create)
@logger.catch()
def brand_brewing_create(brand: val_brands.BrewingBrandCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_brands.BrandBrewing(created_by=current_user.id, updated_by=current_user.id, **brand.dict())
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


@router.get("/brewing", response_model=List[val_brands.BrewingBrandGet], tags=['Brands Brewing'], description=md_brands.brewing_get_all)
@logger.catch()
def brand_brewing_get_all(db: Session = Depends(get_db), active: bool = True, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})
    try:
        data = db.query(mdl_brands.BrandBrewing).order_by(mdl_brands.BrandBrewing.name_brand.asc()).filter(mdl_brands.BrandBrewing.is_active == active).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/brewing/{id}", response_model=val_brands.BrewingBrandGet, tags=['Brands Brewing'], description=md_brands.brewing_get_one)
@logger.catch()
def brand_brewing_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_brands.BrandBrewing).filter(mdl_brands.BrandBrewing.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/brewing/{id}", response_model=val_brands.BrewingBrandGet, tags=['Brands Brewing'], description=md_brands.brewing_update)
@logger.catch()
def brand_brewing_update(brand: val_brands.BrewingBrandUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_brands.BrandBrewing).filter(mdl_brands.BrandBrewing.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = brand.dict()
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


@router.delete("/brewing/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Brands Brewing'], description=md_brands.brewing_delete)
@logger.catch()
def brand_brewing_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_brands.BrandBrewing).filter(mdl_brands.BrandBrewing.id == id)
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


# Brand Finishing
@router.post("/finishing", status_code=status.HTTP_201_CREATED, response_model=val_brands.FinishingBrandGet, tags=['Brands Finishing'], description=md_brands.finishing_create)
@logger.catch()
def brand_finishing_create(brand: val_brands.FinishingBrandCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_brands.BrandFinishing(created_by=current_user.id, updated_by=current_user.id, **brand.dict())
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


@router.get("/finishing", response_model=List[val_brands.FinishingBrandGet], tags=['Brands Finishing'], description=md_brands.finishing_get_all)
@logger.catch()
def brand_finishing_get_all(db: Session = Depends(get_db), active: bool = True, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})
    try:
        data = db.query(mdl_brands.BrandFinishing).join(mdl_brands.BrandBrewing, mdl_brands.BrandFinishing.id_brand_brewing == mdl_brands.BrandBrewing.id, isouter=False).filter(mdl_brands.BrandBrewing.is_active == active).order_by(mdl_brands.BrandFinishing.name_brand.asc()).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/finishing/{id}", response_model=val_brands.FinishingBrandGet, tags=['Brands Finishing'], description=md_brands.finishing_get_one)
@logger.catch()
def brand_finishing_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_brands.BrandFinishing).filter(mdl_brands.BrandFinishing.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/finishing/{id}", response_model=val_brands.FinishingBrandGet, tags=['Brands Finishing'], description=md_brands.finishing_update)
@logger.catch()
def brand_finishing_update(brand: val_brands.FinishingBrandUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_brands.BrandFinishing).filter(mdl_brands.BrandFinishing.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        data = query.first()

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        print(error)
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/finishing/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Brands Finishing'], description=md_brands.finishing_delete)
@logger.catch()
def brand_finishing_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_brands.BrandFinishing).filter(mdl_brands.BrandFinishing.id == id)
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


# Brand Packaging
@router.post("/packaging", status_code=status.HTTP_201_CREATED, response_model=val_brands.PackagingBrandGet, tags=['Brands Packaging'], description=md_brands.packaging_create)
# @logger.catch()
def brand_packaging_create(brand: val_brands.PackagingBrandCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = mdl_brands.BrandPackaging(created_by=current_user.id, updated_by=current_user.id, **brand.dict())
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


@router.get("/packaging", response_model=List[val_brands.PackagingBrandGet], tags=['Brands Packaging'], description=md_brands.packaging_get_all)
@logger.catch()
def brand_packaging_get_all(db: Session = Depends(get_db), active: bool = True, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})
    try:
        data = db.query(mdl_brands.BrandPackaging).join(mdl_brands.BrandFinishing, mdl_brands.BrandPackaging.id_brand_finishing == mdl_brands.BrandFinishing.id, isouter=False).join(mdl_brands.BrandBrewing, mdl_brands.BrandFinishing.id_brand_brewing == mdl_brands.BrandBrewing.id, isouter=False).filter(mdl_brands.BrandBrewing.is_active == active).order_by(mdl_brands.BrandPackaging.name_brand.asc()).all()

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


@router.get("/packaging/{id}", response_model=val_brands.PackagingBrandGet, tags=['Brands Packaging'], description=md_brands.packaging_get_one)
@logger.catch()
def brand_packaging_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_brands.BrandPackaging).filter(mdl_brands.BrandPackaging.id == id).first()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/packaging/{id}", response_model=val_brands.PackagingBrandGet, tags=['Brands Packaging'], description=md_brands.packaging_update)
@logger.catch()
def brand_packaging_update(brand: val_brands.PackagingBrandUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_brands.BrandPackaging)\
            .filter(mdl_brands.BrandPackaging.id == id)
        does_exist = query.first()

        if not does_exist:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = brand.dict()
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


@router.delete("/packaging/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Brands Packaging'], description=md_brands.packaging_delete)
@logger.catch()
def brand_packaging_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_brands.BrandPackaging).filter(mdl_brands.BrandPackaging.id == id)
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
