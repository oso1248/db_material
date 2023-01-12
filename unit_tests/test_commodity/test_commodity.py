import pytest


@pytest.mark.parametrize("user_level, id_supplier, name_local, name_bit, name_common, inventory, type, sap, unit_of_measurement, per_unit, per_pallet, is_active, status_code", [
    ('user_lvl_not_logged', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 401),
    ('user_lvl_1', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 403),
    ('user_lvl_2', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 403),
    ('user_lvl_3', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 403),
    ('user_lvl_4', 1, None, "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", None, "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", None, "Fin", "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", None, "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", None, "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", None, "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", None, 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", None, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, None, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, "wrong", 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 201),
])
def test_create_commodity(client, request, create_users, create_suppliers, user_level, id_supplier, name_local, name_bit, name_common, inventory, type, sap, unit_of_measurement, per_unit, per_pallet, is_active, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/commodity", json={"id_supplier": id_supplier, "name_local": name_local, "name_bit": name_bit, "name_common": name_common, "inventory": inventory, "type": type, "sap": sap, "unit_of_measurement": unit_of_measurement, "per_unit": per_unit, "per_pallet": per_pallet, "is_active": is_active, "created_by": user['id'], "updated_by": user['id']})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data['name_local'] == 'Local 1'
        assert data['name_bit'] == 'Bit 1'
        assert data['name_common'] == 'Common 1'
        assert data['inventory'] == 'Fin'
        assert data['type'] == 'Hop'
        assert data['sap'] == '00000001'
        assert data['unit_of_measurement'] == 'lb'
        assert data['per_unit'] == 44
        assert data['per_pallet'] == 25
        assert data['is_active'] == True


@pytest.mark.parametrize("user_level, status_code", [
    ("user_lvl_not_logged", 401),
    ("user_lvl_1", 200),
    ("user_lvl_2", 200),
    ("user_lvl_3", 200),
    ("user_lvl_4", 200),
    ("user_lvl_5", 200),
    ("user_lvl_6", 200),
])
def test_get_all_commodity(client, request, create_users, create_commodities, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get("/commodity")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, id, status_code", [
    ("user_lvl_not_logged", 1, 401),
    ("user_lvl_1", 100, 404),
    ("user_lvl_2", 'wrong', 422),
    ("user_lvl_3", 1, 200),
])
def test_get_one_commodity(client, request, create_users, create_commodities, user_level, id, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/commodity/{id}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, id_supplier, name_local, name_bit, name_common, inventory, type, sap, unit_of_measurement, per_unit, per_pallet, is_active, status_code", [
    ('user_lvl_not_logged', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 401),
    ('user_lvl_1', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 403),
    ('user_lvl_2', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 403),
    ('user_lvl_3', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 403),
    ('user_lvl_4', 1, None, "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", None, "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", None, "Fin", "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", None, "Hop", "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", None, "00000001", "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", None, "lb", 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", None, 44, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", None, 25, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, None, True, 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, "wrong", 422),
    ('user_lvl_4', 1, "Local 1", "Bit 1", "Common 1", "Fin", "Hop", "00000001", "lb", 44, 25, False, 200),
])
def test_update_commodity(client, request, create_users, create_suppliers, user_lvl_admin, user_level, id_supplier, name_local, name_bit, name_common, inventory, type, sap, unit_of_measurement, per_unit, per_pallet, is_active, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/commodity", json={"id_supplier": 1, "name_local": "Test Local", "name_bit": "Test Bit", "name_common": "Test Common", "inventory": "Brw", "type": "Addition", "sap": "10000000", "unit_of_measurement": "kg", "per_unit": 100, "per_pallet": 100, "is_active": True, "updated_by": user_lvl_admin['id']})
    user_data = res.json()
    print(user_data)
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/commodity/{user_data['id']}", json={"id_supplier": id_supplier, "name_local": name_local, "name_bit": name_bit, "name_common": name_common, "inventory": inventory, "type": type, "sap": sap, "unit_of_measurement": unit_of_measurement, "per_unit": per_unit, "per_pallet": per_pallet, "is_active": is_active, "updated_by": user['id']})

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert data['name_local'] == 'Local 1'
        assert data['name_bit'] == 'Bit 1'
        assert data['name_common'] == 'Common 1'
        assert data['inventory'] == 'Fin'
        assert data['type'] == 'Hop'
        assert data['sap'] == '00000001'
        assert data['unit_of_measurement'] == 'lb'
        assert data['per_unit'] == 44
        assert data['per_pallet'] == 25
        assert data['is_active'] == False


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403), ('user_lvl_4', 403),
    ('user_lvl_5', 403), ('user_lvl_6', 403), ('user_lvl_admin', 204),
])
def test_delete_commodity(client, request, user_lvl_admin, create_users, create_suppliers, user_level, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/commodity", json={"id_supplier": 1, "name_local": "Test Local", "name_bit": "Test Bit", "name_common": "Test Common", "inventory": "Brw", "type": "Addition", "sap": "10000000", "unit_of_measurement": "kg", "per_unit": 100, "per_pallet": 100, "is_active": True, "updated_by": user_lvl_admin['id']})
    user_data = res.json()

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/commodity/{user_data['id']}")

    assert res.status_code == status_code
