from sqlalchemy.ext.declarative import declarative_base
from api.oauth2.oauth2 import create_access_token
from fastapi.testclient import TestClient
from api.database.database import get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from alembic.config import Config
from api.models import mdl_users
from api.config import settings
from alembic import command
from api.main import app
import pytest


TEST_SQLALCHEMY_DATABASE_URL = f"""postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"""


alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option('sqlalchemy.url', str(TEST_SQLALCHEMY_DATABASE_URL))


engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@pytest.fixture(scope='function')
def session():
    # command.downgrade(alembic_cfg, "base")
    # command.upgrade(alembic_cfg, "head")
    mdl_users.Base.metadata.drop_all(bind=engine)
    mdl_users.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # command.downgrade(alembic_cfg, "base")
        db.close()


@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


def token(user_creds):
    jwt_token = create_access_token({'id': user_creds['id'], 'eid': user_creds['eid'], 'name': user_creds['name_first'], 'permissions': user_creds['permissions'], "is_active": user_creds['is_active']})
    return jwt_token


@pytest.fixture(scope='function')
def create_users(session):
    session.execute("""
    INSERT INTO users (eid, name_first, name_last, is_active, permissions, password, created_by, updated_by)
    VALUES ('aa00000', 'Admin', 'Admin', True, 7, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1, 1),
           ('em00000', 'Maria', 'Kowlchuck', TRUE, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1,1),
           ('er00000', 'Rachel', 'Hinkel', TRUE, 2, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1,1),
           ('el00000', 'Liz', 'Zaseck', TRUE, 3, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1,1),
           ('ee00000', 'Elizabeth', 'Davis', TRUE, 4, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1,1),
           ('ej00000', 'Jaymie', 'Castro', TRUE, 5, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1,1),
           ('ef00000', 'Morgan', 'Folino', TRUE, 6, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e', 1,1)
    """)
    session.commit()

    return


@pytest.fixture(scope='function')
def create_brand_brewing(session):
    session.execute("DELETE FROM brand_brewing")
    session.commit()
    session.execute("""
    INSERT INTO brand_brewing (name_brand, is_active, is_organic, is_dryhop, is_addition, created_by, updated_by)
    VALUES ('BH40', TRUE, FALSE, FALSE, FALSE, 1,1), ('BH50', TRUE, FALSE, FALSE, FALSE, 1,1),
           ('GI40', TRUE, FALSE, TRUE, TRUE, 1,1), ('MU40', TRUE, TRUE, FALSE, FALSE, 1,1),
           ('BL40', TRUE, FALSE, FALSE, TRUE, 1,1), ('ML35', TRUE, FALSE, FALSE, FALSE, 1,1)
    """)
    session.commit()

    return


@pytest.fixture(scope='function')
def create_brand_finishing(session, create_brand_brewing):
    session.execute("DELETE FROM brand_finishing")
    session.commit()
    session.execute("""
    INSERT INTO brand_finishing (id_brand_brewing, name_brand, is_preinjection, is_postinjection, created_by, updated_by)
    VALUES ((SELECT id FROM brand_brewing WHERE name_brand = 'BH40'), 'HBBL', FALSE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'BH40'), 'LBBL', FALSE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'BH50'), 'HBUD', FALSE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'BH50'), 'LBUD', FALSE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'GI40'), '9IPA', FALSE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'MU40'), 'MUAM', FALSE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'BL40'), 'BLHP', FALSE, TRUE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'ML35'), 'EBAB', TRUE, FALSE, 1, 1),
           ((SELECT id FROM brand_brewing WHERE name_brand = 'ML35'), 'LBAB', TRUE, FALSE, 1, 1)
    """)
    session.commit()

    return


@pytest.fixture(scope='function')
def create_brand_packaging(session, create_brand_finishing):
    session.execute("DELETE FROM brand_packaging")
    session.commit()
    session.execute("""
    INSERT INTO brand_packaging (id_brand_finishing, name_brand, created_by, updated_by)
    VALUES ((SELECT id FROM brand_finishing WHERE name_brand = 'HBBL'), 'BDL5', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'LBBL'), 'BDL4', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'HBUD'), 'BUD5', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'LBUD'), 'BUD4', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = '9IPA'), 'GPX9', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'MUAM'), 'MAX4', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'BLHP'), 'BLL5', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'EBAB'), 'MAB6', 1, 1),
           ((SELECT id FROM brand_finishing WHERE name_brand = 'LBAB'), 'MAB4', 1, 1)
    """)
    session.commit()

    return


@pytest.fixture(scope='function')
def create_suppliers(session):
    session.execute("DELETE FROM suppliers")
    session.commit()
    session.execute("""
    INSERT INTO suppliers (name_supplier, name_contact, email, phone, is_active, created_by, updated_by)
    VALUES ('Budweiser', 'Morgan Folino', 'mf@abi.com', '(303) 654-5432', TRUE, 1, 1),
           ('Briess', 'Abby Sarnoski', 'as@abi.com', '(303) 654-2345', TRUE, 1, 1)
    """)
    session.commit()

    return


