import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(host="localhost", database="db_material", user="adamcoulson", password="adamcoulson", cursor_factory=RealDictCursor)
cursor = conn.cursor()

# ******** ONLY RUN WHEN DATABASE IS NEW AND ONLY HAS ADMIN USER ********


def RunIt() -> None:
    cursor.execute("""
    INSERT INTO users (eid, name_first, name_last, permissions, created_by, updated_by, password)
    VALUES
    ('ea00000', 'Abby', 'Sarnoski', 1, 1, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e'),
    ('el00000', 'Lydia', 'Tena', 2, 1, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e'),
    ('eb00000', 'Briana', 'Fosher', 3, 1, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e'),
    ('ee00000', 'Elizabeth', 'Davis', 4, 1, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e'),
    ('er00000', 'Rachel', 'Hinkel', 5, 1, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e'),
    ('em00000', 'Maria', 'Kowalchuk', 6, 1, 1, '$2b$12$UwbBZdUBeMjaPXOipWvEUekAtKx5qFx/cm.lMOkp3q04GQwj17c7e')
    Returning id, name_first;
    """)
    conn.commit()
    data = cursor.fetchall()
    for item in data:
        print("User -- ", item)

    print("----------------------------------------------------------------------")
    cursor.execute("""
    INSERT INTO brand_brewing (name_brand, is_active, is_organic, is_dryhop, is_addition, created_by, updated_by)
    VALUES
    ('BH40', TRUE, FALSE, FALSE, FALSE, 1, 1), ('BH50', TRUE, FALSE, FALSE, FALSE, 1, 1),
    ('MU15', TRUE, FALSE, FALSE, FALSE, 1, 1), ('P160', TRUE, FALSE, FALSE, FALSE, 1, 1),
    ('PL50', TRUE, FALSE, FALSE, FALSE, 1, 1), ('NL50', TRUE, FALSE, FALSE, FALSE, 1, 1),
    ('BR10', TRUE, FALSE, TRUE, TRUE, 1, 1), ('EL20', TRUE, FALSE, TRUE, TRUE, 1, 1)
    Returning id, name_brand;
    """)
    conn.commit()
    data = cursor.fetchall()
    for item in data:
        print("Brewing Brand -- ", item)

    print("----------------------------------------------------------------------")
    cursor.execute("""
    INSERT INTO brand_finishing (id_brand_brewing, name_brand, is_preinjection, is_postinjection, created_by, updated_by)
    VALUES
    (1, 'HBBL', FALSE, FALSE, 1, 1), (1, 'LBBL', FALSE, FALSE, 1, 1),
    (2, 'HBUD', FALSE, FALSE, 1, 1), (2, 'LBUD', FALSE, FALSE, 1, 1),
    (3, 'HBMU', FALSE, FALSE, 1, 1), (4, 'HBP1', FALSE, FALSE, 1, 1),
    (5, 'PDPL', FALSE, FALSE, 1, 1), (6, 'HBNL', FALSE, FALSE, 1, 1),
    (7, 'BRVP', FALSE, TRUE, 1, 1), (8, 'ELSP', FALSE, FALSE, 1, 1)
    RETURNING id, name_brand;
    """)
    conn.commit()
    data = cursor.fetchall()
    for item in data:
        print("Finishing Brand -- ", item)

    print("----------------------------------------------------------------------")
    cursor.execute("""
    INSERT INTO brand_packaging (id_brand_finishing, name_brand, created_by, updated_by)
    VALUES
    (1, 'BDL5', 1, 1), (2, 'BDL4', 1, 1),
    (3, 'BUD5', 1, 1), (4, 'BUD4', 1, 1),
    (5, 'MUL5', 1, 1), (6, 'GSH5', 1, 1),
    (7, 'BHL5', 1, 1), (8, 'NHL5', 1, 1),
    (9, 'BRH5', 1, 1), (10, 'ES18', 1, 1)
    RETURNING id, name_brand;
    """)
    conn.commit()
    data = cursor.fetchall()
    for item in data:
        print("Packaging Brand -- ", item)

    print("----------------------------------------------------------------------")
    cursor.execute("""
    INSERT INTO suppliers (name_supplier, name_contact, email, phone, created_by, updated_by)
    VALUES
    ('Abi Inc', 'Rachel Hinkel', 'rh@gmail.com', '(307) 630-1615', 1, 1),
    ('Gea Inc', 'Maria Kowalchuk', 'mk@gmail.com', '(307) 630-0062', 1, 1)
    RETURNING id, name_contact;
    """)
    conn.commit()
    data = cursor.fetchall()
    for item in data:
        print("Supplier -- ", item)

    print("----------------------------------------------------------------------")
    cursor.execute("""
    INSERT INTO commodity (name_local, name_bit, name_common, inventory, type, sap, unit_of_measurement, per_unit, per_pallet, id_supplier, created_by, updated_by)
    VALUES
    ('Hop Local 1', 'Hop Bit 1', 'Hop Common 1', 'Brw', 'Hop', '00000001', 'lb', 44, 25, 1, 1, 1),
    ('Hop Local 2', 'Hop Bit 2', 'Hop Common 2', 'Brw', 'Hop', '00000002', 'lb', 44, 25, 1, 2, 1),
    ('Hop Local 3', 'Hop Bit 3', 'Hop Common 3', 'Brw', 'Hop', '00000003', 'lb', 44, 25, 1, 1, 1),
    ('Hop Local 4', 'Hop Bit 4', 'Hop Common 4', 'Brw', 'Hop', '00000004', 'lb', 44, 25, 1, 2, 1),
    ('Addition Local 1', 'Addition Bit 1', 'Addition Common 1', 'Brw', 'Addition', '00000005', 'lb', 44, 25, 1, 1, 1),
    ('Addition Local 2', 'Addition Bit 2', 'Addition Common 2', 'Brw', 'Addition', '00000006', 'lb', 44, 25, 2, 1, 1),
    ('Addition Local 3', 'Addition Bit 3', 'Addition Common 3', 'Brw', 'Addition', '00000007', 'lb', 44, 25, 1, 1, 1),
    ('Addition Local 4', 'Addition Bit 4', 'Addition Common 4', 'Brw', 'Addition', '00000008', 'lb', 44, 25, 2, 1, 1),
    ('Injection Local 1', 'Injection Bit 1', 'Injection Common 1', 'Fin', 'Injection', '00000009', 'lb', 44, 25, 1, 1, 1),
    ('Injection Local 2', 'Injection Bit 2', 'Injection Common 2', 'Fin', 'Injection', '00000010', 'lb', 44, 25, 2, 1, 1),
    ('Injection Local 3', 'Injection Bit 3', 'Injection Common 3', 'Fin', 'Injection', '00000011', 'lb', 44, 25, 1, 1, 1),
    ('Injection Local 4', 'Injection Bit 4', 'Injection Common 4', 'Fin', 'Injection', '00000012', 'lb', 44, 25, 2, 1, 1)
    RETURNING id, name_local;
    """)
    conn.commit()
    data = cursor.fetchall()
    for item in data:
        print("Commodity -- ", item)

    conn.close()
    cursor.close()


RunIt()
