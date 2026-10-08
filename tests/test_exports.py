from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


PAYLOAD = {
    "document_type": "Service Agreement",
    "parties": (
        "Jane Doe; Acme Corporation"
    ),
    "terms": (
        "Payment within 30 days; "
        "Confidentiality"
    ),
    "effective_date": "2026-10-05",
    "jurisdiction": "Not specified",
    "branding_name": "LegalEase",
    "content": (
        "SERVICE AGREEMENT\n\n"
        "1. Purpose\n"
        "This is a test document.\n\n"
        "2. Signatures\n"
        "Party 1: __________________"
    ),
}


def test_txt_export():

    response = client.post(
        "/export/txt",
        json=PAYLOAD,
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith("text/plain")

    assert (
        b"SERVICE AGREEMENT"
        in response.content
    )


def test_docx_export():

    response = client.post(
        "/export/docx",
        json=PAYLOAD,
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith(
        "application/"
        "vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    )

    # DOCX files are ZIP containers.
    assert response.content[:2] == b"PK"


def test_pdf_export():

    response = client.post(
        "/export/pdf",
        json=PAYLOAD,
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith(
        "application/pdf"
    )

    assert response.content.startswith(
        b"%PDF"
    )