from api.utils.utils import get_random_password
import pendulum as ptime
import random
import pytest


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


@pytest.fixture(scope='function')
def create_last_brews(session, create_inventory_dates):
    data_dates = session.execute("""SELECT inventory_date, uuid FROM inventory_uuid ORDER BY inventory_date DESC """).all()

    session.execute(f"""INSERT INTO inventory_last_brews (uuid, bh_1, bh_2, created_by, updated_by) VALUES ('{data_dates[0][1]}', 'BH40 10001', 'BH50 20001', 1, 1)""")
    session.commit()

    data = session.execute("""SELECT id, uuid, bh_1, bh_2 FROM inventory_last_brews ORDER BY id ASC """).all()

    return data[0]


@pytest.fixture(scope='function')
def create_inventory_hop(session, create_inventory_dates, create_last_brews):
    # data_dates = session.execute("""SELECT inventory_date, uuid FROM inventory_uuid ORDER BY inventory_date DESC """).all()
    data_commodity = session.execute("""SELECT id FROM commodity WHERE type = 'Hop' ORDER BY id """).all()

    values_string = str()
    for item in data_commodity:
        values_string = values_string + f"('{create_last_brews[1]}', {item[0]}, 10, 100, 1000, '{get_random_password()}', {random.choice([True, False])}, 1, 1), "

    values_string = values_string[:-2]

    session.execute(f"""INSERT INTO inventory_hop (uuid, id_commodity, final_boxes, final_pounds, final_total, lot_number, is_current, created_by, updated_by) VALUES {values_string}""")
    session.commit()

    data_inventory = session.execute(f"""SELECT * FROM inventory_hop WHERE uuid = '{create_last_brews[1]}' ORDER BY id """).all()

    return {"last_brews": create_last_brews, "inv": data_inventory}


@pytest.fixture(scope='function')
def create_function_hibernate(session):
    session.execute("""
    CREATE OR REPLACE FUNCTION update_is_complete_inventory_hibernate() RETURNS TRIGGER
    LANGUAGE plpgsql
    AS
    $$
    BEGIN
    IF NEW.tank_final IS NOT NULL AND NEW.tank_final_level IS NOT NULL THEN NEW.is_complete = TRUE;
    END IF;
    RETURN NEW;
    END;
    $$;
    """)
    session.execute("""
    CREATE TRIGGER update_is_complete_inventory_hibernate
    BEFORE UPDATE
    ON inventory_hibernate
    FOR EACH ROW
    EXECUTE PROCEDURE update_is_complete_inventory_hibernate();
    """)

    return


@pytest.fixture(scope='function')
def create_inventory_hibernate(session, create_brand_brewing, create_inventory_dates, create_function_hibernate):
    data_dates = session.execute("""SELECT inventory_date, uuid FROM inventory_uuid ORDER BY inventory_date DESC """).all()
    data_brands = session.execute("""SELECT id, name_brand FROM brand_brewing ORDER By id""").all()

    session.execute(f"""INSERT INTO inventory_hibernate (uuid, id_brand_brewing, tank_origin, tank_origin_level, tank_storage, tank_storage_level, tank_storage_og, tank_storage_abw, tank_storage_o2, tank_final, tank_final_level, is_complete, created_by, updated_by)
    VALUES
    ('{data_dates[0][1]}', {data_brands[0][0]}, 2013, 2500, 2043, 2500, 11.00, 7.62, 10, NULL, NULL, FALSE, 1, 1),
    ('{data_dates[0][1]}', {data_brands[2][0]}, 2025, 2500, 2050, 2500, 11.00, 7.62, 10, NULL, NULL, FALSE, 1, 1),
    ('{data_dates[0][1]}', {data_brands[3][0]}, 7237, 2500, 3102, 2500, 11.00, 7.62, 10, NULL, NULL, FALSE, 1, 1),

    ('{data_dates[0][1]}', {data_brands[0][0]}, 2013, 2500, 2043, 2500, 11.00, 7.62, 10, 7239, 2500, TRUE, 1, 1),
    ('{data_dates[0][1]}', {data_brands[2][0]}, 2025, 2500, 2050, 2500, 11.00, 7.62, 10, 7233, 2500, TRUE, 1, 1),
    ('{data_dates[0][1]}', {data_brands[3][0]}, 7237, 2500, 3102, 2500, 11.00, 7.62, 10, 7235, 2500, TRUE, 1, 1)

    """)
    session.commit()

    data_inventory = session.execute("""SELECT * FROM inventory_hibernate ORDER BY id""").all()

    return {"uuid": data_dates, "brands": data_brands, "inv": data_inventory}
