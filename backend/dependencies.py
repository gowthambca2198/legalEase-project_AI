from functools import lru_cache

from backend.config import (
    Settings,
    get_settings,
)

from backend.services.ai_generator import (
    GeminiDocumentGenerator,
)

from backend.services.document_service import (
    LegalDocumentService,
)


@lru_cache
def get_ai_generator() -> GeminiDocumentGenerator:
    return GeminiDocumentGenerator(
        get_settings()
    )


@lru_cache
def get_document_service() -> LegalDocumentService:
    return LegalDocumentService()


def get_app_settings() -> Settings:
    return get_settings()