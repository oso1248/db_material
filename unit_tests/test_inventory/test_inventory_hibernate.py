import pytest


@pytest.mark.parametrize("user_level, tank_origin, tank_origin_level, tank_storage, tank_storage_level, tank_storage_og, tank_storage_abw, tank_storage_o2, status_code", [
    ('user_lvl_not_logged', 2025, 2500, 2045, 2500, 11.00, 7.62, 10, 401),
    ('user_lvl_1', 2025, 2500, 2045, 2500, 11.00, 7.62, 10, 403),
    ('user_lvl_2', None, 2500, 2045, 2500, 11.00, 7.62, 10, 422),
    ('user_lvl_2', 2025, None, 2045, 2500, 11.00, 7.62, 10, 422),
    ('user_lvl_2', 2025, 2500, None, 2500, 11.00, 7.62, 10, 422),
    ('user_lvl_2', 2025, 2500, 2045, None, 11.00, 7.62, 10, 422),
    ('user_lvl_2', 2025, 2500, 2045, 2500, None, 7.62, 10, 422),
    ('user_lvl_2', 2025, 2500, 2045, 2500, 11.00, None, 10, 422),
    ('user_lvl_2', 2025, 2500, 2045, 2500, 11.00, 7.62, None, 422),
    ('user_lvl_2', 2025, 2500, 2045, 2500, 11.00, 7.62, 10, 201)
])
def test_create_inventory(client, request, create_users, create_inventory_hibernate, user_level, tank_origin, tank_origin_level, tank_storage, tank_storage_level, tank_storage_og, tank_storage_abw, tank_storage_o2, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/inventory/hibernate", json={"id_brand_brewing": create_inventory_hibernate['brands'][0][0],
                                                    "tank_origin": tank_origin, "tank_origin_level": tank_origin_level,
                                                    "tank_storage": tank_storage, "tank_storage_level": tank_storage_level,
                                                    "tank_storage_og": tank_storage_og, "tank_storage_abw": tank_storage_abw,
                                                    "tank_storage_o2": tank_storage_o2, "created_by": user['id'],
                                                    "updated_by": user['id']})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data['tank_origin'] == 2025
        assert data['tank_origin_level'] == 2500
        assert data['tank_storage'] == 2045
        assert data['tank_storage_level'] == 2500
        assert data['tank_storage_og'] == 11.00
        assert data['tank_storage_abw'] == 7.62
        assert data['tank_storage_o2'] == 10


@pytest.mark.parametrize("user_level, complete, status_code", [
    ('user_lvl_not_logged', False, 401), ('user_lvl_not_logged', True, 401), ('user_lvl_1', False, 200), ('user_lvl_1', True, 200)
])
def test_get_all_inventory(client, request, create_users, create_inventory_hibernate, user_level, complete, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/hibernate?complete={complete}")

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert len(data) == 3


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200)
])
def test_get_one_inventory(client, request, create_users, create_inventory_hibernate, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/hibernate/{create_inventory_hibernate['inv'][0][0]}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 200)
])
def test_update_inventory(client, request, create_users, create_inventory_hibernate, user_level, status_code):
    user = request.getfixturevalue(user_level)
    data_update = {"tank_origin": 7237, "tank_origin_level": 2400, "tank_storage": 2001, "tank_storage_level": 2400,
                   "tank_storage_og": 10.00, "tank_storage_abw": 5.55, "tank_storage_o2": 8, "tank_final": 7238,
                   "tank_final_level": 2400, "updated_by": user['id'], "id_brand_brewing": 1}
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/inventory/hibernate/{create_inventory_hibernate['inv'][0][0]}", json=data_update)

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert data['tank_origin'] == data_update['tank_origin']
        assert data['tank_origin_level'] == data_update['tank_origin_level']
        assert data['tank_storage'] == data_update['tank_storage']
        assert data['tank_storage_level'] == data_update['tank_storage_level']
        assert data['tank_storage_og'] == data_update['tank_storage_og']
        assert data['tank_storage_abw'] == data_update['tank_storage_abw']
        assert data['tank_storage_o2'] == data_update['tank_storage_o2']
        assert data['tank_final'] == data_update['tank_final']
        assert data['tank_final_level'] == data_update['tank_final_level']
        assert data['is_complete'] == True


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403), ('user_lvl_4', 204)
])
def test_delete_one_inventory(client, request, create_users, create_inventory_hibernate, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/inventory/hibernate/{create_inventory_hibernate['inv'][0][0]}")

    assert res.status_code == status_code
