from ..models.mdl_inventory import InventoryUUID
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
