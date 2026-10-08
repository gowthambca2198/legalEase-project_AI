# ⚖️ LegalEase

LegalEase is an AI-assisted legal document drafting application.

## Run locally on Windows

Use Python 3.12 or newer. From the project folder, run:

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set `DEMO_MODE=true` in `.env` to try document generation without an API key. To
generate with Gemini, set `GEMINI_API_KEY` and `DEMO_MODE=false` in `.env`.

Start both the backend and frontend from one PowerShell terminal in the project
folder:

```powershell
.\.venv312\Scripts\python.exe run_local.py
```

Press **Ctrl+C** in that terminal to stop both services.

Open <http://localhost:8501> for the app, <http://localhost:8000/docs> for the
API documentation, or <http://localhost:8000/health> to check the backend.
Optional PNG or JPEG branding logos can be uploaded in the app and are included
in DOCX and PDF downloads. Choose Times New Roman, Arial, or Courier New for
the exported documents.

It combines:

- Streamlit
- FastAPI
- Google Gemini
- Pydantic
- python-docx
- fpdf2
- Automated tests

The application allows users to:

1. Select a legal document type.
2. Enter the parties.
3. Enter terms and conditions.
4. Specify an effective date.
5. Specify jurisdiction.
6. Describe the purpose of the document.
7. Add additional instructions.
8. Generate an AI-assisted draft.
9. Edit the generated document.
10. Preview the document.
11. Download it as TXT, DOCX or PDF.

---

# Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── dependencies.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_generator.py
│   │   └── document_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── text_utils.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_documents.py
│   └── test_exports.py
│
├── assets/
│   └── logo.svg
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
