from typing import Any, Dict, List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import controller


# https://testdriven.io/blog/fastapi-crud/
def test_get_root(test_app: TestClient, monkeypatch: Any) -> None:
    test_response_payload = [
        {
            "id": 1,
            "name": "Category 1",
            "sequence": 0,
            "created_at": "2020-08-15T14:33:30.625578",
            "updated_at": "2020-08-15T14:33:30.625578",
            "description": None,
        }
    ]

    # def mock_get_db() -> None:
    #    return None

    def mock_get(db: Session, skip: int, limit: int) -> List[Dict[str, Any]]:
        return test_response_payload

    # main.app.dependency_overrides[db.get_db] = mock_get_db
    monkeypatch.setattr(controller.category_controller, "get_all", mock_get)

    response = test_app.get("/v1/categories",)

    assert response.status_code == 200
    assert response.json() == test_response_payload
