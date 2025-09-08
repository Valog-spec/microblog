import pytest


@pytest.mark.asyncio
async def test_get_current_user_profile(test_client, test_user) -> None:
    """Тестирует получение профиля текущего пользователя."""
    response = await test_client.get(
        "/api/users/me", headers={"api-key": test_user.api_key}
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id
    assert response.json()["name"] == test_user.name


@pytest.mark.asyncio
async def test_follow_user(test_client, test_user) -> None:
    """Тестирует подписку на другого пользователя."""
    response_create = await test_client.post(
        "/api/users/create", json={"name": "user2"}
    )

    response_follow = await test_client.post(
        f"/api/users/2/follow", headers={"api-key": test_user.api_key}
    )
    assert response_follow.status_code == 200
    assert response_follow.json()["result"] == True
