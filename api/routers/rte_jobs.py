from fastapi import status, Depends, APIRouter, Response
from sqlalchemy.dialects.postgresql import insert
from ..validators import val_auth, val_jobs
from ..oauth2.oauth2 import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..models import mdl_users
from .metadata import md_jobs
from loguru import logger
from typing import List
import re


router = APIRouter(prefix="/jobs")


@router.post("/users", status_code=status.HTTP_202_ACCEPTED, description=md_jobs.job_user_update, tags=['User Jobs'])
@logger.catch()
def user_job_add_update_delete(jobs: List[val_jobs.UserJobsUpdate], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):
    # Delete Is From Function In Database That Delete All Rows Where skap = 0
    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        item_list = []
        for item in jobs:
            item = item.dict()
            item['created_by'] = current_user.id
            item['updated_by'] = current_user.id
            item_list.append(item)

        data = insert(mdl_users.BridgeJobsBrewing).values(item_list)
        data = data.on_conflict_do_update(constraint="bridge_jobs_brewing_pkey", set_={"skap": data.excluded.skap, "updated_by": data.excluded.updated_by})
        data = data.returning(mdl_users.BridgeJobsBrewing)
        data = db.scalars(data)
        db.commit()
        data = data.all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/users", response_model=List[val_jobs.BridgeUserJobsGet], description=md_jobs.job_user_view_list, tags=['User Jobs'])
@logger.catch()
def user_job_view_list(db: Session = Depends(get_db), eid: str = "", job: str = "", limit: int = 50, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_users.BridgeJobsBrewing).join(
            mdl_users.Users, mdl_users.Users.id == mdl_users.BridgeJobsBrewing.id_user).join(
                mdl_users.JobsBrewing, mdl_users.JobsBrewing.id == mdl_users.BridgeJobsBrewing.id_jobs_brewing).filter(
                    mdl_users.Users.eid.ilike(f"%{eid}%"),
                    mdl_users.JobsBrewing.name_job.ilike(f"%{job}%")
                ).order_by(mdl_users.JobsBrewing.job_order, mdl_users.Users.name_first).limit(limit).all()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/users/{id}", response_model=List[val_jobs.UserJobsUpdateList], description=md_jobs.job_user_update_list, tags=['User Jobs'])
@logger.catch()
def user_job_update_list(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    if id == 1:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = db.execute("""
        SELECT COALESCE(use.id, :val) AS id_user, job.id AS id_jobs_brewing, (SELECT CONCAT(name_first, ' ', name_last) FROM users WHERE id = :val) AS name_first, job.name_job, COALESCE(brg.skap, 0) AS skap
        FROM users AS use
        FULL OUTER JOIN bridge_jobs_brewing AS brg ON brg.id_user = use.id
        FULL OUTER JOIN jobs_brewing AS job ON job.id = brg.id_jobs_brewing
        WHERE (use.id = :val OR use.id IS NULL) AND NOT job.id IS NULL
        ORDER BY job.job_order;
        """, {'val': id}).fetchall()

        if data[0].name_first == None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/order", status_code=status.HTTP_202_ACCEPTED, description=md_jobs.order_update, tags=['Jobs'])
@logger.catch()
def job_order_update(jobs: List[val_jobs.JobsOrderUpdateList], db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        item_list = []
        order_list = []
        for item in jobs:
            item = item.dict()
            item['created_by'] = current_user.id
            item['updated_by'] = current_user.id
            item_list.append(item)

        if len(order_list) > len(set(order_list)):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': "duplicate numbers in order list"})

        data = insert(mdl_users.JobsBrewing).values(item_list)
        data = data.on_conflict_do_update(constraint="jobs_brewing_name_job_key", set_={"job_order": data.excluded.job_order, "updated_by": data.excluded.updated_by})
        data = data.returning(mdl_users.JobsBrewing)
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


@router.get("/order", response_model=List[val_jobs.JobsOrderUpdateList], description=md_jobs.order_list, tags=['Jobs'])
@logger.catch()
def job_order_update_list(db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.execute("""
        SELECT name_job, name_area, job_order
        FROM jobs_brewing
        WHERE is_active = TRUE
        ORDER BY job_order, id
        """).fetchall()

        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return data

    except SQLAlchemyError as error:
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_jobs.JobsGet, description=md_jobs.create, tags=['Jobs'])
@logger.catch()
def jobs_create(job: val_jobs.JobCreate, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        is_job = db.query(mdl_users.JobsBrewing).filter(mdl_users.JobsBrewing.name_job == job.name_job).first()

        if is_job:
            return Response(status_code=status.HTTP_409_CONFLICT)

        data = mdl_users.JobsBrewing(created_by=current_user.id, updated_by=current_user.id, **job.dict())
        db.add(data)
        db.commit()
        db.refresh(data)

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


@router.get("", response_model=List[val_jobs.JobsGet], description=md_jobs.get_all, tags=['Jobs'])
@logger.catch()
def jobs_get_all(db: Session = Depends(get_db), active: bool = True, current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_users.JobsBrewing).filter(mdl_users.JobsBrewing.is_active == active).order_by(mdl_users.JobsBrewing.name_job).all()

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


@router.get("/{id}", response_model=val_jobs.JobsGet, description=md_jobs.get_one, tags=['Jobs'])
@logger.catch()
def jobs_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        data = db.query(mdl_users.JobsBrewing).filter(mdl_users.JobsBrewing.id == id).first()

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


@router.put("/{id}", response_model=val_jobs.JobsGet, description=md_jobs.update, tags=['Jobs'])
@logger.catch()
def jobs_update(job: val_jobs.JobsUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_users.JobsBrewing).filter(mdl_users.JobsBrewing.id == id)
        is_job = query.first()

        if not is_job:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        new_dict = job.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        data = query.first()

        return data

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description=md_jobs.delete, tags=['Jobs'])
@logger.catch()
def jobs_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        query = db.query(mdl_users.JobsBrewing).filter(mdl_users.JobsBrewing.id == id)
        is_job = query.first()

        if not is_job:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        query.delete(synchronize_session=False)
        db.commit()

        return

    except SQLAlchemyError as error:
        logger.error(f'{error}')
        error = re.sub('[\n"\s+]', " ", ''.join(error.orig.args))
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': error})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
