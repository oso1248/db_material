import pytest


@pytest.mark.parametrize("user_level, name_supplier, name_contact, email, phone, is_active, status_code", [
    ('user_lvl_not_logged', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 401),
    ('user_lvl_1', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_2', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_3', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_4', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_5', None, "contact 1", "sup@gmail.com", "1234567890", True, 422),
    ('user_lvl_5', "supplier 1", None, "sup@gmail.com", "1234567890", True, 422),
    ('user_lvl_5', "supplier 1", "contact 1", None, "1234567890", True, 422),
    ('user_lvl_5', "supplier 1", "contact 1", "wrong", "1234567890", True, 422),
    ('user_lvl_5', "supplier 1", "contact 1", "sup@gmail.com", None, True, 422),
    ('user_lvl_5', "supplier 1", "contact 1", "sup@gmail.com", "wrong", True, 422),
    ('user_lvl_5', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 201),
])
def test_create_supplier(client, request, create_users, user_level, name_supplier, name_contact, email, phone, is_active, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/suppliers", json={"name_supplier": name_supplier, "name_contact": name_contact, "email": email, "phone": phone , "is_active": is_active, "created_by": user['id'], "updated_by": user['id']})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data['name_supplier'] == 'Supplier 1'
        assert data['name_contact'] == 'Contact 1'
        assert data['email'] == 'sup@gmail.com'
        assert data['phone'] == "(123) 456-7890"
        assert data['is_active'] == True


@pytest.mark.parametrize("user_level, status_code", [
    ("user_lvl_not_logged", 401), ("user_lvl_1", 200), ("user_lvl_2", 200), ("user_lvl_3", 200),
    ("user_lvl_4", 200), ("user_lvl_5", 200), ("user_lvl_6", 200),
])
def test_get_all_suppliers(client, request, create_users, create_suppliers, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get("/suppliers")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, id, status_code", [
    ("user_lvl_not_logged", 1, 401), ("user_lvl_1", 10, 404), ("user_lvl_2", 'wrong', 422), ("user_lvl_3", 1, 200),
])
def test_get_one_supplier(client, request, create_users, create_suppliers, user_level, id, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/suppliers/{id}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, name_supplier, name_contact, email, phone, is_active, status_code", [
    ('user_lvl_not_logged', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 401),
    ('user_lvl_1', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_2', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_3', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 403),
    ('user_lvl_4', None, "contact 1", "sup@gmail.com", "1234567890", True, 422),
    ('user_lvl_4', "supplier 1", None, "sup@gmail.com", "1234567890", True, 422),
    ('user_lvl_4', "supplier 1", "contact 1", None, "1234567890", True, 422),
    ('user_lvl_4', "supplier 1", "contact 1", "wrong", "1234567890", True, 422),
    ('user_lvl_4', "supplier 1", "contact 1", "sup@gmail.com", None, True, 422),
    ('user_lvl_4', "supplier 1", "contact 1", "sup@gmail.com", "wrong", True, 422),
    ('user_lvl_4', "supplier 1", "contact 1", "sup@gmail.com", "1234567890", True, 200),
])
def test_update_user(client, request, create_users, user_lvl_admin, user_level, name_supplier, name_contact, email, phone, is_active, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/suppliers", json={"name_supplier": "Test Supplier", "name_contact": "Test Contact", "email": "test@gmail.com", "phone": "0987654321" , "is_active": True, "created_by": 1, "updated_by": 1})
    user_data = res.json()

    user = request.getfixturevalue(user_level)
    user_data = {**user_data, "name_supplier": name_supplier, "name_contact": name_contact, "email": email, "phone": phone , "is_active": is_active, "created_by": user['id'], "updated_by": user['id']}
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/suppliers/{user_data['id']}", json=user_data)

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert data['name_supplier'] == 'Supplier 1'
        assert data['name_contact'] == 'Contact 1'
        assert data['email'] == 'sup@gmail.com'
        assert data['phone'] == "(123) 456-7890"
        assert data['is_active'] == True


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_1', 403), ('user_lvl_2', 403), ('user_lvl_3', 403), ('user_lvl_4', 403),
    ('user_lvl_5', 403), ('user_lvl_6', 403), ('user_lvl_admin', 204),
])
def test_delete_user(client, request, user_lvl_admin, create_users, user_level, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/suppliers", json={"name_supplier": "Test Supplier", "name_contact": "Test Contact", "email": "test@gmail.com", "phone": "0987654321" , "is_active": True, "created_by": 1, "updated_by": 1})
    user_data = res.json()

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/suppliers/{user_data['id']}")

    assert res.status_code == status_code
