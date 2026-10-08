from fastapi.testclient import TestClient

from backend.dependencies import (
    get_ai_generator,
)

from backend.main import app

from backend.services.ai_generator import (
    GeneratedDocument,
)


class FakeGenerator:
    """
    Fake AI generator used during testing.

    This means pytest does not need a real
    Gemini API key.
    """

    def generate_document(
        self,
        request,
    ):

        return GeneratedDocument(
            content=(
                f"DRAFT {request.document_type}\n\n"
                f"Parties: {request.parties}"
            ),
            demo_mode=True,
        )


app.dependency_overrides[
    get_ai_generator
] = lambda: FakeGenerator()


client = TestClient(app)


def test_generate_document():

    payload = {
        "document_type": "NDA",
        "parties": (
            "Jane Doe; Acme Corporation"
        ),
        "terms": (
            "Confidentiality; "
            "Two year term"
        ),
        "effective_date": "2026-10-05",
    }

    response = client.post(
        "/generate",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "NDA"

    assert "DRAFT NDA" in data["content"]

    assert data["demo_mode"] is True


def test_generate_rejects_blank_party():

    payload = {
        "document_type": "NDA",
        "parties": "",
        "terms": "Confidentiality",
        "effective_date": "2026-10-05",
    }

    response = client.post(
        "/generate",
        json=payload,
    )

    assert response.status_code == 422