@pytest.fixture(scope='function')
def create_commodities(session, create_suppliers):
    session.execute("DELETE FROM commodity")
    session.commit()
    session.execute("""
    INSERT INTO commodity (id_supplier, name_local, name_bit, name_common, inventory, type, sap, unit_of_measurement, per_unit, per_pallet, created_by, updated_by)
    VALUES ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Hop 1', 'Bit Hop 1', 'Common Hop 1', 'Brw', 'Hop', '00000001', 'lb', 44, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Hop 2', 'Bit Hop 2', 'Common Hop 2', 'Brw', 'Hop', '00000002', 'lb', 44, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Hop 3', 'Bit Hop 3', 'Common Hop 3', 'Brw', 'Hop', '00000003', 'lb', 44, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Hop 4', 'Bit Hop 1', 'Common Hop 1', 'Brw', 'Hop', '00000001', 'lb', 44, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Hop 5', 'Bit Hop 2', 'Common Hop 2', 'Brw', 'Hop', '00000002', 'lb', 44, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Hop 6', 'Bit Hop 3', 'Common Hop 3', 'Brw', 'Hop', '00000003', 'lb', 44, 25, 1, 1),

           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Add 1', 'Bit Add 1', 'Common Add 1', 'Brw', 'Addition', '00000004', 'lb', 2000, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Add 2', 'Bit Add 2', 'Common Add 2', 'Brw', 'Addition', '00000005', 'lb', 1500, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Add 3', 'Bit Add 3', 'Common Add 3', 'Brw', 'Addition', '00000006', 'lb', 800, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Add 4', 'Bit Add 1', 'Common Add 1', 'Brw', 'Addition', '00000004', 'lb', 1100, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Add 5', 'Bit Add 2', 'Common Add 2', 'Brw', 'Addition', '00000005', 'lb', 1000, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Budweiser'), 'Local Add 6', 'Bit Add 3', 'Common Add 3', 'Brw', 'Addition', '00000006', 'lb', 500, 1, 1, 1),

           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Injection 1', 'Bit Injection 1', 'Common Injection 1', 'Fin', 'Injection', '00000007', 'gal', 220, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Injection 2', 'Bit Injection 2', 'Common Injection 2', 'Fin', 'Injection', '00000008', 'gal', 220, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Injection 3', 'Bit Injection 3', 'Common Injection 3', 'Fin', 'Injection', '00000009', 'gal', 220, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Injection 4', 'Bit Injection 1', 'Common Injection 1', 'Fin', 'Injection', '00000007', 'gal', 220, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Injection 5', 'Bit Injection 2', 'Common Injection 2', 'Fin', 'Injection', '00000008', 'gal', 220, 1, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Injection 6', 'Bit Injection 3', 'Common Injection 3', 'Fin', 'Injection', '00000009', 'gal', 220, 1, 1, 1),

           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Chemical 1', 'Bit Chemical 1', 'Common Chemical 1', 'Fin', 'Chemical', '00000010', 'gal', 55, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Chemical 2', 'Bit Chemical 2', 'Common Chemical 2', 'Fin', 'Chemical', '00000011', 'gal', 55, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Chemical 3', 'Bit Chemical 3', 'Common Chemical 3', 'Fin', 'Chemical', '00000012', 'gal', 55, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Chemical 4', 'Bit Chemical 1', 'Common Chemical 1', 'Fin', 'Chemical', '00000010', 'gal', 55, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Chemical 5', 'Bit Chemical 2', 'Common Chemical 2', 'Fin', 'Chemical', '00000011', 'gal', 55, 25, 1, 1),
           ((SELECT id FROM suppliers WHERE name_supplier = 'Briess'), 'Local Chemical 6', 'Bit Chemical 3', 'Common Chemical 3', 'Fin', 'Chemical', '00000012', 'gal', 55, 25, 1, 1)
    """)
    session.commit()

    return


