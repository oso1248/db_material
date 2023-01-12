import pytest


@pytest.mark.parametrize("user_level, name_brand, is_active, is_organic, is_dryhop, is_addition, status_code", [
    ('user_lvl_not_logged', "BH99", True, False, False, False, 401),
    ('user_lvl_1', "BH99", True, False, False, False, 403),
    ('user_lvl_2', "BH99", True, False, False, False, 403),
    ('user_lvl_3', "BH99", True, False, False, False, 403),
    ('user_lvl_4', "BH99", True, False, False, False, 403),
    ('user_lvl_5', None, True, False, False, False, 422),
    ('user_lvl_5', "wrong", True, False, False, False, 422),
    ('user_lvl_5', "BH99", "wrong", False, False, False, 422),
    ('user_lvl_5', "BH99", True, "wrong", False, False, 422),
    ('user_lvl_5', "BH99", True, False, "wrong", False, 422),
    ('user_lvl_5', "BH99", True, False, False, "wrong", 422),
    ('user_lvl_5', "BH99", True, False, False, False, 201)
])
def test_create_brand(client, request, create_users, user_level, name_brand, is_active, is_organic, is_dryhop, is_addition, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/brand/brewing", json={"name_brand": name_brand, "is_active": is_active, "is_organic": is_organic, "is_dryhop": is_dryhop , "is_addition": is_addition, "created_by": user['id'], "updated_by": user['id']})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data['name_brand'] == 'BH99'
        assert data['is_active'] == True
        assert data['is_organic'] == False
        assert data['is_dryhop'] == False
        assert data['is_addition'] == False


@pytest.mark.parametrize("user_level, status_code", [
    ("user_lvl_not_logged", 401), ("user_lvl_1", 200), ("user_lvl_2", 200), ("user_lvl_3", 200),
    ("user_lvl_4", 200), ("user_lvl_5", 200), ("user_lvl_6", 200),
])
def test_get_all_brands(client, request, create_users, create_brand_brewing, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get("/brand/brewing")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, id, status_code", [
    ("user_lvl_not_logged", 1, 401), ("user_lvl_1", 100, 404), ("user_lvl_2", 'wrong', 422), ("user_lvl_3", 1, 200),
])
def test_get_one_brand(client, request, create_users, create_brand_brewing, user_level, id, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/brand/brewing/{id}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, name_brand, is_active, is_organic, is_dryhop, is_addition, status_code", [
    ('user_lvl_not_logged', "BH99", True, False, False, False, 401), ('user_lvl_1', "BH99", True, False, False, False, 403),
    ('user_lvl_2', "BH99", True, False, False, False, 403), ('user_lvl_3', "BH99", True, False, False, False, 403),
    ('user_lvl_4', None, True, False, False, False, 422), ('user_lvl_4', "wrong", True, False, False, False, 422),
    ('user_lvl_4', "BH99", "wrong", False, False, False, 422), ('user_lvl_4', "BH99", True, "wrong", False, False, 422),
    ('user_lvl_4', "BH99", True, False, "wrong", False, 422), ('user_lvl_4', "BH99", True, False, False, "wrong", 422),
    ('user_lvl_4', "BH53", True, False, False, False, 200)
])
def test_update_brand(client, request, user_lvl_admin, create_users, user_level, name_brand, is_active, is_organic, is_dryhop, is_addition, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post("/brand/brewing", json={"name_brand": "BH40", "is_active": False, "is_organic": True, "is_dryhop": True, "is_addition": True, "created_by": user_lvl_admin['id'], "updated_by": user_lvl_admin['id']})
    user_data = res.json()

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/brand/brewing/{user_data['id']}", json={"name_brand": name_brand, "is_active": is_active, "is_organic": is_organic, "is_dryhop": is_dryhop , "is_addition": is_addition, "updated_by": user['id']})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data['name_brand'] == 'BH53'
        assert data['is_active'] == True
        assert data['is_organic'] == False
        assert data['is_dryhop'] == False
        assert data['is_addition'] == False


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403),
    ('user_lvl_4', 403), ('user_lvl_5', 403), ('user_lvl_6', 403), ('user_lvl_admin', 204),
])
def test_delete_user(client, request, user_lvl_admin, create_users, user_level, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post("/brand/brewing", json={"name_brand": "BH40", "is_active": False, "is_organic": True, "is_dryhop": True, "is_addition": True, "created_by": user_lvl_admin['id'], "updated_by": user_lvl_admin['id']})
    user_data = res.json()

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/brand/brewing/{user_data['id']}")

    assert res.status_code == status_code
