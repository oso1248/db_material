import pytest
import math


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 201)
])
def test_create_inventory(client, request, create_users, create_commodities, user_level, status_code):
    data = [
        {"final_count": 10, "final_total": 1000, "id_commodity": 1}, {"final_count": 10, "final_total": 1000, "id_commodity": 2},
        {"final_count": 10, "final_total": 1000, "id_commodity": 3}, {"final_count": 10, "final_total": 1000, "id_commodity": 4}
    ]

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/inventory/material", json=data)

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert len(data) == 4


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 201)
])
def test_add_inventory(client, request, create_users, create_commodities, create_inventory_material, user_level, status_code):
    data = {"final_count": 11, "final_total": 1111, "id_commodity": 1}

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post(f"/inventory/material/{create_inventory_material['uuid'][0][1]}", json=data)

    assert res.status_code == status_code
    if res.status_code == 201:
        res_data = res.json()
        assert math.isclose(res_data['final_count'], data['final_count'], rel_tol=1e-10)
        assert math.isclose(res_data['final_total'], data['final_total'], rel_tol=1e-10)


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200), ('user_lvl_2', 200), ('user_lvl_3', 200),
    ('user_lvl_4', 200), ('user_lvl_5', 200), ('user_lvl_6', 200)
])
def test_get_all_inventory(client, request, create_users, create_commodities, create_inventory_material, user_level, status_code):
    data = {"uuid": create_inventory_material['uuid'][0][1]}
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/material/all/{create_inventory_material['uuid'][0][1]}")

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert math.isclose(len(data), len(create_inventory_material['inv']), rel_tol=1e-10)


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200), ('user_lvl_2', 200), ('user_lvl_3', 200),
    ('user_lvl_4', 200), ('user_lvl_5', 200), ('user_lvl_6', 200)
])
def test_get_one_inventory(client, request, create_users, create_commodities, create_inventory_material, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/material/one/{create_inventory_material['inv'][0][0]}")
    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert math.isclose(data['final_count'], create_inventory_material['inv'][0][3], rel_tol=1e-10)
        assert math.isclose(data['final_total'], create_inventory_material['inv'][0][4], rel_tol=1e-10)


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 200)
])
def test_update_inventory(client, request, create_users, create_commodities, create_inventory_material, user_level, status_code):
    data_update = {"final_count": 111, "final_total": 1111, "id_commodity": create_inventory_material['inv'][0][0]}
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/inventory/material/one/{create_inventory_material['inv'][0][0]}", json=data_update)

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert math.isclose(data['final_count'], data_update['final_count'], rel_tol=1e-10)
        assert math.isclose(data['final_total'], data_update['final_total'], rel_tol=1e-10)


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403), ('user_lvl_4', 204)
])
def test_delete_all_inventory(client, request, create_users, create_commodities, create_inventory_material, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/inventory/material/all/{create_inventory_material['uuid'][0][1]}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 204)
])
def test_delete_ont_inventory(client, request, create_users, create_commodities, create_inventory_material, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/inventory/material/one/{create_inventory_material['inv'][0][0]}")

    assert res.status_code == status_code
