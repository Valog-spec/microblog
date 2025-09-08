# import io
#
# import pytest
#
#
# @pytest.mark.asyncio
# async def test_upload_media(test_client, test_user, test_tweet) -> None:
#     """Тестирует загрузку медиафайла для твита."""
#     test_file = io.BytesIO(b"fake image data")
#     test_file.name = "test.jpg"
#
#     response = test_client.post(
#         "/api/media",
#         data={"tweet_id": test_tweet.id},
#         files={"file": ("test.jpg", test_file, "image/jpeg")},
#         headers={
#             "api-key": test_user.api_key,
#         },
#     )
#     assert response.status_code == 200
#     assert response.json()["result"] == True
#     assert "media_id" in response.json()
import io

import pytest


@pytest.mark.asyncio
async def test_upload_media(test_client, test_user, test_tweet):
    test_file = io.BytesIO(b"fake image data")
    test_file.name = "test.jpg"

    response = await test_client.post(
        "/api/media",
        data={"tweet_id": test_tweet.id},
        files={"file": ("test.jpg", test_file, "image/jpeg")},
        headers={
            "api-key": test_user.api_key,
        },
    )
    assert response.status_code == 200
    assert response.json()["result"] == True
    assert "media_id" in response.json()
