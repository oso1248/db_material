import pytest
import math


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 201)
])
def test_create_inventory(client, request, create_users, create_commodities, create_last_brews, user_level, status_code):
    data = [
        {"final_boxes": 10, "final_pounds": 100, "final_total": 1000, "lot_number": "test lot 1", "is_current": True, "is_active": True, "id_commodity": 1},
        {"final_boxes": 10, "final_pounds": 100, "final_total": 1000, "lot_number": "test lot 2", "is_current": True, "is_active": True, "id_commodity": 2},
        {"final_boxes": 10, "final_pounds": 100, "final_total": 1000, "lot_number": "test lot 3", "is_current": True, "is_active": True, "id_commodity": 3},
        {"final_boxes": 10, "final_pounds": 100, "final_total": 1000, "lot_number": "test lot 4", "is_current": True, "is_active": True, "id_commodity": 4}
    ]

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/inventory/hop", json=data)

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert len(data) == 4


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 201)
])
def test_add_inventory(client, request, create_users, create_commodities, create_inventory_hop, user_level, status_code):
    data = {"final_boxes": 11, "final_pounds": 11, "final_total": 1111, "lot_number": "test lot 5", "is_current": False, "id_commodity": 1}

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post(f"/inventory/hop/{create_inventory_hop['last_brews'][1]}", json=data)

    assert res.status_code == status_code
    if res.status_code == 201:
        res_data = res.json()
        assert math.isclose(res_data['final_boxes'], data['final_boxes'], rel_tol=1e-10)
        assert math.isclose(res_data['final_pounds'], data['final_pounds'], rel_tol=1e-10)
        assert math.isclose(res_data['final_total'], data['final_total'], rel_tol=1e-10)
        assert res_data['lot_number'] == data['lot_number'].replace(" ", "")
        assert res_data['is_current'] == data['is_current']


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200), ('user_lvl_2', 200), ('user_lvl_3', 200),
    ('user_lvl_4', 200), ('user_lvl_5', 200), ('user_lvl_6', 200)
])
def test_get_all_inventory(client, request, create_users, create_commodities, create_inventory_hop, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/hop/all/{create_inventory_hop['last_brews'][1]}")

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert math.isclose(len(data), len(create_inventory_hop['inv']), rel_tol=1e-10)


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200), ('user_lvl_2', 200), ('user_lvl_3', 200),
    ('user_lvl_4', 200), ('user_lvl_5', 200), ('user_lvl_6', 200)
])
def test_get_one_inventory(client, request, create_users, create_commodities, create_inventory_hop, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/hop/one/{create_inventory_hop['inv'][0][0]}")

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert math.isclose(data['final_boxes'], create_inventory_hop['inv'][0][3], rel_tol=1e-10)
        assert math.isclose(data['final_pounds'], create_inventory_hop['inv'][0][4], rel_tol=1e-10)
        assert math.isclose(data['final_total'], create_inventory_hop['inv'][0][5], rel_tol=1e-10)


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 200)
])
def test_update_inventory(client, request, create_users, create_commodities, create_inventory_hop, user_level, status_code):
    data_update = {"final_boxes": 11, "final_pounds": 11, "final_total": 1111, "lot_number": "new lot 5", "is_current": False, "id_commodity": create_inventory_hop['inv'][0][2]}
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/inventory/hop/one/{create_inventory_hop['inv'][0][0]}", json=data_update)

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert math.isclose(data['final_boxes'], data_update['final_boxes'], rel_tol=1e-10)
        assert math.isclose(data['final_pounds'], data_update['final_pounds'], rel_tol=1e-10)
        assert math.isclose(data['final_total'], data_update['final_total'], rel_tol=1e-10)
        assert data['lot_number'] == data_update['lot_number'].replace(" ", "")
        assert data['is_current'] == data_update['is_current']


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403), ('user_lvl_4', 204)
])
def test_delete_all_inventory(client, request, create_users, create_commodities, create_inventory_hop, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/inventory/hop/all/{create_inventory_hop['last_brews'][1]}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 204)
])
def test_delete_ont_inventory(client, request, create_users, create_commodities, create_inventory_hop, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/inventory/hop/one/{create_inventory_hop['inv'][0][0]}")

    assert res.status_code == status_code
