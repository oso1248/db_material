import pytest
import pendulum as ptime


@pytest.fixture(scope='function')
def create_inventory_dates(session):
    tz = ptime.timezone('America/Denver')
    date_start_of_week = ptime.now(tz).date().start_of("week")
    date_start_of_month = ptime.now(tz).date().start_of("month")

    session.execute(f"""INSERT INTO inventory_uuid (inventory_date, created_by, updated_by) VALUES ('{date_start_of_month}', 1, 1), ('{date_start_of_week}', 1, 1);""")
    session.commit()

    return


@pytest.fixture(scope='function')
def create_inventory_material(session, create_inventory_dates):
    data_dates = session.execute("""SELECT inventory_date, uuid FROM inventory_uuid ORDER BY inventory_date DESC """).all()
    data_commodity = session.execute("""SELECT id FROM commodity ORDER BY id """).all()

    values_string = str()
    for item in data_commodity:
        values_string = values_string + f"('{data_dates[0][1]}', {item[0]}, 10, 100, 1, 1), "

    values_string = values_string[:-2]

    session.execute(f"""INSERT INTO inventory_material (uuid, id_commodity, final_count, final_total, created_by, updated_by) VALUES {values_string}""")
    session.commit()

    data_inventory = session.execute(f"""SELECT * FROM inventory_material WHERE uuid = '{data_dates[0][1]}' ORDER BY id """).all()

    return {"uuid": data_dates, "inv": data_inventory}
