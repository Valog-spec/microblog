import pytest


@pytest.mark.asyncio
async def test_create_tweet(test_client, test_user):
    response = test_client.post(
        "/api/tweets",
        json={"content": "Test tweet content"},
        headers={"api-key": test_user.api_key},
    )
    assert response.status_code == 200
    assert response.json()["result"] == True
    assert "tweet_id" in response.json()


@pytest.mark.asyncio
async def test_get_tweets_feed(test_client, test_user, test_tweet):
    response = test_client.get("/api/tweets", headers={"api-key": test_user.api_key})
    assert response.status_code == 200
    assert response.json()["result"] == True
    assert len(response.json()["tweets"]) >= 1


@pytest.mark.asyncio
async def test_like_tweet(test_client, test_user, test_tweet):
    response = test_client.post(
        f"/api/likes/{test_tweet.id}/likes", headers={"api-key": test_user.api_key}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True


@pytest.mark.asyncio
async def test_delete_tweet(test_client, test_user, test_tweet):
    response = test_client.delete(
        f"/api/tweets/{test_tweet.id}", headers={"api-key": test_user.api_key}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True
