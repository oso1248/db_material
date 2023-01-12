import pytest


@pytest.mark.parametrize("user_level, eid, name_first, name_last, is_active, permissions, status_code", [
    ('user_lvl_not_logged', "zz00000", "Mila", "Azul", True, 1, 401),
    ('user_lvl_1', "zz00000", "Mila", "Azul", True, 1, 403), ('user_lvl_2', "zz00000", "Mila", "Azul", True, 1, 403),
    ('user_lvl_3', "zz00000", "Mila", "Azul", True, 1, 403), ('user_lvl_4', "zz00000", "Mila", "Azul", True, 1, 403),
    ('user_lvl_5', "zz00000", "wrong@", "Azul", True, 1, 422), ('user_lvl_5', "zz00000", "Mila", "wrong@", True, 1, 422),
    ('user_lvl_5', "zz00000", "Mila", "Azul", "wrong", 1, 422), ('user_lvl_5', "zz00000", "Mila", "Azul", True, 9, 422),
    ('user_lvl_5', None, None, None, True, 1, 422), ('user_lvl_5', "", "Mila", "Azul", True, 1, 422),
    ('user_lvl_5', "aa00000", "Adam", "Coulson", False, 6, 409), ('user_lvl_5', "ea92284", "Adam", "Coulson", False, 6, 201)
])
def test_create_user(client, request, create_users, user_level, eid, name_first, name_last, is_active, permissions, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/users", json={"eid": eid, "name_first": name_first, "name_last": name_last, "is_active": is_active ,"permissions": permissions, "password": "BudFort1!"})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data['eid'] == 'ea92284'
        assert data['name_first'] == 'Adam'
        assert data['name_last'] == 'Coulson'
        assert data['is_active'] == False
        assert data['permissions'] == 6


@pytest.mark.parametrize("user_level, status_code", [
    ("user_lvl_not_logged", 401),
    ("user_lvl_1", 200),
    ("user_lvl_2", 200),
    ("user_lvl_3", 200),
    ("user_lvl_4", 200),
    ("user_lvl_5", 200),
    ("user_lvl_6", 200),
])
def test_get_all_users(client, request, create_users, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get("/users")
    data = res.json()

    assert res.status_code == status_code
    if res.status_code == 200:
        for item in data:
            assert item['id'] != 1  # Test Admin Not Icluded


@pytest.mark.parametrize("user_level, id, status_code", [
    ("user_lvl_not_logged", 2, 401),
    ("user_lvl_1", 1, 403),
    ("user_lvl_2", 2, 200),
    ("user_lvl_3", 10, 404),
    ("user_lvl_4", 'wrong', 422),
])
def test_get_one_users(client, request, create_users, user_level, id, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/users/{id}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, eid, name_first, name_last, is_active, permissions, status_code", [
    ('user_lvl_not_logged', "ea92284", "Adam", "Coulson", False, 6, 401),
    ('user_lvl_1', "ea92284", "Adam", "Coulson", False, 6, 403), ('user_lvl_2', "ea92284", "Adam", "Coulson", False, 6, 403),
    ('user_lvl_3', "ea92284", "Adam", "Coulson", False, 6, 403), ('user_lvl_4', "ea92284", "Adam", "Coulson", False, 6, 403),
    ('user_lvl_5', "zz00000", "wrong@", "Azul", True, 1, 422), ('user_lvl_5', "zz00000", "Mila", "wrong@", True, 1, 422),
    ('user_lvl_5', "zz00000", "Mila", "Azul", "wrong", 1, 422), ('user_lvl_5', "zz00000", "Mila", "Azul", True, 9, 422),
    ('user_lvl_5', None, None, None, True, 1, 422), ('user_lvl_5', None, "Mila", "Azul", True, 1, 422),
    ('user_lvl_5', "aa00000", "Adam", "Coulson", False, 6, 409), ('user_lvl_5', "ea92284", "Adam", "Coulson", False, 6, 200)
])
def test_update_user(client, request, create_users, user_lvl_admin, user_level, eid, name_first, name_last, is_active, permissions, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/users", json={"eid": "zz00000", "name_first": "Mila", "name_last": "Azul", "is_active": True, "permissions": 1, "password": "BudFort1!"})
    user_data = res.json()
    user_data = {**user_data, 'eid': eid, 'name_first': name_first, 'name_last': name_last, 'is_active': is_active, 'permissions': permissions}

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/users/{user_data['id']}", json=user_data)

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert data['eid'] == 'ea92284'
        assert data['name_first'] == 'Adam'
        assert data['name_last'] == 'Coulson'
        assert data['is_active'] == False
        assert data['permissions'] == 6


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403), ('user_lvl_4', 403),
    ('user_lvl_5', 403), ('user_lvl_6', 403), ('user_lvl_admin', 204),
])
def test_delete_user(client, request, user_lvl_admin, create_users, user_level, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/users", json={"eid": "zz00000", "name_first": "Mila", "name_last": "Azul", "is_active": True, "permissions": 1, "password": "BudFort1!"})
    user_data = res.json()

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/users/{user_data['id']}")

    assert res.status_code == status_code