@pytest.fixture(scope='function')
def user_lvl_admin(client):
    user_creds = {"id": 1, "eid": "aa00000", "name_first": "Admin", "name_last": "Admin", "is_active": True, "permissions": 7, "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_1(client, session):
    data = session.execute("""SELECT id, eid, name_first, name_last, is_active, permissions FROM users WHERE eid = 'em00000' """).all()
    user_creds = {"id": data[0][0], "eid": data[0][1], "name_first": data[0][2], "name_last": data[0][3], "is_active": data[0][4], "permissions": data[0][5], "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_2(client, session):
    data = session.execute("""SELECT id, eid, name_first, name_last, is_active, permissions FROM users WHERE eid = 'er00000' """).all()
    user_creds = {"id": data[0][0], "eid": data[0][1], "name_first": data[0][2], "name_last": data[0][3], "is_active": data[0][4], "permissions": data[0][5], "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_3(client, session):
    data = session.execute("""SELECT id, eid, name_first, name_last, is_active, permissions FROM users WHERE eid = 'el00000' """).all()
    user_creds = {"id": data[0][0], "eid": data[0][1], "name_first": data[0][2], "name_last": data[0][3], "is_active": data[0][4], "permissions": data[0][5], "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_4(client, session):
    data = session.execute("""SELECT id, eid, name_first, name_last, is_active, permissions FROM users WHERE eid = 'ee00000' """).all()
    user_creds = {"id": data[0][0], "eid": data[0][1], "name_first": data[0][2], "name_last": data[0][3], "is_active": data[0][4], "permissions": data[0][5], "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_5(client, session):
    data = session.execute("""SELECT id, eid, name_first, name_last, is_active, permissions FROM users WHERE eid = 'ej00000' """).all()
    user_creds = {"id": data[0][0], "eid": data[0][1], "name_first": data[0][2], "name_last": data[0][3], "is_active": data[0][4], "permissions": data[0][5], "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_6(client, session):
    data = session.execute("""SELECT id, eid, name_first, name_last, is_active, permissions FROM users WHERE eid = 'ef00000' """).all()
    user_creds = {"id": data[0][0], "eid": data[0][1], "name_first": data[0][2], "name_last": data[0][3], "is_active": data[0][4], "permissions": data[0][5], "password": "BudFort1!"}
    jwt = token(user_creds)
    user_creds['jwt'] = jwt

    return user_creds


@pytest.fixture(scope='function')
def user_lvl_not_logged(client, session):
    user_creds = {"id": 99, "eid": "not logged", "name_first": "not logged", "name_last": "not logged", "is_active": False, "permissions": 0, "password": "BudFort1!"}
    user_creds['jwt'] = "not logged"

    return user_creds


# DON NOT USE BELOW IF USING create_users #############################################################################
def base_lvl_admin(client):  # DO NOT USE IN TESTS
    user_creds = {"id": 1, "eid": "aa00000", "name_first": "Admin", "name_last": "Admin", "is_active": True, "permissions": 7, "password": "BudFort1!"}
    jwt = token(user_creds)
    client.headers = {**client.headers, "Authorization": f"Bearer {jwt}"}
    user_creds['headers'] = client

    return user_creds


@pytest.fixture(scope='function')
def create_lvl_1(client, base_lvl_admin):
    user_creds = {"eid": "em00000", "name_first": "Maria", "name_last": "Kowlchuk", "is_active": True, "permissions": 1, "password": "BudFort1!"}
    res = base_lvl_admin['headers'].post("/users", json=user_creds)
    new_user = res.json()
    new_user['password'] = user_creds['password']

    return new_user


@pytest.fixture(scope='function')
def create_lvl_2(client, base_lvl_admin):
    user_creds = {"eid": "er00000", "name_first": "Rachel", "name_last": "Hinkel", "is_active": True, "permissions": 2, "password": "BudFort1!"}
    res = base_lvl_admin['headers'].post("/users", json=user_creds)
    new_user = res.json()
    new_user['password'] = user_creds['password']

    return new_user


@pytest.fixture(scope='function')
def create_lvl_3(client, base_lvl_admin):
    user_creds = {"eid": "el00000", "name_first": "Liz", "name_last": "Zaseck", "is_active": True, "permissions": 3, "password": "BudFort1!"}
    res = base_lvl_admin['headers'].post("/users", json=user_creds)
    new_user = res.json()
    new_user['password'] = user_creds['password']

    return new_user


@pytest.fixture(scope='function')
def create_lvl_4(client, base_lvl_admin):
    user_creds = {"eid": "ee00000", "name_first": "Elizabeth", "name_last": "Davis", "is_active": True, "permissions": 4, "password": "BudFort1!"}
    res = base_lvl_admin['headers'].post("/users", json=user_creds)
    new_user = res.json()
    new_user['password'] = user_creds['password']

    return new_user


@pytest.fixture(scope='function')
def create_lvl_5(client, base_lvl_admin):
    user_creds = {"eid": "ej00000", "name_first": "Jaymie", "name_last": "Castro", "is_active": True, "permissions": 5, "password": "BudFort1!"}
    res = base_lvl_admin['headers'].post("/users", json=user_creds)
    new_user = res.json()
    new_user['password'] = user_creds['password']

    return new_user


@pytest.fixture(scope='function')
def create_lvl_6(client, base_lvl_admin):
    user_creds = {"eid": "ef00000", "name_first": "Morgan", "name_last": "Folino", "is_active": True, "permissions": 6, "password": "BudFort1!"}
    res = base_lvl_admin['headers'].post("/users", json=user_creds)
    new_user = res.json()
    new_user['password'] = user_creds['password']

    return new_user
