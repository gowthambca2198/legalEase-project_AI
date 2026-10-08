from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.responses import Response

from backend.dependencies import (
    get_ai_generator,
    get_document_service,
)

from backend.schemas import (
    DocumentRequest,
    ExportRequest,
    GenerateResponse,
)

from backend.services.ai_generator import (
    GeminiDocumentGenerator,
)

from backend.services.document_service import (
    LegalDocumentService,
)

from backend.utils.text_utils import (
    safe_filename,
)


router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateResponse,
)
def generate_document(
    request: DocumentRequest,
    generator: GeminiDocumentGenerator = Depends(
        get_ai_generator
    ),
):
    """
    Generate a document using Gemini.
    """

    try:
        result = generator.generate_document(
            request
        )

        return GenerateResponse(
            document_type=request.document_type,
            content=result.content,
            demo_mode=result.demo_mode,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post("/export/txt")
def export_txt(
    request: ExportRequest,
    service: LegalDocumentService = Depends(
        get_document_service
    ),
):
    """
    Export document as TXT.
    """

    filename = (
        f"{safe_filename(request.document_type)}.txt"
    )

    return Response(
        content=service.txt(request),
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )


@router.post("/export/docx")
def export_docx(
    request: ExportRequest,
    service: LegalDocumentService = Depends(
        get_document_service
    ),
):
    """
    Export document as DOCX.
    """

    filename = (
        f"{safe_filename(request.document_type)}.docx"
    )

    return Response(
        content=service.docx(request),
        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )


@router.post("/export/pdf")
def export_pdf(
    request: ExportRequest,
    service: LegalDocumentService = Depends(
        get_document_service
    ),
):
    """
    Export document as PDF.
    """

    filename = (
        f"{safe_filename(request.document_type)}.pdf"
    )

    return Response(
        content=service.pdf(request),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )