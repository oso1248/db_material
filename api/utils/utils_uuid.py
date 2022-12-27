from ..models.mdl_inventory import InventoryUUID, InventoryLastBrews, InventoryHop, InventoryMaterial
from pydantic.types import UUID4
import pendulum as ptime


def get_uuid(id: int, db):

    tz = ptime.timezone('America/Denver')
    date_today = ptime.now(tz).date()
    date_start_of_week = ptime.now(tz).date().start_of("week")
    date_start_of_month = ptime.now(tz).date().start_of("month")

    if date_today == date_start_of_month:
        uuid_date = date_today
    else:
        uuid_date = date_start_of_week

    try:
        query = db.query(InventoryUUID).filter(InventoryUUID.inventory_date == uuid_date).first()

        if query:
            current_uuid = query.uuid
        else:
            data = InventoryUUID(created_by=id, updated_by=id, inventory_date=uuid_date)
            db.add(data)
            db.commit()
            db.refresh(data)
            current_uuid = data.uuid

        return current_uuid

    except Exception as error:
        db.flush()
        db.rollback()
        return error


def check_last_brews(uuid: UUID4, db):
    try:
        data = db.query(InventoryLastBrews).filter(InventoryLastBrews.uuid == uuid).first()

        if data:
            return True
        else:
            return False

    except Exception as error:
        return error


def check_hop_inventory(uuid: UUID4, db):
    try:
        data = db.query(InventoryHop).filter(InventoryHop.uuid == uuid).first()

        if data:
            return True
        else:
            return False

    except Exception as error:
        return error


def check_material_inventory(uuid: UUID4, db):
    try:
        data = db.query(InventoryMaterial).filter(InventoryMaterial.uuid == uuid).first()

        if data:
            return True
        else:
            return False

    except Exception as error:
        return error
