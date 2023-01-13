import pytest


@pytest.mark.parametrize("user_level, bh_1, bh_2, status_code", [
    ('user_lvl_not_logged', "BH40 10001", "BH50 20001", 401), ('user_lvl_1', "BH40 10001", "BH50 20001", 403),
    ('user_lvl_2', None, "BH50 20001", 422), ('user_lvl_2', "BH40 10001", None, 422),
    ('user_lvl_2', "wrong", "BH50 20001", 422), ('user_lvl_2', "BH40 10001", "wrong", 422),
    ('user_lvl_2', "BH40 10001", "BH50 20001", 201)
])
def test_create_last_brews(client, request, create_users, create_commodities, user_level, bh_1, bh_2, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.post("/inventory/lastbrews", json={"bh_1": bh_1, "bh_2": bh_2})

    assert res.status_code == status_code
    if res.status_code == 201:
        data = res.json()
        assert data["bh_1"] == bh_1
        assert data["bh_2"] == bh_2


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200), ('user_lvl_2', 200), ('user_lvl_3', 200),
    ('user_lvl_4', 200), ('user_lvl_5', 200), ('user_lvl_6', 200)
])
def test_get_all_last_brews(client, request, create_users, create_last_brews, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get("/inventory/lastbrews")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401), ('user_lvl_1', 200), ('user_lvl_2', 200), ('user_lvl_3', 200),
    ('user_lvl_4', 200), ('user_lvl_5', 200), ('user_lvl_6', 200)
])
def test_get_one_last_brews(client, request, create_users, create_last_brews, user_level, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/lastbrews/{create_last_brews[0]}")

    assert res.status_code == status_code


@pytest.mark.parametrize("user_level, bh_1, bh_2, status_code", [
    ('user_lvl_not_logged', "OO40 11111", "OO50 22221", 401),
    ('user_lvl_1', "OO40 11111", "OO50 22221", 403),
    ('user_lvl_2', None, "OO50 22221", 422),
    ('user_lvl_2', "OO40 11111", None, 422),
    ('user_lvl_2', "wrong", "OO50 22221", 422),
    ('user_lvl_2', "OO40 11111", "wrong", 422),
    ('user_lvl_2', "OO40 11111", "OO50 22221", 200)
])
def test_update_last_brews(client, request, create_users, create_last_brews, user_level, bh_1, bh_2, status_code):

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.put(f"/inventory/lastbrews/{create_last_brews[0]}", json={"bh_1": bh_1, "bh_2": bh_2})

    assert res.status_code == status_code
    if res.status_code == 200:
        data = res.json()
        assert data['bh_1'] == bh_1
        assert data['bh_2'] == bh_2


@pytest.mark.parametrize("user_level, status_code", [
    ('user_lvl_not_logged', 401),
    ('user_lvl_1', 403),
    ('user_lvl_2', 403),
    ('user_lvl_3', 403),
    ('user_lvl_4', 204)
])
def test_update_last_brews(client, request, create_users, create_last_brews, user_level, status_code):

    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.delete(f"/inventory/lastbrews/delete/{create_last_brews[0]}")

    assert res.status_code == status_code
