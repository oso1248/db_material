import pytest


@pytest.mark.parametrize("eid, password, status_code", [
    ('wrong', 'BudFort1!', 403), ('aa00000', 'wrong', 403),
    (None, 'BudFort1!', 422), ('aa00000', None, 422),
    (None, None, 422), ('aa00000', 'BudFort1!', 200),
])
def test_login(client, create_users, eid, password, status_code):
    res = client.post("/login", data={"username": eid, "password": password})

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert data['access_token'] != None
        assert data['token_type'] == 'bearer'


@pytest.mark.parametrize("user_level, status_code", [
    ("user_lvl_1", 403), ("user_lvl_2", 403), ("user_lvl_3", 403), ("user_lvl_4", 403), ("user_lvl_5", 205),
])
def test_password_reset(client, request, create_users, user_lvl_admin, user_level, status_code):
    client.headers = {"Authorization": f"Bearer {user_lvl_admin['jwt']}"}
    res = client.post(f"/users", json={"eid": "zz00000", "name_first": "Mila", "name_last": "Azul", "is_active": True, "permissions": 1, "password": "BudFort1!"})
    data = res.json()

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post(f"/login/reset/{data['id']}", json={"email": None})

    assert res.status_code == status_code
    if res.status_code == 205:
        reset_data = res.json()
        res = client.post("/login", data={"username": data['eid'], "password": reset_data['temporary_password']})
        reset_login = res.json()
        assert reset_login['access_token'] != None
        assert reset_login['token_type'] == 'bearer'


@pytest.mark.parametrize("eid, old_password, new_password, status_code", [
    (None, "BudFort1!", "BudFort2!", 422), ("em00000", None, "BudFort2!", 422), ("em00000", "BudFort1!", None, 417),
    ("wrong", "BudFort1!", "BudFort2!", 403), ("em00000", "wrong", "BudFort2!", 403), ("em00000", "BudFort1!", "wrong", 417),
    ("em00000", "BudFort1!", "BudFort2!", 205),
])
def test_password_change(client, create_users, eid, old_password, new_password, status_code):
    res = client.post(f"/login/change", data={"username": eid, "password": old_password, "client_secret": new_password})

    if res.status_code == 205:
        res = client.post("/login", data={"username": eid, "password": new_password})
        changed_login = res.json()
        assert changed_login['access_token'] != None
        assert changed_login['token_type'] == 'bearer'
