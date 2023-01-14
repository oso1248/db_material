import pytest


@pytest.mark.parametrize("user_level, inventory, status_code", [
    ('user_lvl_not_logged', 'Brw', 401),
    ('user_lvl_1', 'Log', 404),
    ('user_lvl_1', 'Brw', 200),
    ('user_lvl_1', 'Fin', 200)
])
def test_get_one_inventory(client, request, create_users, create_commodities, create_inventory_material, create_inventory_hop, user_level, inventory, status_code):
    user = request.getfixturevalue(user_level)
    client.headers = {"Authorization": f"Bearer {user['jwt']}"}
    res = client.get(f"/inventory/bit/{create_inventory_material['uuid'][0][1]}?inventory={inventory}")

    assert res.status_code == status_code
